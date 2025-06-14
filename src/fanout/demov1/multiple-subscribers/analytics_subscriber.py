import logging

logging.disable(logging.CRITICAL)
# Disable ALL pika logging - more comprehensive approach
logging.getLogger("pika").setLevel(logging.CRITICAL)
logging.getLogger("pika.connection").setLevel(logging.CRITICAL)
logging.getLogger("pika.channel").setLevel(logging.CRITICAL)
logging.getLogger("pika.adapters").setLevel(logging.CRITICAL)
logging.getLogger("pika.adapters.blocking_connection").setLevel(logging.CRITICAL)

import pika
import json


# Also disable the root logger for pika
pika_logger = logging.getLogger("pika")
pika_logger.disabled = True
pika_loggers_to_silence = [
    "pika",
    "pika.connection",
    "pika.channel",
    "pika.adapters",
    "pika.adapters.blocking_connection",
    "pika.heartbeat",
    # Add any other 'pika.something' logger names if they still appear
]

for logger_name in pika_loggers_to_silence:
    logger = logging.getLogger(logger_name)
    logger.setLevel(
        logging.CRITICAL + 1
    )  # Set level to something that will never be logged
    logger.handlers = []  # Remove any handlers Pika might have added
    logger.addHandler(
        logging.NullHandler()
    )  # Add a handler that does absolutely nothing
    logger.propagate = False  # Prevent messages from bubbling up to parent loggers
# --- END Pika Log Silencing Block ---


# ... rest of your subscriber code (def main():, pika.BlockingConnection(...), etc.)
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

    # Callback function to process analytics messages
    def callback(ch, method, properties, body):
        message = json.loads(body)
        analytics_data = message.get("analytics", "No analytics data")
        print(f"📊 ANALYTICS SERVICE - Processing: {analytics_data}")
        # Add your analytics logic here (store metrics, generate reports)

    # Create temporary queue for real-time analytics (old data less valuable)
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange="server-traces", queue=queue_name)

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("📊 Analytics Service waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
