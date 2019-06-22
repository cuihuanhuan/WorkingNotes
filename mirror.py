# -*- coding: utf-8 -*-


import paramiko
import os.path
import cx_Oracle
from time import sleep
import datetime



src_ip = '192.168.20.1'
tgt_ip = '192.168.19.2'
db_info_sys = 'sqlplus system/12345@orcl'
db_info_src = 'sqlplus huan1/12345'
db_src = 'huan1/12345@192.168.20.1/orcl'
db_tgt = 'huan1/12345@192.168.19.2/orcl'


list_name = []
path = "C:/allcases"
dirs = os.listdir(path)

for file in dirs:
    if file[-7:] == 'src.sql':
        list_name.append(file[:-8])
    else:
        continue

#源端
conn_src = cx_Oracle.connect(db_src)
cursor_src = conn_src.cursor()
#备端
conn_tgt = cx_Oracle.connect(db_tgt)
cursor_tgt = conn_tgt.cursor()

#源端
ssh_src = paramiko.SSHClient()
ssh_src.load_system_host_keys()
ssh_src.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_src.connect(src_ip, 22, 'root', '12345', allow_agent=False, look_for_keys=False, timeout=5)
#备端
ssh_tgt = paramiko.SSHClient()
ssh_tgt.load_system_host_keys()
ssh_tgt.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_tgt.connect(tgt_ip, 22, 'root', '12345', allow_agent=False, look_for_keys=False, timeout=5)

for case_id in list_name:
        try:
            #停止iawork/iatrack,重建同步用户
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --stop 96227F3F-7C50-73BC-D2A7-AECC5D765746')
            print 'cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --stop 96227F3F-7C50-73BC-D2A7-AECC5D765746'
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;killall iawork;killall iatrack')
            print 'cd;source .bash_profile;killall iawork;killall iatrack'
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;' + db_info_sys + '</root/Desktop/i2active/bin/create_user.sql')
            print 'cd;source .bash_profile;' + db_info_sys + '</root/Desktop/i2active/bin/create_user.sql'


            #停止iaback,重建同步用户
            stdin, stdout, stderr = ssh_tgt.exec_command('cd;source .bash_profile;killall iaback')
            print 'cd;source .bash_profile;killall iaback'
            stdin, stdout, stderr = ssh_tgt.exec_command('cd;source .bash_profile;' + db_info_sys + '</root/Desktop/i2active/bin/create_user.sql')
            print 'cd;source .bash_profile;' + db_info_sys + '</root/Desktop/i2active/bin/create_user.sql'


            #源端执行用例
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;' + db_info_src + ' @/allcases/' + case_id + '_src.sql')
            print 'cd;source .bash_profile;' + db_info_src + ' @/allcases/' + case_id + '_src.sql'


            #启动iawork/iatrack
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iawork;/root/Desktop/i2active/bin/iatrack')
            print 'cd;source .bash_profile;/root/Desktop/i2active/bin/iawork;/root/Desktop/i2active/bin/iatrack'


            #启动iaback
            stdin, stdout, stderr = ssh_tgt.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iaback')
            print 'cd;source .bash_profile;/root/Desktop/i2active/bin/iaback'
            sleep(60)

            #重新同步
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --start 96227F3F-7C50-73BC-D2A7-AECC5D765746')
            print 'cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --start 96227F3F-7C50-73BC-D2A7-AECC5D765746'
            sleep(120)

            i = datetime.datetime.now()
            print ("fist time %s" % i)
            filename = 'C:\\allcases\\' + case_id + '_tgt.sql'
            print filename
            fd = open(filename, 'r+')
            next(fd)
            next(fd)
            for line in fd:
                str = line.strip()
                if str == '' or str == '/':
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
            file_src = 'C:\\allcases\\' + case_id + '_src.sql'
            file_tgt = 'C:\\allcases\\' + case_id + '_tgt.sql'
            os.remove(file_src)
            os.remove(file_tgt)
            print('del file ok')

        except cx_Oracle.DatabaseError, msg:
            print (msg)
            print case_id + " error! "
            continue


        except UnicodeDecodeError, msg:
            print (msg)
            print case_id + " error! "
            continue

        except paramiko.ssh_exception.SSHException, msg:
            print (msg)
            print case_id + " error! "
            continue

        except IOError, msg:
            print (msg)
            print case_id + " error! "
            continue