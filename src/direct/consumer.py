# consumer.py
# This script is a RabbitMQ consumer that listens for messages on a queue named 'hello'.
import sys
import pika
import os


def main():
    # create a connection between the producer and broker/RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

    # create a channel to communicate with RabbitMQ server
    channel = connection.channel()

    # Declare a queue named 'hello'. if already the queue exists, it will not be recreated.
    # This queue will be used to receive messages.
    channel.queue_declare(queue="hello")

    # Callback function to process messages from the queue
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")

    # Set up subscription to the queue with auto acknowledgment for deleting the messages from the queue
    # When a message is received, the callback function will be called
    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for messages. To exit press CTRL+C")

    # Start consuming messages
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(" [*] Exiting...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
