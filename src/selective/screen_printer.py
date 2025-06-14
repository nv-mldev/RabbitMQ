import pika
from tools.logging_setup import logging_setup
from pika.exceptions import AMQPConnectionError

logger = logging_setup("SelectiveSubscriber")


def callback(ch, method, properties, body):
    logger.info(f"Received message: {body.decode()}")
    severity = properties.headers.get("severity", "Unknown")
    logger.info(f"Message severity: {severity}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = None
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                port=5672,
                virtual_host="/",
                credentials=pika.PlainCredentials(username="guest", password="guest"),
            )
        )
        channel = connection.channel()

        channel.exchange_declare(exchange="logs_exchange", exchange_type="direct")

        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue

        # severities = ["info", "warning", "error", "critical"]

        channel.queue_bind(
            exchange="logs_exchange", queue=queue_name, routing_key="Error"
        )
        channel.queue_bind(
            exchange="logs_exchange", queue=queue_name, routing_key="Critical"
        )
        channel.queue_bind(
            exchange="logs_exchange", queue=queue_name, routing_key="Warning"
        )
        channel.queue_bind(
            exchange="logs_exchange", queue=queue_name, routing_key="Info"
        )

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=False
        )

        logger.info("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except AMQPConnectionError as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        if connection is not None and connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
