#!/usr/bin/python
#-*- coding:utf-8 -*-

import sys
import os
import datetime
import string
import init
import passwd
import xlrd



class TeachersStoixeia():

	teacherstoixeia=dict()
	
	def __init__(self,Surname,AFM,Name,PhoneNumber):
		
		
		self.Surname=str(Surname)
		self.AFM=str(AFM)
		self.Name=str(Name)
		
		self.PhoneNumber=str(PhoneNumber)
	
		TeachersStoixeia.teacherstoixeia[self.Surname]=[self.AFM,self.Name,self.PhoneNumber]
		

def mvFileToFirstName(filename):
	
	filename_prc=filename
	filename=filename.split('prc')[0]+'xls'
	os.rename(filename_prc,filename)


def read_StoixeiaFile(filename):
	try:
	
		fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	except:
		print "open file error"


	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Teachers'' file'+filename+' and add to dictionary\n')
	
	sheet=fp.sheet_by_index(0)

	for i in range(13,sheet.nrows,1):
		
		"""this is a solution for problem in converting unicode and ascii"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		afm=sheet.row_values(i)[1]
		surname=sheet.row_values(i)[2]
		name=sheet.row_values(i)[3]
		phonenumber=str(sheet.row_values(i)[5])
		
		s=TeachersStoixeia(surname,afm,name,phonenumber)
			
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':add teacher ' + s.AFM +' '+s.Surname+' '+s.Name+' '+str(s.PhoneNumber) +'\n')
	
	

	filename_prc=filename.split('xls')[0]+'prc'
	os.rename(filename,filename_prc)
	

"""def update_dict(filename):
	
	try:
	
		fp=xlrd.open_workbook(filename,encoding_override="cp1252")
	except:
		print "open file error"


	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Students'' file'+filename+' and update dictionary\n')
	
	sheet=fp.sheet_by_index(0)
	print sheet.nrows
	for i in range(15,sheet.nrows,1):
		

		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		afm=sheet.row_values(i)[1]
		surname=sheet.row_values(i)[2]
		name=sheet.row_values(i)[4]
		phonenumber=sheet.row_values(i)[10]
		
		if TeachersStoixeia.teacherstoixeia.has_key(afm):
			tmpStoixeia=TeachersStoixeia.teacherstoixeia.get(afm)
			
			TeachersStoixeia.teacherstoixeia.pop(afm)
			s=TeachersStoixeia(afm,surname,name,phonenumber)
			
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':update student ' + s.AFM +' '+s.Surname+' '+s.Name+' '+str(s.PhoneNumber) +'\n')
			
	filename_prc=filename+'.prc'
	os.rename(filename,filename_prc)"""
	
	
def read_files():
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read Teachers'' information files\n')
	
	for root,dirs,filenames in os.walk(init.stoixeiaDir,topdown=True):
		for name in filenames:
			filename=os.path.join(init.stoixeiaDir,name)
			
			if 'xls' not in filename:
				continue
			read_StoixeiaFile(filename)
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Complete Teachers'' information dictionary\n')
	

"""read_files()
for key,value in TeachersStoixeia.teacherstoixeia.items():
		for v in value:
			print key,"=>",v"""
