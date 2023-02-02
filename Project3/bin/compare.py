import glob
import sys
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
from compressor import compress
from generateAudioSignatures import create_signatures


def compare(sample=None, c_method="gzip"):
    if not sample:
        return

    av_signatures = [f.split(".")[0] for f in os.listdir("sample_signatures/")]

    if sample.split(".")[0] not in av_signatures:
        sample_signature = create_signatures(sample, "sample_signatures/")

    else:
        sample_signature = sample.split(".")[0]+".txt"

    compressed_sample = compress(open(sample_signature, 'rb').read(), c_method)

    print(f"Audio file size: {sys.getsizeof(open(sample, 'rb').read()) * 8} bits")
    print(f"Signature size: {sys.getsizeof(open(sample_signature,'rb').read())*8} bits")
    print(f"Compressed signature size: {sys.getsizeof(compressed_sample) * 8} bits")
    db_signatures = [f for f in glob.glob("signatures/*.txt")]
    results = []

    for db_sig in db_signatures:
        print(db_sig)
        n = normalized_compression_distance(open(sample_signature, 'rb').read(), open(db_sig, 'rb').read(), c_method)
        x = list(range(0, len(n)))

        plt.plot(x, n, label=db_sig[11:16])

        results.append(min(n))

    plt.legend(loc='upper right', numpoints=1, ncol=3, fontsize=8)
    plt.show()
    index_of_min = results.index(min(results))
    print(results)
    print(f"Its probably {db_signatures[index_of_min][11:-4]}.wav")

    return db_signatures, results


def normalized_compression_distance(signature_x, signature_y, c_method):
    c_x = compress(signature_x, c_method)
    results = []

    for i in range(0, len(signature_y)):
        window = signature_y[i:i+len(signature_x)]
        c_y = compress(window, c_method)
        c_xy = compress(signature_x+window, c_method)
        sizes = [sys.getsizeof(c_x),sys.getsizeof(c_y),sys.getsizeof(c_xy)]
        ncd = (sizes[-1] - min(sizes[:-1]))/max(sizes[:-1])
        results.append(ncd)

    return results


if __name__ == '__main__':
    if "-reset" in sys.argv:
        create_signatures()
    compression_methods = ["gzip", "bzip2", "lzma", "zlib"]

    if "-s" in sys.argv and "-c" in sys.argv:
        sample_index = sys.argv.index("-s")+1
        compression_method = sys.argv.index("-c")+1
        compare(sample=sys.argv[sample_index], c_method=sys.argv[compression_method])
