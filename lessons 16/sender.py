"""
Давайте теперь представим, что в нашей CRM системе необходимо сделать ещё одну точку входа для создания заявок.
В рамках данного ДЗ требуется реализовать очередь с использованием RabbitMQ, а также consumer на стороне нашего
приложения (должен находиться и запускаться из отдельного модуля), который будет читать поступающие json-подобные
сообщения из очереди и создавать на основании информации из него заявки в базе.
"""

import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='advance')

body = {
    '1': 'door',
    '2': 'tesla',
    '3': 'act',
    '4': 16,
    '5': 3
}

message_for_rabbit = json.dumps(body).encode()

channel.basic_publish(exchange='',
                      routing_key='advance',
                      body=message_for_rabbit)
print('message for rabbit send')

connection.close()






