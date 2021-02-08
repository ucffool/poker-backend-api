import boto3
from botocore.exceptions import ClientError
import argparse
import os
import json
import datetime
from pprint import pprint
from uuid import uuid4

# these should be pulled in from createtables.py saving them as env in .chalice config.json
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--stage', default='dev',
                    choices=['dev', 'qa', 'prod'], help='DynamoDB Database stage `dev` == local')
parser.add_argument('-r', '--role', default='admin', choices=['admin', 'user'], help='Restricting endpoints')
args = parser.parse_args()

# Retrieve environment_variables from config.json
with open(os.path.join('.chalice', 'config.json')) as f:
    data = json.load(f)
    if args.stage in data['stages']:
        region = data['stages'][args.stage]['environment_variables'].get('dynamodb-region', 'us-west-2') \
            if 'environment_variables' in data['stages'][args.stage] else 'us-west-2'
        port = data['stages'][args.stage]['environment_variables'].get('dynamodb-port', '8000') \
            if 'environment_variables' in data['stages'][args.stage] else '8000'
    else:
        quit(print(f"Stage `{args.stage} not found in config.json. Try running "
                   f"`python createtables.py -o -s {args.stage}` to create the tables and save region/port to config."))

# establish db connection
if args.stage == 'dev':
    endpoint = "http://localhost:" + port
    dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint)
else:
    dynamodb = boto3.resource('dynamodb', region_name=region)

# Get user input
print(f"Let's create a Basic Auth user for API access and save it to the database (Stage: {args.stage})")
user = input("Enter user: ")
if len(user) == 0:
    quit(print("User cannot be blank. Aborting."))
token = input("Enter token (or leave blank to have one generated for you): ")
if len(token) == 0:
    token = uuid4()
    print(f"Password for `{user}` is: {token}")

# Save to DynamoDB
table = dynamodb.Table('api-users')
put = table.put_item(
    Item={
        'user': user,
        'token': token,
        'created': datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        'role': args.role
    }
)
print("**** PUT ****")
pprint(put)
# retrieve it
print("**** GET ****")
try:
    response = table.get_item(Key={'user': user, 'token': token})
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    pprint(response['Item'])
