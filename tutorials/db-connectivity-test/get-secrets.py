#!/usr/bin/python3

#------------------------------------------------------------------------------
# get-secrets.py 
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Copyright (c) RocketML
#------------------------------------------------------------------------------

import boto3
import base64
import requests
import json

session = boto3.session.Session()
client = session.client('secretsmanager','us-west-2')
 
#response = client.get_secret_value(SecretId='arn:aws:secretsmanager:us-west-2:399991052688:secret:rmltestByAsc-b4gBPd') 
response = client.get_secret_value(SecretId='arn:aws:secretsmanager:us-west-2:399991052688:secret:RmlTestSecret-7YY5L9') 
data = json.loads(response['SecretString'])

print ('user name : ' + data['username'])
print ('user name : ' +data['password'])
