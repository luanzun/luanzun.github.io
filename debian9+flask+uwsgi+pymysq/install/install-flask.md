1. 进入到需要保存 flask 的目录下，并使用 pyvenv 来创建虚拟环境。使用 pyvenv创建的虚拟环境，只有 python3 ，并不包含系统自带的 2.7 版本。
```
cd /home/pyte.vip ## *pyte.vip* 是我的网站根目录，请自行替换成自己的网站根目录，下同
python3.6 -m venv flask
```
2.进入虚拟环境
```
source flask/bin/activate
```
注意，虚拟环境状态下，会显示虚拟环境的目录，如
```
(flask) root@debian:/home/pyte.vip# 
```
3.在虚拟环境状态下，使用 pip3 安装 flask及相关扩展
```
pip3 install flask
pip3 install flask-login
pip3 install flask-openid
pip3 install flask-mail
pip3 install flask-sqlalchemy
pip3 install sqlalchemy-migrate
pip3 install flask-whooshalchemy
pip3 install flask-wtf
pip3 install flask-babel
pip3 install guess_language
pip3 install flipflop
pip3 install coverage
```
4.为应用程序创建基本的文件结构(提示：如果退出了虚拟环境状态，那么需要你 *cd* 到 网站根目录（本例中的 *pyte.vip*）中)：

```
mkdir app
mkdir app/static
mkdir app/templates
mkdir tmp
```
到此，基本的 *falsk* 安装已经结束。