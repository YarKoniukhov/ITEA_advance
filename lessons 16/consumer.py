import pika
import json
from lesson_16 import *

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='advance')

print('[*] Waiting for messages.')


def callback(ch, method, properties, body):
    body.decode()
    save(body)


def save(data):
    data = json.loads(data)
    order_profile = Orders(order_type=data['1'],
                           description=data['2'],
                           status=data['3'],
                           serial_no=data['4'],
                           creator_id=data['5'])
    db.session.add(order_profile)
    db.session.flush()
    db.session.commit()

print('Saved in PostgreSQL')

channel.basic_consume('advance', callback, auto_ack=True)

channel.start_consuming()


