from flask import render_template
from flask import Flask, request
import MySQLdb

app = Flask(__name__)

db_noaahourly = MySQLdb.connect(host="database-atw2.cvfgbrtjh8kr.us-east-1.rds.amazonaws.com",
                                user="darren",
                                passwd="aroundtheworld",
                                db="noaahourly")

db_similarity = MySQLdb.connect(host="database-atw2.cvfgbrtjh8kr.us-east-1.rds.amazonaws.com",
                                user="darren",
                                passwd="aroundtheworld",
                                db="similarity")

stations_dict = {}


@app.route('/')
def index():
    cur = db_noaahourly.cursor()
    cur.execute("SELECT * FROM stations")
    stations_list = list(cur.fetchall())
    cur.close()

    # convert list of tuples into list of lists
    stations_list = [list(row) for row in stations_list]

    # some station names have backslashes causing parsing errors
    for row in stations_list:
        if row[1] is not None:
            row[1] = row[1].replace("\\", "")

    # convert list of lists into dictionary
    for row in stations_list:
        stations_dict[row[0]] = row

    return render_template('index.html', data=stations_list)


@app.route('/similarity')
def similarity():
    station = request.args.get("station")
    month = request.args.get("month")
    limit = request.args.get("limit")
    similar_stations_obj = {"stations": []}
    cur = db_similarity.cursor()

    try:
        cur.execute("SELECT * FROM station_" + station + "_" + month)
        similar_stations_list = list(cur.fetchall())

        # convert list of tuples into list of lists
        similar_stations_list = [list(row) for row in similar_stations_list[:101]]

        stations = []

        for row in similar_stations_list:
            station = stations_dict[row[0]]
            if station is not None:
                station.append(row[1])
                stations.append(station)

        similar_stations_obj["stations"] = stations
    except Exception as e:
        print(e)
    finally:
        cur.close()

    return similar_stations_obj
