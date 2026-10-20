---
name: event-driven-architecture
description: Event-driven architecture patterns — Event sourcing, CQRS, saga pattern, eventual consistency, event stream design
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.tf", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# Event-Driven Architecture & Patterns

Event-driven systems decouple services by having them react to events rather than calling each other directly. Build scalable, responsive systems with event sourcing, CQRS, and saga patterns.

---

## Event-Driven Fundamentals

**ALWAYS**:
- Treat events as immutable facts (what happened, not what to do)
- Use event sourcing (append-only event log, replay to reconstruct state)
- Implement CQRS (Command Query Responsibility Segregation) for complex domains
- Handle eventual consistency (accept temporary inconsistency)
- Use event bus for asynchronous event distribution
- Log all events (event store is source of truth)
- Design idempotent handlers (same event processed twice = same result)

**NEVER**:
- Mix events and commands (event = fact, command = request)
- Store mutable snapshots without events (event log is immutable)
- Assume synchronous consistency (expect eventual consistency)
- Lose events (event log is recovery mechanism)
- Create circular event flows (A → B → C → A, infinite loop)

### ✅ GOOD Event-Driven Design

```
Traditional Architecture:
User → API → OrderService (synchronous)
         ↓
         OrderService calls PaymentService (synchronous)
         ↓ (tightly coupled, if Payment fails, whole order fails)

Event-Driven Architecture:
User → API → OrderService (emit event)
         ↓
    ┌────OrderCreatedEvent────┐
    ↓                          ↓
PaymentService            NotificationService
(handle async)            (send email async)
    ↓                          ↓
    PaymentProcessedEvent     OrderConfirmedEvent
    ↓                          ↓
    (decouple, scales independently)
```

---

## Event Sourcing

**ALWAYS**:
- Store every state change as an immutable event
- Never update/delete events (append-only)
- Include: event type, timestamp, aggregate ID, data, version
- Replay events from log to reconstruct current state
- Implement snapshots (periodic state capture for performance)
- Keep event log forever (audit trail + recovery)

**NEVER**:
- Delete events (destroys history & prevents recovery)
- Store snapshots as source of truth (events are truth)
- Assume you'll never need to replay (rebuild from events)

### ✅ GOOD Event Sourcing Setup

```csharp
// Event Sourcing - Store all events, reconstruct state by replaying

public interface IEvent
{
    string EventType { get; }
    Guid AggregateId { get; }
    DateTime OccurredAt { get; }
    int Version { get; }
}

public class OrderCreatedEvent : IEvent
{
    public string EventType => "OrderCreated";
    public Guid AggregateId { get; set; }  // Order ID
    public DateTime OccurredAt { get; set; }
    public int Version { get; set; }  // Event sequence
    
    public Guid CustomerId { get; set; }
    public decimal Amount { get; set; }
    public List<string> Items { get; set; }
}

public class PaymentProcessedEvent : IEvent
{
    public string EventType => "PaymentProcessed";
    public Guid AggregateId { get; set; }  // Order ID
    public DateTime OccurredAt { get; set; }
    public int Version { get; set; }
    
    public decimal Amount { get; set; }
    public string TransactionId { get; set; }
}

// Event Store (append-only log)
public class EventStore
{
    private readonly IDbConnection _db;
    
    public async Task AppendEventAsync(IEvent @event)
    {
        // NEVER update - only INSERT
        await _db.ExecuteAsync(
            @"INSERT INTO Events 
              (AggregateId, EventType, Data, OccurredAt, Version) 
              VALUES (@aggregateId, @eventType, @data, @occurredAt, @version)",
            new
            {
                aggregateId = @event.AggregateId,
                eventType = @event.EventType,
                data = JsonConvert.SerializeObject(@event),
                occurredAt = @event.OccurredAt,
                version = @event.Version
            }
        );
    }
    
    public async Task<List<IEvent>> GetEventsAsync(Guid aggregateId)
    {
        var rows = await _db.QueryAsync<dynamic>(
            @"SELECT EventType, Data FROM Events 
              WHERE AggregateId = @aggregateId 
              ORDER BY Version ASC",
            new { aggregateId }
        );
        
        var events = new List<IEvent>();
        foreach (var row in rows)
        {
            events.Add(DeserializeEvent(row.EventType, row.Data));
        }
        return events;
    }
}

// Aggregate - Reconstruct state by replaying events
public class Order
{
    public Guid Id { get; set; }
    public Guid CustomerId { get; set; }
    public OrderStatus Status { get; set; }  // Derived from events
    public decimal Amount { get; set; }
    public int Version { get; set; }
    
    // Replay events to reconstruct current state
    public static Order LoadFromHistory(List<IEvent> events)
    {
        var order = new Order();
        
        foreach (var @event in events)
        {
            switch (@event)
            {
                case OrderCreatedEvent oc:
                    order.Id = oc.AggregateId;
                    order.CustomerId = oc.CustomerId;
                    order.Amount = oc.Amount;
                    order.Status = OrderStatus.Created;
                    break;
                    
                case PaymentProcessedEvent pp:
                    order.Status = OrderStatus.Paid;
                    break;
                    
                case OrderShippedEvent os:
                    order.Status = OrderStatus.Shipped;
                    break;
            }
            order.Version = @event.Version;
        }
        
        return order;
    }
}

// Create new order (emit event)
public async Task CreateOrderAsync(Guid customerId, decimal amount, List<string> items)
{
    var @event = new OrderCreatedEvent
    {
        AggregateId = Guid.NewGuid(),
        CustomerId = customerId,
        Amount = amount,
        OccurredAt = DateTime.UtcNow,
        Version = 1,
        Items = items
    };
    
    await _eventStore.AppendEventAsync(@event);
    
    // Publish event to bus (other services subscribe)
    await _eventBus.PublishAsync(@event);
}
```

