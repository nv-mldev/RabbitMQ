# Basic Example using default Exchange

- routing key and queue name has to be the same
- If multiple subscribers are attached to a subscriber queue, how the messages are routed to different subscribers by default in roud robin fashion
- Which AMQP entity receives the message from the publisher? Exchange
- Channel is created in a connection
- In a multithreaded application different threads share a connection
- Default exchange is a type of Direct excahnge
- In default excahnge the routing key is the Subscriber's queue name
- In RabbitMQ both subscriber and producer can create the queue
