#! /usr/local/bin/python3

import jinja2
import re


class Sequence:
    '''
    Sequence: A class that holds all necessary info for this assignment
    '''

    def __init__(self, id, desc, sequence=''):
        self.ID = id
        self.Description = desc
        self.Sequence = sequence
        self.Length = len(sequence)


def read_fasta_to_dict(fasta_filepath: str, limit=None) -> dict:
    '''
    read_fasta_to_dict: Parse through a limited number of sequences in a FASTA formatted file and extracts headers/sequences into a dictionary

    Args:
        fasta_filepath (str): The relative or absolute filepath to a FASTA file
        limit (int, optional): The number of sequences to read in. Set value to None to read the whole file. Defaults to None.

    Returns:
        dict: A dictionary containing the desired number of sequences, organized by the header.
    '''
    # if a limit isn't specified
    if limit == None:
        # reset the limit counter to the total number of sequences in the file
        with open(fasta_filepath) as tmp:
            limit = tmp.read().count('>')

    dict, number_of_seqs = {}, 0
    # open file
    with open(fasta_filepath) as fasta:
        line = ''
        # go to first sequence
        while not line.startswith('>'):
            line = fasta.readline()
        # while we haven’t reached the limit
        while number_of_seqs != limit:
            # if we're at a sequence header
            if line.startswith('>'):
                # save header, move to next line
                header = line[1:].rstrip()
                line = fasta.readline()
                # initialize dictionary entry
                dict[header] = ''
                # append sequence line until we reach another header
                while not line.startswith('>'):
                    dict[header] = dict.get(header) + line.rstrip()
                    line = fasta.readline()
            # increment counter once we're finished appending the sequence
            number_of_seqs += 1
    return dict


def main():
    '''
    main: Reads a FASTA file and extracts a specified number of entries, along with desired information. Then, passes the extracted information along to jinja2 for templating an HTML document.
    '''

    dict = read_fasta_to_dict('e_coli_k12_dh10b.faa', 20)
    seqs = []

    # parse sequence dictionary
    for header, seq in dict.items():
        # split the header along the first space
        m = re.search(r'(\S+)\s+(.*)', header)
        if m:
            # add a sequence object to the growing seqs list
            id, desc = m.group(1), m.group(2)
            s = Sequence(id, desc, seq)
            seqs.append(s)

    # jinja2 setup
    templateloader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=templateloader)
    template = env.get_template('unit04.html')

    # cgi print statements, pass seqs list in the render call
    print('Content-Type: text/html\n\n')
    print(template.render(entries=seqs))


if __name__ == '__main__':
    main()
