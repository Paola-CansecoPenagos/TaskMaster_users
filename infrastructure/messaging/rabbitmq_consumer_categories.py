import pika
import json
from infrastructure.services.jwt_service import decode_access_token
from infrastructure.repositories.user_repository import UserRepository

def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials()))
    channel = connection.channel()

    channel.queue_declare(queue='verification_queue')

    def on_request(ch, method, properties, body):
        data = json.loads(body)
        token = data['token']
        response_queue = data['response_queue']

        user_info = decode_access_token(token)
        user_id = user_info.get('user_id') if user_info else None
        repository = UserRepository(connection_string='', db_name='')
        user_exists = repository.find_user(user_id) is not None

        # Enviar la respuesta
        ch.basic_publish(
            exchange='',
            routing_key=response_queue,
            body=json.dumps({'exists': user_exists, 'user_id': user_id})
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='verification_queue', on_message_callback=on_request)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
