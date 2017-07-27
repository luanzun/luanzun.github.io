## debian8 安装 Python3.6.2

查看系统python版本
```
~# python
Python 2.7.9 (default, Mar  1 2015, 18:22:53)
[GCC 4.9.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
更新软件包
```
apt-get update
apt-get upgrade
```
安装依赖包
```
aptitude -y install gcc make zlib1g-dev libffi-dev libssl-dev
```

1.下载 Python 3.6.2 
```
~# wget https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tgz
```
2.解压压缩包
```
~# tar -xvf Python-3.6.2.tgz
```
3.授权文件夹权限
```
~# chmod -R +x Python-3.6.2
```
安装依赖包
安装依赖包
```
aptitude -y install  libffi-dev libssl-dev
```
4.进入文件夹，并执行安装配置
```
~# cd Python-3.6.2/
~# ./configure
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
./configure --enable-optimizations
```
5.编译安装
```
~# make && make install
```
6.清理配置文件（有没有必要进行这一步，我也不知道。）
```
~# make clean 
~# make distclean
```
添加快捷方式
```
# ln -s /opt/python3.6.2/bin/python3.6 /usr/bin/python3
# ln -s /opt/python3.6.2/bin/pip3.6 /usr/bin/pip3.6
# ln -s /opt/python3.6.2/bin/pip3 /usr/bin/pip3
# ln -s /opt/python3.6.2/bin/pyvenv-3.6 /usr/bin/pyvenv
```
切入到需要保存 flask 的目录下，并使用 pyvenv 来创建虚拟环境。如
```
cd luejiao.com
pyvenv flask
```
进入虚拟环境
```
source flask/bin/activate
```
