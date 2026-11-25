---
name: rabbitmq-async
description: "Implement asynchronous messaging using RabbitMQ for distributed systems."
---

# RabbitMQ Async Messaging

## Overview
RabbitMQ is a message broker implementing advanced message queuing protocols for asynchronous communication between services. This skill should be invoked when building async message-based systems, task queues, or event-driven architectures that require reliable message delivery between distributed components.

## Core Principles
- **Exchange Types**: Understand direct, fanout, topic, and headers exchanges
- **Message Acknowledgment**: Use manual acknowledgments for reliable processing
- **Queue Design**: Design queues with DLQ (Dead Letter Queue) for failed messages
- **Publisher Confirms**: Enable publisher confirms for delivery guarantees

## Preparation Checklist
- [ ] Set up RabbitMQ instance (local Docker or cloud service)
- [ ] Choose client library (amqplib, amqp.node, pika for Python)
- [ ] Define message format (JSON, Protobuf, or plain text)
- [ ] Plan exchange and queue topology

## Step-by-Step Process
1. **Connect**: Establish connection to RabbitMQ broker
2. **Declare**: Create exchanges and queues with appropriate bindings
3. **Publish**: Implement publisher to send messages to exchanges
4. **Consume**: Implement consumer with message handlers
5. **Acknowledge**: Process messages and send acknowledgments
6. **Handle Failures**: Configure DLQ for messages that fail processing

## Do's and Don'ts
- ✅ **Do** use dead letter queues for failed message handling
- ✅ **Do** implement idempotent message processing
- ✅ **Do** set appropriate TTL for queue messages
- ❌ **Don't** forget to close connections - causes resource leaks
- ❌ **Don't** process synchronously - block message consumption
- ❌ **Don't** ignore message ordering requirements in design

## Anti-Patterns
- **Fire and Forget**: Publishing without confirms or acknowledgments
- **No DLQ**: Messages lost when processing fails
- **Synchronous Processing**: Blocking consumer on long operations
- **Connection Leak**: Not properly managing connection lifecycle
