import traceback
import json
import os
from chalice import Chalice, Response, BadRequestError
from chalicelib.order_service import OrderService
from chalicelib.order_repository import OrderRepositoryFactory
from chalicelib.event_bus_repository import EventBusRepositoryFactory
from chalicelib.email_repository import EmailRepositoryFactory
from chalicelib.csv_repository import CSVReopsitoryFactory

app = Chalice(app_name='koandina-chalice-lab')

service = OrderService(
        repository=OrderRepositoryFactory(),
        event_bus =EventBusRepositoryFactory(),
        email_repository=EmailRepositoryFactory(),
        csv_repository=CSVReopsitoryFactory()
)

@app.route('/orders', methods=['POST'])
def post_order():
    try:
        order_data = app.current_request.json_body
        response = service.create_order(order_data=order_data)
        return Response(body=json.dumps(response),
                        status_code=200,
                        headers={'Content-Type': 'application/json'}
                        )
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestError(e)


@app.on_sns_message(topic=os.getenv('TOPIC_BUS_NAME'))
def notify(event):
    try:
        return service.send_email(event.message)
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestError(e)    

@app.on_sns_message(topic=os.getenv('TOPIC_BUS_NAME'))
def csv(event):
    try:
        return service.upload_csv(event.message)
    except Exception as e:
        print(traceback.format_exc())
        raise BadRequestError(e)
