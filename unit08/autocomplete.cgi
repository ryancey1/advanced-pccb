#!/usr/local/bin/python3

import mysql.connector
import json
import cgi

# CGI header
print("Content-Type: application/json\n\n")

# grab "term" field
form = cgi.FieldStorage()
term = form.getvalue("term")

# connect to SQL database
conn = mysql.connector.connect(
    user="ryancey3", password="Rancey19931!", host="localhost", database="biotest"
)
curs = conn.cursor()

# set up and execute query
qry = "SELECT product FROM genes WHERE product LIKE %s LIMIT 5"
curs.execute(qry, ("%"+term+"%", ))

# print results to page in JSON format for autocomplete
print(json.dumps([item for product in curs for item in product]))

# close connection
curs.close()
conn.close()
