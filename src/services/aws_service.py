import os

import boto3

# Retrieve the DynamoDB table info
PYTHON_ENV = os.environ.get('PYTHON_ENV') or 'prod'
dynamo = boto3.resource('dynamodb', region_name='us-east-2')
quoteTable = dynamo.Table('FinancialDataQuotes-{0}'.format(PYTHON_ENV))
symbolsTable = dynamo.Table('FinancialDataSymbols-{0}'.format(PYTHON_ENV))