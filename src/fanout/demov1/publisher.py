import time
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
