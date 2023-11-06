# notification-server
Проект содержит producer и receiver контейнеры.

Receiver будет получать сообщения от order сервиса.

Для тестирования можно обратиться к API, которое опубликует сообщение в очередь RabbitMQ.

В контейнере receiver можно увидеть лог о том, что сообщение подбирается.
Если в переменной окружения лежат конфигурации для email-сервера email будет отправлен.

### API
- Send Message
Request to send message to Message Broker. Below is an example request:
```json
POST http://localhost:7000/
Accept: application/json
Content-Type: application/json
Body:
{
    "email": "test_email@gmail.com",
    "order_code": "test_code",
    "created_at": "2023-11-01",
    "products": [
        {"product_id": "123", "product_name": "phone", "quantity": 2},
        {"product_id": "124", "product_name": "laptop", "quantity": 1}
    ]
}
```
