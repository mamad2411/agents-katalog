---
name: "event-driven-patterns"
description: "Event-driven patterns with code: CloudEvents envelopes, Kafka producers and idempotent consumers, the outbox pattern, DLQ retry handlers, and Avro schema evolution. Use when publishing or consuming events between services."
---

# Event-Driven Patterns

> Named patterns with code for CloudEvents envelope, Kafka producer/consumer, outbox pattern, saga choreography, DLQ retry, and event schema evolution.

## Patterns

### Pattern: CloudEvents Envelope (TypeScript)

```typescript
import { CloudEvent, HTTP } from 'cloudevents';

// Producing a CloudEvent
function createOrderPlacedEvent(order: Order): CloudEvent<OrderPlacedPayload> {
  return new CloudEvent({
    specversion: '1.0',
    id: crypto.randomUUID(),
    source: '/services/orders',
    type: 'com.example.orders.v1.OrderPlaced',
    datacontenttype: 'application/json',
    time: new Date().toISOString(),
    data: {
      orderId: order.id,
      customerId: order.customerId,
      items: order.items.map(i => ({ productId: i.productId, quantity: i.quantity })),
      totalAmount: order.total.amount,
      currency: order.total.currency,
    },
  });
}

// Sending via HTTP binding (for webhook/event bridge delivery)
const message = HTTP.binary(event);
await fetch(targetUrl, {
  method: 'POST',
  headers: message.headers,
  body: JSON.stringify(message.body),
});
```

### Pattern: Kafka Producer with Acknowledgment (TypeScript)

```typescript
import { Kafka, CompressionTypes, Partitioners } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'order-service',
  brokers: ['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092'],
});

const producer = kafka.producer({
  createPartitioner: Partitioners.DefaultPartitioner,
  idempotent: true,        // Exactly-once semantics at producer level
  maxInFlightRequests: 5,  // Required for idempotent producer
});

await producer.connect();

// Publish with key = orderId to guarantee ordering per order
await producer.send({
  topic: 'orders',
  compression: CompressionTypes.GZIP,
  messages: [
    {
      key: order.id,        // Partition key — all order events go to same partition
      value: JSON.stringify(cloudEvent.data),
      headers: {
        'ce_type': 'com.example.orders.v1.OrderPlaced',
        'ce_id': cloudEvent.id,
        'ce_source': cloudEvent.source,
      },
    },
  ],
});
```

### Pattern: Kafka Consumer with Idempotency Guard (TypeScript)

```typescript
const consumer = kafka.consumer({ groupId: 'inventory-service' });
await consumer.connect();
await consumer.subscribe({ topic: 'orders', fromBeginning: false });

await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    const eventId = message.headers?.['ce_id']?.toString();
    if (!eventId) throw new Error('Missing CloudEvent ID header');

    // Idempotency: skip if already processed
    const alreadyProcessed = await processedEvents.exists(eventId);
    if (alreadyProcessed) {
      console.log(`Skipping duplicate event ${eventId}`);
      return;
    }

    const payload = JSON.parse(message.value!.toString());
    await inventoryService.reserveItems(payload.orderId, payload.items);

    // Mark processed AFTER successful handling
    await processedEvents.add(eventId, { ttlSeconds: 86400 * 7 });
  },
});
```

### Pattern: Outbox Pattern (Java + Spring)

```java
// Domain: aggregate emits event, stored in outbox table in same transaction
@Service
@Transactional
public class OrderApplicationService {

    private final OrderRepository orders;
    private final OutboxRepository outbox;

    public void placeOrder(PlaceOrderCommand cmd) {
        Order order = Order.create(cmd.customerId(), cmd.items());
        orders.save(order);

        // Outbox write is in the SAME transaction as order save
        // Atomicity guaranteed by database — no dual-write problem
        List<DomainEvent> events = order.collectEvents();
        events.forEach(event ->
            outbox.save(OutboxMessage.from(event))
        );
        // No direct broker publish here — relay does that
    }
}

// Outbox relay: polls outbox and publishes to Kafka (or use Debezium CDC)
@Component
@Scheduled(fixedDelay = 500)
public class OutboxRelay {

    private final OutboxRepository outbox;
    private final KafkaTemplate<String, String> kafka;

    public void relay() {
        List<OutboxMessage> pending = outbox.findUnpublished(limit = 100);
        for (OutboxMessage msg : pending) {
            kafka.send(msg.topic(), msg.aggregateId(), msg.payload());
            outbox.markPublished(msg.id());
        }
    }
}
```

