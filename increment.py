# -*- coding: utf-8 -*-
# This program is used to test increment backup.


import paramiko
import os.path
import cx_Oracle
from time import sleep
import datetime

os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
source_ip = '192.168.17.17'


db_info_src = 'sqlplus huan1/abcde@192.168.17.17/orcl'
db_src = 'huan1/abcde@192.168.17.17/orcl'
db_tgt = 'huan1/abcde@192.168.17.18/orcl'



# loop to get case_id
list_name = []
path = "C:\\allcases"
dirs = os.listdir(path)
for file in dirs:
    if file[-7:] == 'src.sql':
        list_name.append(file[:-8])
    else:
        continue
    #     print list_name
#print list_name
#源端
conn_src = cx_Oracle.connect(db_src)
cursor_src = conn_src.cursor()
#备端
conn_tgt = cx_Oracle.connect(db_tgt)
cursor_tgt = conn_tgt.cursor()
for case_id in list_name:

        try:
            # preparation
            ##source for linux:do case
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(source_ip, 22, 'root', '12345', timeout=5)
            stdin, stdout, stderr = ssh.exec_command( 'cd;source .bash_profile;' + db_info_src + ' @/allcases/' + case_id + '_src.sql')
            ssh.close()
            print('cd;source .bash_profile;' + db_info_src + ' @/allcases/' + case_id + '_src.sql')
            i = datetime.datetime.now()
            print ("fist time %s" % i)
            sleep(60)

            filename='C:\\allcases\\' + case_id +  '_tgt.sql'
            #print filename
            fd= open(filename,'r+')
            next(fd)
            next(fd)
            for line in fd:
                str = line.strip()
                if str == '' or str=='/':
                    continue
                sql = line.strip()
                print (sql)
                cursor_src.execute(sql)
                src_ret = cursor_src.fetchall()
                print(src_ret)
                cursor_tgt.execute(sql)
                tgt_ret = cursor_tgt.fetchall()
                print(tgt_ret)
                if src_ret == tgt_ret:
                    print 'pass'
                else:
                    print 'fail'
            fd.close()
            #ssh和连接数据库是异步的
            file_src = 'C:\\allcases\\' + case_id + '_src.sql'
            file_tgt = 'C:\\allcases\\' + case_id + '_tgt.sql'
            os.remove(file_src)
            os.remove(file_tgt)
            print('del file ok')

        except cx_Oracle.DatabaseError, msg:
            print (msg)
            print case_id + " error! "
            continue

cursor_src.close()
conn_src.close()
cursor_tgt.close()
conn_tgt.close()