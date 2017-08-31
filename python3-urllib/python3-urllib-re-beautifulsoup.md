```
# -*- conding: utf-8 -*-

#修改系统默认编码为utf-8
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


import re #正则
from bs4 import BeautifulSoup #导入html规则库
import urllib.request #爬虫

#请求头文件信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.39 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Connection':'close',
'Referer':'http://www.luanzun.com/'
}

url = 'http://yule.52pk.com/t_236_1.shtml'
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)
html = response.read() #抓取页面内容
html = html.decode('gbk') #对页面进行解析
# title = re.findall(r'title="(.*?)"',html)
# print (title)

#postlist = re.findall(r'<ul class="artlist">(.*?)</ul>',html)  #此行代码错误


#打印纯文字
# soup = BeautifulSoup(html, "html.parser") 
# print (soup.text)



#打印出 class=artlist 的区块内容
# soup = BeautifulSoup(html, "html.parser") 
# for link in soup.select('.artlist'):
#     print(link)

soup = BeautifulSoup(html, "html.parser") 
for newslist in soup.select('.artlist'):
    for news in newslist.select('h3'):  #.artilst 内容只有条，在python list中只是一个元素，所以需要对内容再次进行转化成一个list，这次是以<code>h3</code>为依据
        h3 = news.text #刨除html元素，只保留字符串
        for newshref in news.select('a'):   # <code>news</code>中包含了<code>h3</code>标签，需要导出<code>a</code>标签
            a = newshref['href']
            print(h3,a)
```
如果<code>h3</code>内容有空，只需要用<code>if</code>进行判断大于 0 即可。
[0] 适用于 list 中只有一个元素，用来打印 <code>list</code>中的第一个元素，效果是去除 打印<code>list</code>元素时显示的中括号。如果 <code>list</code>中元素多余1个，就需要用 for 来循环打印出出来，如上面的样例代码。
```
    #print (news.select('h3')[0])
    # if len(news.select('h3'))> 0:
    #     h3 = news.select('h3')[0].text
    #     print(h3)
```


过滤 <code>a</code> 标签
下面代码意思是将 <code>str</code> 中的 <code>a</code> 替换为无。
```
a = re.sub(r'</?a[^>]*>','',str)
```
同理，过滤 <code>p</code> 标签则是
```
a = re.sub(r'</?p[^>]*>','',str)
```
过滤所有的 html 标签
```
r'</?\w+[^>]*>'
```