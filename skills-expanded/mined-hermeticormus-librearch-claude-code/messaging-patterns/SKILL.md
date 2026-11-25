---
name: "messaging-patterns"
description: "Messaging patterns with code: RabbitMQ topic exchanges with dead letter queues, SNS to SQS fan-out in AWS CDK, Kafka consumer groups with idempotency, and competing consumers. Use when wiring services together through a message broker."
---

# Messaging Patterns

> Named patterns with code for RabbitMQ topology, Kafka consumer group, SQS with DLQ, competing consumers, message idempotency, and dead letter queue handling.

## Patterns

### Pattern: RabbitMQ Topic Exchange with DLQ (Python)

```python
import pika
import json

connection = pika.BlockingConnection(pika.URLParameters("amqp://user:pass@localhost/"))
channel = connection.channel()

# Dead letter exchange — receives rejected/expired messages
channel.exchange_declare(exchange="dlx", exchange_type="direct", durable=True)
channel.queue_declare(queue="orders.dlq", durable=True)
channel.queue_bind(queue="orders.dlq", exchange="dlx", routing_key="orders.inventory")

# Main exchange
channel.exchange_declare(exchange="orders", exchange_type="topic", durable=True)

# Main queue with DLQ configuration
channel.queue_declare(
    queue="orders.inventory",
    durable=True,
    arguments={
        "x-dead-letter-exchange": "dlx",
        "x-dead-letter-routing-key": "orders.inventory",
        "x-message-ttl": 86400000,  # 24h TTL
        "x-max-length": 100000,     # Backpressure: reject when full
    }
)
channel.queue_bind(
    queue="orders.inventory",
    exchange="orders",
    routing_key="order.*.placed"    # Matches order.v1.placed, order.v2.placed
)

# Producer
def publish_order_placed(order_id: str, payload: dict):
    channel.basic_publish(
        exchange="orders",
        routing_key="order.v1.placed",
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2,          # Persistent message (survives broker restart)
            message_id=f"order-placed-{order_id}",
            correlation_id=order_id,
        )
    )

# Consumer with manual ACK and prefetch
channel.basic_qos(prefetch_count=5)  # Process 5 at a time — backpressure

def on_message(ch, method, properties, body):
    try:
        event = json.loads(body)
        inventory_service.reserve(event["orderId"], event["items"])
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except InventoryException as e:
        # Requeue=False → goes to DLQ after x-max-delivery-count
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

channel.basic_consume(queue="orders.inventory", on_message_callback=on_message)
channel.start_consuming()
```

### Pattern: SQS + SNS Fan-Out with DLQ (AWS CDK TypeScript)

```typescript
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import { Duration } from 'aws-cdk-lib';

// Dead letter queue — receives messages after 3 failed delivery attempts
const inventoryDlq = new sqs.Queue(this, 'InventoryDLQ', {
  retentionPeriod: Duration.days(14),
  queueName: 'orders-inventory-dlq',
});

// Main consumer queue
const inventoryQueue = new sqs.Queue(this, 'InventoryQueue', {
  visibilityTimeout: Duration.seconds(30),  // Must be > lambda timeout
  deadLetterQueue: {
    queue: inventoryDlq,
    maxReceiveCount: 3,  // Move to DLQ after 3 failed receives
  },
});

// SNS topic for order events
const ordersTopic = new sns.Topic(this, 'OrdersTopic', {
  topicName: 'orders',
});

// Fan-out: both inventory and notification queues receive every order event
ordersTopic.addSubscription(
  new subscriptions.SqsSubscription(inventoryQueue, {
    filterPolicy: {
      eventType: sns.SubscriptionFilter.stringFilter({
        allowlist: ['OrderPlaced', 'OrderCancelled'],
      }),
    },
  })
);

// CloudWatch alarm on DLQ depth
new cloudwatch.Alarm(this, 'InventoryDLQAlarm', {
  metric: inventoryDlq.metricNumberOfMessagesSent(),
  threshold: 1,
  evaluationPeriods: 1,
  alarmDescription: 'Messages arriving in inventory DLQ — consumer is failing',
});
```

### Pattern: Kafka Consumer Group with Idempotency (Java)

