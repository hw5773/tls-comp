import OpenSSL.crypto
import sys
import os
import encodings
import pkgutil
import asn1
import smtplib

sender = "hwlee2014@mmlab.snu.ac.kr"
receivers = ["hwlee2014@mmlab.snu.ac.kr"]

def usage():
	print ("Get SAN list")
	print ("python3 count_sans.py <output prefix>")
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

def count_san(v):
	ret = 0
	n = len(v)

	for i in range(n):
		if v[i] == 0x82:
			ret = ret + 1

	return ret

def main():
	if len(sys.argv) != 2:
		usage()

	c = OpenSSL.crypto
	cert_files = []
	prefix = sys.argv[1]

	for root, dirs, files in os.walk("./"):
		for f in files:
			if f.startswith("201") and f.endswith("_certs"):
				cert_files.append(f)

	print (cert_files)

	head = "-----BEGIN CERTIFICATE-----\n"
	tail = "\n-----END CERTIFICATE-----\n"
	decoder = asn1.Decoder()
	nf = 0

	for fn in cert_files:
		nf = nf + 1
		print ("----- Start Analysis for ", fn, " -----")
		f = open(fn, "r")
		ofn = prefix + "_" + fn + ".out"
		of = open(ofn, "w")
		s = "num, domain, size (PEM), size (DER), key, # of san, san bytes, rate (PEM), rate (DER)\n"
		print (s)
		of.write(s)
		num = 0

		for line in f:
			num = num + 1
			tmp = line.strip().split(",")
			h = tmp[0].strip()
			v = tmp[1].strip()
			pem = head + v + tail

			try:
				cert = c.load_certificate(c.FILETYPE_PEM, pem)
			except:
				s = "error\n"
				of.write(s)
				continue

			der = c.dump_certificate(c.FILETYPE_ASN1, cert)
			cnt = cert.get_extension_count()
			for i in range(cnt):
				if cert.get_extension(i).get_short_name().decode("ascii") == "subjectAltName":
					decoder.start(cert.get_extension(i).get_data())
					try:
						tag, value = decoder.read()
						s = "%d, %s, %d, %d, %d, %d, %d, %f, %f\n" % (num, cert.get_subject().CN, len(pem), len(der), cert.get_pubkey().bits(), count_san(value), len(value), round(len(value)/len(pem), 2), round(len(value)/len(der), 2))
					except:
						continue
					try:
						print(s)
						of.write(s)
					except:
						print("error encoding")
						of.write("error encoding\n")
					break	
		of.close()
		title = "count san in %s succeed" % fn
		msg = "%d out of %d succeed" % (nf, len(cert_files))
		send_email(title, msg)

if __name__ == "__main__":
	main()
