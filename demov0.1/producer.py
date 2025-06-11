import pika

# This code connects to a RabbitMQ server, declares a queue named 'hello', and sends a message "Hello World!" to that queue.
# The message is sent using the default exchange, which routes messages to queues based on their names.
# The print statement confirms that the message has been sent successfully.
# This code is a simple RabbitMQ producer that sends a message to a queue named 'hello'.
# It uses the pika library to establish a connection to the RabbitMQ server, declare the queue, and publish the message.
# The connection is then closed after the message is sent.

# create a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

# create a channel to communicate with RabbitMQ
channel = connection.channel()
# [Optional] Create an exchange and bind it to a queue
# (not necessary for this simple example, but useful for more complex routing)

# Declare a queue named 'hello' using the default exchange
channel.queue_declare(queue="hello")
message = "Hello World! #1"
channel.basic_publish(exchange="", routing_key="hello", body=message)
print(f" [x] Sent '{message}'")

connection.close()
