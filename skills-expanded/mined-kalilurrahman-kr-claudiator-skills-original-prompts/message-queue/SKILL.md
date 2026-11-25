---
name: message-queue
description: Design message queue architectures using Kafka, RabbitMQ, or SQS. Outputs topic/queue design, producer/consumer patterns, dead letter queues, ordering guarantees, and scaling configuration.
argument-hint: [use case, message volume, ordering requirements, delivery guarantees, technology choice]
allowed-tools: Read, Write, Bash
---

# Message Queue Architecture

Design reliable, scalable messaging systems for decoupled async communication. Choose the right technology, guarantee the right semantics, and handle failures gracefully.

## Technology Decision Matrix

| Requirement | Kafka | RabbitMQ | SQS | Redis Streams |
|-------------|-------|----------|-----|---------------|
| High throughput (>100k msg/s) | ✅ Best | ⚠️ Medium | ⚠️ Medium | ✅ Good |
| Message replay / audit | ✅ Built-in | ❌ No | ❌ No | ✅ Limited |
| Complex routing | ⚠️ Limited | ✅ Best | ⚠️ Topic filter | ❌ No |
| Exactly-once delivery | ✅ Transactions | ❌ Hard | ⚠️ With dedup | ❌ No |
| Fan-out to many consumers | ✅ Consumer groups | ✅ Exchange | ✅ SNS+SQS | ✅ Groups |
| Serverless / managed | ✅ Confluent | ✅ CloudAMQP | ✅ Native AWS | ✅ ElastiCache |
| Simple queue (single consumer) | ⚠️ Overkill | ✅ Good | ✅ Best | ✅ Good |

## Process

1. **Define message contracts** — schema, versioning, payload size.
2. **Choose delivery semantics** — at-most-once, at-least-once, exactly-once.
3. **Design topics/queues** — naming, partitioning, routing keys.
4. **Plan consumer groups** — parallelism, ordering constraints.
5. **Configure DLQ** — dead letter handling, retry limits.
6. **Set retention** — storage vs. replay requirements.
7. **Implement idempotent consumers** — handle redelivery safely.
8. **Monitor lag** — consumer group lag is the critical metric.

## Output Format

### Kafka Design

