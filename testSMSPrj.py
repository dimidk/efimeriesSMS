#!/usr/bin/python
#-*- coding: utf-8 -*-

import subprocess
import os
import time

fromDir='/home/boys/projectsPython/SMS/test'

copyDir='/home/boys/projectsPython/SMS/efimeries/efimeriesSMS/efimeries'

xlsName='efimeries.xls'

def findFile(filesDir,tag):
	
	flag=0
	a=False

	for root,dirs,filenames in os.walk(filesDir,topdown=True):
		"""listall=[name for name in filenames if name.find('xls.prc')!=-1]"""
		listall=[name for name in filenames if name.find(tag)!=-1]
		xmllist=[name for name in filenames if name.find('xml')!=-1]
		xlslist=[name for name in filenames if name not in listall and name not in xmllist]
	
	if len(xlslist)>0:
		a=True
		
	return xlslist,a
	


def callCommand(cmd):
	
	if (subprocess.call(cmd))==0:
		print "Ok"
	else:
		print "Error in",cmd," command"
		exit(0)
		

curDir=os.getcwd()
print curDir

xlsList,a=findFile(fromDir,'xls.check')

if a:
	
	for xls in xlsList:
				
		mv_cmd='mv '+ fromDir+'/'+xls+' '+fromDir+'/'+xlsName
		cp_cmd='cp '+fromDir+'/'+xlsName+' '+copyDir
		
		xlsCheck=xls+'.check'
		ren_cmd='mv ' + fromDir+'/'+xlsName +' ' + fromDir+'/'+xlsCheck
		callCommand(mv_cmd.split(' '))
		callCommand(cp_cmd.split(' '))
		callCommand(ren_cmd.split(' '))
		
		time.sleep(3600)
