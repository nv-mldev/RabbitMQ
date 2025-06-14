import pika
import random
from pika.exceptions import AMQPConnectionError
from tools.logging_setup import logging_setup

# This code is a publisher that sends messages with different severity levels to a RabbitMQ exchange.
# It uses the pika library to connect to RabbitMQ and send messages.
# The messages are randomly selected from a predefined list and sent with the corresponding severity level as the routing key.
# The logging setup function configures the logger to write DEBUG and above logs to a file and INFO logs to the console.
# The publisher sends 10 messages in total, each with a random severity level and message.
# The connection to RabbitMQ is closed after sending the messages.


def main():
    # Set up logging
    logger = logging_setup("SelectivePublisher")

    try:
        # Create a connection to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                port=5672,
                virtual_host="/",
                credentials=pika.PlainCredentials(username="guest", password="guest"),
            )
        )
        channel = connection.channel()

        severity = ["Info", "Warning", "Error", "Critical"]

        messages = [
            "System is running smoothly.",
            "Minor issue detected, but system is operational.",
            "Significant problem encountered, immediate attention required.",
            "Critical failure, system is down!",
        ]

        for i in range(10):
            index = random.randint(0, len(severity) - 1)
            message = messages[index]
            severity_level = severity[index]
            try:
                channel.basic_publish(
                    exchange="logs_exchange",
                    routing_key=severity_level.lower(),
                    body=message,
                    properties=pika.BasicProperties(
                        headers={"severity": severity_level}
                    ),
                )
                logger.info(f" [x] Sent '{message}' with severity '{severity_level}'")
            except Exception as e:
                logger.error(f"Failed to publish message: {e}")

        # Close the connection
    except AMQPConnectionError as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
