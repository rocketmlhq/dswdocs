# postgres-connect.py
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Copyright (c) RocketML
#------------------------------------------------------------------------------

import psycopg2
import boto3
import base64
import requests
import json

try:

    session = boto3.session.Session()
    client = session.client('secretsmanager','us-west-2')

    response = client.get_secret_value(SecretId='arn:aws:secretsmanager:us-west-2:399991052688:secret:rmltestpostgres-fJVcf2')
    data = json.loads(response['SecretString'])

    print ('user name : ' + data['username'])
    print ('user name : ' +data['password'])

    connection = psycopg2.connect(user = data['username'],
                                  password = data['password'],
                                  host = "postgresdb968.cbsebh4l1881.us-west-2.rds.amazonaws.com",
                                  port = "5432",
                                  database = "rmltest")
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # execute select query
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    cursor.execute("SELECT * FROM Persons")
    persons_record = cursor.fetchone()
    print("Selected row from Persons table - ", persons_record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")