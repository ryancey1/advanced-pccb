#!/usr/local/bin/python3

import mysql.connector
import cgi


def main():
    form = cgi.FieldStorage()
    input = form.getvalue('search_term')

    conn = mysql.connector.connect(
        user='ryancey3', password='Rancey19931!', host='localhost', database='biotest')
    cursor = conn.cursor()

    query = '''
            SELECT product 
                FROM genes 
            WHERE product LIKE %s 
            LIMIT 5'''

    cursor.execute(query, ('%'+input+'%', ))
    print([item for result in cursor for item in result])


if __name__ == '__main__':
    main()
