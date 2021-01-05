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
import argparse

default_secret = "arn:aws:secretsmanager:us-west-2:399991052688:secret:MariaDBCreds-RBiK6E"
parser = argparse.ArgumentParser()
parser.add_argument("--secret",type=str,help="Secret ARN",default=default_secret)
args = parser.parse_args()


secret_arn = args.secret

session = boto3.session.Session()
client = session.client('secretsmanager','us-west-2')

response = client.get_secret_value(SecretId=secret_arn)
data = json.loads(response['SecretString'])
print(data)
