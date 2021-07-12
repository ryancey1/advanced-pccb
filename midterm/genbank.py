#! /usr/local/bin/python3
import re


class GenbankRecord:
    """A class that stores annotation records in a readable JSON format"""

    def __init__(self, file, file_type):
        self.file = file
        self.name = file_type
        self.features = []
        self.__parse_file()
        self.length = len(self.features)

    def __sort(self):
        self.features = sorted(
            self.features, key=lambda x: x['coords']['start'])

    def __extract_coords(self, operator, seq_string):
        # seq_string = "92527..92721,1..2502"
        start_end = seq_string.replace(")", "").split("..")
        start, end = start_end[0], start_end[2] if len(
            start_end) > 2 else start_end[1]
        # return complement-coordinated dict based on operator, add flags for future use
        return {'start': int(end.replace(">", "")) if operator is not None and 'complement' in operator else int(start.replace("<", "")),
                'stop': int(start.replace("<", "")) if operator is not None and 'complement' in operator else int(end.replace(">", "")),
                'flag': 'trunc-start' if start.startswith('<') else 'trunc-end' if end.startswith('>') else None}

    def __parse_file(self):
        with open(self.file, "r") as gb_file:
            lines = gb_file.readlines()
        for line in lines:
            if line.strip().startswith("CDS "):
                tmp = line.split()
                op_loc, loc = re.search(r'(.*)\((.+)\)', tmp[1]), tmp[1]
                # append feature dict to growing list
                d = {
                    'feature': tmp[0],
                    'strand': 1 if tmp[1].startswith("comp") else 0,
                    'operator': op_loc.group(1).split("(") if op_loc else None,
                    # 'coords': self.__extract_coords(d, op_loc.group(2) if op_loc else loc)
                }
                d['coords'] = self.__extract_coords(
                    d['operator'], op_loc.group(2) if op_loc else loc)
                self.features.append(d)
        self.__sort()
        self.__join_records()

    def __join_records(self):
        for idx, feature in enumerate(list(self.features)):
            if feature['coords']['flag'] is None:
                continue
            curr, prev = feature, self.features[idx-1]
            # fix wraparound features -- join previous and current feature
            if curr['coords']['flag'] == "trunc-start" and prev['coords']['flag'] == 'trunc-end':
                # update the previous entry
                self.features[idx-1]['coords'] = {
                    'start': prev['coords']['start'],
                    'stop': curr['coords']['stop'],
                    'flag': None
                }
                # remove the current entry since it's merged with the previous
                self.features.pop(idx)
