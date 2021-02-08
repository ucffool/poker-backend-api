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

## Requirement for Deploying to AWS

You will also need to create an `.aws` folder in the root project directory and include a file called `config`:

```
[default]
aws_access_key_id={SECRET_KEY}
aws_secret_access_key={SECRET_ACCESS_KEY}
region=xx-xxxx-#
```

Please see [boto3's docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#aws-config-file) for more information.

## Create a local DynamoDB (Recommended)
AWS provides [documentation for a local DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html) which is used in the following scripts (`dev` stage). If you skip this step, make sure you use either `qa` or `prod` stages which will use AWS hosted DynamoDB.


## Creating DynamoDB Initial Tables

From the terminal, you can run `createtables.py` to build the initial tables for your API. If you use the optional `-o` flag, it saves some basic DynamoDB information to _config.json_ environment variables for use in other scripts.

`python createtables.py -o`

There are various optional arguments available:
```
optional arguments:
-h, --help                show this help message and exit
-s, --stage {dev,qa,prod} DynamoDB Database Location (dev == local) (default: dev)
-r, --region REGION       AWS Region -- optional for local (default: us-west-2)
-p, --port PORT           Port used only for local (default: 8000)
-o, --overwrite           Save DynamoDB region/port to config.json for stage (default: False)
-d, --delete              Delete table, if exists, before create (default: False)
-dd, --destroy            Delete table, if exists. Do not create (default: False)

```

#### Add API User (Basic Auth)
Populate `api-users` table with a new user record (defaults to _dev_ stage and thus a local DynamoDB), prompting you for a username and token (this can be generated for you):

`python addapiuser.py` 

Again, there are a few optional arguments:
```
-h, --help                show this help message and exit
-s, --stage {dev,qa,prod} DynamoDB Database stage `dev` == local (default: dev)
-r, --role {admin,user}   Restricting endpoints (default: admin)
```


