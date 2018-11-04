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



toNumbers=['6938802532','6944756730','6976081302','6972944810','6978175044','6977030080','6932333484','6908989307']
def sendSMS(i,to,fromSender,name,text,text1,absences):
	
	"""to='6938802532'"""
	to=toNumbers[i]
	urlsms_sender=passwd.urlsms+'&to='+to+'&from='+fromSender
	
	"""urlsms_sender=urlsms_sender+'&text='+str(text)+str(name)+' '+str(text1)"""
	
	type_xml='&type=xml'
	sms_text=str(text)+str(name)+' '+str(text1) + str(absences)
	"""print "\nsms text ",sms_text"""
	sms_alltext=sms_text

	if '&' in sms_text:
		sms_text=sms_text.replace('&','%26')
	
	urlsms_sender_text=urlsms_sender +'&text='+str(sms_text)+type_xml
	print "sms url",urlsms_sender_text
		
	try:
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':send SMS for teacher ' + name+'\n')
			
		print "send sms to ",to
			
		"""if i<1:"""
		result=urllib.urlretrieve(urlsms_sender_text)
							
	except:

		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':SMS for teacher ' + name+' not send successfull\n')
			
		print "SMS for teacher ",name,"not send successfull\n"


def sendSMSAll():
	
	tmp=0
	
	now=init.get_datetime()
	init.fp_log.write(now[0]+' '+now[1]+':start sms sending \n')
	
	for key,value in TeachersStoixeia.teacherstoixeia.items():
		print "teacher name:",key
		tstoixeia=TeachersStoixeia.teacherstoixeia.get(key)
		
		now=init.get_datetime()
		init.fp_log.write(now[0]+' '+now[1]+':get name and phone number for:'+key+' \n')
		
		init.toSend=tstoixeia[2]
		init.teacherName=key+' '+tstoixeia[1]
		
		"""searchkey=key+' '+tstoixeia[1].decode('utf-8')[0]"""
		
		if MakeInfoDict.infoDict.has_key(key):
			
			infostoixeia=MakeInfoDict.infoDict.get(key)
								
			now=init.get_datetime()
			init.fp_log.write(now[0]+' '+now[1]+':get information for name\n')
		
			efimeries=' '
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
			
			if tmp>=7:
				tmp=0
			else: tmp+=1
