
Oracle rac安装基本用iscsi-target存储比较简单

yum install scsi-target-utils


vim /etc/tgt/targets.conf 

<target iqn.2019-05.com:server>
    backing-store /dev/sdc1     # Becomes LUN 1
    backing-store /dev/sdd1     # Becomes LUN 2
    backing-store /dev/sde1     # Becomes LUN 3
    backing-store /dev/sdf1     # Becomes LUN 4
    write-cache off
    vendor_id MyCompany Inc.
</target>



/etc/init.d/tgtd start
chkconfig tgtd on
##加上分区名才显示出来LUN
tgt-admin --show  
[root@localhost Desktop]# netstat -tlunp|grep tgt
tcp        0      0 0.0.0.0:3260                0.0.0.0:*                   LISTEN      14796/tgtd          
tcp        0      0 :::3260                     :::*                        LISTEN      14796/tgtd          


mkdir /u01
mount /dev/sdb1 /u01




---------客户端配置----

yum install iscsi-initiator-utils
/etc/init.d/iscsid start
chkconfig iscsid on


[root@node1 Desktop]# iscsiadm -m discovery -t st -p 192.168.19.1
192.168.18.1:3260,1 iqn.2019-05.com:server

连接共享存储后才看到共享磁盘

连接所有的共享分区：iscsiadm -m node -L all
退出共享存储
iscsiadm -m node -T iqn.2019-05.com:server -p 192.168.19.1:3260  -u


连接指定的Target： 
iscsiadm -m node -T iqn.2019-05.com:server -p 192.168.18.1 --login


iscsiadm -m node -T iqn.2019-05.com:server -p 192.168.18.1 --logout



即使分区后，在客户端看到的也是块设备名称，但是源端的磁盘操作，在备端能获取的


用这个iscsi共享，直接oracleasm createdisk