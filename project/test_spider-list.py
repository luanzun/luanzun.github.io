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
import pandas # 数据
import openpyxl # 实现 pandas 导出 excel
from sqlalchemy import create_engine # pandas通过 sqlalchemy 连接mysql
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
    #timesource = '2017年' + soup.select('.m_left')[0].contents[2].text.strip('发布时间：')
    #result['dt'] = datetime.strptime(timesource, '%Y年%m月%d日 %H:%M:%S')
    art = soup.select('#article p')[:-1]
    result['article'] = re.sub(r'</?a[^>]*>','',str(art))
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
for i in range(1,2):
    newsurl = url.format(i)
    newsary = parseListLinks(newsurl)
    news_total.extend(newsary)


#把数据保存到 Padnas 中
df = pandas.DataFrame(news_total)
#a = df.to_excel('news.xlsx')

# 打开数据库连接，pandas 无法通过 pymysql 连接数据库库 
#s = pymysql.connect(host='127.0.0.1', port=3306, user='testuser', passwd='luanzun521', db='testuser')

#create_engine("数据库类型+数据库驱动://数据库用户名:数据库密码@IP地址:端口/数据库"，其他参数)
conn = create_engine('mysql+pymysql://testuser:testuser521@localhost:3306/test?charset=utf8',echo=True)
 #通过执行 sql 命令，保存数据
pandas.io.sql.to_sql(df,'post', con = conn,if_exists = 'append',index = False,index_label = False)
#关闭数据库连接
#conn.close()   
