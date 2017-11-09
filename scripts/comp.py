import brotli
import zlib

def main():
    crt = open("test.crt", "rb")
    a = zlib.compress(crt)
    b = brotli.compress(crt)
    print (len(a))
    print (len(b))
