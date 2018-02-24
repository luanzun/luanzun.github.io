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

timenow = datetime.now()
time = timenow.strftime("%Y-%m-%d %H:%M:%S")
#标的信息，函数
def getInvestInfo(jsonurl):
    total = []
    res = urllib.request.Request(jsonurl)
    req = urllib.request.urlopen(res)
    req.encoding = 'utf-8'
    html = req.read()
    soup = BeautifulSoup(html,'html.parser').text
    rows = json.loads(soup)['rows']
    print(rows)
    for row in rows:
        if row.get("rate") >= 13:
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
            #添加到list中
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
#df = pandas.DataFrame(news_total)
#a = df.to_excel('xin-series.xlsx')

#本次数据的投标时间
nexttime = str(news_total[-1]['stime'])
#本次数据的标的数量
targetnum = str(len(news_total))
#不同年率的标数
numA = []
numB = []
numC = []
for i in news_total:
    if i['rate'] == 13.2:
        numA.append(i)
    elif i['rate'] == 13.5:
        numB.append(i)
    else:
        numC.append(i)

puretext = '本次抓取的数据中包含未结束的标的以及下次时间开放的标的。\n下次投标开放时间为：' + nexttime +'\n本次数据采集时间为：'+ time + '\n本次抓取的数据中，标的共有' + targetnum + '个。其中：\n年率 13.2% ：' + str(len(numA)) + '个\n年率 13.5% ：' + str(len(numB)) + '个\n年率 13.8% ：' + str(len(numC)) + '个'

# #发邮件
# class Mailer(object):
#     def __init__(self,maillist,mailtitle,mailcontent):
#         self.mail_list = maillist
#         self.mail_title = mailtitle
#         self.mail_content = mailcontent
 
#         self.mail_host = "smtp.exmail.qq.com"
#         self.mail_user = "爸爸"
#         self.mail_pass = "xiaobao521.Z"
 
#     def sendMail(self):
#         me = self.mail_user + "<luanzun@luanzun.com>"
#         msg = MIMEMultipart()
#         msg['Subject'] = nexttime + '信融投资标的'
#         msg['From'] = me
#         msg['To'] = "".join(self.mail_list)
 
#         #puretext = MIMEText('<h1>你好，<br/>'+self.mail_content+'</h1>','html','utf-8')
#         puretext = MIMEText('本次抓取的数据中包含未结束的标的以及下次时间开放的标的。\n下次投标开放时间为：' + nexttime +'\n本次数据采集时间为：'+ time + '\n本次抓取的数据中，标的共有' + targetnum + '个。其中：\n年率 13.2% ：' + str(len(numA)) + '个\n年率 13.5% ：' + str(len(numB)) + '个\n年率 13.8% ：' + str(len(numC)) + '个' + self.mail_content,'plain', 'utf-8')
#         msg.attach(puretext)
 
#         # 首先是xlsx类型的附件
#         # xlsxpart = MIMEApplication(open('xin-series.xlsx', 'rb').read(), 'utf-8')
#         # xlsxpart.add_header('Content-Disposition', 'attachment', filename='xin-series.xlsx')
#         # msg.attach(xlsxpart)
 
#         try:
#             s = smtplib.SMTP_SSL() #创建邮件服务器对象
#             s.connect(self.mail_host,465) #连接到指定的smtp服务器。参数分别表示smpt主机和端口
#             s.login("luanzun@luanzun.com", self.mail_pass) #登录到你邮箱
#             s.sendmail(me, self.mail_list, msg.as_string()) #发送内容
#             s.close()
#             print("发送成功")
#             return True
#         except smtplib.SMTPException:
#             print("Error:无法发送邮件")
#             return False
 
# if __name__ == '__main__':
#     #send list
#     mailto_list = ["316741501@qq.com"]
#     mail_title = '信融投资标的'
#     mail_content = '\n谢谢'
#     mm = Mailer(mailto_list,mail_title,mail_content)
#     res = mm.sendMail()
#     print(res)