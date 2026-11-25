---
name: distributed-systems
description: Apply distributed systems patterns including idempotency, saga pattern, outbox pattern, eventual consistency, and CQRS to build reliable, consistent distributed services.
invoke_when: Use when designing multi-service architectures, handling distributed transactions, dealing with data consistency across services, or discussing event-driven systems, idempotency, sagas, outbox pattern, or CQRS.
---

# Distributed Systems Patterns

## Core Principle

In a distributed system, you cannot have both strong consistency and high availability during a network partition (CAP theorem). Design for eventual consistency where possible, and use patterns that make the system correct even when components fail independently.

---

## 1. Idempotency

**What it does:** Ensures that performing the same operation multiple times produces the same result as performing it once. This is essential because in distributed systems, messages can be delivered more than once.

**When to apply:** Every mutation endpoint in your API. Every message consumer. Every payment or state-changing operation.

### Idempotency Key Pattern for APIs

The client generates a unique key and sends it with the request. The server stores the result keyed by this value and returns the stored result on duplicate requests.

```typescript
// Client sends: POST /v1/charges
// Header: Idempotency-Key: idem_a1b2c3d4

async function handleChargeRequest(req: Request): Promise<Response> {
  const idempotencyKey = req.headers['idempotency-key'];
  if (!idempotencyKey) {
    return errorResponse(400, 'Idempotency-Key header is required');
  }

  // Check if we already processed this key
  const existing = await idempotencyStore.get(idempotencyKey);
  if (existing) {
    if (existing.status === 'processing') {
      return errorResponse(409, 'Request is already being processed');
    }
    return existing.response; // Return the stored response
  }

  // Lock the key to prevent concurrent processing
  await idempotencyStore.set(idempotencyKey, { status: 'processing' });

  try {
    const result = await processCharge(req.body);
    const response = successResponse(201, result);
    await idempotencyStore.set(idempotencyKey, {
      status: 'completed',
      response,
      expiresAt: Date.now() + 24 * 60 * 60 * 1000, // 24h TTL
    });
    return response;
  } catch (error) {
    await idempotencyStore.delete(idempotencyKey); // Allow retry on failure
    throw error;
  }
}
```

### Python Example -- Database-backed Idempotency

```python
from functools import wraps
from datetime import datetime, timedelta

def idempotent(ttl_hours=24):
    def decorator(fn):
        @wraps(fn)
        def wrapper(idempotency_key: str, *args, **kwargs):
            # Check existing result
            existing = db.idempotency_keys.find_one({"key": idempotency_key})
            if existing and existing["status"] == "completed":
                return existing["result"]
            if existing and existing["status"] == "processing":
                raise ConflictError("Request already in progress")

            # Lock
            db.idempotency_keys.insert_one({
                "key": idempotency_key,
                "status": "processing",
                "created_at": datetime.utcnow(),
            })

            try:
                result = fn(*args, **kwargs)
                db.idempotency_keys.update_one(
                    {"key": idempotency_key},
                    {"$set": {
                        "status": "completed",
                        "result": result,
                        "expires_at": datetime.utcnow() + timedelta(hours=ttl_hours),
                    }},
                )
                return result
            except Exception:
                db.idempotency_keys.delete_one({"key": idempotency_key})
                raise
        return wrapper
    return decorator
```

### Rules for Idempotency Keys

- Keys must be client-generated UUIDs (UUIDv4 or UUIDv7).
- Store results for at least 24 hours before expiring.
- Use a database unique constraint on the key to prevent races.
- Return the same HTTP status code and body for duplicate requests.
- If the original request failed, delete the key so the client can retry.

---

## 2. Saga Pattern

**What it does:** Manages distributed transactions across multiple services by breaking them into a sequence of local transactions, each with a compensating action (rollback).

**When to apply:** Any business process that spans multiple services and must be logically atomic (e.g., order placement that involves inventory, payment, and shipping).

