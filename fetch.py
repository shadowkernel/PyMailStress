#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time

import threading
import ConfigParser

import imaplib
import email

config = ConfigParser.ConfigParser()
config.read('config')

server_addr = config.get('server', 'imap')

username = config.get('account', 'username')
password = config.get('account', 'password')

thread_count = int(config.get('fetch_model', 'thread_count'))
login_times = int(config.get('fetch_model', 'login_times'))
login_interval = int(config.get('fetch_model', 'login_interval'))

class FetchMail(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def get_mail(self):
        server = imaplib.IMAP4_SSL(server_addr, 993)

        try:
            server.login(username, password)
        except:
            print "[AUTHENTICATION_ERROR]: Invalid credentials (Failure)"
            sys.exit(1)

        server.select()
        resp, items = server.search(None, "UNSEEN")
        items = items[0].split()

        for emailid in items:
            try:
                resp, data = server.fetch(emailid, "(RFC822)")
            except:
                pass

            email_body = data[0][1]
            mail = email.message_from_string(email_body)
            # logging

        try:
            server.close()
        except:
            pass

        server.logout()

    def run(self):
        for x in xrange(login_times):
            # logging
            self.get_mail()
            time.sleep(login_interval)

def go():
    threads = [FetchMail() for i in xrange(thread_count)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    go()
