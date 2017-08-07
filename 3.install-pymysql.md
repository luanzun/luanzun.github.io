1.虚拟环境状态下，使用*pip3*安装*PyMySQL*
```
cd /home/pyte.vip  # *pyte.vip* 是我的网站根目录，请自行替换成自己的网站根目录，下同
```
进入虚拟环境
```
source flask/bin/activate
```
安装
```python
pip3 install PyMySQL
```
2.安装成功后，我们来测试连接以下。

* 连接数据库前，请先确认以下事项：
* 您已经创建了数据库 TESTDB.
* 在TESTDB数据库中您已经创建了表 EMPLOYEE
* EMPLOYEE表字段为 FIRST_NAME, LAST_NAME, AGE, SEX 和 INCOME。
* 连接数据库TESTDB使用的用户名为 "testuser" ，密码为 "test123",你可以可以自己设定或者直接使用root用户名及其密码，用户需要拥有**GRANT** 管理权限。Mysql数据库用户授权请使用*Grant*命令。

新建测试文件 *mysql.py*，代码：
```
#!flask/bin/python3
#coding=utf-8

import pymysql

# 打开数据库连接
db = pymysql.connect(host='127.0.0.1', port=3306, user='testuser', passwd='test123', db='TESTDB')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询 
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print ("Database version : %s " % data)

# 关闭数据库连接
db.close()
```
3.在虚拟环境下，执行刚才的*mysql.py*文件：
```
python3 mysql.py
```
4.结果会显示数据库的版本号。
```
Database version : 5.7.19-log
```
到这里，才算是真正的使用*pymysql*连接到了数据库。