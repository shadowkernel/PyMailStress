#!/usr/bin/python2

import ldap
import ConfigParser

class LDAPInfo:
    def __init__(self):
        config=ConfigParser.ConfigParser()
        config.read('mail.conf')
        self.ldap_addr=config.get('server','ldap_addr')
        #self.ldap_admin=config.get('server','ldap_admin')
        #self.ldap_admin_password=config.get('server','ldap_admin_password')
        self.ldap_suffix=config.get('server','ldap_suffix')
        l=ldap.open(self.ldap_addr)
        #l.simple_bind(self.ldap_admin,self.admin_password)
        
    def get_entries(self,num=100):
        searchScope = ldap.SCOPE_SUBTREE
        retrieveAttributes = None 
        searchFilter = "cn=*"

        ldap_result_id = l.search(self.ldap_suffix, 
                searchScope, searchFilter, retrieveAttributes)
        result_set = []
        i=0
        while i<num:
            i=i+1
            result_type, result_data = l.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                ## here you don't have to append to a list
                ## you could do whatever you want with the individual entry
                ## The appending to list is just for illustration. 
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
        print result_set

if __name__=='__main__':
    m=LDAPInfo()
    print m.get_entries(10)
