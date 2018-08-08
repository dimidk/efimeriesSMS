#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import string
import os
import datetime
import init
import passwd
import sendingSMS
import xlrd
import time
import readStoixeia
from readStoixeia import TeachersStoixeia
import readXlsFile
from readXlsFile import MakeInfoDict



"""result=urllib.urlretrieve(urlsms)"""

"""θέλω ένα γονιό που θα δημιουργεί ένα νέο παιδί μόλις διαβάζει νέο xml αρχείο.
ο κώδικας θα τρέχει ο ίδιος στο παιδί και θα κάνει την ίδια δουλειά. Αλλά όταν ο 
γονιός δει καινούριο xml τότε έχω νέο παιδί
ή θα έχω ένα wait status για το παιδί, αλλά δεν το θέλω γιατί θα έχω τέλος.
ή διαφορετικά θα χρησιμοποιήσω το execvp ώστε να έχω ένα νέο process στο παιδί. 
Δηλαδή με το newpid θα καλείται το exec κι έτσι θα έχω δύο διεργασίες ξεχωριστές.
χρειάζομαι κι ένα συγκεκριμένο τέλος για κάθε αρχείο xls"""



xmlfileExist=False
xmlfile=[]
xlsStoixeiaFile=False
xlsfileStoixeia=[]
xlsfileExist=False
xlsfile=[]
first_run=0
xlsFormat=[]
col=[]
row=[]
exit_code=0

	
def checkBasicFiles(pid):
	
	print "checkBasic Files:",pid
	
	global xmlfile
	global xmlfileExist
	xmlfile,xmlfileExist=init.findFile(init.xmlDir,'xml.prc')
	print "check xml file existance for pid:",pid
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+'check xml file existance for pid:'+str(pid)+'\n')
	
		
	"""xlsStoixeiaFile=False"""
	global xlsfileStoixeia
	global xlsStoixeiaFile
	xlsfileStoixeia,xlsStoixeiaFile=init.findFile(init.stoixeiaDir,'prc')
	print "check stoixeia file existance for pid:",pid
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+'check stoixeia file existance for pid:'+str(pid)+'\n')
				
	"""xlsfileExist=False"""
	global xlsfile
	global xlsfileExist
	xlsfile,xlsfileExist=init.findFile(init.xlsDir,'xls.prc')
	print "check excell file existance for pid:",pid
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+'check excell file existance for pid:'+str(pid)+'\n')


def xmlStructure(pid):
			
	
		
	global xlsFormat
	global col
	global row
	global xlsfileExist
			
	print "xml Structure for pid:",pid
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+'xml Structure for pid:'+str(pid)+'\n')
	
	init.xmlFileName=init.xmlDir+'/'+xmlfile[0]
		
	elements=init.readXml(init.xmlFileName)
		
	init.xlsFileName=init.xlsDir+'/'+init.xlsFileName
		
	if init.xlsFileName.split('/')[2] in xlsfile:
		xlsfileExist=True
		
	xlsFormat=init.formatXls(elements)
	"""print "xls format for pid:",pid,len(xlsFormat)"""
					
	if type(xlsFormat)==tuple:
		col=xlsFormat[0]
		row=xlsFormat[1]

	else:
		col=xlsFormat
	
	


