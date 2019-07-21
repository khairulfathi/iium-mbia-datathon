import mysql.connector
from datetime import timedelta, date
from config import dbconfig


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_quater(month):
    if int(month) in [1, 2, 3]:
        return 1
    elif int(month) in [4, 5, 6]:
        return 2
    elif int(month) in [7, 8, 9]:
        return 3
    elif int(month) in [10, 11, 12]:
        return 4
    else:
        return False


try:
    db = mysql.connector.connect(**dbconfig)
except:
    print("Unable to reach database server")
    quit()

insert = db.cursor()

i_date = """
            INSERT INTO `d_date`
            (
                `label`, `day`, `weekday`, `weekday_label`, `week`, `month`,
                `month_label`, `quater`, `year`
            )
            VALUES
            (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

start_date = date(2018, 1, 1)
end_date = date(2020, 1, 1)
args = []

for single_date in daterange(start_date, end_date):

    args.append((
        single_date.strftime("%Y-%m-%d"),
        single_date.strftime("%d"),
        single_date.strftime("%w"),
        single_date.strftime("%A"),
        single_date.strftime("%W"),
        single_date.strftime("%m"),
        single_date.strftime("%B"),
        get_quater(single_date.strftime("%m")),
        single_date.strftime("%Y")
    ))

insert.executemany(i_date, args)
db.commit()
print("d_date SAVED")

i_time = """
            INSERT INTO `d_time`
            (
                `label`, `hour`, `minute`
            )
            VALUES
            (
                %s, %s, %s
            )
            """
args = []

for hour in range(0, 13):

    for minute in range(0, 60):

        args.append((
            str(hour).zfill(2) + ":" + str(minute).zfill(2),
            hour,
            minute
        ))

insert.executemany(i_time, args)
db.commit()
print("d_time SAVED")
