#! /usr/local/bin/python3

import argparse
import cgi
import os


def parseArgs():
    """Sets up arguments for main script to run"""

    # choose from pre-downloaded
    form = cgi.FieldStorage()
    acc = form.getfirst('acc')

    # set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--accession", default="AB011549.2", metavar="acc",
        help="Genbank accession number of an alternate annotation to be run against (default: AB011549.2)")

    # if CGI form is used
    if acc is not None:
        return parser.parse_args(["-a", acc])

    # otherwise return the CLI args
    return parser.parse_args()


def check_environment():
    """Ensures proper directory structure and downloads necessary input files from NCBI (redirects STDOUT and STERR -- to allow CGI script)"""

    GENBANK_ACCESSION = parseArgs().accession
    GENBANK_ANNOTATION = f"gb_{GENBANK_ACCESSION}_annotation.gb"
    PRODIGAL_ANNOTATION = f"pr_{GENBANK_ACCESSION}_annotation.gb"

    if not os.path.isdir('files'):
        os.mkdir('files')
    # make annotation/seq files if they don't exist
    if not os.path.isfile(f'files/{GENBANK_ANNOTATION}'):
        os.system(
            f'wget -O files/{GENBANK_ANNOTATION} "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={GENBANK_ACCESSION}&retmode=text&rettype=gb" >/dev/null 2>&1')
    if not os.path.isfile(f'files/{GENBANK_ACCESSION}.fasta'):
        os.system(
            f'wget -O files/{GENBANK_ACCESSION}.fasta "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={GENBANK_ACCESSION}&retmode=text&rettype=fasta" >/dev/null 2>&1')
    if not os.path.isfile(f'files/{PRODIGAL_ANNOTATION}'):
        os.system(
            f'./prodigal -i files/{GENBANK_ACCESSION}.fasta -o files/{PRODIGAL_ANNOTATION} -p meta >/dev/null 2>&1')

    # return variables, they can be used in main script
    return GENBANK_ANNOTATION, PRODIGAL_ANNOTATION, GENBANK_ACCESSION


def main():
    check_environment()


if __name__ == '__main__':
    main()
