import sys
import os
import smtplib

# insert the sender email address
sender = "hwlee2014@mmlab.snu.ac.kr"
# insert the receivers email address
receivers = ["hwlee2014@mmlab.snu.ac.kr"]

def usage():
	# input the usage of this script
	print "Analyze the Dataset"
	# input the command to execute this script
	print "python3 analysis.py <prefix>"
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

def analysis(csv, of1, of2):
	d = '-'.join(csv.split("_")[3].split("-")[0:3])
	f = open(csv, "r")
	f.readline()

	val = {}
	for i in range(12):
		val[i] = 0

	num = 0
	for line in f:
		num = num + 1
		tmp = line.strip().split(",")

#TODO: add count the number of minimums

		for j in range(12):
			v = int(tmp[j+3].strip())
			val[j] = val[j] + v

	s = "%s, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % (d, val[0]/num, val[1]/val[0], val[2]/val[0], val[3]/val[0], val[4]/val[0], val[5]/val[0], val[6]/num, val[7]/val[6], val[8]/val[6], val[9]/val[6], val[10]/val[6], val[11]/val[6])
	of1.write(s)


def main():
	# check the number of arguments. change the number in the below statement according to the design.
	if len(sys.argv) != 2:
		usage()

	prefix = sys.argv[1]

	of1 = "%s_comp.csv" % prefix
	of2 = "%s_min.csv" % prefix

	of1.write("Date, Size (PEM), deflate (PEM), brotli (PEM), bz2 (PEM), lzma (PEM), lzw (PEM), Size (DER), deflate (DER), brotli (DER), bz2 (DER), lzma (DER), lzw (DER)\n")
	of2.write("Date, deflate (PEM), brotli (PEM), bz2 (PEM), lzma (PEM), lzw (PEM), defalte (DER), brotli (DER), bz2 (DER), lzma (DER), lzw (DER)\n")

	csv_files = []

	for root, dirs, files in os.walk("./"):
		for f in files:
			if "result_" in f and ".csv" in f:
				csv_files.append(f)
	
	for csv in csv_files:
		analysis(csv, of1, of2)

	of1.close()
	of2.close()

	# insert the title and the message you want.
	title = ""
	msg = ""

	# send the email to the receivers from sender.
	send_email(title, msg)	

if __name__ == "__main__":
	main()
