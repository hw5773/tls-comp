import os
import sys

def usage():
    print ("Remove the first comma")
    print ("python3 mining.py")
    exit(1)

def main():
    if len(sys.argv) != 1:
        usage()

    out_files = []

    for root, dirs, files in os.walk("./"):
        for f in files:
            if ".out" in f:
                out_files.append(f)

    for fn in out_files:
        f = open(fn, "r")
        ofn = fn.replace(".out", ".csv")
        of = open(ofn, "w")

        for line in f:
            tmp = line.split(",")
            while (len(tmp) > 15):
                line = line.replace(",", "_", 1)
                tmp = line.split(",")

            of.write(line)

        of.close()

if __name__ == "__main__":
    main()
