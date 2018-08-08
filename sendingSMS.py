#!/usr/bin/python
#-*- coding: utf-8-*-


import urllib
import datetime
import init
import passwd
import time
import readStoixeia
import readXlsFile
from readStoixeia import TeachersStoixeia
from readXlsFile import MakeInfoDict




def sendSMS(i,to,fromSender,name,text,text1,absences):
	
	to='6938802532'
	urlsms_sender=passwd.urlsms+'&to='+to	
	urlsms_sender=urlsms_sender+'&from='+fromSender+'&text='+str(text)+str(name)+" "+str(text1)+str(absences)+"&type=xml"
	print "sms url",urlsms_sender
	
	try:
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':send SMS for teacher ' + name+'\n')
		
		print "send sms to ",to
		
		"""if i<1:		
			result=urllib.urlretrieve(urlsms_sender)"""
					
	except:

		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':SMS for teacher ' + name+' not send successfull\n')
		
		print "SMS for teacher ",name,"not send successfull\n"
		


def sendSMSAll():
	
	tmp=0
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':start sms sending \n')
	
	for key,value in TeachersStoixeia.teacherstoixeia.items():
		tstoixeia=TeachersStoixeia.teacherstoixeia.get(key)
		
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':get name and phone number for:'+key+' \n')
		
		init.toSend=tstoixeia[2]
		init.teacherName=key+' '+tstoixeia[1]
		"""print "teacher full name:",init.teacherName
		print "teacher full name:",tstoixeia[1].decode('utf-8')[0]"""
		
		searchkey=key+' '+tstoixeia[1].decode('utf-8')[0]
		"""print "key:",key, "==>searchkey",searchkey"""
		
		if MakeInfoDict.infoDict.has_key(key):
			
			infostoixeia=MakeInfoDict.infoDict.get(key)
								
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':get information for name\n')
		
			efimeries=''
			for infokey in infostoixeia:

				if type(infokey)==tuple:
					for val in infokey:
						efimeries=efimeries+' '+val

					efimeries=efimeries+','				
				else:
					efimeries=efimeries+' '+infokey
					
					
			init.numberOfAbsences=str(efimeries)
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':which information is'+init.numberOfAbsences+'\n')
			
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':call sms function \n')	
			
			sendSMS(tmp,init.toSend,init.fromSender,init.teacherName,init.text,init.text1,init.numberOfAbsences)
			
			tmp+=1