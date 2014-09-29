#!/usr/bin/python

# coding: utf-8

from smtplib import SMTP
from email.MIMEText import MIMEText
from optparse import OptionParser

parser=OptionParser(usage="%prog [options] title email-message", version="%prog 1.0")
parser.add_option("-u",
                  "--user",
                  dest="user_name",
                  help="SMTP username", 
                  metavar="username")

parser.add_option("-p",
                  "--password",
                  dest="user_passwd",
                  help="SMTP password", 
                  metavar="password")
parser.add_option("-s",
                  "--server",
                  dest="server",
                  help="SMTP server", 
                  metavar="server")

#parser.add_option("-f",
#                  "--from",
#                  dest="me",
#                  help="Source address", 
#                  metavar="EMAIL")

parser.add_option("-t",
                  "--to",
                  dest="you",
                  help="Destination address", 
                  metavar="EMAIL")
                  
(options, args) = parser.parse_args()
                  
                
#me = options.me
me = options.user_name
you = options.you
text = args[1]
subj = args[0]

# SMTP-server
server = options.server
user_name = options.user_name
user_passwd = options.user_passwd

msg = MIMEText(text, "", "utf-8")
msg['Subject'] = subj
msg['From'] = me
msg['To'] = you


s = SMTP(server)
s.ehlo()
s.starttls()
s.ehlo()
s.login(user_name, user_passwd)
s.sendmail(me, you, msg.as_string())
s.quit()

