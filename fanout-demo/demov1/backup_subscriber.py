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

    # Callback function to process backup messages
    def callback(ch, method, properties, body):
        message = json.loads(body)
        backup_data = message.get("backup", "No backup data")
        print(f"💾 BACKUP SERVICE - Processing: {backup_data}")
        # Add your backup logic here (create backups, verify integrity)

    # Create a durable named queue for backup
    queue_name = "backup_queue"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange="server-traces", queue=queue_name)

    # Start consuming messages
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("💾 Backup Service waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
