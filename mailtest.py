#!/usr/bin/python2
# -*- coding: utf-8 -*-

import ConfigParser
import os

import send
import fetch
# from ldapinfo import LDAPInfo

class MailTest:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('mail.conf')
        self.dry_run = config.getint('test','dry_run') == 1
        self.using_ldap = config.getint('test','using_ldap') == 1
        self.account_num = config.getint('test','account_num')

    def run_test(self):
        print "===邮件系统测试工具==="

        if self.using_ldap :
            print "LDAP方式认证"
            L = LDAPInfo()
           #accounts=L.get_entries(self.account_num)
        else:
            accounts = ['test','test1']

        if os.fork() == 0:
            print "发送邮件进程启动"
            send.go()
            print "发送邮件进程结束"
        else:
            print "接收邮件进程启动"
            fetch.go()
            print "接收邮件进程结束"

if __name__ == "__main__":
    m = MailTest()
    m.run_test()
