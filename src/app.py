#!/usr/bin/python3
import random
from datetime import datetime
from flask import Flask, request, render_template, redirect, session, url_for, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'DelhiisDelhi'

connection = sqlite3.connect("MyDatabase.db")
curser = connection.cursor()
query = "SELECT * FROM Groups;" 
result = curser.execute(query)
data = result.fetchall()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'userid' not in session:
        return redirect('/login')
    connection = sqlite3.connect("MyDatabase.db")
    curser = connection.cursor()
    query = "SELECT * FROM Groups;" 
    result = curser.execute(query)
    data = result.fetchall()
    return render_template("index.html", groups=data, data=data, file="dashboard.html")



@app.route("/add_group", methods=['POST','GET'])
def add_group():
    if request.method == 'POST':
        name = request.form['groupname']
        userid = str(session['userid'])+','
        connection = sqlite3.connect("MyDatabase.db")
        curser = connection.cursor()
        groupid = random.randint(1, 99999)
        query = "SELECT * FROM Groups WHERE group_id ='{0}';".format(groupid)
        result = curser.execute(query)
        data = result.fetchone()
        while(data):
            groupid = random.randint(1, 99999)
            query = "SELECT * FROM Groups WHERE group_id ='{0}';".format(groupid)
            result = curser.execute(query)
            data = result.fetchone()
        query = "INSERT INTO Groups (group_id, name,users) VALUES (?,?,?);"
        curser.execute(query, (groupid,name,userid))
        connection.commit()
        return redirect("/get_group/"+str(groupid))
    connection = sqlite3.connect("MyDatabase.db")
    curser = connection.cursor()
    query = "SELECT * FROM Groups;" 
    result = curser.execute(query)
    data = result.fetchall()
    return render_template("add_group.html", data=data)

@app.route("/add_member/<groupid>", methods=['POST','GET'])
def add_member(groupid):
    if request.method == 'POST':
        name = request.form['option']
        connection = sqlite3.connect("MyDatabase.db")
        curser = connection.cursor()
        query = "SELECT * FROM Groups WHERE group_id ='{0}';".format(groupid)
        result = curser.execute(query)
        data = result.fetchone()
        query = "SELECT * FROM Groups WHERE group_id ='{0}';".format(groupid)
        result = curser.execute(query)
        data_set = result.fetchone()
        query = "SELECT * FROM Users;" 
        result = curser.execute(query)
        users = result.fetchall()
        if(name in data[2].split(',')):  
            return render_template('add_member.html',data=users, error=True,group_data=data_set, groupid=groupid)
        name = data[2]+str(name)+","
        query = "UPDATE Groups SET users = '{0}' WHERE group_id ='{1}';".format(name,groupid)
        curser.execute(query)
        connection.commit()
        return redirect("/add_member/"+str(groupid))
    connection = sqlite3.connect("MyDatabase.db")
    curser = connection.cursor()
    query = "SELECT * FROM Users;" 
    result = curser.execute(query)
    users = result.fetchall()
    query = "SELECT * FROM Groups WHERE group_id ='{0}';".format(groupid)
    result = curser.execute(query)
    data = result.fetchone()
    return render_template("add_member.html", data=users,group_data=data, groupid=groupid )


@app.route('/add_transaction/<groupid>', methods=['GET', 'POST'])
def add_transaction(groupid):
    if request.method == 'POST':
        payee = request.form['payee']
        name = request.form['name']
        price = request.form['price']
        
        present = request.form.getlist('present')
        presentcount = len(present)
        foreach = int(price)/presentcount
        presentcal = ""
        for i in present:
            presentcal = presentcal+i+","
        time = datetime.now()
        current_date = time.strftime("%d/%m/%Y")
        current_time = time.strftime("%H:%M:%S")

        connection = sqlite3.connect("MyDatabase.db")
        curser = connection.cursor()
        query = "SELECT * FROM Groups WHERE group_id ='{0}';".format(groupid)
        result = curser.execute(query)
        dataa = result.fetchone()
        transaction_id = random.randint(1, 99999)
        query = "SELECT * FROM Transactions WHERE transaction_id ='{0}';".format(transaction_id)
        result = curser.execute(query)
        data = result.fetchone()
        while(data):
            transaction_id = random.randint(1, 99999)
            query = "SELECT * FROM Transactions WHERE transaction_id ='{0}';".format(transaction_id)
            result = curser.execute(query)
            data = result.fetchone()
        query = "INSERT INTO Transactions (transaction_id, group_id,payee, pending_payment, price, time, date, item_name, foreach) VALUES (?,?,?,?,?,?,?,?,?);"
        curser.execute(query, (transaction_id,groupid,payee,presentcal, price, current_time, current_date,name, foreach))
        connection.commit()
        return redirect("/add_transaction/"+str(groupid))
  
    connection = sqlite3.connect("MyDatabase.db")
    curser = connection.cursor()
    query = "SELECT * FROM Users;" 
    result = curser.execute(query)
    users = result.fetchall()
    query = "SELECT * FROM Groups WHERE group_id ='{0}';".format(groupid)
    result = curser.execute(query)
    data = result.fetchone()
    return render_template("add_transaction.html", data=users,group_data=data, groupid=groupid )


@app.route('/get_group/<id>', methods=['GET','POST'])
def get_group(id):
    connection = sqlite3.connect("MyDatabase.db")
    curser = connection.cursor()
    query = "SELECT * FROM Groups;" 
    result = curser.execute(query)
    groups = result.fetchall()
    query = "SELECT * FROM Groups where group_id = "+id+";" 
    result = curser.execute(query)
    data = result.fetchall()
    query = "SELECT * FROM Users;" 
    result = curser.execute(query)
    users = result.fetchall()
    query = "SELECT * FROM Transactions WHERE group_id = "+id+";"
    result = curser.execute(query)
    transactions = result.fetchall()
    balance = 0
    for transaction in transactions:
        if(str(session['userid']) in transaction[4]):
            print(transaction[8])
            balance = balance + transaction[9]
    return render_template("index.html", file="group.html", data=data, groups=groups, users=users, transactions=transactions, balance=balance)    




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