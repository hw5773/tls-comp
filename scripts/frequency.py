import sys

def usage():
	print ("Count the number of alternative names and key size for each certificate")
	print ("python3 frequency.py <input> <output>")
	exit(1)

def main():
	if len(sys.argv) != 3:
		usage()

	fn = sys.argv[1]
	f = open(fn, "r")
	ofn = '-'.join(fn.split("-")[0:3]) + ("-freq.out")
	of = open(ofn, "w")

	head = "-----BEGIN CERTIFICATE-----\n"
	tail = "\n-----END CERTIFICATE-----\n"

	for line in f:
		

	f.close()
	of.close()

if __name__ == "__main__":
	main()
