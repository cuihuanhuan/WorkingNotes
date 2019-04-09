--查询表中的约束
select table_name,constraint_name,constraint_type from user_constraints where table_name='大写表名'
/
--查询数据库版本
select * from v$version
/
--查询当前登录用户信息
select user from dual
/
--查询当前用户的表
select table_name from user_tables
/
--查询表空间中数据文件具体位置
SQL> select name from v$datafile;

NAME
--------------------------------------------------------------------------------
+DATA/orcl/datafile/system.264.987707247
+DATA/orcl/datafile/sysaux.265.987707269
+DATA/orcl/datafile/undotbs1.266.987707289
+DATA/orcl/datafile/users.268.987707353

--查看redolog路径
select * from v$logfile;
+DATA/orcl/onlinelog/

SQL> archive log list
Database log mode	       Archive Mode
Automatic archival	       Enabled
Archive destination	       +DATA/arch/
Oldest online log sequence     1133
Next log sequence to archive   1135
Current log sequence	       1135
SQL> 

select 'drop table '||table_name||' purge;' from cat where table_type='TABLE';  


select count(*) from user_tables;

SQL>purge recyclebin;

select table_name||','||column_name||','||data_type||','||data_length from user_tab_columns where table_name = 'DDS_CHAR' order by table_name 

/

--查看directory的路径
select directory_path from all_directories where upper(directory_name) = 'MYDIR'
/


select userenv('language') from dual; 
/
--赋权限
grant select on sys.link$ to huan2;
/

--12c赋权限
grant all on sys.user$ to i2;
grant all on sys.seq$ to i2;
grant all on SYS.UNDO$ to i2;

--查询字符串的长度
SQL> select length(name2) from i2_ddl_t1;

LENGTH(NAME2)
-------------
	    3
	    3
	    3


DECLARE 
long_var long:=0;
BEGIN
  DBMS_OUTPUT.PUT_LINE(LENGTH(long_var));
  SELECT lname INTO long_var FROM i2_ddl_t1;
  DBMS_OUTPUT.PUT_LINE(LENGTH(long_var));
END;
/

--查询long的长度
set serveroutput on size 100000
DECLARE 
  CURSOR C1 IS
  SELECT lname FROM i2_ddl_t1;
BEGIN
  FOR i2_ddl_t1 IN c1
  LOOP
    DBMS_OUTPUT.PUT_LINE(LENGTH(i2_ddl_t1.lname));
  END LOOP;
END;
/


select object_name,object_type,status from user_objects where object_type='PROCEDURE';
select object_name,object_type,status from user_objects where object_type='TABLE';
select object_name,object_type,status from user_objects where object_type='INDEX';
select object_name,object_type,status from user_objects where object_type='VIEW';
select object_name,object_type,status from user_objects where object_type='SEQUENCE';
select object_name,object_type,status from user_objects where object_type='FUNCTION';
select object_name,object_type,status from user_objects where object_type='PACKAGE';
select object_name,object_type,status from user_objects where object_type='PACKAGE BODY';
select object_name,object_type,status from user_objects where object_type='SYNONYM';
Synonym
--查询job
select job,what from user_jobs;

select job_name,schedule_name from user_scheduler_jobs;

select job,log_user,priv_user,schema_user,what from user_jobs;

select job,log_user,priv_user,schema_user,what,interval from user_jobs;

select job,broken from user_jobs;

select status from user_scheduler_job_run_details;


select enabled from user_scheduler_jobs;
--删除job
begin
    dbms_job.remove(126);--和select * from user_jobs; 中的job值对应，看what对应的过程
	commit;
end;
/



lsof -i
查看进程占用的端口

--查看view定义语句
select count(*) from user_views
/
select view_name,text from user_views
/


SQL> 
select object_id from dba_objects where object_name=upper('dds_test_seq');
select object_id from dba_objects where object_name=upper('dds_test_seq2');

 OBJECT_ID
----------
    149509
SQL> grant all on sys.seq$ to huan2;
SQL> SELECT USER_ID FROM ALL_users where username='HUAN2';

   USER_ID
----------
       118

SQL> select obj# from sys.obj$ where name='DDS_TEST_SEQ2' and owner#=118;    

      OBJ#
----------
    110399

SQL> select highwater from sys.seq$ where obj#=149509;

 HIGHWATER
----------
       105
--查询INVALID对象
	   SELECT owner, object_name, object_type,status 
FROM dba_objects 
WHERE status = 'INVALID' and owner='HUAN2';


--查询约束
select owner,table_name,CONSTRAINT_NAME from user_constraints where owner='HUAN2';

--查看触发器
select trigger_name,table_owner,table_name,status from user_triggers;

TRIGGER_NAME		       TABLE_OWNER
------------------------------ ------------------------------
TABLE_NAME		       STATUS
------------------------------ --------
test_log_trig1		       HUAN2
test_log		       DISABLED



