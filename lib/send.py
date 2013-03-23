#!/usr/bin/python
# -*- coding: utf-8 -*-
# Send mail script

import sys, os
import time
import ConfigParser
import smtplib
import threading

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from lib import account

config = ConfigParser.ConfigParser()
config.read('etc/pms_config.conf')
accounts = account.get()
server_addr = config.get('smtp', 'addr')
To = config.get('smtp', 'to')
thread_count = len(accounts)
test_duration = int(config.get('smtp', 'test_duration'))
login_interval=int(config.get('smtp', 'login_interval'))
send_count = int(config.get('smtp', 'send_count'))

msg = MIMEMultipart()
msg['Subject'] = 'TEST'
msg['From'] = "Joe"
msg['To'] = "Whatever"

content = "It's a Long Way to the Top if You Wanna Rock'N'Roll!!!!"
msg.attach(MIMEText(content, 'plain'));
msg = msg.as_string()

# statistics
login_success = 0
login_failed = 0
send_success = 0
send_failed = 0
lock = threading.Lock()

class SendMail(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.username = accounts[index][0]
        self.password = accounts[index][1]

    def send_mail(self):
        try:
            server = smtplib.SMTP(server_addr)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.username, self.password)
            lock.acquire()
            global login_success
            login_success = login_success + 1
            lock.release()
        except smtplib.SMTPAuthenticationError:
            print '用户名 %s 与密码不匹配，发送邮件进程中止' % self.username
            os.kill(os.getpid(), 1)
        except:
            lock.acquire()
            global login_failed
            login_failed = login_failed + 1
            lock.release()

        for x in xrange(send_count):
            try:
                server.sendmail(self.username, To, msg)
                lock.acquire()
                global send_success
                send_success = send_success + 1
                lock.release()
            except:
                lock.acquire()
                global send_failed
                send_failed = send_failed + 1
                lock.release()

        server.close()

    def run(self):
        start = time.time()
        while True:
            if time.time() - start > test_duration: break
            self.send_mail()
            time.sleep(login_interval)

def go():
    threads = [SendMail(i) for i in xrange(thread_count)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print '\n----发送邮件统计结果----'
    print '登陆成功次数: %d 次' % login_success
    print '登陆失败次数: %d 次' % login_failed
    print '发送成功邮件: %d 封' % send_success
    print '发送失败邮件: %d 封' % send_failed
    print '发送邮件容量: %d B' % (send_success * sys.getsizeof(msg))

if __name__ == "__main__":
    go()
