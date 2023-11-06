import json
import logging

import pika


class ProducerServer:

    def __init__(self, queue, host, routing_key, username, password, exchange=''):
        self._channel = None
        self._connection = None
        self._queue = queue
        self._host = host
        self._routing_key = routing_key
        self._exchange = exchange
        self._username = username
        self._password = password
        self.start_server()

    def start_server(self) -> None:
        self.create_channel()
        self.create_exchange()
        self.create_bind()
        logging.info('Канал создан')

    def create_channel(self):
        credentials = pika.PlainCredentials(username=self._username, password=self._password)
        parameters = pika.ConnectionParameters(self._host, credentials=credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

    def create_exchange(self) -> None:
        self._channel.exchange_declare(
            exchange=self._exchange,
            exchange_type='direct',
            passive=False,
            durable=True,
            auto_delete=False
        )
        self._channel.queue_declare(queue=self._queue, durable=False)

    def create_bind(self) -> None:
        self._channel.queue_bind(
            queue=self._queue,
            exchange=self._exchange,
            routing_key=self._routing_key
        )

    def publish(self, message=None) -> None:
        if message is None:
            message = {}

        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=self._routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(content_type='application/json')
        )
        logging.info(f'Публикуем сообщение: {format(message)}')
