#! /usr/local/bin/python3

import os
import cgi
import jinja2
import mysql.connector as sql


def main():
    # grab info from HTML form
    form = cgi.FieldStorage()
    queried = form.getfirst('lookfor')

    # if form was left empty show all entries
    if queried is None:
        queried = ''
        q = '%'+queried+'%'
        qq = '<i>No entry</i> -- showing all'
    else:
        # otherwise add wildcards
        q = '%'+queried+'%'
        qq = queried

    # connect to my chado database
    conn = sql.connect(user='ryancey3', password="Rancey19931!",
                       host='localhost', database='ryancey3_chado')
    curs = conn.cursor()

    # build query
    s = """
        SELECT feature.uniquename, product.value AS product
        FROM feature
            JOIN cvterm polypeptide ON feature.type_id=polypeptide.cvterm_id
            JOIN featureprop product ON feature.feature_id=product.feature_id
            JOIN cvterm productprop ON product.type_id=productprop.cvterm_id
        WHERE polypeptide.name='polypeptide'
            AND productprop.name='gene_product_name'
            AND product.value LIKE %s
        """

    # execute query
    curs.execute(s, (q,))
    c = curs.fetchall()  # get list
    l = len(c)  # get length of list

    # jinja2 setup
    templateloader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=templateloader)
    template = env.get_template('unit06.html')

    # cgi print statements, pass info to render call
    print('Content-Type: text/html\n\n')
    print(template.render(entries=c, q=qq, n=l))

    # close cursor/sql connection
    curs.close()
    conn.close()


if __name__ == '__main__':
    main()
