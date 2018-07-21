# Debian8 + Flask + Nginx + uWSGI + uWSGI Emperor 

1. <code>uWSGI</code> 配置文件 <code>/home/luejiao.com/luejiao_uwsgi.ini</code>
```
[uwsgi]
# 指向网站目录
base = /home/luejiao.com

# 启动文件
wsgi-file = run.py

module = app

# 虚拟目录
home = %(base)/flask

# 按字面意思是python的环境变量路径，写的是网站根目录
pythonpath = %(base)

#socket文件的路径 socket file's location
socket = /home/luejiao.com/tmp/%n.sock

#pchmod-socket的权限 ermissions for the socket file
chmod-socket = 644

#the variable that holds a flask application inside the module imported at line #6
callable = app

#日志文件的路径 location of log files
logto = /wwwlogs/uwsgi/%n.log 

# 处理器数
processes = 4

# 线程数
1threads = 2

# 修改代码时，自动重启uwsgi服务
python-autoreload=1
```
2. 新建保存日志的文件夹，并赋权
```
mkdir -p /wwwlogs/uwsgi
chown -R www:www /wwwlogs/uwsgi
```

3. 在网站的 nginx conf 配置文件中，添加：
```
location / {
    try_files $uri @yourapplication;
    }
  location @yourapplication {
        include uwsgi_params;
        uwsgi_pass unix:/home/luejiao.com/tmp/luejiao_uwsgi.sock;# 这里注意替换成自己的socket文件路径
    }
```

下面是重头戏，**debian8** 和 **debian7** 在配置 <code>uWSGI Emperor</code> 是不一样的！！！
**debian7** 是把配置文件放到 <code>/etc/init/uwsgi.conf</code>，而在 **debian8** 中，是放到 <code>/etc/systemd/system/</code> 中的。
本文章是讲 **debian8** 的环境下配置 <code>uWSGI Emperor</code> 。 [官方对应文档](http://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Systemd.html?highlight=conf)

4. 新建<code>/etc/systemd/system/emperor.uwsgi.service</code>文件，代码如下：
```
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
#uwsgi 服务的路径，以及需要启动的 ini 文件路径，根据自己的实际情况进行修改
ExecStart=/usr/local/bin/uwsgi --ini /etc/uwsgi/emperor.ini
# Requires systemd version 211 or newer
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
5. 上述代码中，<code>/etc/uwsgi/emperor.ini</code> 文件的代码如下：
```
[uwsgi]
emperor = /etc/uwsgi/vassals
uid = www
gid = www
```

6. 把网站的 uwsgi.ini 文件要给个软链，加到 <code>/etc/uwsgi/vassals/</code> 文件夹中：
```
mkdir /etc/uwsgi && mkdir /etc/uwsgi/vassals
ln -s /home/luejiao.com/luejiao_uwsgi.ini /etc/uwsgi/vassals
```

7. 在第5步中的文件夹中，设置了文件所有者是 <code>www:www</code>，我们要给对应的文件夹和文件做所有者权限修改（这一步根据实际情况来判断是否需要）：
```
chown -R www:www /home/luejiao.com
chown -R www:www /var/log/uwsgi/
```

8. 运行服务：
```
systemctl start emperor.uwsgi.service
```
检查状态：
```
systemctl status emperor.uwsgi.service
```
