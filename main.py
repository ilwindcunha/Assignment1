from flask import Flask, render_template, request, redirect, url_for, send_from_directory

import sqlite3 as sql
import csv
import os

app = Flask(__name__)

import sqlite3

conn = sqlite3.connect('database.db')
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






@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

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
        #query = 'insert into Picture ({0}) values ({1})'
        query = 'insert into quiz1 ({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))

        #with sql.connect("imageDB.db") as con:
        with sql.connect("practiceQuiz.db") as con:
           cur = con.cursor()

        for data in reader:
            cur.execute(query, data)

            con.commit()
        print('success')
        return render_template('index.php')

@app.route('/show', methods=['POST'])
def show():
    if request.method == 'POST':

        file = request.files['imageFile']
        print("image file "+file.filename)
        destination = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        newfiledest = "/".join([destination, file.filename])
        file.save(newfiledest)

    return render_template('index.php')



@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)