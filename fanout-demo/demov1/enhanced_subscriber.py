import pika
import json
import os
import time


def main():
    # Get process ID for identification
    pid = os.getpid()
    subscriber_id = f"SUB-{pid}"

    print(f"🚀 [{subscriber_id}] Starting subscriber...")

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

    # Callback function to process messages
    def callback(ch, method, properties, body):
        message = json.loads(body)
        timestamp = time.strftime("%H:%M:%S")
        print(f"📨 [{subscriber_id}] [{timestamp}] Received: {message}")

    # Create a temporary queue and bind it to the exchange
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue
    print(f"📋 [{subscriber_id}] Created queue: {queue_name}")

    channel.queue_bind(exchange="server-traces", queue=queue_name)
    print(f"🔗 [{subscriber_id}] Bound to exchange: server-traces")

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f"⏳ [{subscriber_id}] Waiting for messages. To exit press CTRL+C")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"🛑 [{subscriber_id}] Stopped by user")
        channel.stop_consuming()
        connection.close()


if __name__ == "__main__":
    main()
