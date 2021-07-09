#! /usr/local/bin/python3
from genbank import *


def main():
    genbank = GenbankRecord("files/sequence.gb")
    prodigal = GenbankRecord("files/prodigal/e_coli_O157_H7.gbk")

    # print("----------------- SAMPLE GENBANK -----------------")
    # genbank.feature_print()

    # print("\n----------------- SAMPLE PRODIGAL -----------------")
    # prodigal.feature_print()

    genbank.compare(prodigal)


if __name__ == '__main__':
    main()
