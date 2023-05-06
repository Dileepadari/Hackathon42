#!/usr/bin/python3
import random
from flask import Flask, request, render_template, redirect, session, url_for, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'DelhiisDelhi'

connection = sqlite3.connect("MyDatabase.db")
curser = connection.cursor()
query = "SELECT * FROM Users;" 
result = curser.execute(query)
data = result.fetchall()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'userid' not in session:
        return redirect('/login')
    return "successfully connected"


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        connection = sqlite3.connect("MyDatabase.db")
        curser = connection.cursor()
        username = request.form['username']
        password = request.form['password']
        con_pass = request.form['con-password']
        firstname = request.form['Firstname']
        lastname = request.form['Lastname']
        userid = random.randint(1, 99999)
        query = "SELECT * FROM Users WHERE user_id ='{0}';".format(userid)
        result = curser.execute(query)
        data = result.fetchone()
        while(data):
            userid = random.randint(1, 99999)
            query = "SELECT * FROM Users WHERE user_id ='{0}';".format(userid)
            result = curser.execute(query)
            data = result.fetchone()

        query = "SELECT * FROM Users WHERE username ='{0}';".format(username) 
        result = curser.execute(query)
        data = result.fetchone()
        if(data):
            return render_template("signup.html",error="Username already exists")
        else:
            query = "INSERT INTO Users (user_id, username, first_name, last_name, password) VALUES (?,?,?,?,?);"
            result = curser.execute(query, (userid,username,firstname,lastname,password))
            connection.commit()
            session['userid'] = userid
            return redirect("/")
    return render_template("signup.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect("MyDatabase.db")
        curser = connection.cursor()
        query = "SELECT * FROM Users WHERE username ='{0}';".format(username) 
        result = curser.execute(query)
        data = result.fetchone()
        if(data and data[2] == password):
            session['userid'] = data[0]
            return redirect("/")
        else:
            return render_template("login.html",error=True)
    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/login')
if __name__ == '__main__':
    app.run(debug=True)