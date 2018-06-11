from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# import pypyodbc
#import sqlite3 as sql
from datetime import datetime
from datetime import timedelta
import pyodbc
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
# cnxn = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
#                         "Server=tcp:ilwin.database.windows.net;Database=ilwin;Uid=ilwin;Pwd=esxi@S5n;")
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()


@app.route('/')
def home():

   return render_template('index.php')



@app.route('/UI')
def UI():
    return render_template('view.html')


@app.route('/earthquake')
def earthquake():

   return render_template('view2.html')


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

@app.route('/search', methods=['GET', 'POST'])
def search():
   if request.method == 'POST':
        range1 = request.form['range1']
        range2 = request.form['range2']
        duration1 = request.form['length']
        if duration1=="day":
            length=datetime.now()-timedelta(days=1)
        if duration1=="week":
            length=datetime.now()-timedelta(days=7)
        if duration1=="month":
            length=datetime.now()-timedelta(days=30)
        cursor.execute("select mag,latitude,longitude from earthquaketwo where (mag between "+range1+" and "+range2+") and timee > ?", (length,))
        rows = cursor.fetchall()
        for row in rows:
             print(row)
        return render_template('View.html', rows = rows)



@app.route('/searchTwo', methods=['GET', 'POST'])
def searchTwo():
   if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']


        query=("select top 20 mag,latitude,longitude, "
                       "111.045* DEGREES(ACOS(COS(RADIANS(latpoint))"
                       "* COS(RADIANS(latitude))"
                       "* COS(RADIANS(longpoint) - RADIANS(longitude))"
                       "+ SIN(RADIANS(latpoint))"
                       "* SIN(RADIANS(latitude)))) AS distance_in_km "
                       "from earthquaketwo "
                       "JOIN ("
                       "SELECT  "+latitude+" AS latpoint, "+longitude+" AS longpoint"
                       ") AS p ON 1=1 "
                       "ORDER BY distance_in_km")
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
             print(row)
        return render_template('view2.html', rows = rows)


if __name__ == '__main__':
   app.run(debug = True)