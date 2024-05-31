import os
import boto3
import json
import pandas as pd
from datetime import datetime
from botocore.exceptions import ClientError


class CSVReopsitoryFactory():
    def __new__(self):
        s3 = boto3.client('s3')
        if os.getenv('MOCK') == '1':
            return CSVReopsitoryMock(s3=s3)
        return CSVReopsitory(s3=s3)
    
class CSVReopsitory:
    def __init__(self, s3):
        self.s3 = s3

    def process(self, data):
        bucket_name = os.getenv('BUCKET_NAME')
        local_csv_file = '/tmp/local_data.csv'
        timestamp = datetime.now().strftime('%Y-%m-%d')
        s3_file_name = f'data_{timestamp}.csv'
        try:
            self.s3.download_file(bucket_name, s3_file_name, local_csv_file)
            df = pd.read_csv(local_csv_file, delimiter=';')
        except (FileNotFoundError, ClientError):
            df = pd.DataFrame()

        create_csv(df, data, local_csv_file)
        return self.s3.upload_file(local_csv_file, bucket_name, s3_file_name)

class CSVReopsitoryMock:
    def __init__(self, s3):
        self.s3 = s3

    def process(self, data):
        from botocore.stub import Stubber
        stubber = Stubber(self.s3)
        bucket_name = os.getenv('BUCKET_NAME')
        local_csv_file = '/tmp/local_data.csv'
        timestamp = datetime.now().strftime('%Y-%m-%d')
        s3_file_name = f'data_{timestamp}.csv'
        df = pd.DataFrame()
        create_csv(df, data, local_csv_file)

        stubber.add_response('put_object', {})

        with stubber:
            return self.s3.upload_file(local_csv_file, bucket_name, s3_file_name)

def create_csv(df, data, local_csv_file):
    data = json.loads(data)
    new_data = []
    for product in data['products']:
        new_data.append({
            'uid': data['uid'],
            'client_id': data['client_id'],
            'total_amount': data['total_amount'],
            'create_at': data['create_at'],
            'product_name': product['name'],
            'product_quantity': product['quantity'],
            'product_price': product['price'],
        })
    
    new_df = pd.DataFrame(new_data)
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(local_csv_file, sep=';', index=False)
