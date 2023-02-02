import math

from fcm import fcm, get_normalized_string


class Lang:
    def __init__(self, alpha, k):
        self.alpha = alpha
        self.k = k

    def get_model_entropy_table(self, model_filename):
        # table, prob table, alphabet, entropy, ent_table
        print(model_filename[:-4])
        self.alphabet, self.model_entropy_table = fcm(model_filename, self.alpha, self.k)

    def analyze_message_entropy(self, data):
        if not self.model_entropy_table or not self.alphabet:
            raise Exception('No model to compare')

        total_message_entropy = 0
        default_entropy = -math.log2(self.alpha / (self.alpha * len(self.alphabet)))

        for index in range(0, len(data)-self.k):
            _char = data[index+self.k]
            context = data[index:index+self.k]
            if context in self.model_entropy_table and _char in self.model_entropy_table[context]:
                total_message_entropy += self.model_entropy_table[context][_char]
            else:
                total_message_entropy += default_entropy

        return total_message_entropy
