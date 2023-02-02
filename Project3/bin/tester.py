import os
import matplotlib.pyplot as plt

from compare import compare

bzip = [0.7866847826086957, 0.7663551401869159, 0.908320084790673, 0.7339357429718876, 0.8862478777589134, 0.6998972250770812, 0.8998917748917749, 0.7654901960784314, 0.7215189873417721]
zlib = [0.8232189973614775, 0.6956521739130435, 0.9362567811934901, 0.6392961876832844, 0.949003984063745, 0.6016016016016016, 0.9119960668633235, 0.7134283570892723, 0.6141509433962264]
gzip = [0.8103896103896104, 0.6883230904302019, 0.9311905839746492, 0.6318840579710145, 0.9400157853196527, 0.5944609297725024, 0.9066471163245357, 0.7070631970260223, 0.6072761194029851]

if __name__ == '__main__':
    path = 'samples'
    files = os.listdir(path)
    compression_methods = ["bzip2", "zlib", "gzip"]
    noise = ["bass", "br_01", "br_06", "clip", "freq", "samp", "saw", "treb", "wh_01"]
    c_results = [[] for i in range(len(compression_methods))]

    for i in range(len(compression_methods)):
        for file in files:
            if "Africa" in file:
                filename = "samples/" + file
                db_signatures, results = compare(filename, compression_methods[i])
                c_results[i].append(results[2])
                print("Result should be:", file.split('.')[0].split('_')[-1], "\n")

                # plt.scatter([i for i in range(len(results))], results)
                # plt.title("Sample: " + str(file[:-4]))
                # plt.savefig(f'figures/sample_{file[:-4]}.png')
                # plt.show()

        plt.scatter(noise, c_results[i], label=compression_methods[i])
        plt.show()

    # c_results = []
    # c_results.append(bzip)
    # c_results.append(zlib)
    # c_results.append(gzip)

    for i in range(len(compression_methods)):
        plt.scatter(noise, c_results[i], label=compression_methods[i])

    plt.xlabel('Noise')
    plt.ylabel('Score')
    plt.title("Different Scores for music: Africa")
    plt.legend()
    plt.savefig(f'figures/comp_results_Africa.png')
    plt.show()


