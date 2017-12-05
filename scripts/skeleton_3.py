import sys
import os
import smtplib

# insert the sender email address
sender = "hwlee2014@mmlab.snu.ac.kr"
# insert the receivers email address
receivers = ["hwlee2014@mmlab.snu.ac.kr"]

def usage():
	# input the usage of this script
	print "This script is the skeleton for python3"
	# input the command to execute this script
	print "python3 <script name> <arg1> <arg2"
	exit(1)

def send_email(title, msg):
	message = """From: Hyunwoo Lee <hwlee2014@mmlab.snu.ac.kr>
To: Hyunwoo Lee <hwlee2014@mmlab.snu.ac.kr>
Subject: %s

The experiment is on going:
%s
""" % (title, msg)

	try:
		smtpObj = smtplib.SMTP(host="old-mmlab.snu.ac.kr")
		smtpObj.sendmail(sender, receivers, message)
		print ("Successfully sent email")
	except SMTPException:
		print ("Error: unable to send email")

def main():
	# check the number of arguments. change the number in the below statement according to the design.
	if len(sys.argv) != 1:
		usage()

	# insert the title and the message you want.
	title = ""
	msg = ""

	# send the email to the receivers from sender.
	send_email(title, msg)	

if __name__ == "__main__":
	main()
