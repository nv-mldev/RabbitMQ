import time
import json
import logging

logging.disable(logging.CRITICAL)
# Disable ALL pika logging - more comprehensive approach
logging.getLogger("pika").setLevel(logging.CRITICAL)
logging.getLogger("pika.connection").setLevel(logging.CRITICAL)
logging.getLogger("pika.channel").setLevel(logging.CRITICAL)
logging.getLogger("pika.adapters").setLevel(logging.CRITICAL)
logging.getLogger("pika.adapters.blocking_connection").setLevel(logging.CRITICAL)

import pika


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
    # create a message data for Notifications, logging , analytics and backup
    message_data = [
        {
            "notifications": "email has been sent",
            "logging": "user logged in",
            "analytics": "page viewed",
            "backup": "database backup completed",
        },
        {
            "notifications": "SMS sent",
            "logging": "user logged out",
            "analytics": "button clicked",
            "backup": "file backup completed",
        },
        {
            "notifications": "push notification sent",
            "logging": "user updated profile",
            "analytics": "form submitted",
            "backup": "system backup completed",
        },
    ]
    # Publish messages to the exchange
    for message in message_data:
        channel.basic_publish(
            exchange="server-traces", routing_key="", body=json.dumps(message)
        )
        print(f"Sent: {message}")
        time.sleep(3)

    # Close the connection
    connection.close()


if __name__ == "__main__":
    main()
