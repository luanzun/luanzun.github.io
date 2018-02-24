#!flask/bin/python3
# -*- conding: utf-8 -*-

#修改系统默认编码为utf-8
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import re #正则
from bs4 import BeautifulSoup #导入html规则库
from datetime import datetime, timedelta # 时间模组
import urllib.request #爬虫
import json

#数据、pandas导出excel、连接数据库
#import pandas
#import openpyxl 
#from sqlalchemy import create_engine

#发送邮件
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#请求头文件信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.85 Safari/537.36','Accept':'application/json, text/javascript, */*; q=0.01','Connection':'close','origin':'https://luejiao.com','Referer':'https://www.wanghuidai.com/invest/index.html','x-requested-with':'XMLHttpRequest','cookie':'UM_distinctid=15fb49e2bb2bd2-0376e01ffd370a-b7a1c3a-1fa400-15fb49e2bb37df; acw_tc=AQAAAIETkE3NEQsAYLUccPm+t5XaH4jT; CNZZDATA1256849928=459281309-1510561291-https%253A%252F%252Fmail.qq.com%252F%7C1515905443; Hm_lvt_e60d4b02f68b26bf0d7d53c323dc70a9=1515656020,1515657692,1515847329,1515907023; Hm_lpvt_e60d4b02f68b26bf0d7d53c323dc70a9=1515907039; JSESSIONID=F15C106291A5803B3F98A8540BCEFE8F'}

url = 'https://www.wanghuidai.com/invest/investJson.html?type=undefined&aprSearch=-1&moneySearch=-1&timeSearch=-1&statusSearch=-1&methods=-1&borrowName=&randomTime=1515914410299'
res = urllib.request.Request(url)
req = urllib.request.urlopen(res)
req.encoding = 'utf-8'
html = req.read()
soup = BeautifulSoup(html,'html.parser').text
rows = json.loads(soup)['data']['list']

total = []
for row in rows:
    if row.get("status") <= 5: # status=1正在投标，status=6正在还款，status=8还款完毕
        newrowkey = ['scales','putStartTime','timeLimit'] # 进度,开始时间，借款周期
        newrow = dict([(key,row[key]) for key in newrowkey])
        #处理putStartTime，转换格式, timedelta()用来更正为北京时间
        timeStamp = newrow['putStartTime']/1000
        dateArray = datetime.utcfromtimestamp(timeStamp) + timedelta(hours=8)
        newtimeStamp = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        newrow['putStartTime'] = newtimeStamp
        total.append(newrow)
#total.sort()
print(total)
#本次采集到的标的数量
targetnum = str(len(total))
#抢标时间
nexttime = str(total[-1]['putStartTime'])
#不同借款周期的标数
num1 = []
num3 = []
num6 = []
num12 = []
for i in total:
    if i['timeLimit'] == 1:
        num1.append(i)
    elif i['timeLimit'] == 3:
        num3.append(i)
    elif i['timeLimit'] == 6:
        num6.append(i)
    else:
        num12.append(i)
# 投标进度
for i in total:
    if i['scales'] < 100:
        tenderscales = str(total[-1]['scales'])
    else:
        tenderscales = None
print(tenderscales)
timenow = datetime.now()
time = timenow.strftime("%Y-%m-%d %H:%M:%S")
# 不同借款周期的年率
puretext = '网汇贷有' + targetnum + '个在投标的\n本次数据抓取时间为：' + time + '\n其中：\n1月标：' + str(len(num1)) + '个\n3月标：' + str(len(num3)) + '个\n6月标：' + str(len(num6)) + '个\n12月标：' + str(len(num12)) + '个'

print(puretext)
