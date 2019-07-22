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
except:
    print("d_weather FAILED TO LOAD")

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
except:
    print("d_station FAILED TO LOAD")

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
except:
    print("d_line FAILED TO LOAD")

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
except:
    print("d_status FAILED TO LOAD")

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
except:
    print("d_train FAILED TO LOAD")

db.commit()
s_dimensions.close()
i_dimensions.close()
db.close()
