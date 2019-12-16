# -*- coding: utf-8 -*-
# This program is used to test increment backup.


import paramiko
import os.path
import cx_Oracle
from time import sleep
import json
import time
import shutil

os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
source_ip = '192.168.100.11'
src_ip = '192.168.100.11'
tgt_ip = '192.168.100.14'

db_info_src = 'sqlplus huan1/12345@192.168.100.11/orcl'
db_src = 'huan1/12345@192.168.100.11/orcl'
db_tgt = 'huan1/12345@192.168.100.14/orcl'
outfile = '/Users/chh/Desktop/incre/ret.txt'
goodsqlfile = '/Users/chh/Desktop/incre/goodsql.txt'
badsqlfile = '/Users/chh/Desktop/incre/badsql.txt'
uuid = 'D3FB016E-9703-37F8-F81C-C66E876F9559'
trackuuid = 'C240347B-7375-F986-FA90-3488695EBA81'
# loop to get case_id
list_name = []
path = "/Users/chh/Desktop/allcases_incre/"
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

def check_json(input_str):
    try:
        json.loads(input_str)
        return True
    except:
        return False

def print_result(input_str):
    if check_json(input_str):
        print "This is a valid json."
    else:
        #exit(0)
        print "not a valid json."
        exit(0)
#conn_manage = cx_Oracle.connect('i2/12345@192.168.80.7/orcl') 
#cursor_manage = conn_manage.cursor()
#原端ssh
def create_ssh(ip,username,password):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, 22, username, password, allow_agent=False, look_for_keys=False, timeout=5)
    return ssh_client
    
ssh_src = create_ssh(src_ip,'root','12345')
ssh_tgt = create_ssh(tgt_ip,'root','12345')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(source_ip, 22, 'root', '12345', timeout=5)
for case_id in list_name:

        try:
            # preparation
            ##source for linux:do case

            stdin, stdout, stderr = ssh.exec_command('cd;source .bash_profile;' + db_info_src + ' @/allcases_incre/' + case_id + '_src.sql')

            print('cd;source .bash_profile;' + db_info_src + ' @/allcases_incre/' + case_id + '_src.sql')

            filename ='/Users/chh/Desktop/allcases_incre/' + case_id + '_tgt.sql'

            size = os.path.getsize(outfile)
            if size / 1024 >= 100:
                shutil.move(outfile,'/Users/chh/Desktop/incre/ret-' + time.strftime("%m-%d-%H-%M", time.localtime()) + '.txt')
            


            fd_ret = open(outfile, "a+")

            print >> fd_ret, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print >> fd_ret, filename
            sleep(50)
            #print filename
            fd = open(filename, 'r+')
            next(fd)
            next(fd)
            for line in fd:
                str = line.strip()
                if str == '' or str=='/':
                    continue
                sql = line.strip()
                print >>fd_ret, sql
                cursor_src.execute(sql)
                src_ret = cursor_src.fetchall()
                print src_ret
                print >> fd_ret, (src_ret)
                cursor_tgt.execute(sql)
                tgt_ret = cursor_tgt.fetchall()
                print tgt_ret
                print >> fd_ret, (tgt_ret)
                if src_ret == tgt_ret:
                    print >>fd_ret, 'pass'
                    sys_str="update list_case set state='PASS' where case_id =" +"'"+ case_id +"'"+";commit;"
                    #cursor_manage.execute (sys_str) 
                    size_goodsql = os.path.getsize(goodsqlfile)
                    if size_goodsql / 1024 >= 100:
                        shutil.move(goodsqlfile,'/Users/chh/Desktop/incre/goodsql-' + time.strftime("%m-%d-%H-%M", time.localtime()) + '.txt')

                    fd_goodsql = open(goodsqlfile, "a+")
                    
                    print >> fd_goodsql, (sys_str)
                    
                else:
                    print >>fd_ret, 'fail'
                    sys_str="update list_case set state='FAIL' where case_id =" +"'"+ case_id +"'"+";commit;"
                    #cursor_manage.execute (sys_str) 
                    fd_badsql = open(badsqlfile, "a+")
                    print >> fd_badsql, (sys_str)
                    
            fd.close()
            fd_ret.close()
            #判断iatrack是否在
            stdin, stdout, stderr = ssh_src.exec_command('/root/Desktop/i2active/bin/iadebug track --state ' + trackuuid)
            cmd_result = stdout.read()
            #print cmd_result
            ret_track = print_result(cmd_result)
            #判断iaback是否在
            stdin, stdout, stderr = ssh_tgt.exec_command('/root/Desktop/i2active/bin/iadebug back --state ' + uuid)
            cmd_result = stdout.read()
            #print cmd_result
            ret_back = print_result(cmd_result)
            
            file_src = '/Users/chh/Desktop/allcases_incre/' + case_id + '_src.sql'
            file_tgt = '/Users/chh/Desktop/allcases_incre/' + case_id + '_tgt.sql'
            os.remove(file_src)
            os.remove(file_tgt)
           


        except cx_Oracle.DatabaseError, msg:
            print (msg)
            print >> fd_ret, msg
            continue
ssh.close()
cursor_src.close()
conn_src.close()
cursor_tgt.close()
conn_tgt.close()