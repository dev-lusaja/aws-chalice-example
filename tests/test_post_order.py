import json
import os
from chalice.test import Client
from app import app


def test_post_order():
    with Client(app, stage_name='local') as client:
        data = {
            "products": [
                {"name": "Product1", "quantity": 2, "price": 29},
                {"name": "Product2", "quantity": 1, "price": 49}
            ],
            "client_id": "client_789",
            "total_amount": 78
        }
        response = client.http.post(
           '/orders',
           headers={'Content-Type':'application/json'},
           body=json.dumps(data)
       )
        assert response.json_body == {'response': 'Order created'}
