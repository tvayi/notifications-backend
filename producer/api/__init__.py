import logging

from aiohttp import web

from api.enum import EnvironmentVariables
from api.gateway.producer_server import ProducerServer
from api.services.handler import Handler


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )

    rabbitMQ_instance = ProducerServer(
        queue=EnvironmentVariables.RABBITMQ_QUEUE.get_env(),
        host=EnvironmentVariables.RABBITMQ_HOST.get_env(),
        routing_key=EnvironmentVariables.RABBITMQ_ROUTING_KEY.get_env(),
        username=EnvironmentVariables.RABBITMQ_USERNAME.get_env(),
        password=EnvironmentVariables.RABBITMQ_PASSSWORD.get_env(),
        exchange=EnvironmentVariables.RABBITMQ_EXCHANGE.get_env()
    )

    app = web.Application()
    handler = Handler(rabbitMQ_instance)

    app.add_routes([
        web.post('/', handler.publish),
    ])

    web.run_app(
        app,
        port=7000
    )
