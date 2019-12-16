#coding:utf-8
#This program is used to create a table for case management.
import os
import sys
import os.path
import cx_Oracle
import exceptions
import codecs
#os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
#os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'
try:
#conn user/passwd@ip/instance
    conn = cx_Oracle.connect('i2/12345@192.168.100.11/orcl')      
    cursor = conn.cursor () 
    #create table
    cursor.execute("drop table list_case")  
    cursor.execute ("create table list_case (case_id varchar2(20), case_road varchar2(100), case_name varchar2(200), state varchar2(20))")
    #get data
    #f = codecs.open('/Users/chh/Desktop/12c/pk_case/case_name.txt','r','utf-8')
    f = codecs.open('/Users/chh/Desktop/allcases_mirror/case_name.txt','r','utf-8')
    lines = f.readlines()
    f.close()
    #insert
    for index,line in enumerate(lines):
        sql="""insert into list_case (case_id,case_road,case_name,state) values ("""
        for fields in (line.split("@")):  
            sql=sql+"'"+fields+"',"
        sql=sql[:-1]+")"
        #print sql
        cursor.execute(sql) 
    conn.commit()  
    cursor.close ()  
    conn.close ()
    print 'FINISHED'  
except cx_Oracle.DatabaseError,msg:
    print "OPERATION ERROR"
    print(msg)