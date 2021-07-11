#! /usr/local/bin/python3

from genbank import GenbankRecord
from collections import namedtuple
import jinja2
import os

# global variables
FASTA_FILE = "e_coli_O157_H7.fasta"
GENBANK_ACCESSION = "AB011549.2"
GENBANK_ANNOTATION = "genbank_annotation.gb"
PRODIGAL_ANNOTATION = "prodigal_annotation.gb"


def compare_annotation(algo1, algo2):
    # named tuples to store information
    Summary = namedtuple(
        "Summary", "Reference_annotation_source Prediction_annotation_source Reference_CDS_Count Prediction_CDS_Count Exact_Matches Start_Disagrees Stop_Disagrees Unique_To_Reference Unique_To_Predicition")
    Results = namedtuple(
        "Results", "ref_start pred_start start_agrees ref_stop pred_stop stop_agrees")
    # set up counters and a storage list
    perfect, mismatch_5, mismatch_3, results = 0, 0, 0, []
    match = False
    # create a list copy to avoid altering the class
    ref_copy, pred_copy = list(algo1.features), list(algo2.features)
    for ref_record in list(algo1.features):
        ref_start, ref_stop = ref_record['coords']['start'], ref_record['coords']['stop']
        for pred_record in list(algo2.features):
            pred_start, pred_stop = pred_record['coords']['start'], pred_record['coords']['stop']
            # if they perfectly match
            if ref_start == pred_start and ref_stop == pred_stop:
                perfect += 1
                match = True
                ref_copy.remove(ref_record)
                pred_copy.remove(pred_record)
                results.append(
                    Results(ref_start, pred_start, "AGREES", ref_stop, pred_stop, "AGREES"))
                break
            # if only the start site matches
            elif ref_start == pred_start:
                mismatch_3 += 1
                match = True
                ref_copy.remove(ref_record)
                pred_copy.remove(pred_record)
                results.append(
                    Results(ref_start, pred_start, "AGREES", ref_stop, pred_stop, "DISAGREES"))
                break
            # if only the stop site matches
            elif ref_stop == pred_stop:
                mismatch_5 += 1
                match = True
                ref_copy.remove(ref_record)
                pred_copy.remove(pred_record)
                results.append(
                    Results(ref_start, pred_start, "DISAGREES", ref_stop, pred_stop, "AGREES"))
                break
        # if we reach the end of the predicted set and we still haven't found a match in reference
        if not match:
            # append a disagreement
            results.append(
                Results(ref_start, "-", "DISAGREES", ref_stop, "-", "DISAGREES"))
        match = False  # reset boolean flag
    return Summary(algo1.name, algo2.name, algo1.length, algo2.length, perfect,
                   mismatch_5, mismatch_3, len(ref_copy), len(pred_copy)), results


def check_environment():
    """Ensures proper directory structure and downloads necessary input files from NCBI (redirects STDOUT and STERR -- to allow CGI script)"""
    if not os.path.isdir('files'):
        os.mkdir('files')
    # make annotation/seq files if they don't exist
    if not os.path.isfile(f'files/{GENBANK_ANNOTATION}'):
        os.system(
            f'wget -O files/{GENBANK_ANNOTATION} "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={GENBANK_ACCESSION}&retmode=text&rettype=gb" >/dev/null 2>&1')
    if not os.path.isfile(f'files/{FASTA_FILE}'):
        os.system(
            f'wget -O files/{FASTA_FILE} "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={GENBANK_ACCESSION}&retmode=text&rettype=fasta" >/dev/null 2>&1')
    if not os.path.isfile(f'files/{PRODIGAL_ANNOTATION}'):
        os.system(
            'prodigal -i files/e_coli_O157_H7.fasta -o files/prodigal_annotation.gb -p meta >/dev/null 2>&1')


def main():
    # make sure the files are there and in proper directory
    check_environment()

    # read files into GenbankRecord objects
    alg1 = GenbankRecord("./files/genbank_annotation.gb", "Genbank")
    alg2 = GenbankRecord("./files/prodigal_annotation.gb", "Prodigal")

    # store summary and results
    summary, results = compare_annotation(alg1, alg2)

    # jinja2 setup
    templateloader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=templateloader)
    template = env.get_template('midterm.html')

    # cgi print statements, pass seqs list in the render call
    print('Content-Type: text/html\n\n')
    print(template.render(summary=zip(summary._fields, summary),
                          results=results, ref=alg1, pred=alg2))


if __name__ == '__main__':
    main()