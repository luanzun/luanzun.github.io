```
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
import pymysql
from app import app

config = {
    'host':'localhost',
    'port':3306,
    'user':'test',
    'password':'testuser',
    'db':'test'
    }
db = pymysql.connect(**config)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html", title="注册")


@app.route("/signup",methods=["POST"])
def signup():
    username = str(request.form["user"])
    password = str(request.form["password"])
    email = str(request.form["email"])

    cursor = db.cursor()

    cursor.execute("INSERT INTO user (name,password,email)VALUES(%s,%s,%s)",(username,password,email))
    db.commit()
    return redirect(url_for("loginlogin.html"))

@app.route("/login.html")
def login():
    return render_template("login.html",title="data")

@app.route("/checkuser",methods=["POST"])
def check():
    username = str(request.form["user"])
    password = str(request.form["password"])
    cursor = db.cursor()
    cursor.execute("SELECT name FROM user WHERE name ='"+ username +"'")
    user = cursor.fetchone()

    if len(user) is 1:
        return redirect(url_for("home"))
    else:
        return "failed"

@app.route("/home.html")
def home():
    return render_template("home.html")

#微信公众号
@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        token = "baba521"
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        temparr = [timestamp,nonce,token]
        temparr.sort()
        s = temparr[0] + temparr[1] + temparr[2]
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        if hascode == signature:
            return echostr
        else:
            return ""
    else:  # POST
        #print("POST")
        xml_data = request.data
        xmldict = wechat.recv_msg(xml_data)
        reply = wechat.submit_msg(xmldict)
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response
```

<code>app/templates/index.html</code>
```
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{title}}</title>
    </head>
    <body>
        <h1>{{title}}</h1>
        <form action="/signup" method="post">
        <input type="text" name="user" placeholder="username">
        <br>
        <input type="text" name="password" placeholder="password">
        <br>
        <input type="text" name="email" placeholder="email">
        <br>
        <input type="submit">
        </form>
    </body>
</html>
```
<code>app/templates/login.html</code>
```
<!-- extend from base layout -->
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{data}}</title>
    </head>
    <body>
        <form action="/checkuser" method="post">
        <input type="text" name="user" placeholder="username">
        <input type="text" name="password" placeholder="password">
        <input type="submit">
        </form>
    </body>
</html>
```

<code>app/templates/home.html</code>
```
<!-- extend from base layout -->
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{{data}}</title>
    </head>
    <body>
        <form action="/checkuser" method="post">
        <input type="text" name="user" placeholder="username">
        <input type="text" name="password" placeholder="password">
        <input type="submit">
        </form>
    </body>
</html>
```
