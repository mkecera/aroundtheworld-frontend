from flask import render_template
from flask import Flask, request
import MySQLdb

app = Flask(__name__)

stations_dict = {}
similarity_tables_list = []


@app.route('/')
def index():
    db_noaahourly = MySQLdb.connect(host="database-atw2.cvfgbrtjh8kr.us-east-1.rds.amazonaws.com",
                                    user="darren",
                                    passwd="aroundtheworld",
                                    db="noaahourly")

    db_similarity = MySQLdb.connect(host="database-atw2.cvfgbrtjh8kr.us-east-1.rds.amazonaws.com",
                                    user="darren",
                                    passwd="aroundtheworld",
                                    db="similarity")

    cur_noaahourly = db_noaahourly.cursor()
    cur_similarity = db_similarity.cursor()
    stations_list = []

    try:
        # get list of all stations
        cur_noaahourly.execute("SELECT * FROM stations")
        stations_list = [list(row) for row in list(cur_noaahourly.fetchall())]

        # some station names have backslashes causing parsing errors
        for row in stations_list:
            if row[1] is not None:
                row[1] = row[1].replace("\\", "")

        # convert list of lists into dictionary
        for row in stations_list:
            stations_dict[row[0]] = row

        # get list of similarity tables
        cur_similarity.execute("SHOW TABLES")
        global similarity_tables_list
        similarity_tables_list = [row[0] for row in list(cur_similarity.fetchall())]

        # get list of stations with at least 1 similarity table
        similarity_tables_list_unique = [int(table[table.find("_")+1:table.rfind("_")]) for table in
                                         similarity_tables_list if table.count("_") == 2]
        similarity_tables_list_unique = list(dict.fromkeys(similarity_tables_list_unique))

        # filter list of all stations so that remaining stations each have at least 1 similarity table
        stations_list = [stations_dict[table] for table in similarity_tables_list_unique
                         if table in stations_dict.keys()]
    except Exception as e:
        print(e)
    finally:
        cur_noaahourly.close()
        cur_similarity.close()
        db_noaahourly.close()
        db_similarity.close()

    return render_template('index.html', data=stations_list)


@app.route('/similarity')
def similarity():
    db_similarity = MySQLdb.connect(host="database-atw2.cvfgbrtjh8kr.us-east-1.rds.amazonaws.com",
                                    user="darren",
                                    passwd="aroundtheworld",
                                    db="similarity")

    station = request.args.get("station")
    month = request.args.get("month")
    limit = 100
    cur = db_similarity.cursor()
    similar_stations_obj = {"stations": [], "available": []}

    if station is not None and month is not None and limit is not None:
        available = []

        for i in range(1, 13):
            if "station_" + station + "_" + str(i) in similarity_tables_list:
                available.append(i)

        similar_stations_obj["available"] = available

        try:
            cur.execute("SELECT * FROM station_" + station + "_" + month + " LIMIT " + str(limit))
            similar_stations_list = [list(row) for row in list(cur.fetchall())]
            stations = []

            for row in similar_stations_list:
                station = stations_dict[row[0]]
                if station is not None:
                    station.append(row[1])
                    stations.append(station)

            similar_stations_obj["stations"] = stations
        except Exception:
            pass
        finally:
            cur.close()
            db_similarity.close()

    return similar_stations_obj
