#!flask/bin/python3
# -*- conding: utf-8 -*-

#修改系统默认编码为utf-8
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

#正则
import re 
#导入html规则库
from bs4 import BeautifulSoup 
# 时间模组
from datetime import datetime 
#爬虫
import urllib.request 
# 数据整理
import pandas 
import openpyxl
#链接mysql
import pymysql 
from sqlalchemy import create_engine

#请求头文件信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.39 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Connection':'close',
'Referer':'http://www.luanzun.com/'
}

#获取文章的标题、来源、时间、内容、作者
def getNewsDetail(url):
    result = {}
    res = urllib.request.urlopen(url)
    res.encoding = 'gb18030'
    soup = BeautifulSoup(res, "html.parser") 
    result['title'] = soup.select('h1')[0].text
    result['newssource'] = soup.select('.m_left')[0].contents[0].text.strip('来源：')
    #timesource = soup.select('.m_left')[0].contents[2].text.strip('发布时间：')
    #result['dt'] = datetime.strptime(timesource, '%m月%d日 %H:%M:%S')
    result['article'] = ' '.join([p.text.strip() for p in soup.select('#article p')[:-1]])
    result['editor'] = soup.select('.m_left')[0].contents[1].text.strip('作者：')
    return result

#爬取列表页，获取文章url
def parseListLinks(url):
    newsdetails = []
    res = urllib.request.urlopen(url)
    res.encoding = 'gb18030'
    soup = BeautifulSoup(res, "html.parser") 
    for newsurls in soup.select('.artlist h3 a'):
        newsdetails.append(getNewsDetail(newsurls['href']))
    return newsdetails

# 获取多分页中的文章链接
url = 'http://yule.52pk.com/mingxing/list_{}.shtml'
news_total = []
for i in range(1,4):
    newsurl = url.format(i)
    newsary = parseListLinks(newsurl)
    news_total.extend(newsary)

#把数据保存到 Padnas 中
df = pandas.DataFrame(news_total)
# 把数据导出到 excel 表格中，本意为检测数据。
a = df.to_excel('news.xlsx')
# 打开数据库连接
conn = create_engine('mysql+pymysql://root:password@localhost:port/testuser?charset=utf8')
 #通过执行 sql 命令，保存数据, addend 为如果表存在则添加数据
pandas.io.sql.to_sql(df,'post', con = conn,if_exists = 'append',index = False,index_label = False)
#关闭数据库连接，代码无效
#conn.close()   
