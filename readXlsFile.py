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
		
	def __init__(self,surname,specialty,listElement='',tup=''):
		
		self.surname=str(surname)
		self.specialty=str(specialty)
		
		self.tup=tup
		self.listElement=listElement
		
		if tup=='':
			
			if (self.surname,self.specialty) not in MakeInfoDict.infoDict:
				MakeInfoDict.infoDict[(self.surname,self.specialty)]=[self.listElement]
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+' first time teacher found '+surname+' '+specialty)
				init.fp_log.write('\n'.join(x for x in listElement))
			else:
				MakeInfoDict.infoDict[(self.surname,self.specialty)].append(self.listElement)
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+' more than one time teacher found '+surname+' '+specialty)
				init.fp_log.write('\n'.join(x for x in listElement))
		else:
			
			if (self.surname,self.specialty) not in MakeInfoDict.infoDict:
				MakeInfoDict.infoDict[(self.surname,self.specialty)]=[self.tup]
			else:
				MakeInfoDict.infoDict[(self.surname,self.specialty)].append(self.tup)
			


def startRow(line,col):
	i=0
	start_col=0

	for info in line:

		x=info		
		if x in col:
			
			index=col.index(x)
			temp=col[i]
			col.pop(i)
			col.insert(i,x)
			col.pop(index)
			col.insert(index,temp)
			i+=1
			
			
		else:
			
			start_col+=1
	
	"""for c in col:
		print "col:",c"""
	return start_col


"""read xls from first data row line, and first col data line"""
def readSpecificXls(index,start_row,nrows,ncols,start_col,sheet,col,row=''):
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Read excell row \n')

	for i in range(start_row+1,nrows):
		
		"""Τελικά η μοναδική λύση στο encoding"""
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		line=sheet.row_values(i)
		
		""" αν βρει στοιχείο το row τότε συνεχίζει αλλιώς σταματά"""
		if index==0:
			if line.count("")==ncols:
				continue
			else:
				pass
				
		k=start_col
		if start_col>0:
			"""here the file has data in row and in col"""
			
			for j in range(sheet.ncols-start_col):
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+' '+line[k]+'\n')
				if line[k]=="":
					continue
				
				rowdata=[t for t in line if line.index(t)<start_col]

				rowdata.append(col[j])
				"""parenthesis creates a generator, so it must explicitly declared"""
				tup=tuple(t for t in rowdata)
				
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1])
				init.fp_log.write('\n'.join(x for x in tup))
				teachername=line[k].decode('utf-8').strip().upper()
				init.fp_log.write('\n'+now[0]+' '+now[1]+' '+teachername)
				"""print "first time read teachername",teachername"""
				tonoExist=init.checkInTono(teachername)
				if tonoExist:
					"""print "teacherName:",teachername"""
					teachername=init.replaceTono(teachername)
					"""print "teachername after tono:",teachername"""
					init.fp_log.write('\n'+now[0]+' '+now[1]+'teachername after tono '+teachername)
				
				
				k+=1
				if teachername.find(' ')!=-1:
					allname=teachername.split()
					teachername=allname[0].strip()
					"""print "teachername after split",teachername," ", len(teachername)"""
					init.fp_log.write('\n'+now[0]+' '+now[1]+' teachername after split '+ teachername)
					specialty=allname[1].strip()
					init.fp_log.write('\n'+now[0]+' '+now[1]+' specialty after split '+specialty)
					"""print "specialty teacher ",specialty," ", len(specialty)"""
							
				s=MakeInfoDict(teachername,specialty,tup)
				
				
		else:				
		
			for j in range(sheet.ncols-start_col):
				
				if line[k]=="":
					continue
					
				teachername=line[k].strip().upper()
				teachername=init.replaceTono(teachername)
				teachername=teachername.decode('utf-8')
				"""print teachername"""
				k+=1
				if teachername.find(' ')!=-1:
					allname=teachername.split()
					teachername=allname[0].strip()
					specialty=allname[1].strip()
					
				
				s=MakeInfoDict(teachername,specialty,col[j])
				


def readXlsFile(xlsFormat,col,row):
		

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
	print "row and columns in excell:",sheet.nrows,sheet.ncols
	
	"""start line in xls file"""
	for i in range(sheet.nrows):
		
		line=sheet.row_values(i)
		if col[i] not in line:
			continue
		start_row=i
		
		break
		
	"""start row in xls file, if start_col=0 then there is no row format"""
	start_col=startRow(line,col)
	
	print "start reading excell from row:",start_row, " and from column:",start_col
	
	"here is the problem. To stop when the file efimeries file ends"
	
	if type(xlsFormat)==tuple:
		"""print "process excell with row"""
		
		index=1
		readSpecificXls(index,start_row,sheet.nrows,sheet.ncols,start_col,sheet,col,row)
	else:
		"""print "process file with no row"""
		index=0
		readSpecificXls(index,start_row,sheet.nrows,sheet.ncols,start_col,sheet,col)
		
	"""for key,value in MakeInfoDict.infoDict.items():
		print key,"==>"
		for val in value:
			for t in val:
				print t"""
	
	
	