---

## CQRS (Command Query Responsibility Segregation)

**ALWAYS**:
- Separate read model from write model
- Commands change state (CreateOrder, ProcessPayment)
- Queries read state (GetOrder, GetOrderHistory)
- Maintain read model eventually consistent with write model
- Use projections (denormalized views optimized for queries)
- Different schemas for write (normalized) vs. read (denormalized)

**NEVER**:
- Query from normalized write database (slow, complex joins)
- Update read model synchronously (defeats CQRS purpose)
- Assume read model is always up-to-date

### ✅ GOOD CQRS Setup

```csharp
// COMMAND SIDE (Write Model) — Normalized
public class OrderCommandService
{
    private readonly EventStore _eventStore;
    private readonly EventBus _eventBus;
    
    public async Task CreateOrderAsync(CreateOrderCommand cmd)
    {
        // Validate business rules
        if (cmd.Amount <= 0)
            throw new InvalidOperationException("Amount must be positive");
        
        // Emit event (only source of truth)
        var @event = new OrderCreatedEvent
        {
            AggregateId = cmd.OrderId,
            CustomerId = cmd.CustomerId,
            Amount = cmd.Amount,
            OccurredAt = DateTime.UtcNow,
            Version = 1
        };
        
        // Append to event store (immutable)
        await _eventStore.AppendEventAsync(@event);
        
        // Publish to event bus (subscribers will update read model)
        await _eventBus.PublishAsync(@event);
    }
}

// QUERY SIDE (Read Model) — Denormalized for performance
public class OrderReadModel
{
    // Optimized for queries (flattened, indexed)
    public Guid OrderId { get; set; }
    public Guid CustomerId { get; set; }
    public decimal Amount { get; set; }
    public OrderStatus Status { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? PaidAt { get; set; }
    public DateTime? ShippedAt { get; set; }
    
    // Index on these for fast queries
    public string CustomerName { get; set; }  // Denormalized
    public int ItemCount { get; set; }  // Pre-calculated
}

public class OrderQueryService
{
    private readonly IDbConnection _readDb;  // Different database/schema
    
    public async Task<OrderReadModel> GetOrderAsync(Guid orderId)
    {
        // Simple query (no joins, no complex logic)
        return await _readDb.QuerySingleAsync<OrderReadModel>(
            "SELECT * FROM OrderReadModel WHERE OrderId = @orderId",
            new { orderId }
        );
    }
    
    public async Task<List<OrderReadModel>> GetCustomerOrdersAsync(Guid customerId)
    {
        // Fast query using denormalized data
        return await _readDb.QueryAsync<OrderReadModel>(
            "SELECT * FROM OrderReadModel WHERE CustomerId = @customerId ORDER BY CreatedAt DESC",
            new { customerId }
        ).ToList();
    }
}

// Event Handler - Updates read model asynchronously
public class OrderCreatedEventHandler
{
    private readonly IDbConnection _readDb;
    
    public async Task HandleAsync(OrderCreatedEvent @event)
    {
        // Insert into read model (eventually consistent)
        await _readDb.ExecuteAsync(
            @"INSERT INTO OrderReadModel 
              (OrderId, CustomerId, Amount, Status, CreatedAt, ItemCount) 
              VALUES (@orderId, @customerId, @amount, @status, @createdAt, @itemCount)",
            new
            {
                orderId = @event.AggregateId,
                customerId = @event.CustomerId,
                amount = @event.Amount,
                status = nameof(OrderStatus.Created),
                createdAt = @event.OccurredAt,
                itemCount = @event.Items.Count
            }
        );
    }
}
```

---

## Saga Pattern (Distributed Transactions)

