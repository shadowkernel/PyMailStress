#!/usr/bin/python
# -*- coding: utf-8 -*-
# Send mail script
# Author: Xiaoyang Li <hsiaoyonglee@gmail.com>

import smtplib
import time
import threading
import ConfigParser

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

config = ConfigParser.ConfigParser()
config.read('config')

server_addr = config.get('server', 'smtp')
port = 587

username = config.get('account', 'username')
password = config.get('account', 'password')

To = config.get('account', 'to')
From = username

thread_count = int(config.get('send_model', 'thread_count'))
send_count = int(config.get('send_model', 'send_count'))
login_times = int(config.get('send_model', 'login_times'))
login_interval=int(config.get('send_model', 'login_interval'))

fp = open('att.png', 'rb')
img = MIMEImage(fp.read())
fp.close()

msg = MIMEMultipart()
msg['Subject'] = 'TEST'
msg['From'] = "Joe Jeong"
msg['To'] = "Whatever"

content = "It's a Long Way to the Top if You Wanna Rock'N'Roll!!!!"
msg.attach(MIMEText(content,'plain'));
msg.attach(img)

class SendMail(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def send_mail(self, usingTLS=True):
        if usingTLS == True :
            server = smtplib.SMTP(server_addr, port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            for x in xrange(send_count):
                try:
                    server.sendmail(From, To, msg.as_string())
                except:
                    pass
            server.close()

    def run(self):
        for i in range(login_times):
            # logging
            self.send_mail()
            time.sleep(login_interval)

def go():
    threads = [SendMail() for i in xrange(thread_count)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    go()
