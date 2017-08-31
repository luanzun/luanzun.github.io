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
import urllib.parse
import http.cookiejar #cookie
import json
import pandas # 数据
import openpyxl # 实现 pandas 导出 excel
from sqlalchemy import create_engine
#请求头文件信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.59 Safari/537.36',
'Accept':'application/json, text/javascript, */*; q=0.01',
'Connection':'close',
'origin':'https://www.luanzun.com',
'Referer':'https://www.xinrong.com/invest.shtml',
'content-type':'text/plain;charset=UTF-8',
'x-requested-with':'XMLHttpRequest',
'cookie':'CSESSION:115.159.226.210-w-1502351809-e8219651,NELz_5e33_lastvisit:1502506977,NELz_5e33_saltkey:YOfHZFTo,NELz_5e33_smile:1D1,NELz_5e33_visitedfid:57D65,channel:http%3A%2F%2Fwww.luanzun.com%2F,inviter:xinrong_13034634916'}

# #设置 data，意为访问 url 时需要的参数
# #两行代码简写为 data = urllib.parse.urlencode({'pageSize':'5','pageIndex':'1'}).encode('utf-8)
# data = urllib.parse.urlencode({'pageSize':'5','pageIndex':'6'})
# data = data.encode('utf-8')
# url = 'https://www.xinrong.com/v2/project/obtain_available_big_section_list.jso'
# res = urllib.request.Request(url,data)
# response = urllib.request.urlopen(res)
# html = response.read()
# response.encoding = 'utf-8'
# soup = BeautifulSoup(html, 'html.parser').text

# row = json.loads(soup)['rows']
# # for row in json.loads(soup)['rows']:
# #     result = {}
# #     result['id'] = row['id']
# #     result['deadlineStr'] = row['deadlineStr']

# news_total = []
# news_total.extend(row)
# df = pandas.DataFrame(news_total)
# a = df.to_excel('news.xlsx')
# #print(df)


jsonurl = 'https://www.xinrong.com/v2/project/obtain_available_big_section_list.jso'
#标的信息，函数
def getInvestInfo(jsonurl):
    news_total = []
    data = urllib.parse.urlencode({'pageSize':'10','pageIndex':'1'})
    data = data.encode('utf-8')
    res = urllib.request.Request(jsonurl,data)
    req = urllib.request.urlopen(res)
    req.encoding = 'utf-8'
    html = req.read()
    soup = BeautifulSoup(html,'html.parser').text
    rows = json.loads(soup)['rows']
    for row in rows:
        newrowkey = ['id','conDeadline','rate','refundType','loanType','amount','raisedAmount','origiPtime','stime','deadlineStr']
        newrow = dict([(key,row[key]) for key in newrowkey])
        news_total.append(newrow)
    return news_total
b = getInvestInfo(jsonurl)
df = pandas.DataFrame(b)
a = df.to_excel('news.xlsx')
print(df)
```