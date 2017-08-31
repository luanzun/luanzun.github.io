```
#!flask/bin/python3
# -*- conding: utf-8 -*-

#修改系统默认编码为utf-8
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import re #正则
from bs4 import BeautifulSoup #导入html规则库
from datetime import datetime # 时间模组
import urllib.request #爬虫

#请求头文件信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.39 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Connection':'close',
'Referer':'http://www.luanzun.com/'
}

url = 'http://yule.52pk.com/shipin/7050650.shtml'
req = urllib.request.urlopen(url)
#response = urllib.request.urlopen(req)
html = req.read() #抓取页面内容
html = html.decode('gbk') #对页面进行解析

# 使用正则形式获取标题
# titles = re.search(r'(?<=<h1>)(.*)(?=</h1>)',html)
# title = titles.group(0)

# 使用 BeautifulSoup 来获取标题
soup = BeautifulSoup(html, "html.parser") 
title = soup.select('h1')[0].text

#获取 来源
# souces = re.search(r'(?<=来源：)(.*)(?=</span><span>作者)',html)
# souce = souces.group(0)
# BS 提取 来源
souce = soup.select('.m_left')[0].contents[0].text.strip('来源：')

# 提取 作者
# authors = re.search(r'(?<=作者：)(.*)(?=</span><span>发布)',html)
# author = authors.group(0)
#BS 提取 作者
author = soup.select('.m_left')[0].contents[1].text.strip('作者：')

#提取 发布时间
# releasetimes = re.search(r'(?<=发布时间：)(.*)(?=</span>)',html)
# releasetime = releasetimes.group(0)

releasetime = soup.select('.m_left')[0].contents[2].text.strip('发布时间：')
#字符串 转换成 时间格式
dt = datetime.strptime(releasetime, '%m月%d日 %H:%M:%S')


#提取 正文
#article = soup.select('#article p')[:-1] #[-1]为不提取最后一个元素

#' '.join([p.text.strop() for p in soup.select('#article p')])  #一行代码是下面四行代码的简写
article = []
for p in soup.select('#article p')[:-1]:
    article.append(p.text.strip()) 
' '.join(article) #合并元素内容
print(article)
```

## 列表页

列表页抓取文章列表
```
url = 'http://yule.52pk.com/t_236_1.shtml'
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)
html = response.read() #抓取页面内容
html = html.decode('gbk') #对页面进行解析

soup = BeautifulSoup(html, "html.parser") 
for newslist in soup.select('.artlist h3 a'):
    newsurl = newslist['href']
    print(newsurl)
```

爬取列表页，获取文章url
```
def newsurllinks(url):
    newsdetails = []
    res = urllib.request.urlopen(url)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res, "html.parser") 
    for newsurls in soup.select('.artlist h3 a'):
        newsdetails.append(getNewsDetail(newsurls['href']))
    return newsdetails
```

```
# 生成分页链接
url = 'http://yule.52pk.com/t_236_{}.shtml'
for i in range(1,10):
    print(url.format(i))
```