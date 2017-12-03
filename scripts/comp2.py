import sys
import os
import brotli
import zlib
import lzw

sender = "hwlee2014@mmlab.snu.ac.kr"
receivers = ["hwlee2014@mmlab.snu.ac.kr"]

def usage():
    print "Compress certificates"
    print "python2 comp.py <input directory> <output file>"
    exit()

def main():
    if len(sys.argv) != 3:
        usage()

    d = sys.argv[1]
    of = open(sys.argv[2], "w")
    of.write("domain, size, zlib, zlib ratio, brotli, brotli ratio, lzw, lzw ratio\n")
    max_size = -1
    min_size = 1000000
    num = 0

    for root, dirs, files in os.walk(d):
        for f in files:
            num = num + 1
            dom = '.'.join(f.split(".")[0].split("_")[0:-1])
            fname = os.path.join(root, f)
            statinfo = os.stat(fname)
            size = statinfo.st_size
            crt = open(fname, "rb").read()
            a = zlib.compress(crt)
            b = brotli.compress(crt)
            c = lzw.compress(crt)
            lzw.writebytes("test.out", c)
            lzw_size = os.stat("test.out").st_size
            cmd = "rm test.out"
            os.system(cmd)
            s = "%s, %d, %d, %f, %d, %f, %d, %f\n" % (dom, size, len(a), round(len(a)/size, 2), len(b), round(len(b)/size, 2), lzw_size, round(lzw_size/size, 2))
            print (num, ") ", s)
            of.write(s)

    of.close()

if __name__ == "__main__":
    main()
