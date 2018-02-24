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

#获取文章的标题、来源、时间、内容、作者
def getNewsDetail(url):
    result = {}
    res = urllib.request.urlopen(url)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res, "html.parser") 
    title = soup.select('h1')[0].text
    #result['newssource'] = soup.select('.m_left')[0].contents[0].text.strip('来源：')
    releasetime = soup.select('.m_left')[0].contents[2].text.strip('发布时间：')
    #result['updatetime'] = datetime.strptime(releasetime, '%m月%d日 %H:%M:%S')
    #result['article'] = ' '.join([p.text.strip() for p in soup.select('#article p')[:-1]])
    #result['editor'] = soup.select('.m_left')[0].contents[1].text.strip('作者：')
    return title

a = getNewsDetail('http://yule.52pk.com/yingshi/7053410.shtml')
print(a)