#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 这个类用于提供邮件的用户名密码，设计模式：Factory


class MailAccount:
    @staticmethod
    def get_account(method="txt", num):
        # 返回字典字典方式的用户名和密码，返回的数量为最多num个
        # 如果可用的帐号小于num个，则返回可用的帐号数量
        #{"user1":"pass1", "user2","pass2"}
        if (method=="txt"):
            return TxtAccount.get_account(num)
        elif (method=="ldap"):
            return LDAPAccount.get_account(num)
        else:
            # 返回空字典
            return None


class LDAPAccount:
    def get_account(num):
        #从LDAP服务获取用户名和密码

class TxtAccount:
    def get_account(num):
        #从用户制定的文本文件获取用户名和密码


if __name__=="__main__":
    # For testing
    m=MailAccount
    print m.get_account("txt",200)
