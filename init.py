#!/usr/bin/python
#-*- coding: utf-8 -*-

import codecs
import os
import datetime
import passwd
import xml.etree.ElementTree as xml
import string


toSend=''
fromSender="epalMoiron"
text="Αγαπητέ συνάδελφε "
text1=''
teacherName=''
numberOfAbsences=''


log_file="log_sms.txt"
stoixeiaDir="./stoixeia"
xlsDir="./efimeries"
xmlDir="./xml"
xmlFileName=''
xlsFileName=""
fp_log=codecs.open(log_file,'a+')




letterTono=['Ά','Έ','Ή','Ί','Ό','Ύ','Ώ','Ϊ','Ϋ']
letterWithoutTono=['Α','Ε','Η','Ι','Ο','Υ','Ω','Ϊ','Ϋ']

def replaceTono(name):
	

	for n in name:
		
		if n not in letterTono:
			continue
		else:
			break
		

	indexTono=letterTono.index(n)
	nn=letterWithoutTono[indexTono]
	"""nn=nn.decode('utf-8')"""
	name=name.replace(n,nn)
	
	return name.rstrip()



def readXml(xmlname):
	
	global xlsFileName
	global text1
	
	tree=xml.parse(xmlname)
	root=tree.getroot()
	text1=root.tag

	element_names=[elem.tag for elem in root.iter() if not elem==root]
	elements=[child.tag for child in root]
	xlsFileName=root[0].text
	
	elements.remove('name')
	subelements=[elem for elem in element_names if elem not in elements]


	i=0
	for child in root:
		if child.tag=='name':
			continue
			
		elements[i]=dict()
		for subchild in child:
			elements[i][subchild.tag]=subchild.text
		i+=1
	
	return elements


	
def formatXls(elements):
	
	if len(elements)>=2:
		
		"""temporary 'cause could be more than 2 columns or rows"""
		
		col=[value for value in elements[0].values()]
		row=[value for value in elements[1].values()]
			
		return col,row
	else:
		col=[value for value in elements[0].values()]
		
		"""print col"""
		
		return col


def findFile(filesDir,tag):
	
	flag=0
	a=False

	for root,dirs,filenames in os.walk(filesDir,topdown=True):
		"""listall=[name for name in filenames if name.find('xls.prc')!=-1]"""
		listall=[name for name in filenames if name.find(tag)!=-1]
		sublist=[name for name in filenames if name not in listall]
	
	if len(sublist)>0:
		a=True
		
	return sublist,a
	
	
	
def get_datetime():
	
	now=str(datetime.datetime.now())
	now_date=now.split(' ')[0]
	now_time=now.split(' ')[1].split('.')[0]
	
	return now_date,now_time
	






	
