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
	
	"""class which makes a dictionary for teachers
	if there are teachers with the same surname then the first letter of their first name is add to key"""

	teacherstoixeia=dict()
	findDupNames=0
	
			
	def __init__(self,Surname,Specialty,AFM,Name,PhoneNumber):
		
		
		self.Surname=str(Surname)
		self.Specialty=str(Specialty)
		self.AFM=str(AFM)
		self.Name=str(Name)
		
		self.PhoneNumber=str(PhoneNumber)
		
		if (self.Surname,self.Specialty) not in TeachersStoixeia.teacherstoixeia:
	
			TeachersStoixeia.teacherstoixeia[(self.Surname,self.Specialty)]=[self.AFM,self.Name,self.PhoneNumber]
		else:
						
			TeachersStoixeia.findDupNames+=1
			
			Surname=Surname+" "+Name[0]
			self.Surname=str(Surname)
			TeachersStoixeia.teacherstoixeia[(self.Surname,self.Specialty)]=[self.AFM,self.Name,self.PhoneNumber]
			

def mvFileToFirstName(filename):
	
	filename_prc=filename
	filename=filename.split('prc')[0]+'xls'
	os.rename(filename_prc,filename)


def read_StoixeiaFile(filename):
	
	"""this function read excell file and call a class (TeacherStoixeia) to make a dictionary with this information"""
	
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
		specialty=sheet.row_values(i)[2]
		surname=sheet.row_values(i)[3].strip()
		name=sheet.row_values(i)[4].strip()
		phonenumber=str(sheet.row_values(i)[6])

		if surname.find(' ')!=-1:
			surname=surname.split()[0]
		
		s=TeachersStoixeia(surname,specialty,afm,name,phonenumber)
			
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':add teacher ' + str(s.AFM) +' '+str(s.Surname)+' '+str(s.Specialty)+' '+str(s.Name)+' '+str(s.PhoneNumber) +'\n')
	
	
	"""print "teachers' information\n"
	for key,val in TeachersStoixeia.teacherstoixeia.items():
		for k in key:
			print k,
		print "==>",
		for t in val:
			print t,
		print "\n"
	
	print "duplicate names:",TeachersStoixeia.findDupNames"""
	
	
	filename_prc=filename.split('xls')[0]+'prc'
	os.rename(filename,filename_prc)
	
def fixDupKeys():
	
	"""it changes the key that is the same surname with others"""
	
	if TeachersStoixeia.findDupNames>0:
		
		keysList=TeachersStoixeia.teacherstoixeia.keys()
		
		findkey=[k for k in keysList if ' ' in k][0].split()[0]
		
		stoixeia=TeachersStoixeia.teacherstoixeia.get(findkey)
		new_key=str(findkey+' '+stoixeia[1].decode(encoding='UTF-8')[0])
		TeachersStoixeia.teacherstoixeia[new_key]=TeachersStoixeia.teacherstoixeia[findkey]
		del TeachersStoixeia.teacherstoixeia[findkey]
		
		"""print "fix key:",new_key,"==>"
		for t in TeachersStoixeia.teacherstoixeia.get(new_key):
			
			print t"""
		
		codenum=0
	else: codenum=-1	
	
	return codenum
		
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
	
	"""this function checks if there is a file for teachers information"""
	
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
	
"""testing purpose"""
"""read_files()"""

