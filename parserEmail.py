#!/usr/bin/python
# -*-coding:utf-8-*-

import imaplib
import email
import email.header
import time
import sys
import init
import subprocess
import passwd


GREETINGS=['Εφημερίες','εφημερίες','Εφημεριες','εφημεριες']
epal='[Λίστα ΕΠΑΛ] '
greetingsList=[epal+s for s in GREETINGS]

server='imap.gmail.com'
port=993
org_email='@gmail.com'
username=passwd.username+org_email
password=passwd.password


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
		
			if subject in greetingsList:
				print "There is in ",subject," new message"
				"""print "Working ",msg_id," ",subject"""
				
				for part in msg.walk():
					
					ctype=part.get_content_type()
					
					if ctype in ['image/jpeg','image/png','image/jpg']:
						filename=part.get_filename()
						open(part.get_filename(), 'wb').write(part.get_payload(decode=True))
						
						
					else:
						"""get the attachment data"""
						filedata=part.get_payload(decode=True)

						if part.get_filename()==None:
							continue
						"""open(part.get_filename(), 'w').write(part.get_payload(decode=True))"""
						
						"""find the name of the attachment"""
						fp=email.header.decode_header(part.get_filename())
						
						"""decode to greek if  name is in greek characters"""
						print fp[0][0].decode(encoding='utf-8')
						
						if fp[0][0].decode(encoding='utf-8')==init.xlsFileName:
												
							open(fp[0][0].decode(encoding='utf-8'), 'w').write(filedata)
							
							if subprocess.call(init.cp_cmd.split()) == 0:
								print "Ok! file moved to directory efimeries"
							else:
								print "erron in copying file"
						else:
							print "Error in filename"							
								

			else:
				continue
			
		
	
			
	print "close imap connection"	
	imapClient.close()
	imapClient.logout()
	
	
