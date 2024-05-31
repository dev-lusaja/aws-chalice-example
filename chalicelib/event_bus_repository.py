import boto3
import os
import json


class EventBusRepositoryFactory():
    def __new__(self):
        sns = boto3.client('sns')
        if os.getenv('MOCK') == '1':
            return EventBusRepositoryMock(sns=sns)
        return EventBusRepository(sns=sns)
        
class EventBusRepository():

    def __init__(self, sns):
        self.sns = sns

    def send(self, data):
        self.sns.publish(
            TopicArn=os.getenv('TOPIC_BUS_ARN'),
            Message=json.dumps(data),
            Subject="OrderCreated Domain Event"
        )

class EventBusRepositoryMock():

    def __init__(self, sns):
        self.sns = sns

    def send(self, data):
        from botocore.stub import Stubber
        stubber = Stubber(self.sns)

        input = {
            'TopicArn': 'test',
            'Message': json.dumps(data),
            'Subject': 'OrderCreated Domain Event Test'
        }

        expected_response = {
            'MessageId': '12345'
        }
        
        stubber.add_response('publish', expected_response, input)
        with stubber:
            return self.sns.publish(**input)