```python
# kafka_producer.py
from confluent_kafka import Producer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import json
import uuid
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

@dataclass
class OrderCreatedEvent:
    event_id: str
    order_id: str
    user_id: str
    total_cents: int
    items: list[dict]
    created_at: str
    schema_version: str = "1.0"

class KafkaEventProducer:
    def __init__(self, bootstrap_servers: str, schema_registry_url: str = None):
        self._producer = Producer({
            "bootstrap.servers": bootstrap_servers,
            "acks": "all",                    # Wait for all replicas
            "enable.idempotence": True,       # Exactly-once semantics
            "max.in.flight.requests.per.connection": 5,
            "retries": 2147483647,            # Retry forever
            "delivery.timeout.ms": 30000,
            "compression.type": "snappy",
            "batch.size": 65536,              # 64KB batches
            "linger.ms": 5,                   # Wait 5ms to batch
        })
        
        self._dlq_topic = "dlq-events"
    
    def publish(
        self,
        topic: str,
        event: dict,
        key: str = None,
        headers: dict = None
    ) -> None:
        """Publish event with delivery guarantee."""
        
        # Add standard envelope fields
        envelope = {
            **event,
            "event_id": event.get("event_id") or str(uuid.uuid4()),
            "published_at": datetime.now(timezone.utc).isoformat(),
        }
        
        kafka_headers = []
        if headers:
            for k, v in headers.items():
                kafka_headers.append((k, str(v).encode()))
        
        def delivery_callback(err, msg):
            if err:
                logger.error(
                    f"Message delivery failed: {err}",
                    extra={"topic": topic, "key": key}
                )
                # Send to DLQ
                self._send_to_dlq(topic, key, envelope, str(err))
            else:
                logger.debug(
                    f"Message delivered to {msg.topic()} [{msg.partition()}] @{msg.offset()}"
                )
        
        self._producer.produce(
            topic=topic,
            key=key.encode() if key else None,
            value=json.dumps(envelope).encode(),
            headers=kafka_headers,
            on_delivery=delivery_callback
        )
    
    def flush(self, timeout: float = 10.0):
        remaining = self._producer.flush(timeout=timeout)
        if remaining > 0:
            raise TimeoutError(f"{remaining} messages not delivered after {timeout}s")
    
    def _send_to_dlq(self, original_topic: str, key: str, event: dict, error: str):
        dlq_event = {
            "original_topic": original_topic,
            "original_key": key,
            "original_event": event,
            "error": error,
            "failed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._producer.produce(
            topic=self._dlq_topic,
            key=key.encode() if key else None,
            value=json.dumps(dlq_event).encode()
        )


# kafka_consumer.py
from confluent_kafka import Consumer, KafkaError, TopicPartition
import signal
import threading

class KafkaEventConsumer:
    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str,
        topics: list[str],
        max_poll_interval_ms: int = 300000
    ):
        self._consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,        # Manual commit for reliability
            "max.poll.interval.ms": max_poll_interval_ms,
            "session.timeout.ms": 30000,
            "heartbeat.interval.ms": 3000,
            "fetch.min.bytes": 1,
            "fetch.max.wait.ms": 500,
        })
        
        self._consumer.subscribe(topics)
        self._running = True
    
    def consume(self, handler, batch_size: int = 10, timeout_ms: int = 1000):
        """Process messages with at-least-once delivery semantics."""
        
        while self._running:
            messages = self._consumer.consume(
                num_messages=batch_size,
                timeout=timeout_ms / 1000
            )
            
            if not messages:
                continue
            
            # Process batch
            failed_offsets = []
            for msg in messages:
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error(f"Consumer error: {msg.error()}")
                    continue
                
                try:
                    event = json.loads(msg.value())
                    handler(event, msg.headers() or [])
                except Exception as e:
                    logger.error(
                        f"Failed to process message: {e}",
                        extra={
                            "topic": msg.topic(),
                            "partition": msg.partition(),
                            "offset": msg.offset(),
                        }
                    )
                    # Don't commit this offset — will be reprocessed
                    failed_offsets.append((msg.topic(), msg.partition(), msg.offset()))
                    continue
            
            # Commit offsets for successfully processed messages
            if not failed_offsets:
                self._consumer.commit(asynchronous=False)
    
    def stop(self):
        self._running = False
        self._consumer.close()


# Topic configuration
TOPIC_CONFIG = {
    "orders.created": {
        "partitions": 12,           # Allows 12 parallel consumers
        "replication_factor": 3,
        "retention.ms": 7 * 24 * 60 * 60 * 1000,  # 7 days
        "cleanup.policy": "delete",
        "compression.type": "snappy",
        "min.insync.replicas": 2,   # Requires 2 replicas to ack
    },
    "orders.status-updates": {
        "partitions": 6,
        "replication_factor": 3,
        "retention.ms": 3 * 24 * 60 * 60 * 1000,  # 3 days
    },
    "dlq-events": {
        "partitions": 3,
        "replication_factor": 3,
        "retention.ms": 30 * 24 * 60 * 60 * 1000,  # 30 days for debugging
    }
}
```

### RabbitMQ Design

