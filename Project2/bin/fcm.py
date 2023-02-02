import math
import re
import string
import time
from pathlib import Path


def get_normalized_string(data):
    # remove all but words and spaces
    data = re.sub("\s\s+", " ", data)
    data  =data.translate(str.maketrans('', '', string.punctuation))

    return data


def get_alphabet(data):
    alphabet = sorted(list(set(data)))

    return alphabet


def get_expressions_from_data(data, table, alphabet, k):
    # pass through all the characters and insert every 3 in the dict
    # along with the next character and the times they appear
    for i in range(len(data) - k):
        context = data[i:i + k]
        next_char = data[i + k]

        if context not in table:
            table[context] = {next_char: 1}
        else:
            if next_char not in table[context]:
                table[context][next_char] = 1
            else:
                table[context][next_char] += 1
    return table


def get_probability_table(data, table, alphabet, k, a):
    alphabet.extend([' '])
    total_sequences = len(data) - k
    entropy = 0
    t = time.time()
    entropy_table = dict()

    i = 0
    print(len(table))
    for context in table:
        #print(i)
        i+=1

        entropy_table[context] = dict()
        total = sum(table[context].values())
        entropy_table[context] = {k: -math.log2((a/(total+(a*len(alphabet))))) for k in alphabet}
        for char in table[context]:
            entropy_table[context][char] = -math.log2((table[context][char] + a) / (total + (a * len(alphabet))))
    print(time.time()-t)

    return entropy_table


def fcm(filename="sherlock.txt", a=0.1, k=1):
    _message = open(filename, 'r', encoding = 'utf-8')

    data = get_normalized_string(_message.read())
    alphabet = get_alphabet(data)

    table = get_expressions_from_data(data, table=dict(), alphabet=alphabet, k=k)

    entropy_table = get_probability_table(data, table, alphabet, k, a)

    return alphabet, entropy_table


