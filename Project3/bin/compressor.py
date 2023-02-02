import glob
import lzma
import subprocess
import sys
import gzip, bz2
import os
import zlib


def compress(data, method = "gzip"):
    if method == "gzip":
        compressed_value = gzip.compress(data)
        return compressed_value
    elif method == "bzip2":
        f = bz2.compress(data)
        return f
    elif method == "lzma":
        f = lzma.LZMACompressor().compress(data)
        return f
    else:
        return zlib.compress(data)
if __name__ == '__main__':
    filename = sys.argv[1]
    f_in = open(filename, 'rb').read()
    compress(f_in)
