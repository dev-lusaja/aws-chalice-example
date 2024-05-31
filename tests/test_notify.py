from chalice.test import Client
from app import app


def test_notify():
    with Client(app, stage_name='local') as client:
        data = {
            "products": [
                {"name": "Product1", "quantity": 2, "price": 29},
                {"name": "Product2", "quantity": 1, "price": 49}
            ],
            "client_id": "client_789",
            "total_amount": 78
        }

        event = {
            'Records': [{
                'Sns': {
                    'Message': data,
                    'TopicArn': 'test',
                    'Subject': 'test',
                    'MessageAttributes': {}
                }
            }]
        }

        with client:
            response = client.lambda_.invoke(
                'notify', event
            )
            assert response.payload == {'response': 'email sended'}
