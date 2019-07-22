import mysql.connector

from config import dbconfig, process

try:
    db = mysql.connector.connect(**dbconfig)
except:
    print("Unable to reach database server")
    quit()

s_dimensions = db.cursor(buffered=True)
i_dimensions = db.cursor()
args = []

try:
    i_dimensions.execute("TRUNCATE TABLE d_weather")

    i_dimensions.execute(
        """
        INSERT INTO d_weather(`code`, `label`)
        SELECT DISTINCT `weatherCode`, `weatherDesc`
        FROM weather
        ORDER BY `weatherCode`
        """
    )

    print("d_weather LOADED")
except mysql.connector.Error as err:
    print("d_weather FAILED TO LOAD: {}".format(err))

try:
    i_dimensions.execute("TRUNCATE TABLE d_station")

    i_dimensions.execute(
        """
        INSERT INTO d_station(`label`, `code`, `postal_code`, `latitude`,
        `longitude`, `address`)
        SELECT `from`, `from_id`, `postal_code`, `lat`, `lng`,
        `formatted_address`
        FROM station
        ORDER BY `from_id`
        """
    )

    print("d_station LOADED")
except mysql.connector.Error as err:
    print("d_station FAILED TO LOAD: {}".format(err))

try:
    i_dimensions.execute("TRUNCATE TABLE d_line")

    i_dimensions.execute(
        """
        INSERT INTO d_line(`label`, `type`)
        SELECT DISTINCT `line`, `type`
        FROM train_trip
        ORDER BY `type`, `line`
        """
    )

    print("d_line LOADED")
except mysql.connector.Error as err:
    print("d_line FAILED TO LOAD: {}".format(err))

try:
    i_dimensions.execute("TRUNCATE TABLE d_status")

    i_dimensions.execute(
        """
        INSERT INTO d_status(`label`)
        SELECT DISTINCT `status`
        FROM train_trip
        ORDER BY `status`
        """
    )

    print("d_status LOADED")
except mysql.connector.Error as err:
    print("d_status FAILED TO LOAD: {}".format(err))

try:
    i_dimensions.execute("TRUNCATE TABLE d_train")

    i_dimensions.execute(
        """
        INSERT INTO d_train(`label`)
        SELECT DISTINCT `train_id`
        FROM train_trip
        ORDER BY `train_id`
        """
    )

    print("d_train LOADED")
except mysql.connector.Error as err:
    print("d_train FAILED TO LOAD: {}".format(err))

try:
    i_dimensions.execute("TRUNCATE TABLE d_event_venue")

    i_dimensions.execute(
        """
        INSERT INTO d_event_venue(station_id, label, latitude, longitude)
        SELECT DISTINCT d_station.id, venue_name,
        CAST(venue_latitude AS DECIMAL(11,8)),
        CAST(venue_longitude AS DECIMAL(11,8))
        FROM eventbrite
        LEFT JOIN d_station
        ON eventbrite.from_id = d_station.code
        """
    )

    print("d_event_venue LOADED")
except mysql.connector.Error as err:
    print("d_event_venue FAILED TO LOAD: {}".format(err))

db.commit()
s_dimensions.close()
i_dimensions.close()
db.close()
