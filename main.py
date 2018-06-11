from flask import Flask, render_template, request, redirect, url_for, send_from_directory
# import pypyodbc
#import sqlite3 as sql
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
        query = 'insert into quizone ({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))

        for data in reader:
            cursor.execute(query, data)

        cursor.commit()

        m = os.path.getsize(newfiledest)

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


    return render_template('index.php')


@app.route('/name')
def vehicle():
    return render_template('names.php')





@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        result = []
        courceNo = request.form['courceNo']
        day = request.form['day']
        print(courceNo)
        #cursor.execute("select room from pic WHERE vehicle=?", (vehicleName,))
        # cursor.execute("select room,picture from pic WHERE vehicle='Car'")
        cursor.execute("select Instructor from quizone where Course=? and Dayss = ?", (courceNo,day))

        rows = cursor.fetchall()
        return render_template("list.html", rows=rows)

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

@app.route('/list')
def list():

    cursor.execute("select * from pic")

    rows = cursor.fetchall()
    return render_template("list.html", rows=rows)



if __name__ == '__main__':
   app.run(debug = True)