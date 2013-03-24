#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
import os

from lib import send, fetch

def runtest():
    print "===邮件系统测试工具==="

    if os.fork() == 0:
        print "发送邮件进程启动"
        send.go()
        print "发送邮件进程结束\n"
    else:
        print "接收邮件进程启动"
        fetch.go()
        print "接收邮件进程结束\n"

if __name__ == "__main__":
    runtest()
