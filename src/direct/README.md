# Direct Exchange

A **Direct Exchange** in RabbitMQ is one of the core types of exchanges used to route messages from producers to queues based on a specific routing key.

### How Direct Exchange Works

- **Routing Key:** When a producer sends a message, it specifies a routing key.
- **Binding:** Queues are bound to the direct exchange with a specific binding key.
- **Message Routing:** The direct exchange delivers the message to all queues whose binding key exactly matches the message’s routing key.

#### Example

Suppose you have a direct exchange named `logs_direct` and two queues:

- `info_queue` bound with binding key `info`
- `error_queue` bound with binding key `error`

If a producer sends a message with routing key `info`, only `info_queue` receives it. If the routing key is `error`, only `error_queue` receives it.

#### Key Points

- **Exact Match:** Routing is based on an exact match between the routing key and the binding key.
- **Multiple Queues:** Multiple queues can be bound with the same binding key; all will receive the message.
- **Default Exchange:** The default exchange in RabbitMQ is a direct exchange with no name (`""`). It routes messages to *queues whose name matches the routing key*.

#### Use Cases

- Task distribution where each type of task has its own queue.
- Logging systems where logs are separated by severity (info, warning, error).

#### Gotchas

- If no queue is bound with the routing key, the message is dropped (unless configured otherwise).
- Direct exchanges are not suitable for broadcast scenarios (use fanout exchange for that).

#### Example Code

````python
# Python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare direct exchange
channel.exchange_declare(exchange='logs_direct', exchange_type='direct')

# Declare queues
channel.queue_declare(queue='info_queue')
channel.queue_declare(queue='error_queue')

# Bind queues
channel.queue_bind(exchange='logs_direct', queue='info_queue', routing_key='info')
channel.queue_bind(exchange='logs_direct', queue='error_queue', routing_key='error')

# Publish message
channel.basic_publish(exchange='logs_direct', routing_key='info', body='This is an info message')

connection.close()
````

This example shows how to set up a direct exchange and route messages based on routing keys.

- routing key and queue name has to be the same
- If multiple subscribers are attached to a subscriber queue, how the messages are routed to different subscribers by default in roud robin fashion
- Which AMQP entity receives the message from the publisher? Exchange
- Channel is created in a connection
- In a multithreaded application different threads share a connection
- Default exchange is a type of Direct excahnge
- In default excahnge the routing key is the Subscriber's queue name
- In RabbitMQ both subscriber and producer can create the queue
