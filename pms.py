#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import os

import send
import fetch

config = ConfigParser.ConfigParser()
config.read('config')

def runtest():
    print "===邮件系统测试工具==="

    if os.fork() == 0:
        print "发送邮件进程启动"
        send.go()
        print "发送邮件进程结束"
    else:
        print "接收邮件进程启动"
        fetch.go()
        print "接收邮件进程结束"

if __name__ == "__main__":
    runtest()
