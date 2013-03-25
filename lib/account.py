#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import re

def get():
    """return list of  user information
    """
    result = []
    db = open('etc/userdb.txt', 'r')
    lines = db.read().splitlines()
    db.close()
    for line in lines:
        result.append(re.split('\s+', line, 1))

    return result