```python
# rabbitmq.py
import pika
import json
import time
from typing import Callable

class RabbitMQSetup:
    """Exchange + queue topology for order processing."""
    
    def __init__(self, connection_url: str):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(connection_url)
        )
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)  # One message at a time per consumer
    
    def setup_topology(self):
        """Declare exchanges, queues, and bindings."""
        
        # Dead Letter Exchange
        self.channel.exchange_declare(
            exchange="dlx",
            exchange_type="direct",
            durable=True
        )
        
        # Dead Letter Queue
        self.channel.queue_declare(
            queue="dead-letter",
            durable=True,
            arguments={"x-queue-type": "quorum"}  # Highly available
        )
        self.channel.queue_bind(
            exchange="dlx",
            queue="dead-letter",
            routing_key="#"
        )
        
        # Main exchange (topic routing)
        self.channel.exchange_declare(
            exchange="orders",
            exchange_type="topic",
            durable=True
        )
        
        # Order processing queue (workers)
        self.channel.queue_declare(
            queue="order-processor",
            durable=True,
            arguments={
                "x-queue-type": "quorum",
                "x-dead-letter-exchange": "dlx",
                "x-dead-letter-routing-key": "order-processor",
                "x-message-ttl": 600000,  # 10 min TTL
            }
        )
        self.channel.queue_bind(
            exchange="orders",
            queue="order-processor",
            routing_key="order.created"
        )
        
        # Notification queue (fan-out)
        self.channel.queue_declare(
            queue="order-notifications",
            durable=True,
            arguments={
                "x-queue-type": "quorum",
                "x-dead-letter-exchange": "dlx",
            }
        )
        self.channel.queue_bind(
            exchange="orders",
            queue="order-notifications",
            routing_key="order.*"  # All order events
        )


class RabbitMQProducer:
    def __init__(self, channel):
        self.channel = channel
    
    def publish(self, routing_key: str, event: dict, priority: int = 0):
        self.channel.basic_publish(
            exchange="orders",
            routing_key=routing_key,
            body=json.dumps(event).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,  # Survive broker restart
                content_type="application/json",
                message_id=event.get("event_id"),
                timestamp=int(time.time()),
                priority=priority,
            )
        )


class RabbitMQConsumer:
    def __init__(self, channel, queue: str, max_retries: int = 3):
        self.channel = channel
        self.queue = queue
        self.max_retries = max_retries
    
    def consume(self, handler: Callable):
        def callback(ch, method, properties, body):
            retry_count = int(
                (properties.headers or {}).get("x-retry-count", 0)
            )
            
            try:
                event = json.loads(body)
                handler(event)
                ch.basic_ack(delivery_tag=method.delivery_tag)
                
            except Exception as e:
                logger.error(f"Processing failed (attempt {retry_count + 1}): {e}")
                
                if retry_count < self.max_retries:
                    # Requeue with incremented retry count
                    headers = properties.headers or {}
                    headers["x-retry-count"] = retry_count + 1
                    
                    # Delay retry with exponential backoff
                    delay_ms = 1000 * (2 ** retry_count)  # 1s, 2s, 4s
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                    
                    # Republish with delay (requires rabbitmq-delayed-message-exchange)
                    self.channel.basic_publish(
                        exchange="orders",
                        routing_key=method.routing_key,
                        body=body,
                        properties=pika.BasicProperties(
                            headers={**headers, "x-delay": delay_ms},
                            delivery_mode=pika.DeliveryMode.Persistent,
                        )
                    )
                else:
                    # Max retries exceeded — send to DLQ
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=callback
        )
        self.channel.start_consuming()
```

### SQS + SNS (AWS)

```python
# sqs_sns.py
import boto3
import json
import uuid
from datetime import datetime, timezone

class SQSConsumer:
    def __init__(self, queue_url: str, max_messages: int = 10):
        self.sqs = boto3.client("sqs")
        self.queue_url = queue_url
        self.max_messages = max_messages
    
    def process(self, handler: callable, delete_on_success: bool = True):
        while True:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=self.max_messages,
                WaitTimeSeconds=20,          # Long polling — avoid empty responses
                MessageAttributeNames=["All"],
                AttributeNames=["ApproximateReceiveCount"]
            )
            
            for message in response.get("Messages", []):
                receive_count = int(
                    message.get("Attributes", {}).get("ApproximateReceiveCount", 1)
                )
                
                try:
                    # SNS wraps the original message
                    body = json.loads(message["Body"])
                    if "Message" in body:  # From SNS
                        event = json.loads(body["Message"])
                    else:
                        event = body
                    
                    handler(event)
                    
                    if delete_on_success:
                        self.sqs.delete_message(
                            QueueUrl=self.queue_url,
                            ReceiptHandle=message["ReceiptHandle"]
                        )
                
                except Exception as e:
                    logger.error(f"Processing failed (receive #{receive_count}): {e}")
                    # Message becomes visible again after VisibilityTimeout
                    # SQS auto-moves to DLQ after maxReceiveCount


# Infrastructure as code (CDK/Terraform equivalent in Python)
def create_queue_infrastructure():
    sqs = boto3.client("sqs")
    
    # DLQ first
    dlq = sqs.create_queue(
        QueueName="orders-dlq.fifo",
        Attributes={
            "FifoQueue": "true",
            "MessageRetentionPeriod": str(14 * 24 * 3600),  # 14 days
        }
    )
    dlq_arn = sqs.get_queue_attributes(
        QueueUrl=dlq["QueueUrl"],
        AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]
    
    # Main queue
    main_queue = sqs.create_queue(
        QueueName="orders.fifo",
        Attributes={
            "FifoQueue": "true",
            "ContentBasedDeduplication": "true",
            "VisibilityTimeout": "300",      # 5 min processing timeout
            "MessageRetentionPeriod": str(4 * 24 * 3600),  # 4 days
            "RedrivePolicy": json.dumps({
                "deadLetterTargetArn": dlq_arn,
                "maxReceiveCount": "3"       # Move to DLQ after 3 failures
            })
        }
    )
```

