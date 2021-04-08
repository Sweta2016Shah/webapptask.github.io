from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="remotemysql.com",user="rQf9cA1H1m",password="vHGGnRUZuI",database="rQf9cA1H1m")
mycursor=conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
       return render_template('home.html')
    else:
        return redirect('/')


@app.route('/login_validation', methods = [ 'POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    return render_template('home.html')

    mycursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """.format(email,password))
    users=mycursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user',methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    mycursor.execute("""INSERT INTO `users` (`users_id`,`name`,`email`,`password`) VALUES(NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()
    mycursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=mycursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
app.run()
