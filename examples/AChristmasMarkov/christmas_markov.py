import os, json, argparse

from markov import MarkovChain


def christmas_parser(text):
    # drop unneeded whitespace
    text = text.replace("\n", " ").replace("\r", "")

    # drop punctuation (optional)
    #text = text.replace(";", "").replace(".", "").replace("!", "").replace(",", "")
    text = text.replace('"', "")

    return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('length', type=int, help='Maximum number of words to generate.')
    parser.add_argument('--lines', type=int, help='Number of lines to generate (default=1).', default=1)

    args = parser.parse_args()

    chain = MarkovChain()

    if not os.path.isfile("table.json"):
        f = open("source.txt")
        lines = [christmas_parser(f.read())]
        f.close()
        chain.create_table(lines)
        chain.save_table("table.json")

    else:
        f = open("table.json")
        raw_table = f.read()
        f.close()

        chain.parse_table(raw_table)

    for i in range(0, args.lines):
        print chain.generate_chain(args.length) + "\n"
