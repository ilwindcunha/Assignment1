from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pyodbc
import sqlite3 as sql
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
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()

##################
#conn = sqlite3.connect('database.db')
m = 0
# print("Opened database successfully")
# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print("Table created successfully")
# conn.close()

@app.route('/')
def home():
   return render_template('index.php')

@app.route('/enternew')
def new_student():
   return render_template('student.html')




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
        query = 'insert into pic ({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))

        for data in reader:
            cursor.execute(query, data)

        cursor.commit()

        m = "success"
        return render_template('index.php', variable=m)


@app.route('/show', methods=['POST'])
def show():
    if request.method == 'POST':

        file = request.files['imageFile']

        print("image file "+file.filename)
        destination = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        newfiledest = "/".join([destination+"/static", file.filename])
        file.save(newfiledest)
        m=os.path.getsize(newfiledest)
        print(m)
        sep = '.'
        name=file.filename.split(sep,1)[0]
        print(name)
        print(newfiledest)
        #cursor.execute('UPDATE pic SET IMGSRC = ? WHERE name = ?', (newfiledest,name))
        #cursor.execute("UPDATE pic SET picture = 'abc' WHERE name='Nora'")
        # query = "insert into im VALUES('" + name + "','" + newfiledest+ "');"
        # print (query)
        # cursor.execute(query)
        # cursor.commit

        # in_file = open(newfiledest, "rb")  # opening for [r]eading as [b]inary
        # data = in_file.read()  # if you only wanted to read 512 bytes, do .read(512)
        # in_file.close()
        #sql = "update pic set picture = ? where name= 'Nora'"
        #cursor.execute(sql, (pyodbc.Binary(data),))
        #cursor.commit()


    return render_template('index.php', variable=m)


@app.route('/vehicle')
def vehicle():
    return render_template('Vehicle.html', variable=m)





@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        result = []
        vehicleName = request.form['vehicleName']
        print(vehicleName)
        #cursor.execute("select room from pic WHERE vehicle=?", (vehicleName,))
        cursor.execute("select room,picture from pic WHERE vehicle='Car'")
        room = []
        picture = []

        for row in cursor:
            result.append(row)
        print(result)

        room = [x[0] for x in result]

        picture = [x[1] for x in result]

        zipped_data = zip(picture, room)

        print(room)
        print(picture)

        print(zipped_data)


    return render_template('View.html', zipped_data=zipped_data)

# @app.route('/uploadCSV',methods=['POST'])
# def uploadCSV():
#     file = request.files['file']
#     print(file.filename)
#
#     with sql.connect("practiceQuiz.db") as con:
#         cur = con.cursor()
#
#         cur.execute("delete from quiz1")
#
#         con.commit()
#
#     #######
#     destination = os.path.join(os.path.dirname(os.path.abspath(__file__)))
#     newfiledest = "/".join([destination, file.filename])
#     file.save(newfiledest)
#     #######
#
#     with open(file.filename, encoding='ISO-8859-1') as f:
#
#         reader = csv.reader(f)
#         columns = next(reader)
#         print(columns)
#         #query = 'insert into Picture ({0}) values ({1})'
#         query = 'insert into quiz1 ({0}) values ({1})'
#         query = query.format(','.join(columns), ','.join('?' * len(columns)))
#
#         #with sql.connect("imageDB.db") as con:
#         with sql.connect("practiceQuiz.db") as con:
#            cur = con.cursor()
#
#         for data in reader:
#             cur.execute(query, data)
#
#             con.commit()
#         print('success')
#         return render_template('index.php')
#
# @app.route('/show', methods=['POST'])
# def show():
#     if request.method == 'POST':
#
#         file = request.files['imageFile']
#
#         print("image file "+file.filename)
#         destination = os.path.join(os.path.dirname(os.path.abspath(__file__)))
#         newfiledest = "/".join([destination, file.filename])
#         file.save(newfiledest)
#         m=os.path.getsize(newfiledest)
#         print(m)
#
#
#     return render_template('index.php', variable=m)





if __name__ == '__main__':
   app.run(debug = True)