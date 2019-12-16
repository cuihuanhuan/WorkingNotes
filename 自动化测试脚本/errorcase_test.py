#coding:utf-8
#This program is used to create a table for case management.
import os
import sys
import os.path
import shutil
fd = open('/Users/chh/Desktop/fail_case.txt','r+')
#fd_out = open('/Users/chh/Desktop/out.txt', "a+")
for line in fd:
	#print line.strip()

	name = line.strip()
	# s = '\'' + name + '\''+','
	# print  >>  fd_out,s
	#print '/Users/chh/Desktop/allcases/' + name + '_src.sql'
	shutil.copy('/Users/chh/Desktop/allcases_mirror/' + name + '_src.sql','/Users/chh/Desktop/error_case/')
	shutil.copy('/Users/chh/Desktop/allcases_mirror/' + name + '_tgt.sql','/Users/chh/Desktop/error_case/')

exit(0)

