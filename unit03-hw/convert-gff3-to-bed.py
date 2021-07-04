#! /usr/bin/env python3

'''
This file converts a GFF3 formatted annotation file into a BED6 file containing all the annotated gene features.

For more info on BED6/GFF3 formats, visit: https://genome.ucsc.edu/FAQ/FAQformat.html#format1 and https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md respectively.
'''

import re
import sys
import os


class FileNotGff3Error(Exception):
    pass


class HelpMenu(Exception):
    pass


class FileNotBedError(Exception):
    pass


class FileDoesntExistError(Exception):
    pass


def convert_gff3_to_bed(infile: str) -> str:
    # initialize a storage string
    bed = ""
    # parse file
    with open(infile) as gff:
        # look at each line
        for line in gff:
            # if features have ended, break the loop
            if line == "##FASTA\n":
                break
            # if we hit a gene feature
            if not line.startswith("#") and line.split()[2] == "gene":
                # split line on the whitespace
                gene = line.split()
                # search for the gene ID
                name = re.search(r"ID=([^;]+);", gene[8]).group(1)
                # add the line to the growing list
                # convert starting index to 0-based
                bed += f"{gene[0]}\t{int(gene[3])-1}\t{gene[4]}\t{name}\t0\t{gene[6]}\n"
    # remove final newline and return string
    return bed


def main():
    outfile = None

    try:
        # if help menu is asked for
        if sys.argv[1] in ["-h", "--help"]:
            raise HelpMenu

        # first argument is input
        infile = sys.argv[1]

        # make sure file is a gff3 file
        if not infile.endswith(".gff3"):
            raise FileNotGff3Error

        # make sure file input exists
        if not os.path.exists(infile):
            raise FileDoesntExistError

        # if no output file is specified
        if len(sys.argv) < 3:
            # return the last level of filepath (filename)
            filename = infile.split(os.path.sep)[-1]
            # remove extension and replace with "bed"
            out = filename[0:len(filename)-4] + "bed"
        else:
            # otherwise use the argument provided
            out = sys.argv[2]

            # make sure the output has a .bed extension
            if not out.endswith(".bed"):
                raise FileNotBedError

        # open output stream
        with open(out, "w") as outfile:
            # write the converted string to the output file
            outfile.write(convert_gff3_to_bed(infile))
            # let user know what the file is called
            print(f'Converted file written to: {out}')

    # catch a whole host of potential errors
    except (NameError):
        print("No input file is passed in.")

    except (HelpMenu):
        print(
            "Usage: python3 unit3-3.py [-h|--help] INPUT [OUTPUT]\nConvert a GFF3 file to a BED6 file of genes.\n\nRequired:\n* INPUT\t\t/path/to/input.gff3\n\nOptional:\n* OUTPUT\t/path/to/output.bed (default: input filename in current directory)\n* -h|--help\tShow this message and exit.")

    except (IndexError):
        print("Usage: python3 unit3-3.py [-h|--help] INPUT [OUTPUT]")

    except (FileNotGff3Error):
        print("Input file is not GFF3.")

    except(FileNotBedError):
        print("Output file is not BED.")

    except(FileDoesntExistError):
        print("File does not exist.")

    # end by closing the output stream
    finally:
        if outfile != None:
            outfile.close()


if __name__ == '__main__':
    main()
