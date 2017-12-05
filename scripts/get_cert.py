import sys

def usage():
	print ("Getting the cert")
	print ("python3 get_cert.py <file name> <number>")
	exit(1)

def main():
	if len(sys.argv) != 3:
		usage()

	fn = sys.argv[1]
	f = open(fn, "r")
	num = int(sys.argv[2])
	n = 0
	ofn = '-'.join(fn.split("-")[0:3]) + ("-%s.crt" % num)
	of = open(ofn, "w")

	head = "-----BEGIN CERTIFICATE-----\n"
	tail = "\n-----END CERTIFICATE-----\n"

	for line in	f:
		n = n + 1
		if n == num:
			tmp = line.strip().split(",")
			v = tmp[1].strip()
			pem = head + v + tail
			print ("pem: ", pem)
			of.write(pem)
	
	f.close()
	of.close()

if __name__ == "__main__":
	main()
