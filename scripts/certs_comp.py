import sys
import os
import smtplib
import brotli
import bz2
import lzma
import zlib
import OpenSSL.crypto
import binascii

sender = "hwlee2014@mmlab.snu.ac.kr"
receivers = ["hwlee2014@mmlab.snu.ac.kr"]

def usage():
    print ("Compress certificates")
    print ("python3 comp.py <output prefix>")
    exit()

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

def make_output(result):
    ret = ""

    ret = "# of domains: %d\n" % result[0]
    ret = ret + "===== PEM Results =====\n"
    ret = ret + "  Average size: %f\n" % (result[1] / result[0])
    ret = ret + "  Max size: %d\n" % result[2]
    ret = ret + "  Min size: %d\n" % result[3]
    ret = ret + "  zLib size: %f\n" % (result[4] / result[0])
    ret = ret + "  brotli size: %f\n" % (result[5] / result[0])
    ret = ret + "  bz2 size: %f\n" % (result[6] / result[0])
    ret = ret + "  lzma size: %f\n" % (result[7] / result[0])
    ret = ret + "  lzw size: %f\n" % (result[8] / result[0])

    ret = ret + "===== DER Results =====\n"
    ret = ret + "  Average size : %f\n" % (result[9] / result[0])
    ret = ret + "  Max size: %d\n" % result[10]
    ret = ret + "  Min size: %d\n" % result[11]
    ret = ret + "  zLib size: %f\n" % (result[12] / result[0])
    ret = ret + "  brotli size: %f\n" % (result[13] / result[0])
    ret = ret + "  bz2 size: %f\n" % (result[14] / result[0])
    ret = ret + "  lzma size: %f\n" % (result[15] / result[0])
    ret = ret + "  lzw size: %f\n" % (result[16] / result[0])

    return ret

def make_val(v1, v2):
    return round(v1/v2, 2)

def make_bin(s):
    return ''.join(map(bin, bytearray(s, 'ascii')))

def main():    
    if len(sys.argv) != 2:
        usage()

    cert_files = []
    prefix = sys.argv[1]

    for root, dirs, files in os.walk("./"):
        for f in files:
            if f.startswith("201") and f.endswith("_certs"):
                cert_files.append(f)

    print (cert_files)

    rfn = prefix + ".out"
    rf = open(rfn, "w")
    s = "File name, # of certs, Avg. PEM size, Max PEM size, Min PEM size, zlib (PEM), brotli (PEM), bz2 (PEM), lzma (PEM), lzw (PEM), Avg. DER size, Max DER size, Min DER size, zlib (DER), brotli (DER), bz2 (DER), lzma (DER), lzw (DER)\n"
    rf.write(s)

    c = OpenSSL.crypto
    head = "-----BEGIN CERTIFICATE-----\n"
    tail = "\n-----END CERTIFICATE-----\n"

    for fn in cert_files:
        print ("----- Start Analysis for ", fn, " -----")
        f = open(fn, "r")
        ofn = prefix + "_" + fn + ".out"
        of = open(ofn, "w")
        of.write("num, domain, issuer, size (PEM), zlib (PEM), brotli (PEM), bz2 (PEM), lzma (PEM), size (DER), zlib (DER), brotli (DER), bz2 (DER), lzma (DER)\n")
        num = 0
        result = {}

        for i in range(17):
            result[i] = 0
        result[2] = -sys.maxsize + 1
        result[3] = sys.maxsize
        result[10] = -sys.maxsize + 1
        result[11] = sys.maxsize

        for line in f:
            result[0] = result[0] + 1
            num = num + 1
            tmp = line.strip().split(",")
            h = tmp[0].strip()
            v = tmp[1].strip()
            pem = head + v + tail

            try:
                cert = c.load_certificate(c.FILETYPE_PEM, pem)
            except:
                s = "error"
                of.write(s)
                continue

            der = c.dump_certificate(c.FILETYPE_ASN1, cert)

            try:
                dom = cert.get_subject().CN
                issuer = cert.get_issuer().CN
            except:
                s = "error"
                of.write(s)
                continue

            try:
                pem = pem.encode('ascii')
            except:
                pem = pem.encode('utf8')

            pem_size = len(pem)
            pem_zlib = len(zlib.compress(pem))
            pem_brotli = len(brotli.compress(pem))
            pem_bz2 = len(bz2.compress(pem))
            pem_lzma = len(lzma.compress(pem))

            der_size = len(der)
            der_zlib = len(zlib.compress(der))
            der_brotli = len(brotli.compress(der))
            der_bz2 = len(bz2.compress(der))
            der_lzma = len(lzma.compress(der))

            pfw = open("pem.tmp", "wb")
            pfw.write(pem)
            pfw.close()
            dfw = open("der.tmp", "wb")
            dfw.write(der)
            dfw.close()

            os.system("python2 certs_lzw.py")

            pem_lzw = os.stat("pem_out.tmp").st_size
            der_lzw = os.stat("der_out.tmp").st_size

            result[1] = result[1] + pem_size
            if pem_size > result[2]:
                result[2] = pem_size
            if pem_size < result[3]:
                result[3] = pem_size
            result[4] = result[4] + pem_zlib
            result[5] = result[5] + pem_brotli
            result[6] = result[6] + pem_bz2
            result[7] = result[7] + pem_lzma
            result[8] = result[8] + pem_lzw

            result[9] = result[9] + der_size
            if der_size > result[10]:
                result[10] = der_size
            if der_size < result[11]:
                result[11] = der_size
            result[12] = result[12] + der_zlib
            result[13] = result[13] + der_brotli
            result[14] = result[14] + der_bz2
            result[15] = result[15] + der_lzma
            result[16] = result[16] + der_lzw

            s = "%d, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (num, dom, issuer, pem_size, pem_zlib, pem_brotli, pem_bz2, pem_lzma, pem_lzw, der_size, der_zlib, der_brotli, der_bz2, der_lzma, der_lzw)

            try:
                print (num, ") ", s)
                of.write(s)
            except:
                print (num, ") error encoding")
                of.write("error encoding")

        of.close()

        de = result[0]

        s = "%s, %d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n" % (fn, de, make_val(result[1], de), result[2], result[3], make_val(result[4], de), make_val(result[5], de), make_val(result[6], de), make_val(result[7], de), make_val(result[8], de), make_val(result[9], de), result[10], result[11], make_val(result[12], de), make_val(result[13], de), make_val(result[14], de), make_val(result[15], de))
        rf.write(s)

        title = "%s succeed" % fn
        msg = make_output(result)

        send_email(title, msg)

        for i in range(17):
            result[i] = 0
        result[2] = -sys.maxsize + 1
        result[3] = sys.maxsize
        result[10] = -sys.maxsize + 1
        result[11] = sys.maxsize

    rf.close()

    title = "Certificate compression info end"
    msg = "Finish!"

    send_email(title, msg)

if __name__ == "__main__":
    main()
