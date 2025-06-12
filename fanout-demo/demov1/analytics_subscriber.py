import pika
import json


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
