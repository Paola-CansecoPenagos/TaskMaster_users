# infrastructure/messaging/rabbitmq_consumer.py

import pika
import json
from infrastructure.services.jwt_service import decode_access_token
from infrastructure.repositories.user_repository import UserRepository

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='user_verification')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        token = data['token']
        user_info = decode_access_token(token)
        response = {"exists": False}
        if user_info:
            user_id = user_info.get('user_id')
            repository = UserRepository(connection_string='mongodb://localhost:27017/', db_name='taskMasterU')
            user_exists = repository.find_user(user_id) is not None
            response = {"exists": user_exists}
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='user_verification', on_message_callback=callback, auto_ack=False)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()