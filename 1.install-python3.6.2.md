## debian8 安装 Python3.6.2
很多 flask 的教程，指出服务器需要搭建 nginx 环境。为了方便管理，我是用的 lnmp 一键安装包。大家自行抉择。

查看系统python版本
```
python
Python 2.7.9 (default, Mar  1 2015, 18:22:53)
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
1.更新软件包
```
apt-get update
apt-get upgrade
```
2.安装依赖包
```
aptitude -y install gcc make zlib1g-dev libffi-dev libssl-dev
```

3.下载 Python 3.6.2 
```
wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
```
4.解压压缩包
```
tar -xvf Python-3.6.2.tgz
```
5.授权文件夹权限
```
chmod -R +x Python-3.6.2
```

6.进入文件夹，并执行安装配置
```
cd Python-3.6.2/
./configure
```
或者将python3安装到其它目录下
```
./configure --prefix=/opt/python3.6.2
```
会提示以下信息
```
If you want a release build with all optimizations active (LTO, PGO, etc), please run ./configure --enable-optimizations.
```
按照提示进行执行代码，参考链接：http://stackoverflow.com/questions/41405728/what-does-enable-optimizations-do-while-compiling-python?noredirect=1
```
注意，如果按照提示执行了代码，那么刚才设置的指定安装路径则无效，会安装到 usr/local/bin 里面。如果你只想用 python3 来执行 flask，那么是否安装到指定目录，对你的目标并没有影响。
./configure --enable-optimizations
```
7.安装依赖包，
```
aptitude -y install  libffi-dev libssl-dev
```
8.编译安装
```
make && make install
```
9.清理配置文件（有没有必要进行这一步，我也不知道。）
```
make clean 
make distclean
```
10.添加快捷方式
```
# ln -s /opt/python3.6.2/bin/python3.6 /usr/bin/python3
# ln -s /opt/python3.6.2/bin/pip3.6 /usr/bin/pip3.6
# ln -s /opt/python3.6.2/bin/pip3 /usr/bin/pip3
# ln -s /opt/python3.6.2/bin/pyvenv-3.6 /usr/bin/pyvenv
```
