#!/usr/local/bin/python3

import mysql.connector
import json
import cgi

print("Content-Type: application/json\n\n")
form = cgi.FieldStorage()

term = form.getvalue('term')

conn = mysql.connector.connect(
    user='ryancey3', password='Rancey19931!', host='localhost', database='biotest'
)
curs = conn.cursor()
qry = "SELECT product FROM genes"

curs.execute(qry)

print(json.dumps([item for product in curs for item in product]))

curs.close()
conn.close()
