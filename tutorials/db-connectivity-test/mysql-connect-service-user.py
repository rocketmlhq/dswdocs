#!/usr/bin/python3

#------------------------------------------------------------------------------
# mysql-connect-service-user.py
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Copyright (c) RocketML
#------------------------------------------------------------------------------

#!/usr/bin/python3

#------------------------------------------------------------------------------
# mysql-connect.py
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Copyright (c) RocketML
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# User name : rmltest4 | Password : rmltest123 | Database : rmltest2 | Secrets name : rmltest4
#------------------------------------------------------------------------------

import pymysql
import boto3
import base64
import requests
import json


session = boto3.session.Session()
client = session.client('secretsmanager','us-west-2')

response = client.get_secret_value(SecretId='arn:aws:secretsmanager:us-west-2:399991052688:secret:rmltest4-jUMvIq')

data = json.loads(response['SecretString'])

print ('user name : ' + data['username'])
print ('user name : ' +data['password'])

# Open database connection
db = pymysql.connect("rmltest.cbsebh4l1881.us-west-2.rds.amazonaws.com",data['username'],data['password'],"rmltest2" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

cursor.execute("SELECT * FROM Persons")

myresult = cursor.fetchall()

for x in myresult:
    print(x)

# disconnect from server
db.close()