### Idempotent Consumer Pattern

```python
# idempotent_consumer.py
import redis
from functools import wraps

class IdempotencyStore:
    def __init__(self, redis_client, ttl: int = 86400):
        self.redis = redis_client
        self.ttl = ttl
    
    def is_processed(self, event_id: str) -> bool:
        return bool(self.redis.exists(f"processed:{event_id}"))
    
    def mark_processed(self, event_id: str):
        self.redis.setex(f"processed:{event_id}", self.ttl, "1")


def idempotent(idempotency_store: IdempotencyStore):
    """Decorator: skip duplicate events."""
    def decorator(func):
        @wraps(func)
        def wrapper(event: dict, *args, **kwargs):
            event_id = event.get("event_id")
            if not event_id:
                logger.warning("Event missing event_id — cannot ensure idempotency")
                return func(event, *args, **kwargs)
            
            if idempotency_store.is_processed(event_id):
                logger.info(f"Skipping duplicate event {event_id}")
                return  # Silently skip
            
            result = func(event, *args, **kwargs)
            idempotency_store.mark_processed(event_id)
            return result
        return wrapper
    return decorator


# Usage
store = IdempotencyStore(redis_client)

@idempotent(store)
def handle_order_created(event: dict):
    order = create_order_in_db(event)
    send_confirmation_email(order)
    update_inventory(order)
```

### Monitoring

```yaml
# Prometheus alerting rules for Kafka
groups:
  - name: kafka
    rules:
      - alert: KafkaConsumerLagHigh
        expr: kafka_consumer_group_lag > 10000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Consumer group {{ $labels.group }} lag > 10k on {{ $labels.topic }}"

      - alert: KafkaConsumerLagCritical
        expr: kafka_consumer_group_lag > 100000
        for: 2m
        labels:
          severity: critical

      - alert: KafkaProducerErrors
        expr: rate(kafka_producer_failed_requests_total[5m]) > 0
        labels:
          severity: warning

# SQS CloudWatch alarm (Terraform)
resource "aws_cloudwatch_metric_alarm" "dlq_messages" {
  alarm_name          = "orders-dlq-not-empty"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 60
  threshold           = 0
  alarm_actions       = [aws_sns_topic.alerts.arn]
  dimensions = {
    QueueName = aws_sqs_queue.orders_dlq.name
  }
}
```

## Rules

- **DLQ on every queue** — unprocessable messages must go somewhere, never silently drop.
- **Alert on DLQ depth** — any message in DLQ needs human attention.
- **Idempotent consumers always** — at-least-once delivery means duplicates are inevitable.
- **Include `event_id` in every message** — enables idempotency and deduplication.
- **Version your event schemas** — add `schema_version` to every event.
- **Consumer lag is the SLO** — not throughput. High lag = falling behind.
- **Partition by natural key** — order events by `order_id`, not randomly, for ordering guarantees.
- **Don't share consumer groups across environments** — staging and prod must never compete.
- **Manual offset commit** — auto-commit loses messages on crash before processing completes.
- **Monitor the DLQ** — don't just file and forget DLQ messages, they represent processing failures.
