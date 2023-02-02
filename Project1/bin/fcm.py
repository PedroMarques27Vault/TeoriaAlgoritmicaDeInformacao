import math
import re
from pathlib import Path

def make_table(alphabet, k):
    occupied_space = get_table_space(alphabet, k)
    a_size = len(alphabet)

    if occupied_space <= 1024:
        table = [[0] * a_size for x in range(a_size ** k)]
    else:
        table = {}
    return table

def get_normalized_string(data):
    # remove all but words and spaces
    data = re.sub(r'[^a-zA-Z ]+', '', data.lower())
    data = re.sub("\s\s+", " ", data)
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

        if type(table) == dict:
            if context not in table:
                table[context] = {next_char: 1}
            else:
                if next_char not in table[context]:
                    table[context][next_char] = 1
                else:
                    table[context][next_char] += 1
        else:
            table[get_index(context, alphabet, k)][alphabet.index(next_char)] += 1
    return table

def get_index(context, alphabet, k):
    a_size = len(alphabet)
    index = 0
    count = k - 1

    for i in context:
        index += (a_size ** count) * alphabet.index(i)
        count -= 1

    return index


def get_table_space(alphabet, k):
    a_size = len(alphabet)
    return (a_size ** k) * a_size * 16 / 8 / 1024 / 1024

def get_probability_table(data, table, alphabet, k, a):
    entropy = 0
    total_sequences = len(data) - k

    if type(table) == dict:
        probabilities_table = {}
        for context in table:
            total = sum(table[context].values())
            for char in table[context]:
                occurrence = table[context][char]
                if context not in probabilities_table:
                    probabilities_table[context] = {}
                probabilities_table[context][char] = (occurrence + a) / (total + (a * len(alphabet)))
            ent_row = -sum([x * math.log2(x) for x in probabilities_table[context].values()])
            entropy += (total / total_sequences) * ent_row

    else:
        probabilities_table = []
        for row in table:
            total = sum(row)
            prob_row = [(occurrence + a) / (total + (a * len(alphabet))) for occurrence in row]
            probabilities_table.append(prob_row)

            ent_row = -sum([x*math.log2(x) for x in prob_row])
            entropy += (total / total_sequences) * ent_row
    return probabilities_table, entropy



def fcm(filename="sherlock.txt", a=0.1, k=1):

    data = Path("../example/"+filename).read_text(encoding='utf-8')
    data = get_normalized_string(data)
    alphabet = get_alphabet(data)
    table = make_table(alphabet,k)
    table = get_expressions_from_data(data, table=table, alphabet=alphabet, k=k)
    probabilities_table, entropy = get_probability_table(data, table, alphabet, k, a)

    return table, probabilities_table,alphabet, entropy


