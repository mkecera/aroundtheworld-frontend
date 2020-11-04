from flask import render_template
from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'database-atw2.cvfgbrtjh8kr.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'darren'
app.config['MYSQL_PASSWORD'] = 'aroundtheworld'
app.config['MYSQL_DB'] = 'noaahourly'

mysql = MySQL(app)

bla = "ho"
ble = "hu"

@app.route('/')
def index(name=None):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stations")
    data = list(cur.fetchall())

    # convert list of tuples into list of lists
    data = [list(row) for row in data]

    # some station names have backslashes causing parsing errors
    for row in data:
        if row[1] is not None:
            row[1] = row[1].replace("\\", "")

    cur.close()

    return render_template('index.html', name=name, data=data)