**ALWAYS**:
- Use sagas for multi-step business processes (Order → Payment → Shipment)
- Each step is a separate service (Order, Payment, Shipment)
- Communicate via events (not direct calls)
- Implement compensating transactions (rollback on failure)
- Track saga state (orchestrator pattern)
- Idempotent service calls (handle duplicate messages)

**NEVER**:
- Use distributed transactions (2-phase commit, slow & complex)
- Assume all services will succeed (plan for failure)
- Forget to implement rollback logic

### ✅ GOOD Saga Implementation

```csharp
// Saga Orchestrator - Coordinates multi-step order process
public class OrderSaga
{
    public Guid SagaId { get; set; }
    public Guid OrderId { get; set; }
    public SagaStatus Status { get; set; }
    public List<SagaStep> Steps { get; set; } = new();
    
    // Step 1: Create Order
    public async Task StartAsync(CreateOrderCommand cmd)
    {
        Status = SagaStatus.InProgress;
        await _eventBus.PublishAsync(new CreateOrderEvent
        {
            SagaId = SagaId,
            OrderId = cmd.OrderId,
            CustomerId = cmd.CustomerId,
            Amount = cmd.Amount
        });
    }
    
    // Step 2: Process Payment (when Order Created event arrives)
    public async Task OnOrderCreatedAsync(OrderCreatedEvent @event)
    {
        Steps.Add(new SagaStep { StepType = "OrderCreated", Status = "Success" });
        
        // Publish payment command
        await _eventBus.PublishAsync(new ProcessPaymentEvent
        {
            SagaId = SagaId,
            OrderId = @event.AggregateId,
            Amount = @event.Amount,
            CustomerId = @event.CustomerId
        });
    }
    
    // Step 3: Ship Order (when Payment Processed event arrives)
    public async Task OnPaymentProcessedAsync(PaymentProcessedEvent @event)
    {
        Steps.Add(new SagaStep { StepType = "PaymentProcessed", Status = "Success" });
        
        // Publish shipment command
        await _eventBus.PublishAsync(new ShipOrderEvent
        {
            SagaId = SagaId,
            OrderId = @event.AggregateId
        });
    }
    
    // Complete saga (when Order Shipped event arrives)
    public async Task OnOrderShippedAsync(OrderShippedEvent @event)
    {
        Steps.Add(new SagaStep { StepType = "OrderShipped", Status = "Success" });
        Status = SagaStatus.Complete;
        
        // Publish order completed event
        await _eventBus.PublishAsync(new OrderCompletedEvent
        {
            SagaId = SagaId,
            OrderId = @event.AggregateId
        });
    }
    
    // Compensating transactions on failure
    public async Task OnPaymentFailedAsync(PaymentFailedEvent @event)
    {
        Steps.Add(new SagaStep { StepType = "PaymentProcessed", Status = "Failed" });
        Status = SagaStatus.RollingBack;
        
        // Compensate: Cancel the order
        await _eventBus.PublishAsync(new CancelOrderEvent
        {
            SagaId = SagaId,
            OrderId = @event.OrderId,
            Reason = "Payment failed"
        });
    }
}

// Service 1: Order Service
public class OrderService
{
    public async Task CreateOrderAsync(CreateOrderEvent @event)
    {
        // Create order
        await _db.ExecuteAsync(
            "INSERT INTO Orders (OrderId, CustomerId, Amount, Status) VALUES (@id, @cid, @amt, @status)",
            new { id = @event.OrderId, cid = @event.CustomerId, amt = @event.Amount, status = "Created" }
        );
        
        // Emit event
        await _eventBus.PublishAsync(new OrderCreatedEvent
        {
            AggregateId = @event.OrderId,
            CustomerId = @event.CustomerId,
            Amount = @event.Amount
        });
    }
}

// Service 2: Payment Service
public class PaymentService
{
    public async Task ProcessPaymentAsync(ProcessPaymentEvent @event)
    {
        try
        {
            // Charge customer (idempotent — use OrderId as idempotency key)
            var txId = await _paymentGateway.ChargeAsync(
                @event.CustomerId,
                @event.Amount,
                idempotencyKey: @event.OrderId.ToString()
            );
            
            // Emit success event
            await _eventBus.PublishAsync(new PaymentProcessedEvent
            {
                AggregateId = @event.OrderId,
                Amount = @event.Amount,
                TransactionId = txId
            });
        }
        catch (PaymentException ex)
        {
            // Emit failure event
            await _eventBus.PublishAsync(new PaymentFailedEvent
            {
                OrderId = @event.OrderId,
                Reason = ex.Message
            });
        }
    }
}

// Service 3: Shipment Service
public class ShipmentService
{
    public async Task ShipOrderAsync(ShipOrderEvent @event)
    {
        // Ship order
        await _db.ExecuteAsync(
            "UPDATE Orders SET Status = 'Shipped' WHERE OrderId = @id",
            new { id = @event.OrderId }
        );
        
        // Emit event
        await _eventBus.PublishAsync(new OrderShippedEvent
        {
            AggregateId = @event.OrderId
        });
    }
}
```

