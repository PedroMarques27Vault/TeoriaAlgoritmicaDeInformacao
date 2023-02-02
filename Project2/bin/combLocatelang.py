import math
import random
import sys
from findLang import get_language_files
import time
from lang import Lang
from fcm import get_normalized_string
import matplotlib.pyplot as plt
import codecs
from locateLang import visualize


def comb_locate_languages(alpha,filename):
    lang_files = get_language_files()
    message_file = open(f'../languages/mixed/{filename}', 'r', encoding='utf-8')

    _max = 0
    text_arr = get_normalized_string(message_file.read())
    weights = [0.2, 0.3, 0.5]
    ks = [3, 4, 5]
    for i in range(len(ks)):
        k = ks[i]
        context_arr = [text_arr[i:i + k + 1] for i in range(len(text_arr) - k)]

        languages_results = {k: dict() for k in lang_files}
        _lang = Lang(alpha, k)

        languages_smooth_results = {k: dict() for k in lang_files}
        languages_smooth_results_below_threshold = {k: dict() for k in lang_files}

        for _file in lang_files:
            _lang.get_model_entropy_table(f'../languages/train/{_file}')

            index = k
            for message in context_arr:
                total = _lang.analyze_message_entropy(message)
                languages_results[_file][index] = total
                index += 1

        threshold = math.log2(len(_lang.alphabet)) / 2
        for _file in lang_files:
            index = k
            for message in context_arr:
                if index <= len(context_arr) - k:
                    _sum = 0
                    for j in range(0, k):
                        _sum += languages_results[_file][index + j]
                    if index in languages_smooth_results[_file]:
                        languages_smooth_results[_file][index] += _sum / k * weights[i]
                    else:
                        languages_smooth_results[_file][index] = (_sum / k) * weights[i]
                    index += 1

    for _file in lang_files:
        languages_smooth_results_below_threshold[_file] = {k: v for k, v in languages_smooth_results[_file].items() if v < threshold}



    for language in languages_smooth_results_below_threshold:
        x = languages_smooth_results_below_threshold[language].keys()

        rgb = (random.random(), random.random(), random.random())
        plt.scatter(x, [language]*len(x), c=[rgb], label=language)

    # x-axis label
    plt.xlabel('Position')
    # frequency label
    plt.ylabel('Language')
    # plot title
    plt.title(f'k=3,4,5, alpha= {alpha}')
    # showing legend
    plt.legend()

    # function to show the plot

    plt.savefig(f'figures/CombLocateLang_{k}_{alpha}.png')
    plt.show()
    return languages_smooth_results_below_threshold




def main():
    args = sys.argv[1:]

    if len(args) == 0:
        raise Exception("Too little arguments")

    file_name = args[0]
    alpha = 0.01 if len(args) < 3 else float(args[1])


    start_time = time.time()
    comb_locate_languages(alpha,file_name)

    print('Time:' + str(time.time() - start_time) + "s")
    print('-' * 22)


if __name__ == "__main__":
    main()
