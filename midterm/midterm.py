#! /usr/local/bin/python3
# from Bio import SeqIO
import re
from pprint import pprint


class GenbankFeature:
    def __init__(self, feature: str, strand: int, operator: str, location: str):
        self.feature = feature
        self.strand = strand
        self.operator = operator
        self.location = self.parse_location(location)

    def fprint(self):
        print(*vars(self))

    def split(self):
        pass

    def parse_location(self, location):
        return {
            'start': int(location.split("..")[0].replace('<', '')),
            'end': int(location.split("..")[1].replace('>', '')),
            'flag': 'trunc-start' if location.split("..")[0].startswith('<') else 'trunc-end' if location.split("..")[1].startswith('>') else None
        }


class Genbank:
    def __init__(self, file):
        self.file = file
        self.features = []
        self.__parse_file()
        self.number_of_features = len(self.features)

    def split_entry(self, f, r):
        # 92527..92721,1..2502
        # split location1/location2 on comma
        joins = r.group(2).split(',')
        # append the correct flags for later
        joins[0] = joins[0].replace('..', '..>')
        joins[1] = '<' + joins[1]
        # add the two features
        self.features.append(
            GenbankFeature(
                feature=f[0],
                # minus strand: 1 | plus strand: 0
                strand=1 if f[1].startswith(
                    'complement') else 0,
                # operator may be join() or complement()
                operator=r.group(1),
                location=joins[0]
            )
        )
        self.features.append(
            GenbankFeature(
                feature=f[0],
                # minus strand: 1 | plus strand: 0
                strand=1 if f[1].startswith(
                    'complement') else 0,
                # operator may be join() or complement()
                operator=r.group(1),
                location=joins[1]
            )
        )

    def __parse_file(self):
        with open(self.file, "r") as gb_file:
            # skip to the features table
            for line in gb_file:
                if line.startswith("FEATURES"):
                    break
            # we only care about the FEATURES table
            while not line.startswith("ORIGIN") and not line.startswith("//"):
                # we also only care for CDS entries
                if line.split()[0] == 'CDS':
                    # if we are at a 'joined' sequence
                    f = line.split()
                    r = re.search(r'(.*)\((.+)\)', f[1])
                    if 'join' in f[1]:
                        # it'll be easier to compare the joins by splitting them
                        self.split_entry(f, r)
                    else:
                        self.features.append(
                            GenbankFeature(
                                feature=f[0],
                                # minus strand: 1 | plus strand: 0
                                strand=1 if f[1].startswith(
                                    'complement') else 0,
                                # operator may be join() or complement()
                                operator=r.group(1) if r else None,
                                location=r.group(2) if r else f[1]
                            )
                        )
                line = gb_file.readline().strip()

    def correct_plasmid(self):
        potential_start, potential_end = self.features[-1], self.features[0]

    def feature_print(self):
        for feature in self.features:
            print(vars(feature))

    def print_features(self):
        print(*self.features, sep="\n")


def main():
    genbank = Genbank("files/sequence.gb")
    prodigal = Genbank("files/prodigal/e_coli_O157_H7.gbk")

    print("----------------- SAMPLE GENBANK -----------------")
    genbank.feature_print()
    print("\n----------------- SAMPLE PRODIGAL -----------------")
    prodigal.feature_print()


if __name__ == '__main__':
    main()
