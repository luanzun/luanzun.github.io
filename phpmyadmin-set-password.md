phpmyadmin 忘记密码，使用以下代码进行修改：
1.停止mysql服务：
```
/etc/init.d/mysql stop
```
2.跳过验证启动MySQL
```
/usr/local/mysql/bin/mysqld_safe –-skip-grant-tables >/dev/null 2>&1 &
```
第三步，准备重新设置新密码
```
/usr/local/mysql/bin/mysql -u root mysql
```
重置新密码
```
update user set authentication_string = Password('新密码') where User = 'root';
```
更新权限
```
flush privileges;
```
退出
```
exit;
```
4.重新启动MYSQL
```
killall mysqld
/etc/init.d/mysql start
```