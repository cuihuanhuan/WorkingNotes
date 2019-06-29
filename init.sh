!#/bin/bash
groupadd -g 1001 oinstall
groupadd -g 1002 dba
groupadd -g 1003 oper
groupadd -g 1004 asmadmin
groupadd -g 1006 asmdba
groupadd -g 1007 asmoper

useradd -u 1001 -g oinstall -G dba,asmadmin,asmdba,asmoper grid
useradd -u 1002 -g oinstall -G dba,asmdba,oper oracle

echo 'oracle' | passwd --stdin grid
echo 'oracle' | passwd --stdin oracle

echo '192.168.62.102 asm'>>/etc/hosts

echo 'fs.aio-max-nr = 1048576'>>/etc/sysctl.conf 
echo 'fs.file-max = 6815744'>>/etc/sysctl.conf 
echo 'kernel.shmall = 2097152'>>/etc/sysctl.conf 
echo 'kernel.shmmax = 4294967295'>>/etc/sysctl.conf 
echo 'kernel.shmmni = 4096'>>/etc/sysctl.conf 
echo 'kernel.sem = 250 32000 100 128'>>/etc/sysctl.conf 
echo 'net.ipv4.ip_local_port_range = 9000 65500'>>/etc/sysctl.conf 
echo 'net.core.rmem_default = 262144'>>/etc/sysctl.conf 
echo 'net.core.rmem_max = 4194304'>>/etc/sysctl.conf 
echo 'net.core.wmem_default = 262144'>>/etc/sysctl.conf 
echo 'net.core.wmem_max = 1048576'>>/etc/sysctl.conf 

/sbin/sysctl -p

echo 'oracle soft nproc 2047'>>/etc/security/limits.conf
echo 'oracle hard nproc 16384'>>/etc/security/limits.conf
echo 'oracle soft nofile 1024'>>/etc/security/limits.conf
echo 'oracle hard nofile 65536'>>/etc/security/limits.conf
echo 'grid soft nproc 2047'>>/etc/security/limits.conf
echo 'grid hard nproc 16384'>>/etc/security/limits.conf
echo 'grid soft nofile 1024'>>/etc/security/limits.conf
echo 'grid hard nofile 65536'>>/etc/security/limits.conf

echo 'session required pam_limits.so'>>/etc/pam.d/login

echo 'if [ $USER = "oracle" ] || [ $USER = "grid" ]; then '>>/etc/profile
echo 'if [ $SHELL = "/bin/ksh" ]; then '>>/etc/profile
echo 'ulimit -p 16384 '>>/etc/profile
echo 'ulimit -n 65536 '>>/etc/profile
echo 'else '>>/etc/profile 
echo 'ulimit -u 16384 -n 65536 '>>/etc/profile
echo 'fi  '>>/etc/profile
echo 'umask 022 '>>/etc/profile
echo 'fi '>>/etc/profile

mkdir -p /u01/app/oraInventory
chown -R grid:oinstall /u01/app/oraInventory
chmod -R 775 /u01/app/oraInventory

mkdir -p /u01/app/grid
chown -R grid:oinstall /u01/app/grid
chmod -R 775 /u01/app/grid

mkdir -p /u01/app/oracle
mkdir -p /u01/app/oracle/cfgtoollogs
chown -R oracle:oinstall /u01/app/oracle 
chmod -R 775 /u01/app/oracle

mkdir /u01/app/11.2.0/grid -p
chown grid:oinstall /u01/app/11.2.0/grid
chmod -R 775 /u01/app/11.2.0/grid

echo 'export ORACLE_SID=+ASM' >> /home/grid/.bash_profile
echo 'export ORACLE_BASE=/u01/app/grid' >> /home/grid/.bash_profile
echo 'export ORACLE_HOME=/u01/app/11.2.0/grid' >> /home/grid/.bash_profile
echo 'export PATH=$ORACLE_HOME/bin:$PATH' >> /home/grid/.bash_profile


echo 'export ORACLE_SID=orcl' >> /home/oracle/.bash_profile
echo 'export ORACLE_UNQNAME=orcl' >> /home/oracle/.bash_profile
echo 'export ORACLE_BASE=/u01/app/oracle' >> /home/oracle/.bash_profile
echo 'export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1' >> /home/oracle/.bash_profile
echo 'export PATH=$ORACLE_HOME/bin:$PATH' >> /home/oracle/.bash_profile







