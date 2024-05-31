import os
import boto3

class OrderRepositoryFactory:
    def __new__(self):
        dynamodb = boto3.client('dynamodb')
        if os.getenv('MOCK') == '1':
            return OrderRepositoryMock(dynamodb=dynamodb)
        return OrderRepository(dynamodb=dynamodb)

class OrderRepository:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb
    
    def save(self, data):
        input = {
            'TableName': os.getenv('TABLE_NAME'),
            'Item': convert_to_dynamodb_format(data)
        }
        response = self.dynamodb.put_item(**input)
        return response

class OrderRepositoryMock:
    def __init__(self, dynamodb):
        self.dynamodb = dynamodb

    def save(self, data):
        from botocore.stub import Stubber
        stubber = Stubber(self.dynamodb)
        input = {
            'TableName': os.getenv('TABLE_NAME'),
            'Item': convert_to_dynamodb_format(data)
        }

        response = {
            'ConsumedCapacity': {
                'CapacityUnits': 1,
                'TableName': os.getenv('TABLE_NAME'),
            },
            'ResponseMetadata': {
                'test': 'test',
            },
        }

        stubber.add_response('put_item', response, input)
        with stubber:
            return self.dynamodb.put_item(**input)

def convert_to_dynamodb_format(data):
    if isinstance(data, dict):
        return {k: convert_to_dynamodb_format(v) for k, v in data.items()}
    elif isinstance(data, list):
        return {'L': [{'M': convert_to_dynamodb_format(v)} if isinstance(v, dict) else convert_to_dynamodb_format(v) for v in data]}
    elif isinstance(data, str):
        return {'S': data}
    elif isinstance(data, (int, float)):
        return {'N': str(data)}
    else:
        raise TypeError("Tipo de dato no soportado")
