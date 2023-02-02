import sys
import os
import time
import random
from lang import Lang
from fcm import fcm, get_normalized_string


def find_language(alpha,k, analyze):
    lang_files = get_language_files()
    _lang =Lang(alpha, k)
    results = []
    _max = 0
    for file in lang_files:
        _lang.get_model_entropy_table(f'../languages/train/{file}')
        total = _lang.analyze_message_entropy(open(f'../languages/test/{analyze}', 'r', encoding = 'utf-8').read())
        if results == [] or total>max(results):
            _max = len(results)
        results.append(round(total,3))
    sorted_results = sorted([(lang_files[i], results[i]) for i in range(len(lang_files))], key = lambda item:item[1])
    print(sorted_results)

def main():
    args = sys.argv[1:]

    if len(args)==0:
        raise Exception("Too little arguments")

    file_name = args[0]
    k = 1 if len(args)<2 else int(args[1])
    alpha = 1 if len(args)<3 else float(args[2])

    starttime = time.time()

    find_language(alpha,k,file_name)

    print('Time:' + str(time.time() - starttime) + "s")
    print('-' * 22)

def get_language_files():
    text_files = [f for f in os.listdir('../languages/train') if f.endswith('.utf8')]
    return [(filename) for filename in text_files]

if __name__== "__main__":
    main()
