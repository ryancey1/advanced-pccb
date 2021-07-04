#! /usr/local/bin/python3

import jinja2
import re

templateloader = jinja2.FileSystemLoader(searchpath="./templates")
env = jinja2.Environment(loader=templateloader)
template = env.get_template('unit03.html')


class BedEntry:
    def __init__(self, chrom, start, end, name, strand):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.name = name
        self.score = 0
        self.strand = strand

    def print_entry(self):
        print(*vars(self).values(), sep="\t")


def main():
    entries = []
    with open("yeast.gff3") as file:
        for line in file:
            if not line.startswith("#"):
                if len(line.split()) == 9 and line.split()[2] == "gene":
                    entry = line.split()
                    name = re.search(r"ID=([^;]+);", entry[8]).group(1)
                    bed = BedEntry(entry[0], entry[3],
                                   entry[4], name, entry[6])
                    entries.append(bed)
    print("Content-Type: text/html\n\n")
    print(template.render(bed=entries))


if __name__ == '__main__':
    main()
