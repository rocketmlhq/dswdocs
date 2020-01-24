# redshift-connect.py  [create table , insert record , select record]
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

    connection = psycopg2.connect(user = 'rmltesttwo',
                                  password = 'Admin123',
                                  host = "rmltestclustertwo.chylmikgqdwb.us-west-2.redshift.amazonaws.com",
                                  port = "5439",
                                  database = "rmltestclustertwo")


    #connection = psycopg2.connect(user = 'admin',
    #                             password = 'Admin123',
    #                              host = "ascredshiftthree.caiczb81y5bu.us-west-2.redshift.amazonaws.com",
    #                              port = "5439",
    #                              database = "ascredshiftthree")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")


    create_table = "CREATE TABLE Persons (PersonID int,LastName varchar(255)" \
                   ",FirstName varchar(255),Address varchar(255),City varchar(255));"

    insert_data = "INSERT INTO Persons (PersonID, LastName, FirstName, Address, City) " \
                  "VALUES ('1', 'rocketmml', 'rocketmml', 'address', 'city');"

    select_data = "SELECT * FROM Persons"

    cursor.execute(create_table);
    cursor.execute(insert_data);
    cursor.execute(select_data);

    selected_record = cursor.fetchone()
    print("Selected record - ", selected_record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to Redshift", error)
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("Redshift connection is closed")