#!/usr/bin/python
# -*- coding: utf-8 -*-
# Send mail script

import sys, os
import time
import ConfigParser
import smtplib
import threading
from random import choice, randint

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from lib import account

config = ConfigParser.ConfigParser()
config.read('etc/pms_config.conf')
# check
accounts = account.get()
# check
server_addr = config.get('smtp', 'addr')
# check
thread_count = len(accounts)
test_duration = int(config.get('general', 'test_duration'))
# check
min_interval = int(config.get('general', 'min_interval'))
# check
max_interval = int(config.get('general', 'max_interval'))
# check
verbose = int(config.get('general','verbose'))
send_count = int(config.get('smtp', 'send_count'))
# check

msg = MIMEMultipart()
msg['Subject'] = 'TEST'
msg['From'] = "Joe"
msg['To'] = "Whatever"

# rewrite
content_file = config.get('smtp', 'content')
if content_file == '':
    content = "It's a Long Way to the Top if You Wanna Rock'N'Roll!!!!"
else:
    fp = open(content_file, 'r')
    # check
    content = fp.read()
    fp.close()

msg.attach(MIMEText(content, 'plain'))

attach_file = config.get('smtp', 'attachment')
if attach_file != '':
    fp = open(attach_file, 'rb')
    attachment = MIMEApplication(fp.read())
    fp.close()
    msg.attach(attachment)

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
                server.sendmail(self.username, choice(accounts)[0], msg)
                lock.acquire()
                global send_success
                send_success = send_success + 1
                lock.release()
            except Exception as e:
                lock.acquire()
                if verbose:
                    print "发送邮件失败：", e
                global send_failed
                send_failed = send_failed + 1
                lock.release()

        server.close()

    def run(self):
        start = time.time()
        while True:
            if time.time() - start > test_duration: break
            self.send_mail()
            time.sleep(randint(min_interval, max_interval))

def go():
    threads = [SendMail(i) for i in xrange(thread_count)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print '\n----发送邮件统计结果----'
    print '登录成功次数: %d 次' % login_success
    print '登录失败次数: %d 次' % login_failed
    print '发送成功邮件: %d 封' % send_success
    print '发送失败邮件: %d 封' % send_failed
    print '发送邮件容量: %d B' % (send_success * sys.getsizeof(msg))

if __name__ == "__main__":
    go()
