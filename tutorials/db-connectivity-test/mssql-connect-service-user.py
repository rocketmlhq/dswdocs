# mssql-connect.py
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Copyright (c) RocketML
#------------------------------------------------------------------------------

import pyodbc
import boto3
import base64
import requests
import json

session = boto3.session.Session()
client = session.client('secretsmanager','us-west-2')

response = client.get_secret_value(SecretId='arn:aws:secretsmanager:us-west-2:399991052688:secret:rmltestsqlserver2016-46PuZx')
data = json.loads(response['SecretString'])

server = 'sqlserver2016.cbsebh4l1881.us-west-2.rds.amazonaws.com'
database = 'rmltest'
username = data['username']
password = data['password']

print ('user name : ' + data['username'])
print ('user name : ' + data['password'])

driver = sorted(pyodbc.drivers()).pop()

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
print(cnxn)
cursor = cnxn.cursor()

sql_select_Query = "SELECT * FROM Persons"
cursor.execute(sql_select_Query)
records = cursor.fetchall()

print (records)

#close the connection
cnxn.close()




