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
s_stations = db.cursor(buffered=True)
i_stations = db.cursor()

args = []

s_stations.execute(
    """
    SELECT DISTINCT `from`, `from_id`
    FROM train_trip
    WHERE 1 = 1
    AND type = 'NJ Transit'
    UNION
    SELECT DISTINCT `to`, `to_id`
    FROM train_trip
    WHERE 1 = 1
    AND type = 'NJ Transit'
    """
)

for station in s_stations:

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

    args.append(
        (
            station[0], station[1], lat, lng, formatted_address,
            postal_code, req.text
        )
    )

    print(station[0], station[1], 'RETRIEVED')

    time.sleep(1)

try:

    i_stations.executemany(
        """
        INSERT INTO `station`
        (
            `from`, `from_id`, `lat`, `lng`, `formatted_address`,
            `postal_code`, `response`
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s
        )
        """,
        args
    )

    db.commit()
    print('station LOADED')

except mysql.connector.Error as err:

    print("station FAILED TO LOAD: {}".format(err))

s_stations.close()
i_stations.close()
db.close()
