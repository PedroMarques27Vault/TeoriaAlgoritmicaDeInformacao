import sys

import time
import random
from fcm import fcm, get_index, get_normalized_string

def get_initial_sequence(alphabet, k):
    sequence = ""

    for i in range(0, k):
        sequence += random.choice(alphabet)

    return sequence

def generator(filename, alpha, k, length, initialText):
    table, probabilities_table, alphabet, entropy = fcm(filename, alpha,k)
    if not initialText:
        initialText = get_initial_sequence(alphabet, k)
    else:
        initialText = get_normalized_string(initialText)
    print('Total entropy: ' + str(entropy))

    i = 0

    while i <  length:
        i += 1
        lastKcharacters = initialText[-k:]

        initialText+=get_next_char(probabilities_table, alphabet=alphabet, context=lastKcharacters, k=k, a=alpha)

    write_to_file(initialText)

def get_next_char(probabilities_table, alphabet, context, k, a):
    selected_char = random.random()
    initial_value = 0
    if type(probabilities_table) == dict:
        if context not in probabilities_table:
            return random.choice(alphabet)
        probs = {k: v for k, v in sorted( probabilities_table[context].items(), key=lambda item: item[1], reverse=True)}
        for char in probs:
            prob = probs[char]
            if initial_value <= selected_char < initial_value + prob:
                return char
            initial_value += prob
        return random.choice([x for x in alphabet if x not in probabilities_table[context]])


    else:
        index = int(get_index(context, alphabet, k=k))
        lista =list( zip(probabilities_table[index], alphabet))

        lista.sort(reverse=True)
  
        for i in lista:
            if initial_value <= selected_char < initial_value + i[0]:
                return i[1]
            initial_value += i[0]

def write_to_file(string):
    f = open("../src/output.txt", "w", encoding='utf-8')
    f.write(str(string) + "\n")
    f.close()

def main():
    args = sys.argv[1:]

    if len(args)==0:
        raise Exception("Too little arguments")

    file_name = args[0]
    k = 1 if len(args)<2 else int(args[1])
    alpha = 1 if len(args)<3 else float(args[2])
    length = 1000 if len(args)<4 else float(args[3])

    initalText = None if len(args)<5 else str(args[4])

    starttime = time.time()
    generator(file_name, k=k, alpha=alpha, length=length, initialText=initalText)
    print('Time:' + str(time.time() - starttime) + "s")
    print('-' * 22)


if __name__== "__main__":
    main()
