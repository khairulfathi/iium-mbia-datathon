'''
   TODO:
       1. Add pagination support from API response. Now only retrieved
       first 50 records.
'''

import requests
import json
import mysql.connector
import time
from config import dbconfig, eventbrite, process

try:
    db = mysql.connector.connect(**dbconfig)
except:
    print("Unable to reach database server")
    quit()

stations = db.cursor(buffered=True)
insert = db.cursor()

sstation = """
            SELECT `id`, `from`, `from_id`, `lat`, `lng`
            FROM station
            """
ievent = """
            INSERT INTO `eventbrite`
            (
                `station_id`, `from`, `from_id`, `name`, `start_local`,
                `end_local`, `venue_name`, `venue_latitude`, `venue_longitude`,
                `response`
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
stations.execute(sstation)

for station in stations:

    query = {
        'location.latitude': station[3],
        'location.longitude': station[4],
        'location.within': '1km',
        'expand': 'venue',
        'start_date.range_start': process['start_date'],
        'start_date.range_end': process['end_date']
        }
    args = []

    req = requests.get(
            url=eventbrite['endpoint'],
            params=query,
            headers={'Authorization': 'Bearer ' + eventbrite['key']}
        )
    data = req.json()

    if data['pagination']['has_more_items'] is True:
        print(
            "Responses over 50 records, saving first 50 only. Station:",
            station[1]
            )

    for event in data['events']:

        if event['online_event'] is True:
            continue

        args.append(
            (
                station[0], station[1], station[2], event['name']['text'],
                event['start']['local'], event['end']['local'],
                event['venue']['name'], event['venue']['latitude'],
                event['venue']['longitude'], req.text
            )
        )

    try:
        insert.executemany(ievent, args)
        db.commit()
        print(station[1], 'OK')
    except:
        print(station[1], 'FAILED')
        continue
