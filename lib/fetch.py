#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
import time
import ConfigParser
import imaplib
import threading
import email
from random import randint

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

server_addr = config.get('imap', 'addr')
thread_count = len(accounts)
test_duration = int(config.get('general', 'test_duration'))
min_interval = int(config.get('imap', 'min_interval'))
max_interval = int(config.get('imap', 'max_interval'))
verbose = int(config.get('general','verbose'))

# statistics
login_success = 0
login_failed = 0
fetch_mail = 0
download_size = 0
lock = threading.Lock()

class FetchMail(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        try:
            self.username = accounts[index][0]
            self.password = accounts[index][1]
        except:
            print '用户信息有误，程序中止'
            os.kill(os.getpid(), 1)
            os.kill(os.getppid(), 1)

    def get_mail(self):
        try:
            session = imaplib.IMAP4_SSL(server_addr)
            session.login(self.username, self.password)
            lock.acquire()
            global login_success
            login_success = login_success + 1
            lock.release()
        except imaplib.IMAP4.error:
            print '用户名 %s 密码不匹配，程序中止' % self.username
            os.kill(os.getpid(), 1)
            os.kill(os.getppid(), 1)
        except:
            lock.acquire()
            global login_failed
            login_failed = login_failed + 1
            lock.release()

        session.select()
        typ, data = session.search(None, "UNSEEN")

        for emailid in data[0].split():
            resp, data = session.fetch(emailid, "(RFC822)")
            lock.acquire()
            global fetch_mail, download_size
            fetch_mail = fetch_mail + 1
            download_size = download_size + sys.getsizeof(data)
            lock.release()

        session.logout()

    def run(self):
        start = time.time()
        while True:
            if time.time() - start > test_duration: break
            self.get_mail()
            time.sleep(randint(min_interval, max_interval))

def go():
    threads = [FetchMail(i) for i in xrange(thread_count)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print '\n----接收邮件统计结果----'
    print '登录成功次数: %d 次' % login_success
    print '登录失败次数: %d 次' % login_failed
    print '下载邮件: %d 封' % fetch_mail
    print '下载邮件容量: %s' % pretty_filesize(download_size)


def pretty_filesize(bytes):
    if bytes >= 1073741824:
        return str(bytes / 1024 / 1024 / 1024) + ' GiB'
    elif bytes >= 1048576:
        return str(bytes / 1024 / 1024) + ' MiB'
    elif bytes >= 1024:
        return str(bytes / 1024) + ' KiB'
    elif bytes < 1024:
        return str(bytes) + ' Bytes'
