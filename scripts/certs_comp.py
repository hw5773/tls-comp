import sys
import os
import smtplib
import brotli
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
    ret = ret + "  Average size : %f\n" % (result[1] / result[0])
    ret = ret + "  ZLib Size: %f\n" % (result[2] / result[0])
    ret = ret + "  ZLib Ratio: %f\n" % (result[3] / result[0])
    ret = ret + "  Brotli Size: %f\n" % (result[4] / result[0])
    ret = ret + "  Brotli Ratio: %f\n\n" % (result[5] / result[0])

    ret = ret + "===== DER Results =====\n"
    ret = ret + "  Average size : %f\n" % (result[6] / result[0])
    ret = ret + "  ZLib Size: %f\n" % (result[7] / result[0])
    ret = ret + "  ZLib Ratio: %f\n" % (result[8] / result[0])
    ret = ret + "  Brotli Size: %f\n" % (result[9] / result[0])
    ret = ret + "  Brotli Ratio: %f\n\n" % (result[10] / result[0])

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

    c = OpenSSL.crypto
    head = "-----BEGIN CERTIFICATE-----\n"
    tail = "\n-----END CERTIFICATE-----\n"

    for fn in cert_files:
        print ("----- Start Analysis for ", fn, " -----")
        f = open(fn, "r")
        ofn = prefix + "_" + fn + ".out"
        of = open(ofn, "w")
        of.write("domain, issuer, size (PEM), zlib (PEM), zlib ratio (PEM), brotli (PEM), brotli ratio (PEM), size (DER), zlib (DER), zlib ratio (DER), brotli (DER), brotli ratio (DER)\n")
        max_size = -1
        min_size = 1000000
        num = 0
        result = {}
        for i in range(11):
            result[i] = 0

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
            pem_zlib_ratio = round(pem_zlib / pem_size)
            pem_brotli = len(brotli.compress(pem))
            pem_brotli_ratio = round((pem_brotli / pem_size), 2)

            der_size = len(der)
            der_zlib = len(zlib.compress(der))
            der_zlib_ratio = round((der_zlib / der_size), 2)
            der_brotli = len(brotli.compress(der))
            der_brotli_ratio = round((der_brotli / der_size), 2)

            result[1] = result[1] + pem_size
            result[2] = result[2] + pem_zlib
            result[3] = result[3] + pem_zlib_ratio
            result[4] = result[4] + pem_brotli
            result[5] = result[5] + pem_brotli_ratio

            result[6] = result[6] + der_size
            result[7] = result[7] + der_zlib
            result[8] = result[8] + der_zlib_ratio
            result[9] = result[9] + der_brotli
            result[10] = result[10] + der_brotli_ratio

            s = "%s, %s, %d, %d, %f, %d, %f, %d, %d, %f, %d, %f\n" % (dom, issuer, pem_size, pem_zlib, pem_zlib_ratio, pem_brotli, pem_brotli_ratio, der_size, der_zlib, der_zlib_ratio, der_brotli, der_brotli_ratio)

            try:
                print (num, ") ", s)
                of.write(s)
            except:
                print (num, ") error encoding")
                of.write("error encoding")

        of.close()

        de = result[0]

        s = "%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f\n" % (de, make_val(result[1], de), make_val(result[2], de), make_val(result[3], de), make_val(result[4], de), make_val(result[5], de), make_val(result[6], de), make_val(result[7], de), make_val(result[8], de), make_val(result[9], de), make_val(result[10], de))
        rf.write(s)

        title = "%s succeed" % fn
        msg = make_output(result)

        send_email(title, msg)

        for i in range(11):
            result[i] = 0

    rf.close()

    title = "Certificate compression info end"
    msg = "Finish!"

    send_email(title, msg)

if __name__ == "__main__":
    main()
