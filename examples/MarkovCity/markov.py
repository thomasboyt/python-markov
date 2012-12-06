import json, random

# source should be a list of lines to put in
# if importing a larger source without separate lines, simply make it a one-element list

class MarkovChain:
    def __init__(self):
        self.table = {}

    def create_table(self, source):
        for line in source:
            words = line.split(" ")
            for index, word in enumerate(words):
                if index+1 < len(words):
                    if word not in self.table:
                        self.table[word] = {}
                    if words[index+1] not in self.table[word]:
                        self.table[word][words[index+1]] = 1
                    else:
                        self.table[word][words[index+1]] += 1

    def save_table(self, file):
        serialized = json.JSONEncoder().encode(self.table)
        f = open(file, 'w')
        f.write(serialized)
        f.close()

    def parse_table(self, serialized_table):
        table = json.JSONDecoder().decode(serialized_table)
        self.table = table

    def generate_chain(self, length):
        table = self.table

        words = []

        # pick a random word to start the chain
        words.append(random.choice(table.keys()))

        while len(words) < length:
            last_idx = len(words)-1
            last_word = words[last_idx]

            try:
                entries = table[last_word]
            except KeyError:
                return " ".join(words)

            probabilities = {}

            total_count = sum(entries.values())
            choice = random.randint(0, total_count-1)
            word = weighted_probability(entries, choice)
            words.append(word)

        return " ".join(words)


def weighted_probability(entries, rnd):
    for word, weight in entries.iteritems():
        if (rnd < weight):
            return word
        rnd -= weight