```java
@Configuration
public class KafkaConsumerConfig {

    @Bean
    public ConsumerFactory<String, String> consumerFactory() {
        Map<String, Object> props = Map.of(
            ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092",
            ConsumerConfig.GROUP_ID_CONFIG, "inventory-service",
            ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest",
            ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false,  // Manual commit
            ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 50,
            ConsumerConfig.ISOLATION_LEVEL_CONFIG, "read_committed"
        );
        return new DefaultKafkaConsumerFactory<>(props);
    }
}

@Component
public class OrderEventConsumer {

    private final InventoryService inventoryService;
    private final ProcessedEventRepository processedEvents;

    @KafkaListener(topics = "orders.placed", groupId = "inventory-service")
    @Transactional
    public void consume(ConsumerRecord<String, String> record, Acknowledgment ack) {
        String eventId = record.headers().lastHeader("ce_id") != null
            ? new String(record.headers().lastHeader("ce_id").value())
            : record.key() + "-" + record.offset();

        // Idempotency: skip if already processed (at-least-once → effectively-once)
        if (processedEvents.exists(eventId)) {
            log.debug("Skipping duplicate event {}", eventId);
            ack.acknowledge();
            return;
        }

        OrderPlacedEvent event = objectMapper.readValue(record.value(), OrderPlacedEvent.class);
        inventoryService.reserveStock(event.orderId(), event.items());

        processedEvents.save(new ProcessedEvent(eventId, Instant.now()));
        ack.acknowledge();  // Commit offset only after successful processing
    }
}
```

### Pattern: Competing Consumers with RabbitMQ Work Queue

```python
# Multiple consumers on same queue — RabbitMQ round-robins
# Scale by adding more consumer processes (not by adding queues)

WORKERS = 4  # Each worker is a separate process / Kubernetes pod

def worker_main():
    conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    ch = conn.channel()
    ch.queue_declare(queue="email-jobs", durable=True)

    # Prefetch 1: worker must ACK before receiving next message
    # Prevents fast workers from stealing from slow workers
    ch.basic_qos(prefetch_count=1)

    ch.basic_consume(queue="email-jobs", on_message_callback=process_email_job)
    ch.start_consuming()  # Blocking — each worker runs this in its own process

def process_email_job(ch, method, properties, body):
    job = json.loads(body)
    email_service.send(job["to"], job["subject"], job["body"])
    ch.basic_ack(delivery_tag=method.delivery_tag)
```

## Anti-Patterns

### Anti-Pattern: One Queue Per Service Pair

Creating a dedicated queue for every sender-receiver pair: `order-service-to-inventory`, `order-service-to-notification`, etc. With 10 services, this creates O(n²) queues. Adding a new consumer requires modifying the producer to add a new queue. Brittle, hard to trace.

Fix: use a fan-out exchange (RabbitMQ) or SNS topic (AWS) that multiple consumer queues subscribe to. Producers publish to a topic; consumers subscribe to topics they care about.

### Anti-Pattern: Synchronous Wait After Publishing

```python
# WRONG: publishing message and then immediately querying for its effect
producer.publish("inventory.reserve", order_id)
time.sleep(2)  # Hoping the consumer processed it
result = inventory_db.query(order_id)
```

Messaging is asynchronous by nature. The sleep is a race condition — it will fail under load or when the consumer is busy. Fix: redesign the flow to be event-driven end-to-end, or use request-reply pattern (correlation ID + reply-to queue) if synchronous response is genuinely required.

### Anti-Pattern: Not Configuring DLQ

Messages that fail processing retry forever, consuming consumer capacity on un-processable messages and hiding failures from operators. Every consumer queue must have a DLQ configured.

### Anti-Pattern: Unlimited Prefetch (prefetch_count=0)

With unlimited prefetch, RabbitMQ delivers all messages to the first available consumer. Under load, one consumer instance holds thousands of unprocessed messages in memory while other instances sit idle. Kills even distribution. Set prefetch_count to 1 (slow consumers) to 10-50 (fast consumers).

## References

- Hohpe, Gregor, and Bobby Woolf. _Enterprise Integration Patterns_. Addison-Wesley, 2003.
- RabbitMQ AMQP model: rabbitmq.com/tutorials/amqp-concepts.html
- Kleppmann, Martin. _Designing Data-Intensive Applications_. O'Reilly, 2017. Chapter 11.
- AWS SQS visibility timeout and DLQ: docs.aws.amazon.com/sqs/latest/dg
