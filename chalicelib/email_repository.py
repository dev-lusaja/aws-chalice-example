import boto3
import os
import json

class EmailRepositoryFactory:
    def __new__(self):
        sns = boto3.client('sns')
        if os.getenv('MOCK') == '1':
            return EmailRepositoryMock(sns=sns)
        return EmailRepository(sns=sns)
    
class EmailRepository:

    def __init__(self, sns):
        self.sns = sns

    def send(self, data):
        self.sns.publish(
            TopicArn=os.getenv('TOPIC_EMAIL_ARN'),
            Message=json.dumps(data),
            Subject="Notification OrderCreated"
        )

class EmailRepositoryMock:

    def __init__(self, sns):
        self.sns = sns

    def send(self, data):
        from botocore.stub import Stubber
        stubber = Stubber(self.sns)

        input = {
            'TopicArn': 'test',
            'Message': json.dumps(data),
            'Subject': 'Notification OrderCreated Test'
        }

        expected_response = {
            'MessageId': '12345'
        }
        
        stubber.add_response('publish', expected_response, input)
        with stubber:
            return self.sns.publish(**input)