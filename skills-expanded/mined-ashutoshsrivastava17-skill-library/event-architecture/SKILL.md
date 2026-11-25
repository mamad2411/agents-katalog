---
name: event-architecture
description: >
  Design event-driven systems — event schemas, message broker selection,
  ordering guarantees, dead letter queues, saga patterns, and idempotency.
  TRIGGER when: user says /event-architecture, needs to design event-driven
  systems, or asks about message queues, pub/sub, or async processing.
argument-hint: "[system or workflow to make event-driven]"
user-invocable: true
---

# Event-Driven Architecture

You are a distributed systems engineer. Design event architectures that are reliable, scalable, and debuggable.

## Process

### Step 1: Identify Event-Driven Fit

| Signal | Event-Driven Suits | Request-Response Suits |
|--------|-------------------|----------------------|
| Coupling | Loose coupling between services | Tight coupling OK |
| Latency | Eventual consistency acceptable | Immediate response required |
| Fan-out | Multiple consumers per event | Single consumer |
| Reliability | Must not lose events | Retry on failure is fine |
| Scale | Variable, bursty workloads | Predictable load |

### Step 2: Design Event Schema

```json
{
  "event_id": "uuid",
  "event_type": "order.placed",
  "version": "1.2",
  "timestamp": "2025-03-15T10:30:00Z",
  "source": "order-service",
  "correlation_id": "uuid",
  "data": {
    "order_id": "12345",
    "customer_id": "67890",
    "total": 99.99
  },
  "metadata": {
    "trace_id": "abc123",
    "environment": "production"
  }
}
```

**Schema rules:**
- Use past tense for event names (`order.placed`, not `place.order`)
- Version all schemas — breaking changes require new versions
- Include `event_id` for idempotency
- Include `correlation_id` for distributed tracing
- Keep events self-contained — consumers shouldn't need to call back

### Step 3: Select Message Broker

| Broker | Ordering | Retention | Scale | Best For |
|--------|---------|-----------|-------|---------|
| Kafka | Per-partition | Days-forever | Very high | Event streaming, log |
| RabbitMQ | Per-queue | Until consumed | High | Task queues, RPC |
| SQS | Best-effort (FIFO available) | 14 days | Very high | AWS-native, simple queues |
| SNS + SQS | Fan-out | Via SQS | Very high | Pub/sub + queue combo |
| Pub/Sub (GCP) | Per-key | 31 days | Very high | GCP-native streaming |
| NATS | Per-subject | Configurable | Very high | Low-latency, lightweight |

### Step 4: Handle Reliability

| Concern | Solution |
|---------|---------|
| Message loss | At-least-once delivery + idempotent consumers |
| Duplicate processing | Idempotency key (event_id) + processed event log |
| Ordering | Partition by entity ID (e.g., order_id) |
| Poison messages | Dead letter queue (DLQ) after N retries |
| Consumer lag | Autoscaling consumers, monitoring lag metrics |
| Schema evolution | Schema registry, backward-compatible changes |

### Step 5: Design Saga Patterns (if multi-step)

| Pattern | How | Use When |
|---------|-----|----------|
| Choreography | Each service emits events, others react | Simple flows, few steps |
| Orchestration | Central coordinator directs steps | Complex flows, many steps |

**Compensating transactions:**

| Step | Action | Compensation (on failure) |
|------|--------|--------------------------|
| 1. Reserve inventory | `inventory.reserved` | `inventory.released` |
| 2. Charge payment | `payment.charged` | `payment.refunded` |
| 3. Ship order | `order.shipped` | `shipment.cancelled` |

### Step 6: Plan Observability

| What to Monitor | How |
|----------------|-----|
| Consumer lag | Broker metrics (Kafka consumer group lag) |
| Processing time | Histogram per event type |
| Error rate | DLQ depth, failed event count |
| Throughput | Events/second per topic/queue |
| End-to-end latency | Correlation ID tracing from publish to final consume |

## Output Format

```markdown
## Event Architecture: [System]

### Events: [Event catalog with schemas]
### Broker: [Selection with rationale]
### Reliability: [Delivery guarantees, idempotency approach]
### Sagas: [Multi-step workflow design, if applicable]
### Monitoring: [Key metrics]
```

## Quality Checklist

- [ ] Events are self-contained and versioned
- [ ] Consumers are idempotent
- [ ] Dead letter queues handle poison messages
- [ ] Ordering is guaranteed where needed (partition key)
- [ ] Schema evolution strategy defined
- [ ] Monitoring covers lag, errors, and throughput
- [ ] Compensating transactions exist for saga steps

## Edge Cases

- For CQRS, separate command and query models with events bridging them
- If events are large (>1MB), store payload externally and reference by ID
- For cross-region, plan for event replication latency
- If exactly-once semantics are required, use transactional outbox pattern
- For debugging, build an event replay capability for dev/staging
