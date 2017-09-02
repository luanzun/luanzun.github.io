```
# 发送邮件
sender = 'luanzun@luanzun.com'
receivers = ['baba@qq.com']
message = MIMEMultipart()
#message = MIMEText('Python 邮件发送测试！', 'plain', 'utf-8')
message['from'] = Header("爸爸", 'utf-8')
message['To'] = Header("朋友你好", 'utf-8')
subject = '信融投资标的内容'
message['Subject'] = Header(subject, 'utf-8')
#邮件正文
message.attach(MIMEText('这事爸爸做的标的邮件', 'plain', 'utf-8'))
#构造附件
att1 = MIMEText(open('xin-series.xlsx', 'rb').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="xin.xlsx'
message.attach(att1)
try:
    smtpObj = smtplib.SMTP_SSL()
    smtpObj.connect("smtp.exmail.qq.com",465)
    smtpObj.login("luanzun@luanzun.com","密码")
    smtpObj.sendmail(sender, receivers ,message.as_string())
    print("发送邮件成功")
except smtplib.SMTPException:
    print("Error:无法发送邮件")
```
另外一种方法：
```
#发邮件
class Mailer(object):
    def __init__(self,maillist,mailtitle,mailcontent):
        self.mail_list = maillist
        self.mail_title = mailtitle
        self.mail_content = mailcontent
 
        self.mail_host = "smtp.exmail.qq.com"
        self.mail_user = "爸爸"
        self.mail_pass = "xiao"
 
    def sendMail(self):
        me = self.mail_user + "<luanzun@luanzun.com>"
        msg = MIMEMultipart()
        msg['Subject'] = nexttime + '信融投资标的'
        msg['From'] = me
        msg['To'] = "".join(self.mail_list)
 
        #puretext = MIMEText('<h1>你好，<br/>'+self.mail_content+'</h1>','html','utf-8')
        puretext = MIMEText('本次抓取的数据中包含未结束的标的以及下次时间开放的标的' + self.mail_content,'plain', 'utf-8')
        msg.attach(puretext)
 
        # 首先是xlsx类型的附件
        # xlsxpart = MIMEApplication(open('xin-series.xlsx', 'rb').read(), 'utf-8')
        # xlsxpart.add_header('Content-Disposition', 'attachment', filename='xin-series.xlsx')
        # msg.attach(xlsxpart)
 
        try:
            s = smtplib.SMTP_SSL() #创建邮件服务器对象
            s.connect(self.mail_host,465) #连接到指定的smtp服务器。参数分别表示smpt主机和端口
            s.login("luanzun@luanzun.com", self.mail_pass) #登录到你邮箱
            s.sendmail(me, self.mail_list, msg.as_string()) #发送内容
            s.close()
            print("发送成功")
            return True
        except smtplib.SMTPException:
            print("Error:无法发送邮件")
            return False
 
if __name__ == '__main__':
    #send list
    mailto_list = ["316741501@qq.com]
    mail_title = '信融投资标的'
    mail_content = '\n谢谢'
    mm = Mailer(mailto_list,mail_title,mail_content)
    res = mm.sendMail()
    print(res)
```