```
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
from datetime import datetime, timedelta 
#爬虫
import urllib.request 
import json
import pandas # 数据
import openpyxl # 实现 pandas 导出 excel
from sqlalchemy import create_engine #连接数据库
#请求头文件信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.59 Safari/537.36','Accept':'application/json, text/javascript, */*; q=0.01','Connection':'close','origin':'https://www.luanzun.com','Referer':'https://www.xinrong.com/invest.shtml','content-type':'text/plain;charset=UTF-8','x-requested-with':'XMLHttpRequest','cookie':'CSESSION:115.159.226.210-w-1502351809-e8219651,NELz_5e33_lastvisit:1502506977,NELz_5e33_saltkey:YOfHZFTo,NELz_5e33_smile:1D1,NELz_5e33_visitedfid:57D65,channel:http%3A%2F%2Fwww.luanzun.com%2F,inviter:xinrong_13034634916'}

url = 'https://www.xinrong.com/v2/project/obtain_available_big_section_list.jso?pageSize={}&pageIndex={}'
# getAmount ，json数据总量
def getAmount(url):
    jsonurl = url.format('1','1')
    res1 = urllib.request.Request(jsonurl)
    req1 = urllib.request.urlopen(res1)
    req1.encoding = 'utf-8'
    html1 = req1.read()
    soup1 = BeautifulSoup(html1,'html.parser').text
    result = json.loads(soup1)['total']
    return result
    
#标的信息，函数
def getInvestInfo(jsonurl):
    total = []
    res = urllib.request.Request(jsonurl)
    req = urllib.request.urlopen(res)
    req.encoding = 'utf-8'
    html = req.read()
    soup = BeautifulSoup(html,'html.parser').text
    rows = json.loads(soup)['rows']
    for row in rows:
        if row.get("rate") in [13.5,13.8]:
            newrowkey = ['id','conDeadline','rate','refundType','loanType','amount','raisedAmount','origiPtime','stime','deadlineStr']
            newrow = dict([(key,row[key]) for key in newrowkey])
            #处理stime，转换格式, timedelta()用来更正为北京时间
            timeStamp = newrow['stime']
            dateArray = datetime.utcfromtimestamp(timeStamp) + timedelta(hours=8)
            newtimeStamp = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            newrow['stime'] = newtimeStamp
            #处理origiPtime，转换格式
            StampOP = newrow['origiPtime']
            dateOP = datetime.utcfromtimestamp(StampOP) + timedelta(hours=8)
            neworigiPtime = dateOP.strftime("%Y-%m-%d %H:%M:%S")
            newrow['origiPtime'] = neworigiPtime
            #添加到
            total.append(newrow)
    return total

amount = getAmount(url)
#根据总标数来判断json地址分页
news_total = []
if amount >20 and amount%20 == 0:
    pageSize = amount//20 +1
    for i in range(1,pageSize):
        jsonurl = url.format('20',i)
        b = getInvestInfo(jsonurl)
        news_total.extend(b)
else:
    pageSize = amount//20 + 2
    for i in range(1,pageSize):
        jsonurl = url.format('20',i)
        b = getInvestInfo(jsonurl)
        news_total.extend(b)
df = pandas.DataFrame(news_total)
a = df.to_excel('xin-series.xlsx')
```