---

## Event Stream Design

**ALWAYS**:
- Use topic-based (Kafka) or subscription-based (RabbitMQ) event bus
- Design event schema with versioning (v1, v2 compatible)
- Include correlation IDs (trace across services)
- Add timestamps and sequence numbers
- Handle slow consumers (don't block fast producers)
- Retain events (for replay, recovery)

**NEVER**:
- Design tightly coupled event schemas (breaks on change)
- Lose events (event stream is recovery mechanism)
- Block on event publishing (async always)

### ✅ GOOD Event Stream Setup

```yaml
# Kafka Topic Configuration
topics:
  order-events:
    partitions: 10  # Scale horizontally
    replication-factor: 3  # High availability
    retention-ms: 604800000  # 7 days (keep for replay)
    config:
      compression.type: snappy  # Compress events

  payment-events:
    partitions: 5
    replication-factor: 3
    retention-ms: 604800000

# Event Envelope (all events follow this schema)
event:
  schema: |
    {
      "eventId": "uuid",  # Unique event ID
      "eventType": "OrderCreated|PaymentProcessed|...",
      "aggregateId": "guid",  # Order ID, Payment ID, etc.
      "correlationId": "guid",  # Trace across services
      "timestamp": "2026-04-09T10:30:00Z",
      "version": 1,  # Event version (for breaking changes)
      "payload": {
        # Event-specific data
      }
    }
```

---

## Handling Eventual Consistency

**ALWAYS**:
- Accept that read model lags behind write model (eventually consistent)
- Show "processing" state to users (Order → Paid → Shipped)
- Implement idempotent operations (same operation twice = same result)
- Use event deduplication (prevent duplicate processing)
- Monitor lag (alert if read model > 5 seconds behind)

**NEVER**:
- Assume immediate consistency (defeats event-driven purpose)
- Process events out of order (sort by version/timestamp)

### ✅ GOOD Eventual Consistency Handling

```csharp
// Idempotent handler (safe to call multiple times)
public class PaymentProcessedEventHandler
{
    private readonly IIdempotencyStore _idempotency;
    
    public async Task HandleAsync(PaymentProcessedEvent @event)
    {
        // Check if already processed (event deduplication)
        var processed = await _idempotency.IsProcessedAsync(@event.EventId);
        if (processed)
            return;  // Already handled, skip
        
        // Process payment (safe to retry)
        await _db.ExecuteAsync(
            "UPDATE Orders SET Status = 'Paid', PaidAt = @paidAt WHERE OrderId = @id",
            new { id = @event.AggregateId, paidAt = @event.OccurredAt }
        );
        
        // Mark as processed
        await _idempotency.MarkProcessedAsync(@event.EventId);
    }
}

// Monitor event handler lag
public class EventHandlerMonitoring
{
    public async Task MonitorLagAsync()
    {
        var lag = await _eventBus.GetConsumerLagAsync("order-service");
        
        if (lag.TotalSeconds > 5)
        {
            // Alert: read model is stale
            await _alertService.AlertAsync(
                "Event handler lag > 5s",
                severity: AlertSeverity.High
            );
        }
    }
}
```

---

## Event-Driven Architecture Checklist

- [ ] Event schema designed with versioning (v1, v2, compatibility)
- [ ] Event sourcing implemented (append-only event store)
- [ ] Events include: ID, type, aggregate ID, timestamp, version, data
- [ ] CQRS implemented (separate read & write models)
- [ ] Event bus configured (Kafka topic, RabbitMQ exchange)
- [ ] Saga pattern for multi-step processes (compensation on failure)
- [ ] Idempotent handlers (safe to replay events)
- [ ] Event deduplication (prevent double-processing)
- [ ] Eventual consistency handled (show processing state to users)
- [ ] Event retention configured (7+ days for replay)
- [ ] Correlation IDs tracked across services
- [ ] Event handler lag monitored (alert if > threshold)
- [ ] Disaster recovery tested (replay events to recover state)

---

## Summary

Good event-driven architecture:
1. **Event sourcing** — All state changes stored as immutable events
2. **CQRS** — Separate read model from write model
3. **Async communication** — Services react to events, not calls
4. **Saga pattern** — Multi-step processes with compensating transactions
5. **Eventual consistency** — Accept temporary inconsistency
6. **Idempotence** — Safe to process same event multiple times
7. **Event retention** — Keep events for replay & recovery

Event-driven systems are naturally scalable, resilient, and auditable.
