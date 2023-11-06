import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pika


def _send_email(email_data: dict) -> None:
    smtp_server = os.getenv('EMAIL_HOST', '')
    port = os.getenv('EMAIL_PORT', '')

    password = os.getenv('EMAIL_PASSWORD', '')

    if not password:
        return

    sender = os.getenv('EMAIL_SENDER')
    receiver = email_data['email']
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Notification of your order'
    body = 'Your order was successfully created.'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
    except Exception as e:
        print('error occurred while sending email', e)


class SendingEmailServer:
    def __init__(self, queue, host, routing_key, username, password, exchange='') -> None:
        self._connection = None
        self._channel = None
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

    def create_channel(self) -> None:
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
        self._channel.basic_qos(prefetch_count=1)

    @staticmethod
    def callback(channel, method, properties, body) -> None:
        logging.info('Отправление email')
        _send_email(body)

    def get_messages(self) -> None:
        try:
            logging.info('Запуск сервера')
            self._channel.basic_consume(
                queue=self._queue,
                on_message_callback=SendingEmailServer.callback,
                auto_ack=True
            )
            logging.info('Ожидание сообщений')
            self._channel.start_consuming()
        except Exception as e:
            logging.debug(f'Exception: {e}')
