#!/usr/local/bin/python3

import cgi
import json
import os
import mysql.connector


def main():
    # CGI header & gather variables
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue("term")

    # connect to database
    conn = mysql.connector.connect(
        user="ryancey3", password="Rancey19931!", host="localhost", database="biotest"
    )
    cursor = conn.cursor()

    # build and execute query
    qry = """
          SELECT locus_id, product
            FROM genes
           WHERE product LIKE %s
    """
    cursor.execute(qry, ("%" + term + "%", ))

    # build dictionary from results
    results = {"match_count": 0, "matches": list()}
    for (locus_id, product) in cursor:
        results["matches"].append({"locus_id": locus_id, "product": product})
        results["match_count"] += 1

    # close connection & print results
    conn.close()
    print(json.dumps(results))


if __name__ == "__main__":
    main()
