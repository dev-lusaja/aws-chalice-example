import json
from chalice.test import Client
from app import app


def test_csv():
    with Client(app, stage_name='local') as client:
        data = {
            "products": [
                {"name": "Product1", "quantity": 2, "price": 29},
                {"name": "Product2", "quantity": 1, "price": 49}
            ],
            "uid": "8ef6d507-c740-4d94-9bc4-dd720e596919",
            "create_at": "05/30/2024 21:03:50",
            "client_id": "client_789",
            "total_amount": 78
        }

        event = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps(data),
                    'TopicArn': 'test',
                    'Subject': 'test',
                    'MessageAttributes': {}
                }
            }]
        }

        with client:
            response = client.lambda_.invoke(
                'csv', event
            )
            assert response.payload == {'response': 'csv created'}
