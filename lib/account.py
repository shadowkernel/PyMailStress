#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re

def get():
    """return list of  user information
    """
    result = []
    try:
        db = open('etc/userdb.txt', 'r')
    except:
        print '文件 %s 打开失败，程序中止' % file
        os.kill(os.getpid(), 1)
        os.kill(os.getppid(), 1)
    lines = db.read().splitlines()
    db.close()
    for line in lines:
        result.append(re.split('\s+', line, 1))

    return result
