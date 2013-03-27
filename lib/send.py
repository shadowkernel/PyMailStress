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
if config.read('etc/pms_config.conf') == []:
    print '配置文件读取失败，程序中止'
    os.kill(os.getpid(), 1)
    os.kill(os.getppid(), 1)

accounts = account.get()
if accounts == []:
    print '用户信息读取失败，程序中止'
    os.kill(os.getpid(), 1)
    os.kill(os.getppid(), 1)

server_addr = config.get('smtp', 'addr')
tsl_mode = int(config.get('smtp', 'tsl_mode'))
thread_count = len(accounts)
test_duration = int(config.get('general', 'test_duration'))
min_interval = int(config.get('smtp', 'min_interval'))
max_interval = int(config.get('smtp', 'max_interval'))
verbose = int(config.get('general','verbose'))
send_count = int(config.get('smtp', 'send_count'))

msg = MIMEMultipart()
msg['Subject'] = 'TEST'
msg['From'] = "Joe"
msg['To'] = "Whatever"

content_files = config.get('smtp', 'content').split()
content = ''
if content_files == []:
    content = "It's a Long Way to the Top if You Wanna Rock'N'Roll!!!!"
else:
    for file in content_files:
        try:
            fp = open(file, 'r')
        except:
            print '文件 %s 打开失败，程序中止' % file
            os.kill(os.getpid(), 1)
            os.kill(os.getppid(), 1)
        content = content + fp.read()
        fp.close()

msg.attach(MIMEText(content+'\n\n', 'plain', 'utf-8'))

attach_files = config.get('smtp', 'attachment').split()
if attach_files != []:
    for file in attach_files:
        try:
            fp = open(file, 'r')
        except:
            print '文件 %s 打开失败，程序中止' % file
            os.kill(os.getpid(), 1)
            os.kill(os.getppid(), 1)
        msg.attach(MIMEApplication(fp.read()))
        fp.close()

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
            session = smtplib.SMTP(server_addr, port=25)
            session.ehlo()
            if tsl_mode:
                session.starttls()
                session.ehlo()
            session.login(self.username, self.password)
            lock.acquire()
            global login_success
            login_success = login_success + 1
            lock.release()
        except smtplib.SMTPAuthenticationError:
            print '用户名 %s 与密码不匹配，程序中止' % self.username
            os.kill(os.getpid(), 1)
            os.kill(os.getppid(), 1)
        except:
            lock.acquire()
            global login_failed
            login_failed = login_failed + 1
            lock.release()

        for x in xrange(send_count):
            try:
                session.sendmail(self.username, choice(accounts)[0], msg)
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

        session.quit()

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
    print '发送邮件容量: %s' % pretty_filesize(send_success * sys.getsizeof(msg))

def pretty_filesize(bytes):
    if bytes >= 1073741824:
        return str(bytes / 1024 / 1024 / 1024) + ' GiB'
    elif bytes >= 1048576:
        return str(bytes / 1024 / 1024) + ' MiB'
    elif bytes >= 1024:
        return str(bytes / 1024) + ' KiB'
    elif bytes < 1024:
        return str(bytes) + ' Bytes'
