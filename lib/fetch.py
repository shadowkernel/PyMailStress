#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
import time
import ConfigParser
import imaplib
import threading
import email

import account

config = ConfigParser.ConfigParser()
config.read('etc/pms_config.conf')
accounts = account.get()
server_addr = config.get('imap', 'addr')
thread_count = len(accounts)
test_duration = int(config.get('imap', 'test_duration'))
login_interval = int(config.get('imap', 'login_interval'))
verbose=bool(int(config.get('logging','verbose')))

# statistics
login_success = 0
login_failed = 0
fetch_mail = 0
download_size = 0
lock = threading.Lock()

class FetchMail(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.username = accounts[index][0]
        self.password = accounts[index][1]

    def get_mail(self):
        try:
            server = imaplib.IMAP4_SSL(server_addr)
            server.login(self.username, self.password)
            lock.acquire()
            global login_success
            login_success = login_success + 1
            lock.release()
        except imaplib.IMAP4.error:
            print '用户名 %s 密码不匹配，接收邮件进程中止' % self.username
            os.kill(os.getpid(), 1)
        except:
            lock.acquire()
            global login_failed
            login_failed = login_failed + 1
            lock.release()

        server.select()
        typ, data = server.search(None, "UNSEEN")

        for emailid in data[0].split():
            resp, data = server.fetch(emailid, "(RFC822)")
            lock.acquire()
            global fetch_mail, download_size
            fetch_mail = fetch_mail + 1
            download_size = download_size + sys.getsizeof(data)
            lock.release()

        server.close()
        server.logout()

    def run(self):
        start = time.time()
        while True:
            if time.time() - start > test_duration: break
            self.get_mail()
            time.sleep(login_interval)

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
    print '下载邮件容量: %d B' % download_size

if __name__ == '__main__':
    go()
