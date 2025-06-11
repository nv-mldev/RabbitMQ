import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        virtual_host="/",
        credentials=pika.PlainCredentials(username="guest", password="guest"),
    )
)
channel = connection.channel()  # Create a channel to communicate with RabbitMQ

# create an exchange
channel.exchange_declare(exchange="fanout-demo", exchange_type="fanout")

# create a temporary queue
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

# bind the queue to the exchange
channel.queue_bind(exchange="fanout-demo", queue=queue_name)

print(f" [*] Waiting for messages in {queue_name}. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")


# set up subscription to the queue
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()  # Start consuming messages from the queue