SQL> desc user_procedures; 
 Name					   Null?    Type
 ----------------------------------------- -------- ----------------------------
 OBJECT_NAME					    VARCHAR2(128)
 PROCEDURE_NAME 				    VARCHAR2(30)
 OBJECT_ID					    NUMBER
 SUBPROGRAM_ID					    NUMBER
 OVERLOAD					    VARCHAR2(40)
 OBJECT_TYPE					    VARCHAR2(19)
 AGGREGATE					    VARCHAR2(3)
 PIPELINED					    VARCHAR2(3)
 IMPLTYPEOWNER					    VARCHAR2(30)
 IMPLTYPENAME					    VARCHAR2(30)
 PARALLEL					    VARCHAR2(3)
 INTERFACE					    VARCHAR2(3)
 DETERMINISTIC					    VARCHAR2(3)
 AUTHID 					    VARCHAR2(12)

SQL> desc user_objects;
 Name					   Null?    Type
 ----------------------------------------- -------- ----------------------------
 OBJECT_NAME					    VARCHAR2(128)
 SUBOBJECT_NAME 				    VARCHAR2(30)
 OBJECT_ID					    NUMBER
 DATA_OBJECT_ID 				    NUMBER
 OBJECT_TYPE					    VARCHAR2(19)
 CREATED					    DATE
 LAST_DDL_TIME					    DATE
 TIMESTAMP					    VARCHAR2(19)
 STATUS 					    VARCHAR2(7)
 TEMPORARY					    VARCHAR2(1)
 GENERATED					    VARCHAR2(1)
 SECONDARY					    VARCHAR2(1)
 NAMESPACE					    NUMBER
 EDITION_NAME					    VARCHAR2(30)

SQL> 

--查询同义词
select synonym_name,table_owner,table_name from user_synonyms;


--user_procedures表包含function,procedure,package


select object_name from user_procedures;

OBJECT_NAME
--------------------------------------------------------------------------------
DDS_PACK_TEST
DDS_PROC_TEST
DDS_PACK_TEST


--查询用户权限
SQL>  select * from user_sys_privs;

USERNAME		       PRIVILEGE				ADM
------------------------------ ---------------------------------------- ---
HUAN2			       EXECUTE ANY TYPE 			NO
PUBLIC			       EXECUTE ANY TYPE 			NO
HUAN2			       UNLIMITED TABLESPACE			NO

--查询user_id
SQL> select username,user_id from all_users where user_id=107;

USERNAME			  USER_ID
------------------------------ ----------
HUAN3				      107

select object_name,object_type,status from user_objects;


--查询物化视图
select name from all_snapshots;
select MVIEW_NAME from all_mviews;
select mview_name from user_mviews;



all_views;
user_views;
user_users;
all_users;


desc user_objects;



select object_name,status from user_objects where object_type='JAVA CLASS';
select object_name,status from user_objects where object_type='JAVA SOURCE';



SQL> desc v$log
 Name					   Null?    Type
 ----------------------------------------- -------- ----------------------------
 GROUP# 					    NUMBER
 THREAD#					    NUMBER
 SEQUENCE#					    NUMBER
 BYTES						    NUMBER
 BLOCKSIZE					    NUMBER
 MEMBERS					    NUMBER
 ARCHIVED					    VARCHAR2(3)
 STATUS 					    VARCHAR2(16)
 FIRST_CHANGE#					    NUMBER
 FIRST_TIME					    DATE
 NEXT_CHANGE#					    NUMBER
 NEXT_TIME					    DATE

SQL> select FIRST_TIME,NEXT_TIME from v$log;

FIRST_TIME   NEXT_TIME
------------ ------------
09-JAN-19    09-JAN-19
09-JAN-19    10-JAN-19
10-JAN-19

SQL> 


grant all on sys.seq$ to huan1;


select trigger_name,status from user_triggers;
select object_name,object_type,status from user_objects where object_type='TRIGGER'


select INDEX_NAME,TABLE_NAME from user_indexes;
select constraint_name,table_name from user_constraints;


SELECT OBJ#,DATAOBJ#,NAME FROM SYS.OBJ$ WHERE OWNER#=108;


select owner,object_name from dba_objects where object_type='DATABASE LINK';


--远程连接数据库
sqlplus I2/12345@192.168.1.120:1521/pdb

sqlplus I2/12345@192.168.1.119:1521/pdb


SQL> desc all_directories;
 Name					   Null?    Type
 ----------------------------------------- -------- ----------------------------
 OWNER					   NOT NULL VARCHAR2(30)
 DIRECTORY_NAME 			   NOT NULL VARCHAR2(30)
 DIRECTORY_PATH 				    VARCHAR2(4000)



SQL> select directory_name,owner,directory_path from all_directories where owner='HUAN2';

--查看当前用户的表空间名称
SQL> select default_tablespace from dba_users where username='HUAN1';

DEFAULT_TABLESPACE
------------------------------
USERS

alter user huan1 default tablespace users;
alter user huan1 default tablespace system;
alter user 用户名 default tablespace 表空间名字 ;--创建时候指定表空间。

select OBJ#,DATAOBJ#,NAME,OWNER# FROM sys.obj$ where name='DDS_DEPT' AND OWNER#=150;
select OBJ#,DATAOBJ#,NAME,OWNER# FROM sys.obj$ where name='OBJECTS' AND OWNER#=150;
SELECT USER#,NAME FROM SYS.USER$ WHERE NAME='HUAN1';
select user#,name from sys.user$ where user#=135;
