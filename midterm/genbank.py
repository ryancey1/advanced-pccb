#! /usr/local/bin/python3
import re


class Feature:
    def __init__(self, feature: str, strand: int, operator: str, location: str):
        self.feature = feature
        self.strand = strand
        self.operator = operator
        self.__string = location
        self.start = self.parse_location(self.__string)['start']
        self.end = self.parse_location(self.__string)['end']
        self.location_flag = self.parse_location(self.__string)['flag']

    def fprint(self):
        print(*vars(self))

    def split(self):
        pass

    def parse_location(self, location):
        return {
            'start': int(location.split("..")[0].replace('<', '')),
            'end': int(location.split("..")[1].replace('>', '')),
            'flag': 'trunc-start' if location.split("..")[0].startswith('<') else 'trunc-end' if location.split("..")[1].startswith('>') else "complete"
        }


class GenbankRecord:
    def __init__(self, file):
        self.file = file
        self.features = []
        self.__parse_file()
        self.sort()
        self.number_of_features = len(self.features)

    def sort(self):
        from operator import attrgetter
        self.features = sorted(
            self.features, key=attrgetter('start'))

    def compare(self, other):
        # store results
        # result = []
        for i_0, feati in enumerate(self.features):
            for j_0, featj in enumerate(other.features):
                i, j = i_0+1, j_0+1
                print(f'genbank feature {i}: {feati.start}..{feati.end}')
                print(f'prodigal feature {j}: {featj.start}..{featj.end}')
                if feati.start == featj.start and feati.end == featj.end:
                    print("Complete match!", f"{i}:{j}")
                    break
                else:
                    # check for 5' or 3' matches, print accordingly
                    print(f"{i}:{j}", "Matching 5-prime" if feati.start ==
                          featj.start else "5-prime mismatch", "Matching 3-prime" if feati.end == featj.end else "3-prime mismatch", sep="\t")
                    # if one matches, it's likely that the algorithms are just off,
                    # not that there's another match, so break here and move to next sequence
                    if feati.start == featj.start or feati.end == featj.end:
                        break

    def __startsite(self, index):
        return self.__location(index)["start"]

    def __location(self, index):
        return self.features[index].parse_location()

    def __split_entry(self, f, r):
        # 92527..92721,1..2502
        # split location1/location2 on comma
        joins = r.group(2).split(',')
        # append the correct flags for later
        joins[0] = joins[0].replace('..', '..>')
        joins[1] = '<' + joins[1]
        # add the two features
        self.features.append(
            Feature(
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
            Feature(
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
                        self.__split_entry(f, r)
                    else:
                        self.features.append(
                            Feature(
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
