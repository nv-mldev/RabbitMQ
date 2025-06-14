import pika
import json
import logging

logging.getLogger("pika").setLevel(logging.WARNING)  # Suppress pika debug logs


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

    # Callback function to process notification messages
    def callback(ch, method, properties, body):
        message = json.loads(body)
        notification_data = message.get("notifications", "No notification data")
        print(f"📧 NOTIFICATION SERVICE - Processing: {notification_data}")
        # Add your notification logic here (send emails, push notifications)

    # Create temporary queue for real-time notifications (old notifications less useful)
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="server-traces", queue=queue_name)

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("📧 Notification Service waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