### Pattern: DLQ Retry Handler (Java)

```java
// SQS DLQ consumer — inspect, fix, re-enqueue
@SqsListener("${queue.orders.dlq}")
public void handleDeadLetter(String rawMessage, @Header("ApproximateReceiveCount") int receiveCount) {
    try {
        OrderEvent event = objectMapper.readValue(rawMessage, OrderEvent.class);

        // Classify failure type
        if (isDataAnomaly(event)) {
            // Permanent failure: log and discard
            log.error("Permanent DLQ failure for event {}: data anomaly", event.id());
            metrics.increment("dlq.discarded");
            return;
        }

        // Transient failure: re-enqueue to main queue for retry
        sqsTemplate.send(mainQueueUrl, rawMessage);
        metrics.increment("dlq.requeued");

    } catch (Exception e) {
        log.error("DLQ handler failed for message: {}", rawMessage, e);
        metrics.increment("dlq.handler_error");
        // Do not re-throw — message will be re-delivered and loop endlessly
    }
}
```

### Pattern: Event Schema Evolution with Avro

```json
// orders-placed-v1.avsc
{
  "type": "record",
  "name": "OrderPlaced",
  "namespace": "com.example.orders.v1",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "totalAmount", "type": "double"}
  ]
}

// orders-placed-v2.avsc — backward compatible: added optional field with default
{
  "type": "record",
  "name": "OrderPlaced",
  "namespace": "com.example.orders.v2",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "customerId", "type": "string"},
    {"name": "totalAmount", "type": "double"},
    {"name": "currency", "type": "string", "default": "USD"}
  ]
}
```

Register with Confluent Schema Registry using `BACKWARD` compatibility:
```bash
curl -X POST http://schema-registry:8081/subjects/orders-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{"schema": "<avro-json-escaped>", "schemaType": "AVRO"}'
```

## Anti-Patterns

### Anti-Pattern: Publishing Events Inside a Database Transaction

```java
// WRONG: broker publish is outside the transaction — if publish fails, data saved but event lost
@Transactional
public void placeOrder(PlaceOrderCommand cmd) {
    Order order = Order.create(cmd);
    orderRepo.save(order);  // DB write committed
    kafkaTemplate.send("orders", order.id(), event);  // This can fail AFTER commit
    // If Kafka is down: order created, event never published → inconsistency
}
```

Fix: use the outbox pattern. Write to an outbox table in the same transaction. Let a relay publish asynchronously.

### Anti-Pattern: Choreography for Long Multi-Step Sagas

A saga with 7 steps across 7 services using pure choreography: each service reacts to the previous service's event. When step 4 fails, which service is responsible for compensating steps 1-3? The business process is invisible — it exists only as the emergent result of event handlers across 7 codebases.

Fix: use an orchestrator (Temporal, Axon Saga, AWS Step Functions) for sagas with more than 2-3 steps or with compensation requirements.

### Anti-Pattern: Fat Events Carrying Full State

Publishing the entire aggregate state with every event creates tight coupling between producers and consumers. Consumers depend on the producer's internal data model. Every schema change is a breaking change.

Use thin events: carry only the identity and the changed data. Consumers that need more context load it from the producer's API or their own read model.

### Anti-Pattern: No DLQ Monitoring

Teams that set up DLQs but don't alert on them. Failed events accumulate silently. Business operations are dropped without anyone knowing. DLQ depth > 0 must be an alert, not a dashboard to check manually.

## References

- Hohpe, Gregor, and Bobby Woolf. _Enterprise Integration Patterns_. Addison-Wesley, 2003.
- Richardson, Chris. microservices.io/patterns/data/transactional-outbox.html
- CNCF CloudEvents specification v1.0: cloudevents.io/docs/spec
- Confluent Schema Registry compatibility: docs.confluent.io/platform/current/schema-registry
- Kleppmann, Martin. _Designing Data-Intensive Applications_. O'Reilly, 2017. Chapter 11.
