#! /usr/local/bin/python3

from genbank import *
from collections import namedtuple
import jinja2


def compare_annotation(algo1, algo2):
    # named tuples to store information
    Summary = namedtuple(
        "Summary", "ref_name pred_name ref_count pred_count exact_match start_mismatch stop_mismatch unique_to_reference unique_to_prediction")
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
                    Results(ref_start, pred_start, "agrees", ref_stop, pred_stop, "agrees"))
                break
            # if only the start site matches
            elif ref_start == pred_start:
                mismatch_3 += 1
                match = True
                ref_copy.remove(ref_record)
                pred_copy.remove(pred_record)
                results.append(
                    Results(ref_start, pred_start, "agrees", ref_stop, pred_stop, "DISAGREES"))
                break
            # if only the stop site matches
            elif ref_stop == pred_stop:
                mismatch_5 += 1
                match = True
                ref_copy.remove(ref_record)
                pred_copy.remove(pred_record)
                results.append(
                    Results(ref_start, pred_start, "DISAGREES", ref_stop, pred_stop, "agrees"))
                break
        # if we reach the end of the predicted set and we still haven't found a match in reference
        if not match:
            # append a disagreement
            results.append(
                Results(ref_start, "n/a", "DISAGREES", ref_stop, "n/a", "DISAGREES"))
        match = False  # reset boolean flag
    return Summary(algo1.name, algo2.name, algo1.length, algo2.length, perfect,
                   mismatch_5, mismatch_3, len(ref_copy), len(pred_copy)), results


def main():
    alg1 = GenbankRecord("./files/sequence.gb", "Genbank")
    alg2 = GenbankRecord("./files/prodigal/e_coli_O157_H7.gbk", "Prodigal")

    summary, results = compare_annotation(alg1, alg2)

    # jinja2 setup
    templateloader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=templateloader)
    template = env.get_template('midterm.html')

    # cgi print statements, pass seqs list in the render call
    print('Content-Type: text/html\n\n')
    print(template.render(summary=summary, results=results))


if __name__ == '__main__':
    main()
