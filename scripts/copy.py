import os

def usage():
    print ("Copy the certificate if the size of the file is not zero.")
    print ("python3 copy.py")
    exit()

def main():
    num = 0
    for root, dirs, files in os.walk("/home/hwlee/study/cert/certs_kor_20170123"):
        for f in files:
            fname = os.path.join(root, f)
            print ("Certificate: %s" % fname)
            statinfo = os.stat(fname)
            if statinfo.st_size == 0:
                print ("Not the target")
                continue
            cmd = "cp %s /home/hwlee/tls_comp/certs" % fname
            os.system(cmd)
            print ("Copy Complete")
            num = num + 1

    print ("Total: %s" % num)

if __name__ == "__main__":
    main()