def mainFunction(pid):
	
	print "mainFunction for pid:",pid
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+'mainFunction for pid:'+str(pid)+'\n')
	
	if xlsStoixeiaFile:
		print "create teacher's dictionary for pid ",pid
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+'create teacher''s dictionary for pid:'+str(pid)+'\n')
	
		stoixeiaFile=init.stoixeiaDir+'/'+xlsfileStoixeia[0]
		readStoixeia.read_files()
		
	if not xmlfileExist and not xlsfileExist:
		print "there is nothing new for pid",pid
		exit_code=1
		time.sleep(5)
		return exit_code
					
	if first_run==0:
			
		xmlStructure(pid)
		xmlname_prc=init.xmlFileName+'.prc'
		os.rename(init.xmlFileName,xmlname_prc)
		
		print "in first_run pid:",pid,init.xlsFileName,init.xmlFileName
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+'in first_run pid:'+str(pid)+'\n')

	"""if pid==0:
		
		xmlStructure(pid)
		xmlname_prc=init.xmlFileName+'.prc'
		os.rename(init.xmlFileName,xmlname_prc)
		
		print "in child first_run pid:",pid,init.xlsFileName,init.xmlFileName"""
					
	if (not xmlfileExist and xlsfileExist) or (xmlfileExist and xlsfileExist):
		
		print "in second if in pid:",pid,xmlfileExist,xlsfileExist
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+'checking xml file and xls file for pid:'+str(pid)+'\n')
		
		if init.xlsFileName.split('/')[2] not in xlsfile:
			exit_code=1
			return exit_code
		
		"""print init.xlsFileName"""
		
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':Read xls file:'+ init.xlsFileName+'for pid:'+str(pid)+'\n')
			
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':Make information dictionary for pid:'+str(pid)+'\n')
						
		print "Read excell file for pid:",pid									
		print "Make Information Dictionary for pid:",pid
		readXlsFile.readXlsFile(xlsFormat,col)
		
		xlsfilename_prc=init.xlsFileName+'.prc'
		os.rename(init.xlsFileName,xlsfilename_prc)
		print "rename xls file after processed for pid:",pid
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+'rename xls file after processed for pid:'+str(pid)+'\n')
		time.sleep(2)

		print "Send Sms for pid:",pid
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':Send sms to for pid'+str(pid)+'\n')
		time.sleep(2)
		sendingSMS.sendSMSAll()
						

		
if __name__== '__main__':
	
				
	first_run=0
	child=0
	pid=os.getpid()
	
	print "Start sms application for pid",pid
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':Start application for pid'+str(pid)+'\n')
	
	checkBasicFiles(pid)
	"""print "xml exist,stoixeia exist,xls exist for pid",pid,xmlfileExist,xlsStoixeiaFile,xlsfileExist
	print "xml name,stoixeia name,xls name for pid:",pid,xmlfile,xlsfileStoixeia,xlsfile"""
	print "sleep 2 for pid",pid
	time.sleep(2)
	
			
	mainFunction(pid)
	first_run+=1
	print "sleep 4 after first process for pid",pid	
	time.sleep(4)

	while True:
		
		checkBasicFiles(pid)
		"""print "xml exist,stoixeia exist,xls exist for pid",pid,xmlfileExist,xlsStoixeiaFile,xlsfileExist
		print "xml name,stoixeia name,xls name for pid",pid,xmlfile,xlsfileStoixeia,xlsfile"""
		print "sleep 2 for pid",pid
		time.sleep(2)
		
		if not xmlfileExist:
			
			"""print "no new xml file for pid",pid"""
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':there is no new xml file for pid'+str(pid)+'\n')
				
			exit_code=mainFunction(pid)
			if exit_code==1:
				"""print "there is no new xls file for pid",pid"""
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+':there is no new xls file for pid'+str(pid)+'\n')
				print "sleep 2 for pid",pid
				time.sleep(2)
				
			print "sleep 8 after process for pid",pid	
			time.sleep(8)
			
		else:
			child+=1
			
			temp_a=False
			temp_filename,temp_a=init.findFile(init.stoixeiaDir,'xls')
			
			temp_filename1=init.stoixeiaDir+'/'+temp_filename[0]
			
			readStoixeia.mvFileToFirstName(temp_filename1)
			
			newpid=os.fork()
			if newpid==0:
				
				print "new child process pid\n"
				now=init.get_datetime()
				init.fp_log.write(now[0]+' '+now[1]+':new process for pid'+str(newpid)+'\n')
				os.execlp('./bulkSMS.py','')							
			
			else:
				print "father process pid",pid
				print "sleep for 10 pid",pid
				time.sleep(10)
			
	
	init.fp_log.close()
	
	
