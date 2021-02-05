![Build Status](https://github.com/ucffool/poker-backend-api/workflows/Pytest/badge.svg)

Python powered, Chalice built, poker backend API for AWS Lambdas and API gateway.

```
pip3 install chalice
```

## Running Locally

```
chalice local
OR
chalice local --port=xxxx
```
The port option allows you run DynamoDB locally (also defaults to port 8000) as well without a port conflict.

## Deploying to AWS

You will also need to create an `.aws` folder in the root project directory and include a file called `config`:

```
[default]
aws_access_key_id={SECRET_KEY}
aws_secret_access_key={SECRET_ACCESS_KEY}
region=xx-xxxx-#
```

Please see [boto3's docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#aws-config-file) for more information.

## Creating DynamoDB Initial Tables

From the terminal, you can run `createtables.py` to build the initial tables for your API. There are various optional arguments available:
```
optional arguments:
  -h, --help             show this help message and exit
  -e, --env {local,prod} DynamoDB Database Location (default: local)
  -r, --region REGION    AWS Region -- optional for local (default: us-west-2)
  -p PORT, --port PORT   Port used only for local (default: 8000)
  -d, --delete           Delete table, if exists, before create (default: False)
  -dd, --destroy         Delete table, if exists. Do not create (default: False)

```