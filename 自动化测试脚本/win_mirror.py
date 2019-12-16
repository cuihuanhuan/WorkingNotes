# -*- coding: utf-8 -*-
# This program is used to test increment backup.



import os.path
import cx_Oracle
from time import sleep
import winrm
import cx_Oracle
import time
import shutil
import json

os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
source_ip = '192.168.80.50'


db_info_src = 'sqlplus huan1/12345@192.168.80.50/orclpdb'
db_src = 'huan1/12345@192.168.80.50/orclpdb'
db_tgt = 'huan1/12345@192.168.80.51/orclpdb'
uuid = '2197238F-3EB1-A2B1-3FDA-4FFB30D2E0D9'

outfile ='/Users/chh/Desktop/mirror/ret.txt'


conn_src = cx_Oracle.connect(db_src)
cursor_src = conn_src.cursor()
conn_tgt = cx_Oracle.connect(db_tgt)
cursor_tgt = conn_tgt.cursor()

list_name = []
path = "/Users/chh/Desktop/allcases_mirror/"
dirs = os.listdir(path)
for file in dirs:
    if file[-7:] == 'src.sql':
        list_name.append(file[:-8])
    else:
        continue



winsrc = winrm.Session('http://192.168.80.50', auth=('administrator', 'qwe123!@#'))
wintgt = winrm.Session('http://192.168.80.51', auth=('administrator', 'qwe123!@#'))
for case_id in list_name:
    winsrc.run_cmd('iadebug work --stop ' + uuid)
    while 1:
        win_ret = wintgt.run_cmd('iadebug back --state '+ uuid)
        state_back = win_ret.std_out
        state_json = json.loads(state_back)
        state = state_json['fullbackup']['state']
        if state == 'pause':
            print 'pause'
            break
        else:
            print 'no pause'
            sleep(10)
            continue

    #需要加个break在get_command_output函数的while里
    winsrc.run_cmd(db_info_src + ' @C:\Users\chh\Desktop\/allcases_mirror\/'+ case_id +'_src.sql')
    sleep(50)
    winsrc.run_cmd('iadebug work --start ' + uuid)

    while 1:
        state_back = wintgt.run_cmd('iadebug back --state ' + uuid)
        state_str = state_back.std_out
        state_json = json.loads(state_str)
        state = state_json['fullbackup']['state']
        if state == 'track':
            print 'track'
            break
        else:
            print 'dump'
            sleep(10)
            continue
    filename = '/Users/chh/Desktop/allcases_mirror/' + case_id + '_tgt.sql'
    print case_id + '--' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    size = os.path.getsize(outfile)
    if size / 1024 >= 100:
        shutil.move(outfile, '/Users/chh/Desktop/mirror/ret-' + time.strftime("%m-%d-%H-%M", time.localtime()) + '.txt')
    fd_ret = open(outfile, "a+")

    print >> fd_ret, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print >> fd_ret, filename


    fd = open(filename, 'r+')
    next(fd)
    next(fd)
    try:
        for line in fd:
            str = line.strip()
            if str == '' or str == '/':
                continue
            sql = line.strip()
            print >> fd_ret, sql
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
        fd_ret.close()
        file_src = '/Users/chh/Desktop/allcases_mirror/' + case_id + '_src.sql'
        file_tgt = '/Users/chh/Desktop/allcases_mirror/' + case_id + '_tgt.sql'
        os.remove(file_src)
        os.remove(file_tgt)
    except cx_Oracle.DatabaseError, msg:
        print (msg)
        print case_id + " error! "
        continue
cursor_src.close()
conn_src.close()
cursor_tgt.close()
conn_tgt.close()