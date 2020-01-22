#------------------------------------------------------------------------------
# oracle-connect-service-user.py
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Copyright (c) 2017, 2018, Oracle and/or its affiliates. All rights reserved.
#------------------------------------------------------------------------------

from __future__ import print_function

import cx_Oracle
import boto3
import base64
import requests
import json

session = boto3.session.Session()
client = session.client('secretsmanager','us-west-2')

response = client.get_secret_value(SecretId='arn:aws:secretsmanager:us-west-2:399991052688:secret:rmlorcl-NZgHIN')
data = json.loads(response['SecretString'])

dsn_tns = cx_Oracle.makedsn('oracledb.cbsebh4l1881.us-west-2.rds.amazonaws.com', '1521','orcl')

conn = cx_Oracle.connect(data['username'],data['password'],dsn_tns)
print("Database version:", conn.version)
cur = conn.cursor()
cur.execute('select * from Persons')
res = cur.fetchmany(numRows=1)
print (res)

cur.close()
conn.close()