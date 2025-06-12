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


channel = connection.channel()

channel.exchange_declare(exchange="fanout-demo", exchange_type="fanout")

for i in range(5):
    message = f"Message {i}"
    channel.basic_publish(exchange="fanout-demo", routing_key="", body=message)
    print(f"Sent: {message}")

channel.exchange_delete(exchange="fanout-demo", if_unused=False)

connection.close()
