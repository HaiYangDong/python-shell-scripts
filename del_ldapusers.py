#!/usr/bin/env python
# _*_ encoding:utf-8 _*_

import MySQLdb
import os
import sys
import commands

def connect_mysql_gmaster(sql):

    db_info = {'host':'gmaster.dns.com.cn',
               'user':'gmasteruser',
               'passwd':'Usl1UpdobM',
               'db':'GMailDB' }
    try:        
        connect = MySQLdb.connect(**db_info)
        cursor = connect.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print "Can't find any information in GMailDB!!!"
        cursor.close()
        connect.close()
    except Exception as e:
        print e    

def make_ldap_content(domain,user,ID):
    address = user + '@' + domain
    content = '''
dn: cn={address},dc=dns,dc=com,dc=cn
cn: {address}
givenname: {domain}
mail: {address}
objectclass: inetOrgPerson
objectclass: top
sn: {user}
userpassword: H0peUm!ssMe
'''.format(address=address,user=user,domain=domain)
    return content 

def main():
    File = '.user.ldif'
    with open(File,'a+') as f:
        f.truncate()

    domain = sys.argv[1]
    query = 'select ID,EmailBox from EmailBoxDetail where Domain="{0}"'.format(domain)
    try:
        result = connect_mysql_gmaster(query)
        for i in result:
            ID,user = i
            if user == 'postmaster':
                continue
            else:
                ldap_content = make_ldap_content(domain,user,ID)
                with open(File,'a+') as f:
                    f.write(ldap_content)
                email = user + '@' + domain
                cmd = 'ldapdelete -x -D "cn=Manager,dc=dns,dc=com,dc=cn" -w rgdnscomcn "cn={0},dc=dns,dc=com,dc=cn"'.format(email)
                commands.getoutput(cmd)
    except Exception:
        print "can't find information in EmailBoxDetail!"

if __name__ == '__main__':
        main()
