# -*- coding: utf-8 -*-


import paramiko
import os.path
import cx_Oracle
from time import sleep
import time
import shutil


src_ip = '192.168.80.3'
tgt_ip = '192.168.80.4'

db_info_src = 'sqlplus huan1/12345@orclpdb'
db_src = 'huan1/12345@192.168.80.3/orclpdb'
db_tgt = 'huan1/12345@192.168.80.4/orclpdb'
local_path='/Users/chh/Desktop/allcases_mirror/'
uuid = 'A963A66E-C97F-DC06-4394-36F96800059F'
outfile ='/users/chh/Desktop/mirror/ret.txt'
list_name = []

dirs = os.listdir(local_path)

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
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;' + db_info_src + ' @/root/Desktop/i2active/del_tab.sql')
            #print(stdout.read().decode('utf-8'))

            stdin, stdout, stderr = ssh_tgt.exec_command('cd;source .bash_profile;' + db_info_src + ' @/root/Desktop/i2active/del_tab.sql')

            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --stop '+ uuid)


            #源端执行用例
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;' + db_info_src + ' @/allcases_mirror/' + case_id + '_src.sql')
            print 'cd;source .bash_profile;' + db_info_src + ' @/allcases_mirror/' + case_id + '_src.sql'
            #重新同步
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --start '+uuid)

            sleep(50)
            filename = local_path + case_id + '_tgt.sql'

            size = os.path.getsize(outfile)
            if size/1024>=100:
                shutil.move(outfile, '/users/chh/Desktop/mirror/ret-'+time.strftime("%m-%d-%H-%M", time.localtime()) +'.txt')
            fd_ret = open(outfile, "a+")
            print >> fd_ret, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print >> fd_ret, filename

            fd = open(filename, 'r+')
            next(fd)
            next(fd)
            for line in fd:
                str = line.strip()
                if str == '' or str == '/':
                    continue
                sql = line.strip()
                print >> fd_ret, (sql)
                cursor_src.execute(sql)
                src_ret = cursor_src.fetchall()
                print >> fd_ret, (src_ret)
                cursor_tgt.execute(sql)
                tgt_ret = cursor_tgt.fetchall()
                print >> fd_ret, (tgt_ret)
                if src_ret == tgt_ret:
                    print >> fd_ret, 'pass'
                else:
                    print >> fd_ret, 'fail'
            fd.close()

            os.remove(local_path + case_id + '_src.sql')
            os.remove(local_path + case_id + '_tgt.sql')


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

cursor_src.close()
conn_src.close()
cursor_tgt.close()
conn_tgt.close()
