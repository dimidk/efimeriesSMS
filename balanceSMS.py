#!/usr/bin/python
#-*-coding: utf-8 -*-

import os
from urllib import urlopen
import passwd
import xml.etree.ElementTree as xml
import smtplib
from email.mime.text import MIMEText
import email.header
import datetime



server_host='smtp.gmail.com'
port=465
org_email='@gmail.com'
username=passwd.username+org_email
password=passwd.password
targets=passwd.targets
sender=username


bodytext="Το υπόλοιο των μηνυμάτων είναι: "


def balanceAndXml(url):
	
	print "Get HTTP Request Balance"
	
	response=urlopen(url)
	html=response.read()
	print "OK, request success:",response.getcode()
	response.close()

	tree=xml.fromstring(html)
	"""print tree.tag"""
	for c in tree:
		if c.tag=='balance':
			balance=c.text
			print c.tag, "==>",c.text

	return balance


def sendEMail(msg):
	
	print "prepare sending email"
	server=smtplib.SMTP_SSL(server_host,port)
	server.login(username,password)
	server.sendmail(sender,targets,msg.as_string())
	print "email sent "
	server.quit()
	
type_xml='&type=xml'

urlbal_sender=passwd.urlbalance+type_xml


print "Start process for checking balance"

		
balance=balanceAndXml(urlbal_sender)
Bodytext=bodytext+balance+"\n"

msg=MIMEText(Bodytext)
msg['Subject']='SMS Balance'
msg['From']=sender
msg['To']=', '.join(targets)

print "create file\n"

"""curDir=os.getcwd()"""
curDir=passwd.icurDir+"/sms_balance.txt"

fp=open(curDir,"w")

fp.write(Bodytext)
fp.close()

print "exit process\n"


"""sendEMail(msg)"""


	
			
		
