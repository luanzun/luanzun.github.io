python3 中用的是 urllib.request 。

## urllib是一个包,收集几个模块来处理网址:

1. <code>urllib.request</code> 打开和浏览 <code>url</code> 中内容
2. <code>urllib.error</code> 包含从 <code>urllib.request</code> 发生的错误或异常
3. <code>urllib.parse</code> 解析 <code>url</code>
4. <code>urllib.robotparser</code> 解析 <code>robots.txt</code>文件

使用方法有几种：
```
import urllib.request
html = urllib.request.urlopen('url')
```
```
form urllib.request import urlopen
html = urlopen('url')
```

## <code>html.geturl()</code> 会输出请求的url
```
# -*- conding: utf-8 -*-
import urllib.request

html = urllib.request.urlopen('https://www.baidu.com')
print (html.geturl())
```

## <code>html.info()</code> 会输出页面的请求信息
```
# -*- conding: utf-8 -*-
import urllib.request

html = urllib.request.urlopen('https://www.baidu.com')
print (html.info())
```

## <code>sep='\n'</code> 是python函数，用于指定输出内容的分隔符为换行。
```
# -*- conding: utf-8 -*-
import urllib.request

html = urllib.request.urlopen('https://www.baidu.com')
print (html.geturl(),html.info(),sep='\n')
```
## <code>UnicodeEncodeError: 'ascii' codec can't encode characters</code> 错误解决办法
原始码是如下：

```
# -*- conding: utf-8 -*-
import urllib.request

html = urllib.request.urlopen('http://www.luanzun.com')
print (html.read().decode('utf-8'))
```
执行后，提示错误：
```
Traceback (most recent call last):
  File "crawler.py", line 5, in <module>
    print (html.read().decode('UTF-8'))
UnicodeEncodeError: 'ascii' codec can't encode characters in position 284-288: ordinal not in range(128)
```

这是因为<code>python</code>默认使用的是 <code>ascii</code> 编码，而导出的文件却是 utf-8 编码。所以，我们必须要把系统默认的编码改成 <code>utf-8</code> 才行。

将代码改为
```
# -*- conding: utf-8 -*-

#修改系统默认编码为utf-8
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import urllib.request
html = urllib.request.urlopen('http://www.luanzun.com')
print (html.read().decode('utf-8'))
```
同时要注意，代码末尾的 <code>.decode('utf-8')</code> 这里的编码是网页用编码。

## 通过 <code>Request</code> 来请求

```
# -*- conding: utf-8 -*-

#修改系统默认编码为utf-8
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import urllib.request

req = urllib.request.Request('http://www.luanzun.com/')
response = urllib.request.urlopen(req)
the_page = response.read()
print (the_page.decode('utf-8'))
```