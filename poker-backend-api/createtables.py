import boto3
import argparse
from uuid import uuid4

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-e', '--env', default='local',
                    choices=['local', 'prod'], help='DynamoDB Database Location')
parser.add_argument('-r', '--region', default='us-west-2', help='AWS Region -- optional for local')
parser.add_argument('-p', '--port', default='8000', help='Port used only for local')
parser.add_argument('-d', '--delete', default=False, action='store_true', help='Delete table, if exists, before create')
parser.add_argument('-dd', '--destroy', default=False, action='store_true',
                    help='Delete table, if exists. Do not create')
args = parser.parse_args()

if args.env == 'prod':
    dynamodb = boto3.resource('dynamodb', region_name=args.region)
else:
    endpoint = "http://localhost:" + args.port
    dynamodb = boto3.resource('dynamodb', region_name=args.region, endpoint_url=endpoint)


def create_api_users_table(ddb=None):
    if ddb:
        create_table = ddb.create_table(
            TableName='api-users',
            KeySchema=[
                {
                    'AttributeName': 'user',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'token',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'token',
                    'AttributeType': 'S'
                }
            ],
            BillingMode="PAY_PER_REQUEST"
        )
    # noinspection PyUnboundLocalVariable
    return create_table


# Check to see if the table already exists
"""
try:
    dynamodb.describe_table(TableName="api-users")['Table']['TableStatus']
except dynamodb.exceptions.ResourceNotFoundException:
    print("Table `api-users` not found.")
    pass
"""

if __name__ == '__main__':
    if args.delete or args.destroy:
        table = dynamodb.Table("api-users")
        try:
            table.delete()
            table.wait_until_not_exists()
            print("Table deleted: `api-users`")
        except dynamodb.meta.client.exceptions.ResourceNotFoundException:
            print("`api-users` table doesn't exist; nothing deleted.")
        finally:
            pass
    if not args.destroy:
        # create `api-users` table
        try:
            api_users_table = create_api_users_table(dynamodb)
            print(f"Table being created (`api-users`): {api_users_table.table_status}")
            api_users_table.wait_until_exists()
            print("Table created: `api-users`")
        except dynamodb.meta.client.exceptions.ResourceInUseException:
            api_users_table = dynamodb.Table('api-users')
            print("`api-users` table already exists. To delete it first, pass the -d flag.")
            pass
        print(api_users_table.key_schema, api_users_table.attribute_definitions)

user = "admin"
token = uuid4()
