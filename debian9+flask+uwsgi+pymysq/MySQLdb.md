from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost",user="root",password="root",db="login_data")

@app.route("/")
def index():
    return render_template("index.html", title="登陆")

@app.route("/signup",methods=["POST"])
def signup():
    username = str(request.form["user"])
    password = str(request.form["password"])
    email = str(request.form["email"])

    cousor = conn.cousor()

    cousor.execute("INSERT INTO user (name,password,email)values(%s,%s,%s)"),(username,password,email)
    conn.commit()
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html",title="data")

@app.route("/checkuser",mathods=["POST"])
def check():
    username = str(request.form["user"])
    password = str(request.form["password"])
    cursor = conn.cursor()
    cursor.execute("SELECTname FROM user WHERE name ='"+ username +"'")
    user = cursor.fetchone()

    if len(user) is 1:
        return redirect(url_for("home"))
    else:
        return "failed"

@app.route("/home")
def home():
    return render_template("home.html")