### Orchestration (Centralized Coordinator)

A single saga orchestrator service directs each step and handles compensation on failure.

```
Orchestrator -> InventoryService.reserve()
             -> PaymentService.charge()
             -> ShippingService.schedule()

If PaymentService.charge() fails:
  Orchestrator -> InventoryService.releaseReservation()  // compensate
```

```typescript
class OrderSaga {
  async execute(order: Order): Promise<SagaResult> {
    const steps: SagaStep[] = [
      {
        action: () => inventoryService.reserve(order.items),
        compensate: () => inventoryService.release(order.items),
      },
      {
        action: () => paymentService.charge(order.customerId, order.total),
        compensate: () => paymentService.refund(order.customerId, order.total),
      },
      {
        action: () => shippingService.schedule(order.id, order.address),
        compensate: () => shippingService.cancel(order.id),
      },
    ];

    const completedSteps: SagaStep[] = [];

    for (const step of steps) {
      try {
        await step.action();
        completedSteps.push(step);
      } catch (error) {
        // Compensate in reverse order
        for (const completed of completedSteps.reverse()) {
          await completed.compensate();
        }
        return { status: 'failed', error };
      }
    }

    return { status: 'completed' };
  }
}
```

### Choreography (Event-Driven, Decentralized)

Each service listens for events and triggers the next step. No central coordinator.

```
OrderService emits OrderCreated
  -> InventoryService listens, reserves stock, emits StockReserved
    -> PaymentService listens, charges card, emits PaymentCompleted
      -> ShippingService listens, schedules delivery, emits OrderShipped

If PaymentService fails, it emits PaymentFailed
  -> InventoryService listens, releases stock
```

### When to Use Which

| Factor | Orchestration | Choreography |
|---|---|---|
| Number of steps | 4+ steps | 2-3 steps |
| Visibility | Easy to trace and debug | Hard to follow event chains |
| Coupling | Services depend on orchestrator | Services are fully decoupled |
| Complexity | Logic centralized | Logic distributed across services |
| Best for | Complex business workflows | Simple event chains |

---

## 3. Outbox Pattern

**What it does:** Guarantees that a database write and a message/event publication happen atomically, preventing lost or duplicate messages.

**When to apply:** Any time you need to update a database AND publish an event. This is the correct solution to the dual-write problem.

### How It Works

1. Write the business data AND the outbox message in the same database transaction.
2. A separate process (poller or CDC) reads the outbox table and publishes messages to the message broker.
3. After successful publish, mark the outbox row as sent.

```sql
-- Step 1: Write both in one transaction
BEGIN;

INSERT INTO orders (id, customer_id, total, status)
VALUES ('ord_123', 'cust_456', 99.99, 'created');

INSERT INTO outbox (id, aggregate_type, aggregate_id, event_type, payload, created_at)
VALUES (
  'evt_789',
  'Order',
  'ord_123',
  'OrderCreated',
  '{"orderId": "ord_123", "customerId": "cust_456", "total": 99.99}',
  NOW()
);

COMMIT;
```

```python
# Step 2: Outbox poller (runs on a schedule, e.g., every 1 second)
def poll_and_publish():
    unsent = db.execute(
        "SELECT * FROM outbox WHERE sent_at IS NULL ORDER BY created_at LIMIT 100"
    )
    for event in unsent:
        try:
            message_broker.publish(
                topic=f"{event.aggregate_type}.{event.event_type}",
                key=event.aggregate_id,
                value=event.payload,
            )
            db.execute(
                "UPDATE outbox SET sent_at = NOW() WHERE id = %s", (event.id,)
            )
        except Exception as e:
            log.warning(f"Failed to publish {event.id}, will retry: {e}")
            break  # Preserve ordering -- stop on first failure
```

**Key rules:**
- The outbox table and the business table must be in the same database.
- Consumers must be idempotent because the poller may publish a message more than once (at-least-once delivery).
- Use Change Data Capture (CDC) with Debezium for higher throughput instead of polling.

