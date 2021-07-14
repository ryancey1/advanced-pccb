#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector

def main():
    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('search_term')
        
    conn = mysql.connector.connect(user='hopkins', password='fakepass', host='localhost', database='biotest')
    cursor = conn.cursor()
    
    qry = """
          SELECT locus_id, product
            FROM genes
           WHERE product LIKE %s
    """
    cursor.execute(qry, ('%' + term + '%', ))

    results = { 'match_count': 0, 'matches': list() }
    for (locus_id, product) in cursor:
        results['matches'].append({'locus_id': locus_id, 'product': product})
        results['match_count'] += 1

    conn.close()

    print(json.dumps(results))


if __name__ == '__main__':
    main()
