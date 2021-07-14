#!/usr/local/bin/python3

import mysql.connector
import json

conn = mysql.connector.connect(
    user='ryancey3', password='Rancey19931!', host='localhost', database='biotest'
)

curs = conn.cursor()

curs.execute("SELECT product FROM genes")

print(json.dumps([item for product in curs for item in product]))
curs.close()
conn.close()
