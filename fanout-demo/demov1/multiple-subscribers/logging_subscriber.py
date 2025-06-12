import pika
import json
import logging

logging.getLogger("pika").setLevel(logging.WARNING)


def main():
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            port=5672,
            virtual_host="/",
            credentials=pika.PlainCredentials("guest", "guest"),
        )
    )
    channel = connection.channel()

    # Declare a fanout exchange
    channel.exchange_declare(exchange="server-traces", exchange_type="fanout")

    # Callback function to process logging messages
    def callback(ch, method, properties, body):
        message = json.loads(body)
        log_data = message.get("logging", "No logging data")
        print(f"📝 LOGGING SERVICE - Processing: {log_data}")
        # Add your logging logic here (write to files, databases, etc.)

    # Create a durable named queue for logging
    queue_name = "logging_queue"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange="server-traces", queue=queue_name)

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("📝 Logging Service waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
