import OpenSSL.crypto
import sys
import time
from datetime import date

def usage():
	print ("Test reading the certificate")
	print ("python3 read_cert.py <input file>")
	exit(1)

def display_cert(line):
	h = line.strip().split(",")[0].strip()
	v = line.strip().split(",")[1].strip()
	c = OpenSSL.crypto
	head = "-----BEGIN CERTIFICATE-----\n"
	tail = "\n-----END CERTIFICATE-----\n"
	data = head + v + tail
	cert = c.load_certificate(c.FILETYPE_PEM, data)
	der = c.dump_certificate(c.FILETYPE_ASN1, cert)

	print ("====================")
	print ("Common Name: ", cert.get_subject().CN)
	print ("Issuer: ", cert.get_issuer().CN)
	print ("Size (PEM): ", len(data))
	print ("Size (DER): ", len(der))
	print ("====================")
	print ("")

def main():
	if len(sys.argv) != 2:
		usage()

	f = open(sys.argv[1], "r")

	for line in f:
		display_cert(line)

if __name__ == "__main__":
	main()
