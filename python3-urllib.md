python3 中用的是 urllib.request 。

urllib是一个包,收集几个模块来处理网址:

1. urllib.request 打开和浏览 <code>url</code> 中内容
2. urllib.error 包含从 urllib.request 发生的错误或异常
3. urllib.parse 解析 url
4. urllib.robotparser 解析 robots.txt文件

使用方法有几种：
```
import urllib.request
html = urllib.request.urlopen('url')
```
```
form urllib.request import urlopen
html = urlopen('url')
```

html.geturl() 会输出请求的url
```
# -*- conding: utf-8 -*-
import urllib.request

html = urllib.request.urlopen('https://www.baidu.com')
print (html.geturl())
```

html.info() 会输出页面的请求信息
```
# -*- conding: utf-8 -*-
import urllib.request

html = urllib.request.urlopen('https://www.baidu.com')
print (html.info())
```

sep='\n' 是python函数，用于指定输出内容的分隔符为换行。
```
# -*- conding: utf-8 -*-
import urllib.request

html = urllib.request.urlopen('https://www.baidu.com')
print (html.geturl(),html.info(),sep='\n')
```