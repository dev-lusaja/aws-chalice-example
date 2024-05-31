import uuid
from datetime import datetime

class OrderService:

    def __init__(self, repository, event_bus, email_repository, csv_repository):
        self.repository = repository
        self.event_bus  = event_bus
        self.email_repository = email_repository
        self.csv_repository = csv_repository
    
    def create_order(self, order_data):
        order_data['uid'] = uuid.uuid4().__str__()
        order_data['create_at'] = self.__create_at()

        self.repository.save(data=order_data)
        
        # Publish domain event
        self.event_bus.send(data=order_data)

        return {
            'response': 'Order created'
        }

    def send_email(self, order_data):
        self.email_repository.send(data=order_data)
        return {
            'response': 'email sended'
        }

    def upload_csv(self, order_data):
        self.csv_repository.process(data=order_data)
        return {
            'response': 'csv created'
        }

    
    def __create_at(self):
        return datetime.now().strftime("%m/%d/%Y %H:%M:%S")
