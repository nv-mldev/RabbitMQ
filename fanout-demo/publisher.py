import pika

connection = pika.BlockingConnection(
    (
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            virtual_host="/",
            credentials=pika.PlainCredentials(username="guest", password="guest"),
        )
    )
)
