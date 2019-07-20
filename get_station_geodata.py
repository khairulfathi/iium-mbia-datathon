import requests
import json
import ssl
import mysql.connector
import time
from config import dbconfig, gmap, process

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

db = mysql.connector.connect(**dbconfig)
stations = db.cursor(buffered=True)
insert = db.cursor()

sstation = """
            SELECT DISTINCT `from`, `from_id`
            FROM train_trip_2
            WHERE type = 'NJ Transit'
            AND line = 'Main Line'
            """
istation = """
            INSERT INTO `station`
            (
                `from`, `from_id`, `lat`, `lng`, `formatted_address`,
                `postal_code`, `geodata`
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s
            )
            """

stations.execute(sstation)

for station in stations:

    parms = dict()
    parms["address"] = station[0] + " train station"
    parms["key"] = gmap['key']

    try:
        req = requests.get(url=gmap['geo'], params=parms)
        data = req.json()
    except:
        print(parms, "REQUEST FAILED")
        continue

    if 'status' not in data or (
        data['status'] != 'OK' and data['status'] != 'ZERO_RESULTS'
    ):
        break

    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    formatted_address = data['results'][0]['formatted_address']

    for address_components in data['results'][0]['address_components']:
        if address_components['types'][0] == 'postal_code':
            postal_code = address_components['long_name']

    args = (
        station[0], station[1], lat, lng, formatted_address,
        postal_code, data
        )
    insert.execute(istation, args)

    print(station, formatted_address, postal_code)

    time.sleep(2)

db.commit()
stations.close()
insert.close()
db.close()
