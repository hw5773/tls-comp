import os
import subprocess

valid = []

def usage():
    print ("Determine whether valid or not")
    print ("python3 cn_san.py")
    exit()

def main():
    num = 0
    for root, dirs, files in os.walk("/home/hwlee/tls_comp/certs"):
        for f in files:
            num = num + 1
            dom = '.'.join(f.split(".")[0].split("_")[0:-1])
            dom1 = "www." + dom
            dom2 = "*." + dom
            crt = os.path.join(root, f)
            print ("%d) Domain: " % num, dom)

            cmd1 = "openssl x509 -in %s -noout -subject" % crt
            ret1 = os.popen(cmd1).read()
            cn = ret1.strip().split("CN=")[-1].split("/")[0]
            print ("  CN: ", cn)

            cmd2 = "openssl x509 -in %s -noout -text | grep DNS:" % crt
            ret2 = os.popen(cmd2).read()
            san = ret2.split(",")

            for i in range(len(san)):
                san[i] = san[i].split("DNS:")[-1].strip()

            print ("  SAN: ", san)

            if (dom1 in cn) or (dom2 in cn):
                print ("  valid!")
                print ("")
                continue

            for e in san:
                if (dom1 in e) or (dom2 in e):
                    print ("  valid!")
                    print ("")
                    continue

            print ("  invalid!")
            os.remove(crt)
            print ("")

if __name__ == "__main__":
    main()
