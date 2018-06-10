from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pypyodbc
#import sqlite3 as sql
from datetime import datetime
from datetime import timedelta
# import pyodbc
import csv
import os

app = Flask(__name__)

import sqlite3

##################
server = 'ilwin.database.windows.net'
database = 'ilwin'
username = 'ilwin'
password = 'esxi@S5n'
driver = '{SQL Server}'
cnxn = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                        "Server=tcp:ilwin.database.windows.net;Database=ilwin;Uid=ilwin;Pwd=esxi@S5n;")
# cnxn = pyodbc.connect(
#     'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()


@app.route('/')
def home():

   return render_template('index.php')

@app.route('/uploadCSV',methods=['POST'])
def uploadCSV():
    file = request.files['file']
    print(file.filename)
    #######
    destination = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    newfiledest = "/".join([destination, file.filename])
    file.save(newfiledest)
    #######
    with open(file.filename, encoding='ISO-8859-1') as f:
        reader = csv.reader(f)
        columns = next(reader)
        print(columns)
        query = 'insert into EarthquakeTwo ({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))

        for data in reader:
            cursor.execute(query, data)
            cursor.commit()

        m = os.path.getsize(newfiledest)

        return render_template('index.php', variable=m)


@app.route('/UI')
def UI():
    return render_template('view.html')

@app.route('/test1', methods=['GET', 'POST'])
def query_search1():
   if request.method == 'POST':
        range1 = request.form['range1']
        range2 = request.form['range2']
        duration1 = request.form['length']
        if duration1=="day":
            day2=datetime.now()-timedelta(days=1)
        if duration1=="week":
            day2=datetime.now()-timedelta(days=7)
        if duration1=="month":
            day2=datetime.now()-timedelta(days=30)
        cursor.execute("select mag,latitude,longitude from earthquaketwo where (mag between "+range1+" and "+range2+") and timee > ?", (day2,))
        rows = cursor.fetchall()
        for row in rows:
             print(row)
        return render_template('View.html', rows = rows)


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    # print("here")

    if request.method == 'POST':
        # print("inside")
        query = "select count(*) from EarthquakeTwo where mag > 5.0"
        print(query)
        cursor.execute(query)
        result=cursor.fetchone()
        print("code here")
        print(result)
        value=result[0]
        print(value)

        return render_template("View.html", msg=value)


if __name__ == '__main__':
   app.run(debug = True)