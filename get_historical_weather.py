import requests
import calendar
import json
import mysql.connector
import time
from config import dbconfig, wwo, process

try:
    db = mysql.connector.connect(**dbconfig)
except:
    print("Unable to reach database server")
    quit()

postal_codes = db.cursor(buffered=True)
insert = db.cursor()

spostal = """
            SELECT DISTINCT postal_code
            FROM station
            WHERE postal_code NOT IN (SELECT DISTINCT postal_code FROM weather)
            LIMIT 3
            """
iweather = """
            INSERT INTO `weather`
            (
                `date`, `time`, `postal_code`, `type`, `tempC`,
                `windspeedKmph`, `weatherCode`, `weatherDesc`, `humidity`,
                `HeatIndexC`, `DewPointC`, `WindChillC`, `WindGustKmph`,
                `uvIndex`, `response`
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
postal_codes.execute(spostal)

for postal_code, in postal_codes:

    for month in process['months']:

        for day in range(1, calendar.monthrange(process['year'], month)[1]):

            date = str(process['year']) + "-" + str(month).zfill(2) + "-" \
                + str(day).zfill(2)

            parms = dict()
            parms['key'] = wwo['key']
            parms['q'] = postal_code
            parms['format'] = 'json'
            parms['tp'] = 1
            parms['date'] = date

            try:
                req = requests.get(url=wwo['past_weather'], params=parms)
                data = req.json()

                if 'error' in data['data']:
                    print(data['data']['error'][0]['msg'])
                    exit()

            except:
                print(parms, "REQUEST FAILED")
                continue

            args = []

            for hourly in data['data']['weather'][0]['hourly']:

                args.append(
                    (
                        date, str(hourly['time']).zfill(4), postal_code, 'A',
                        hourly['tempC'], hourly['windspeedKmph'],
                        hourly['weatherCode'],
                        hourly['weatherDesc'][0]['value'], hourly['humidity'],
                        hourly['HeatIndexC'], hourly['DewPointC'],
                        hourly['WindChillC'], hourly['WindGustKmph'],
                        hourly['uvIndex'], req.text
                    )
                )

            try:
                insert.executemany(iweather, args)
                db.commit()
            except:
                print(parms['q'], parms['date'], "INSERT FAILED")
                continue

            print(parms['q'], parms['date'], "OK")

            time.sleep(1)

        time.sleep(3)

postal_codes.close()
insert.close()
db.close()