---

## 4. Eventual Consistency

**What it does:** Accepts that data across services will be temporarily inconsistent but will converge to a consistent state given enough time.

**When to apply:** Most inter-service data flows. Strong consistency across services is extremely expensive and fragile. Reserve strong consistency for within a single service/database.

### Documenting Consistency Guarantees

For every service-to-service data flow, document:

1. **What is the consistency window?** (e.g., "Order status propagates to the analytics service within 5 seconds under normal load.")
2. **What happens during inconsistency?** (e.g., "Dashboard may show stale order counts for up to 5 seconds.")
3. **How do you detect inconsistency?** (e.g., "Reconciliation job runs hourly and alerts if counts diverge by more than 1%.")
4. **How do you resolve inconsistency?** (e.g., "Re-publish events from the outbox for the affected time window.")

### Reconciliation Pattern

```python
def reconcile_orders():
    """Run hourly to detect and fix inconsistencies between OrderService and AnalyticsService."""
    order_counts = order_service.get_counts_by_status(since=hours_ago(2))
    analytics_counts = analytics_service.get_counts_by_status(since=hours_ago(2))

    for status, expected_count in order_counts.items():
        actual_count = analytics_counts.get(status, 0)
        if abs(expected_count - actual_count) > expected_count * 0.01:
            alert(f"Inconsistency detected: {status} orders expected={expected_count} actual={actual_count}")
            # Trigger re-sync for affected records
            order_service.republish_events(status=status, since=hours_ago(2))
```

---

## 5. CQRS (Command Query Responsibility Segregation)

**What it does:** Uses separate models (and often separate databases) for reading and writing data.

**When to apply:** Use CQRS when read and write patterns differ significantly. Do NOT use it by default -- it adds significant complexity.

### When CQRS is Worth the Complexity

| Signal | Use CQRS | Do Not Use CQRS |
|---|---|---|
| Read/write ratio | >10:1 reads to writes | Roughly equal reads and writes |
| Read model shape | Very different from write model | Same shape as write model |
| Scale requirements | Reads must scale independently | Uniform scaling is sufficient |
| Query complexity | Complex aggregations across entities | Simple lookups by ID |
| Team size | Team can maintain two models | Small team, keep it simple |

### Practical Example

```typescript
// Write side -- optimized for consistency and validation
class OrderCommandHandler {
  async createOrder(cmd: CreateOrderCommand): Promise<void> {
    const order = new Order(cmd);
    order.validate();
    await this.orderRepository.save(order);          // Write to normalized DB
    await this.eventBus.publish(new OrderCreated(order)); // Publish event
  }
}

// Read side -- optimized for query performance
class OrderQueryHandler {
  // Reads from a denormalized read-optimized store (e.g., Elasticsearch, Redis)
  async getOrderDashboard(customerId: string): Promise<OrderDashboard> {
    return this.readStore.query({
      customerId,
      includes: ['orderSummary', 'recentActivity', 'spendingTrends'],
    });
  }
}

// Projection -- keeps the read model in sync
class OrderProjection {
  async onOrderCreated(event: OrderCreated): Promise<void> {
    await this.readStore.upsert({
      id: event.orderId,
      customerId: event.customerId,
      status: 'created',
      total: event.total,
      createdAt: event.timestamp,
    });
  }
}
```

---

## Checklist Before Shipping a Distributed System

- [ ] Every API mutation endpoint accepts an idempotency key.
- [ ] Multi-service workflows use the saga pattern with explicit compensation.
- [ ] Database writes + event publishing use the outbox pattern (no dual writes).
- [ ] Consistency windows are documented for every inter-service data flow.
- [ ] Reconciliation jobs exist to detect and correct drift.
- [ ] CQRS is only used where read/write asymmetry justifies the complexity.
- [ ] Every message consumer is idempotent.
- [ ] Saga state is persisted so it survives process restarts.
