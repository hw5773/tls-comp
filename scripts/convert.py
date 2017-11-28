import sys
import os

def usage():
    print ("Convert PEM to DER")
    print ("python3 convert.py <input directory> <output directory>")
    exit()

def main():
    if len(sys.argv) != 3:
        usage()

    ind = sys.argv[1]
    outd = sys.argv[2]

    for root, dirs, files in os.walk(ind):
        for f in files:
            fname = os.path.join(root, f)
            gname = os.path.join(outd, f)
            cmd = "openssl x509 -in %s -out %s -outform DER" % (fname, gname)
            os.system(cmd)

if __name__ == "__main__":
    main()
