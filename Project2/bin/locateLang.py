
import math
import random
import sys
from findLang import get_language_files
import time
from lang import Lang
from fcm import get_normalized_string
import matplotlib.pyplot as plt
import codecs


def locate_languages(alpha, k, filename):
    lang_files = get_language_files()
    message_file = open(f'../languages/mixed/{filename}', 'r', encoding='utf-8')

    _max = 0
    text_arr = get_normalized_string(message_file.read())

    context_arr = [text_arr[i:i + k + 1] for i in range(len(text_arr) - k)]

    languages_smooth_results_below_threshold = {k: dict() for k in lang_files}

    _lang = Lang(alpha, k)
    languages_smooth_results = dict()
    languages_results = dict()
    for _file in lang_files:
        _lang.get_model_entropy_table(f'../languages/train/{_file}')
        languages_results.clear()
        index = k

        threshold = math.log2(len(_lang.alphabet)) / 2

        for message in context_arr:
            total = _lang.analyze_message_entropy(message)

            languages_results[index] = total
            index += 1


        index = k
        for _ in context_arr:
            if index <= len(context_arr) - k:
                _sum = 0
                for i in range(0, k):
                    _sum += languages_results[index + i]
                languages_smooth_results[index] = _sum / k
                index += 1

                if _sum / k <= threshold:
                    languages_smooth_results_below_threshold[_file][index] = _sum / k
        visualize(_file,languages_smooth_results, languages_results, threshold, k, alpha)

    for language in [y for y in languages_smooth_results_below_threshold if
                     len(languages_smooth_results_below_threshold[y] )!= 0]:
        x = languages_smooth_results_below_threshold[language].keys()

        rgb = (random.random(), random.random(), random.random())
        plt.scatter(x, [language] * len(x), c=[rgb], label=language)

    # x-axis label
    plt.xlabel('Position')
    # frequency label
    plt.ylabel('Language')
    # plot title
    plt.title(f'k={k}, alpha= {alpha}')
    # showing legend
    plt.legend()

    # function to show the plot

    plt.savefig(f'figures/LocateLang{k}_{alpha}.png')
    plt.show()

    return languages_smooth_results_below_threshold


def visualize(lang, smooth, not_smooth, threshold, k="multi", alpha=0.01):

    plt.plot(smooth.keys(), smooth.values(), label="smooth", color="blue", linewidth=2)
    plt.plot(not_smooth.keys(), not_smooth.values(), label="Not Smooth", color="red", linewidth=2)

    plt.plot(not_smooth.keys(), [threshold] * len(not_smooth.keys()), label="Threshold", color="green", linewidth=2)
    plt.title(f'k={k}, alpha={alpha}, {lang}')
    plt.xlabel('Char Position')
    plt.ylabel('Entropy')
    plt.legend()
    plt.savefig(f'figures/comb_smooth_{k}_{alpha}_{lang}.png')
    plt.show()


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        raise Exception("Too little arguments")

    file_name = args[0]
    k = 3 if len(args) < 2 else int(args[1])
    alpha = 0.01 if len(args) < 3 else float(args[2])


    start_time = time.time()
    locate_languages(alpha, k, file_name)

    print('Time:' + str(time.time() - start_time) + "s")
    print('-' * 22)


if __name__ == "__main__":
    main()