# -*- coding: utf-8 -*-
import re
import js2py
import requests
import requests
from lxml import etree
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import time
import random


i = 0
def send_email():
    my_sender='dyzhl15@126.com'    # 发件人邮箱账号
    my_pass = 'zgm01432'           # 发件人邮箱密码（是通过邮箱授权smtp的密码，不是邮箱密码）
    my_user='dyzhl15@126.com'      # 收件人邮箱账号，我这边发送给自己
    def mail():
        ret=True
        try:
            msg=MIMEText('可以报名了抓紧,地址：\nhttp://www.hzjypg.net:8000/studentInit','plain','utf-8')
            msg['From']=formataddr(["Heron",my_sender])  			# 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To']=formataddr(["Heron",my_user])             	# 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject']="普通话报名开始了。。。"                	# 邮件的主题，也可以说是标题
     
            server=smtplib.SMTP("smtp.126.com", 25)  				# 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  						# 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender,[my_user,],msg.as_string())  	# 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  											# 关闭连接
        except Exception:  											
            ret=False
        return ret
     
    ret=mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")    

TARGET_URL = 'http://www.hzjypg.net:8000/queryExamInfo'
def getHtml(url, cookie=None):
    header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8', }
    html = requests.get(url=url, headers=header, timeout=30, cookies=cookie)
    return html.text
def executeJS(js_func_string, arg):
    func = js2py.eval_js(js_func_string)
    return func(arg)
def parseCookie(string):
    string = string.replace("document.cookie='", "")
    clearance = string.split(';')[0]
    return {clearance.split('=')[0]: clearance.split('=')[1]} 


def get_real_data():
    # 第一次访问获取动态加密的JS
    first_html = getHtml(TARGET_URL)
    #print(first_html)
    # 提取其中的JS加密函数
    js_func = ''.join(re.findall(r'(function .*?)</script>', first_html))
    #print('get js func:\n', js_func)
    # 提取其中执行JS函数的参数
    js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html))
    #print('get ja arg:\n', js_arg)
    # 修改JS函数，使其返回Cookie内容 
    js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')
    # 执行JS获取Cookie 
    cookie_str = executeJS(js_func, js_arg)
    # 将Cookie转换为字典格式
    cookie = parseCookie(cookie_str) # 
    #print(cookie) 
    # 带上Cookie再次访问url,获取正确数据
    return getHtml(TARGET_URL, cookie)

def send_alert():
    sel = etree.HTML(get_real_data())
    exam_num = len(sel.xpath('//table[@class="pth_smrtable"]/tr'))
    if exam_num != 1:
        send_email()
        print("Start...")
    else:
        global i
        i += 1
        print('the %s times' % str(i))

if __name__ == '__main__':
    while True:
        send_alert()
        time.sleep(3600)