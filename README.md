# RabbitMQ Tutorial

Welcome to the RabbitMQ Tutorial Repository!  
This repository provides hands-on examples and guides to help you learn and master RabbitMQ, a powerful open-source message broker.

## 🚀 What is RabbitMQ?

RabbitMQ is a robust messaging broker that enables applications to communicate with each other using messages, supporting multiple messaging protocols and patterns.

## 📚 Contents

- **Introduction to RabbitMQ**
- **Installation & Setup**
- **Basic Messaging (Producer/Consumer)**
- **Exchanges & Queues**
- **Routing & Topics**
- **Work Queues**
- **RPC with RabbitMQ**
- **Advanced Patterns**

## 🛠️ Getting Started

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/rabbitmq-tutorial.git
    cd rabbitmq-tutorial
    ```

2. **Install RabbitMQ:**
    - [Official Installation Guide](https://www.rabbitmq.com/download.html)
    - run the script `rabbitMQ-install.sh`

3. **Common Commands**
    - Accessing the rabbitmq managment console

        ```bash
        sudo rabbitmq-plugins enable rabbitmq_management
        sudo chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/
        ```

        After the above commands open - <http://localhost:15672>
    - Accessing the queues using terminal

        ```bash
        sudo rabbitmqctl list_queues 
        ```

3. **Run the examples:**
    - Each folder contains a README with instructions.

## 📖 Prerequisites

- Basic knowledge of programming (Python)
- Docker (optional, for containerized setup)

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

Happy Messaging! 📨
