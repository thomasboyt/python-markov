from xml.etree import ElementTree 
import re, os, json, argparse

from markov import MarkovChain

### Initial parsing & table creation

# Parse through the dialog XML file and take all of the dialogue out for parsing, removing character names
def parse_xml():
    tree = ElementTree.parse("dialog.xml")
    root = tree.getroot()

    pattern = r"(\w+): ([^/]*)$"

    all_lines = []
    for issue in root.iter("issue"):
        text = issue.find("dialog").text
        lines = text.split("\n")

        for line in lines:
            result = re.match(pattern, line)
            if result:
                all_lines.append(result.group(2))

    return all_lines


### Command line usage

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('length', type=int, help='Maximum number of words to generate.')
    parser.add_argument('--lines', type=int, help='Number of lines to generate (default=1).', default=1)

    args = parser.parse_args()

    chain = MarkovChain()

    if not os.path.isfile("table.json"):
        lines = parse_xml()
        table = chain.create_table(lines)
        chain.save_table("table.json")
    else:
        f = open("table.json")
        raw_table = f.read()
        f.close()

        table = chain.parse_table(raw_table)

    for i in range(0, args.lines):
        print chain.generate_chain(args.length) + "\n"
