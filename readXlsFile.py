#!/usr/bin/python
#-*-coding:utf-8 -*-

import os
import sys
import xlrd
import datetime
import init
import passwd


class MakeInfoDict():
	
	infoDict=dict()
	
	def emptyDict(self):
		MakeInfoDict.infoDict.clear()
		
	
	"""na do mipos na valo parametro tin kathe stili.pos na to ftiakso an den ksero ton arithmo stilo kai to matho"""
		
	def __init__(self,surname,listElement='',tup=''):
		
		self.surname=str(surname)
		
		self.tup=tup
		self.listElement=listElement
		
		if tup=='':
			
			if self.surname not in MakeInfoDict.infoDict:
				MakeInfoDict.infoDict[self.surname]=[self.listElement]
			else:
				MakeInfoDict.infoDict[self.surname].append(self.listElement)
		else:
				
			if self.surname not in MakeInfoDict.infoDict:
				MakeInfoDict.infoDict[self.surname]=[self.tup]
			else:
				MakeInfoDict.infoDict[self.surname].append(self.tup)


def startRow(line,col):
	i=0
	start_col=0
	for info in line:

		if info=='':
			start_col+=1
			continue
		col.pop(i)
		col.insert(i,info)
		i+=1
		
	return start_col


"""read xls from first data row line, and first col data line"""
def readSpecificXls(start_row,nrows,start_col,sheet,col):
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read excell row \n')
	
	for i in range(start_row+1,nrows):
		
		"""Τελικά η μοναδική λύση στο encoding"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		line=sheet.row_values(i)
		if i==28 or "" in line: 
			break
				
		k=start_col
		if start_col>0:
			
			for j in range(sheet.ncols-start_col):
				rowdata=[t for t in line if line.index(t)<start_col]
				rowdata.append(col[j])
				"""parenthesis creates a generator, so it must explicitly declared"""
				tup=tuple(t for t in rowdata)
				
				teachername=line[k].strip().upper()
				teachername=init.replaceTono(teachername)
				k+=1
				if teachername.find(' ')!=-1:
					allname=teachername.split()
					teachername=allname[0]+' '+allname[1][0]
							
				s=MakeInfoDict(teachername,tup)
				
		else:				
		
			for j in range(sheet.ncols-start_col):
						
				teachername=line[k].strip().upper()
				teachername=init.replaceTono(teachername)
				"""print teachername"""
				k+=1
				if teachername.find(' ')!=-1:
					allname=teachername.split()
					teachername=allname[0]+' '+allname[1][0]
				
				s=MakeInfoDict(teachername,col[j])
				


def readXlsFile(xlsFormat,col):
		

	try:
		fp=xlrd.open_workbook(init.xlsFileName,encoding_override="cp1252")
	except:
		print "open file error"
		
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read excell file '+ init.xlsFileName+ 'and create info dictionary\n')
	
	if len(MakeInfoDict.infoDict)>0:
		MakeInfoDict.infoDict.clear()
		
	print init.xlsFileName
	sheet=fp.sheet_by_index(0)
	"""print "row and columns in excell:",sheet.nrows,sheet.ncols"""
	
	"""start line in xls file"""
	for i in range(sheet.nrows):

		line=sheet.row_values(i)
		if col[i] not in line:
			continue
		start_row=i
		break
		
	"""start row in xls file, if start_col=0 then there is no row format"""
	start_col=startRow(line,col)
	
	
	readSpecificXls(start_row,sheet.nrows,start_col,sheet,col)
	
	
	"""print "len dict ", len(MakeInfoDict.infoDict)
	for key,value in MakeInfoDict.infoDict.items():
		if type(value)==list and len(value)>1:
			for value1 in value:
				for val in value1:
					print key,val

		else:
			for val in value:
				print key,val"""
				


				
		
	
"""readXlsFile(xlsFormat)"""
