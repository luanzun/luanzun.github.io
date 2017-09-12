<code>app/__init__.py</code> 添加初始化代码

```
# -*- conding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# 数据库连接
# http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
#"数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"
app.config['SECRET_KEY'] ='hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://testuser:testuser521@localhost:3306/test'
#设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app)
```
<code>app/models.py</code> 定义模型：
```
# -*- conding: utf-8 -*-
from app import db

#'''定义模型，建立关系'''
class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串，虽然不是完全必要，不过用于调试和测试还是很不错的。
    def __repr__(self):
        return '<Role {}> '.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)
```
<code>db_migrate.py</code> 执行操作代码，其中部分操作代码被我注释了，可以根据实际情况取消注释来测试效果：
```
#!flask/bin/python3
# -*- conding: utf-8 -*-
from app import db
from app import models

if __name__ == '__main__':
    #删除旧表
    db.drop_all()
    db.create_all()

    #插入数据
    admin_role = models.Role(name='Admin')
    #mod_role = models.Role(name='Moderator')
    user_role = models.Role(name='User')
    # role 属性也可使用，虽然不是真正的数据库列，但却是一对多关系的高级表示
    user_john = models.User(username='john', role=admin_role)
    user_susan = models.User(username='susan', role=user_role)
    user_david = models.User(username='david', role=user_role)

    # 准备把对象写入数据库之前，先要把其添加到会话中，数据库会话 db.session 和 Flask session 对象没有关系，数据库会话也称事物
    db.session.add_all([admin_role, user_role, user_john, user_susan, user_david])
    # 提交会话到数据库
    db.session.commit()

    # #修改roles名
    # admin_role.name = 'Administrator'
    # db.session.add(admin_role)
    # db.session.commit()

    # 删除数据库会话，从数据库中删除“Moderator”角色
    #db.session.delete(mod_role)
    #db.session.commit()
    # 注意删除，和插入更新一样，都是在数据库会话提交后执行

    # 查询
    #print(user_role)
    print(models.User.query.filter_by(role=user_role).all())
```