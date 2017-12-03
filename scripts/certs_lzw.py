import sys
import os
import lzw

def main():    
    pem = open("pem.tmp", "rb").read()
    der = open("der.tmp", "rb").read()
    p = lzw.compress(pem)
    d = lzw.compress(der)
    lzw.writebytes("pem_out.tmp", p)
    lzw.writebytes("der_out.tmp", d)

if __name__ == "__main__":
    main()
