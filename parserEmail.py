#!/usr/bin/python
# -*-coding:utf-8-*-

import imaplib
import email
import email.header
import time
import sys
import codecs

"""GREETINGS="Εφημερίες"""
GREETINGS=['Εφημερίες','εφημερίες','Εφημεριες','εφημεριες']

server='imap.gmail.com'
port=993
org_email='@gmail.com'
username="dimi.epalefimeries"+org_email
password="epalEfimeries"

while True:
	
	print "starting"
	imapClient=imaplib.IMAP4_SSL(server)
	imapClient.login(username,password)
	imapClient.select("INBOX")
	

	folderStatus, UnseenInfo = imapClient.status('INBOX', "(UNSEEN)")
	print folderStatus," and ", UnseenInfo
	
	if '0' in UnseenInfo[0]:
		print "go to sleep for a minute"
			
		time.sleep(60)
		
	else:
		print "there is a new message"
		x,message_ids=imapClient.search(None,"UNSEEN")
		for msg_id in message_ids[0].split():
		
			_, data=imapClient.fetch(msg_id,"(RFC822)")
		
			msg=email.message_from_string(data[0][1])
			decode = email.header.decode_header(msg['Subject'])[0]
			
			"""parser = email.parser.HeaderParser()
			headers = parser.parsestr(msg.as_string())
			
			for h in headers.items():
				print "header ",h
			don't need the above  but keep just in case.
			
			decode=decode[0].decode(encoding='UTF-8')
			εκτυπώνει το θέμα του μηνύματος"""
			subject = decode[0]
		
			if subject in GREETINGS:
				print "There is in ",GREETINGS," new message"
				"""print "Working ",msg_id," ",subject"""
				
				"""i=0"""
				for part in msg.walk():
					
					"""print "in loop ",i"""
					ctype=part.get_content_type()
					"""print ctype"""
					
					if ctype in ['image/jpeg','image/png','image/jpg']:
						open(part.get_filename(), 'wb').write(part.get_payload(decode=True))
					
						
					else:
						"""get the attachment data"""
						filedata=part.get_payload(decode=True)

						if part.get_filename()==None:
							continue
						"""open(part.get_filename(), 'w').write(part.get_payload(decode=True))"""
						
						"""find the name of the attachment"""
						fp=email.header.decode_header(part.get_filename())
						
						"""decode to greek if the name is in greek characters"""
						print fp[0][0].decode(encoding='utf-8')
						"""open(part.get_filename(), 'w').write(filedata)"""
												
						open(fp[0][0].decode(encoding='utf-8'), 'w').write(filedata)
			
					"""i+=1"""
			else:
				continue
			
			mail_subject=msg['subject']
			mail_sender=msg['From']
		
	
			
	print "close imap connection"	
	imapClient.close()
	imapClient.logout()
	
	
