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
        cur_noaahourly.execute("SELECT * FROM stations2 WHERE elevation > -300")
        stations_list = [list(row) for row in list(cur_noaahourly.fetchall())]

        # some station names have backslashes causing parsing errors
        for row in stations_list:
            if row[1] is not None:
                row[1] = row[1].replace("\\", "")

        # convert list of lists into dictionary
        global stations_dict
        for row in stations_list:
            station = row[0]
            month = row[5]
            if station in stations_dict.keys():
                stations_dict[station][month] = row
            else:
                stations_dict[station] = {month: row}

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
    station = request.args.get("station")
    month = request.args.get("month")
    limit = 100
    similar_stations_obj = {"stations": [], "available": []}

    if station is not None and month is not None and limit is not None:
        db_similarity = MySQLdb.connect(host="database-atw2.cvfgbrtjh8kr.us-east-1.rds.amazonaws.com",
                                        user="darren",
                                        passwd="aroundtheworld",
                                        db="similarity")
        cur = db_similarity.cursor()
        available = []

        global similarity_tables_list
        for i in range(1, 13):
            if "station_" + station + "_" + str(i) in similarity_tables_list:
                available.append(i)

        similar_stations_obj["available"] = available

        try:
            cur.execute("SELECT * FROM station_" + station + "_" + month + " LIMIT " + str(limit))
            similar_stations_list = [list(row) for row in list(cur.fetchall())]
            similar_stations = []

            global stations_dict
            for row in similar_stations_list:
                if row[0] in stations_dict.keys() and int(month) in stations_dict[row[0]]:
                    similar_station = stations_dict[row[0]][int(month)]
                    similar_station.append(row[1])
                    similar_stations.append(similar_station)

            similar_stations_obj["stations"] = similar_stations
            similar_stations_obj["similarity_tables_list"] = similarity_tables_list
            similar_stations_obj["similar_stations_list"] = similar_stations_list
        except Exception as e:
            similar_stations_obj = {
                "e": e,
                "similarity_tables_list": similarity_tables_list,
                "similar_stations_list": similar_stations_list
            }
        finally:
            cur.close()
            db_similarity.close()

    return similar_stations_obj
