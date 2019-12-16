# -*- coding: utf-8 -*-


import paramiko
import os.path
import cx_Oracle
from time import sleep
import time
import shutil
import json
os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'


src_ip = '192.168.100.11'
tgt_ip = '192.168.100.14'


db_info_src = 'sqlplus huan1/12345@orcl'

db_src = 'huan1/12345@192.168.100.11/orcl'
db_tgt = 'huan1/12345@192.168.100.14/orcl'

db_conn_src = 'i2/12345@192.168.100.11/orcl'
db_conn_tgt = 'i2/12345@192.168.100.14/orcl'

local_path='/Users/chh/Desktop/allcases_mirror/'

outfile ='/Users/chh/Desktop/mirror/ret.txt'
goodsqlfile = '/Users/chh/Desktop/mirror/goodsql.txt'
badsqlfile = '/Users/chh/Desktop/mirror/badsql.txt'


uuid = '4FC418A8-CA9E-FDAE-FC8C-167C88671427'

list_name = []
def create_ssh(ip,username,password):
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(ip, 22, username, password, allow_agent=False, look_for_keys=False, timeout=5)
    return ssh_client


def recreate_user(dbconn,machine):
    conn = cx_Oracle.connect(dbconn)
    cursor_conn = conn.cursor()           
    cursor_conn.execute('select sid,serial# from v$session where username =\'HUAN1\'')
    conn_ret = cursor_conn.fetchall()
    if len(conn_ret):
        print conn_ret
        for i,x in enumerate(conn_ret):
            sql =  'alter system kill session \''+  str(x[0]) +',' +str(x[1]) +'\''
            cursor_conn.execute(sql)
            print sql
    cursor_conn.execute('select username from all_users where username=\'HUAN1\'')
    conn_ret = cursor_conn.fetchall()
    if len(conn_ret)!=0:
        cursor_conn.execute('drop user huan1 cascade')
        cursor_conn.execute('select username from all_users where username=\'HUAN1\'')
        conn_ret = cursor_conn.fetchall()
        if len(conn_ret)==0:
            print 'drop '+machine+ ' user'
    cursor_conn.execute('create user huan1 identified by 12345')
    cursor_conn.execute('grant dba to huan1')
    cursor_conn.execute('select username from all_users where username=\'HUAN1\'')
    conn_ret = cursor_conn.fetchall()
    print conn_ret
    if len(conn_ret):
        print 'create '+machine+ ' user'


def get_rule_state(ssh_client,uuid):

    countpause = 0
    countdump = 0
    while 1:
        stdin, stdout, stderr = ssh_client.exec_command('/root/Desktop/i2active/bin/iadebug back --state ' + uuid)
        cmd_result = stdout.read(), stderr.read()
        ret = json.loads(cmd_result[0])
        state = ret['fullbackup']['state']
        if state == 'track':
            print 'track'
            break;
        elif state == 'dump':
            print 'dump'
            countdump = countdump+1
            if countdump>30:
                ssh_client.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --start '+uuid)
                print 'start rule again'
            sleep(10)
        elif state =='pause':
            countpause=countpause+1
            if countpause>30:#-3522
                ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --start '+uuid)
                print 'start rule again'
            print 'pause'
            sleep(10)
        else:
            print "unkown state"
            exit(0)

def query_print_ret(local_path,case_id,db_src,db_tgt,outfile,goodsqlfile,badsqlfile):
    filename = local_path + case_id + '_tgt.sql'

    size = os.path.getsize(outfile)
    if size/1024>=100:
        shutil.move(outfile, '/users/chh/Desktop/mirror/ret-'+time.strftime("%m-%d-%H-%M", time.localtime()) +'.txt')
    fd_ret = open(outfile, "a+")
    print >> fd_ret, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print >> fd_ret, filename
    #cmd = 'cd;source .bash_profile;' + db_info_src + ' @/allcases_mirror/' + case_id + '_src.sql'
    #print >> fd_ret, cmd

    conn_src = cx_Oracle.connect(db_src)
    cursor_src = conn_src.cursor()
    conn_tgt = cx_Oracle.connect(db_tgt)
    cursor_tgt = conn_tgt.cursor()

    fd = open(filename, 'r+')
    next(fd)
    next(fd)
    for line in fd:
        try:
            strx = line.strip()
            if strx == '' or strx == '/':
                continue
            sql = line.strip()
            print >> fd_ret, (sql)
            cursor_src.execute(sql)
            src_ret = cursor_src.fetchall()
            print >> fd_ret, (src_ret)
            print src_ret
            
            cursor_tgt.execute(sql)
            tgt_ret = cursor_tgt.fetchall()
            print >> fd_ret, (tgt_ret)
            print tgt_ret
            if src_ret == tgt_ret:
                print >> fd_ret, 'pass'
                sys_str="update list_case set state='PASS' where case_id =" +"'"+ case_id +"'"+";commit;"
                #sys_str = case_id
                size_goodsql = os.path.getsize(goodsqlfile)
                if size_goodsql / 1024 >= 100:
                    shutil.move(goodsqlfile,'/Users/chh/Desktop/mirror/goodsql-' + time.strftime("%m-%d-%H-%M", time.localtime()) + '.txt')

                fd_goodsql = open(goodsqlfile, "a+")
                
                print >> fd_goodsql, (sys_str)
                fd_goodsql.close()
            else:
                print >> fd_ret, 'fail'
                sys_str="update list_case set state='FAIL' where case_id =" +"'"+ case_id +"'"+";commit;"
                #sys_str = case_id
                fd_badsql = open(badsqlfile, "a+")
                print >> fd_badsql, (sys_str)
                fd_badsql.close()

        except cx_Oracle.DatabaseError, msg:
            print (msg)
            print case_id + " error! "
            print >> fd_ret, msg
            continue

    fd.close()
    fd_ret.close()
    cursor_src.close()
    conn_src.close()
    cursor_tgt.close()
    conn_tgt.close()






dirs = os.listdir(local_path)

for file in dirs:
    if file[-7:] == 'src.sql':
        list_name.append(file[:-8])
    else:
        continue


ssh_src = create_ssh(src_ip,'root','12345')
ssh_tgt = create_ssh(tgt_ip,'root','12345')


for case_id in list_name:
        try:

            
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --stop '+uuid)


            recreate_user(db_conn_src,'work')
            recreate_user(db_conn_tgt,'back')

            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;' + db_info_src + ' @/allcases_mirror/' + case_id + '_src.sql')
            print 'cd;source .bash_profile;' + db_info_src + ' @/allcases_mirror/' + case_id + '_src.sql'
            sleep(5)
            stdin, stdout, stderr = ssh_src.exec_command('cd;source .bash_profile;/root/Desktop/i2active/bin/iadebug work --start '+uuid)
            sleep(60)
            get_rule_state(ssh_tgt,uuid)

            query_print_ret(local_path,case_id,db_src,db_tgt,outfile,goodsqlfile,badsqlfile)
            
            os.remove(local_path + case_id + '_src.sql')
            os.remove(local_path + case_id + '_tgt.sql')


        except UnicodeDecodeError, msg:
            print (msg)
            print case_id + " error! "
            continue

        except paramiko.ssh_exception.SSHException, msg:
            print (msg)
            print case_id + " error! "
            exit(0)
            continue

        except IOError, msg:
            print (msg)
            print case_id + " error! "
            continue







