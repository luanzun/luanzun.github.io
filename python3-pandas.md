安装代码
```
pip3 install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
```
如果是在 <code>flask</code> 虚拟环境里的项目使用，最好在虚拟环境里安装
```
flask/bin/pip3 install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
```



pandas坑之to_sql

pandas是将格式化数据直接编成 python 可读的 DataFrame 格式（本质就是字典，并且自动设置了index和colunms）。《利用python进行数据分析》书中提到一个函数<code>to_sql</code>。

使用 <code>to_sql</code> 这个函数有一个问题，虽然 <code>to_sql</code>函数可以直接将字典数据直接存入数据库，但，<code>to_sql</code> 限制非常大。
小白可能会用到的代码：
```
import pandas
import pymysql

df = pandas.DataFrame(list)
a = pymysql.connect(host,port,user,password,charset,db)
df.to_sql(tablename,con = a)
```
网上很多地方说的都是这种做法，但实际根本没法运行。


根据库的文档，我们看到to_sql函数支持两类MySQL引擎一个是sqlalchemy，另一个是sqlliet3.没错，在你写入库的时候，pymysql是不能用的！！！mysqldb也是不能用的，你只能使用sqlalchemy或者sqlliet3！！鉴于sqllift3已经很久没有更新了，笔者这里建议使用sqlalchemy！！

所以上面那段要改写成下面这样：
```
import pandas as pd
from sqlalchemy import create_engine
conn = create_engine('mysql+mysqldb://root:password@localhost:3306/databasename?charset=utf8')  
```
下面一步很关键，注意！！！to_sql函数并不在pd之中，而是在io.sql之中，是sql脚本下的一个类！！！所以to_sql的最好写法就是：
```
pd.io.sql.to_sql(df1,tablename,con=conn,if_exists='repalce')
```
是不是感觉大功告成了？？？

那是你的错觉，赶紧回到数据库看看吧！！你会发现WTF为什么我原来的数据都没有了！！

这就是to_sql的第二个坑if_exists字段：

很多新人按照网上的教程，都将if_exists字段定义为‘replace’活着‘fail’，要么发现原来数据没有了，要么发现什么时候都没有做！

* fail的意思如果表存在，什么也不做。
* replace的意思，如果表存在，删了表，再建立一个新表，把数据插入.
* append的意思，如果表存在，把数据插入，如果表不存在创建一个表！！
