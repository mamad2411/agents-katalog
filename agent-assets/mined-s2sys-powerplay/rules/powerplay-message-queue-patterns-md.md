---
name: message-queue-patterns
description: Message queue patterns — RabbitMQ, Kafka, async messaging, topic vs queue, consumer groups, dead letter queues
globs: ["**/*.cs", "**/*.ts", "**/*.js", "**/*.yaml", "**/*.yml"]
alwaysApply: false
---

# Message Queue Patterns

Message queues enable asynchronous communication between services. Choose between queues (point-to-point) and topics (publish-subscribe), handle failures with dead letter queues, and scale consumers.

---

## Queues vs. Topics

**Queue (Point-to-Point)**:
- One producer → One consumer (exclusive delivery)
- Message processed once
- Use case: Tasks, jobs, work queues
- Example: Order processing, batch jobs

**Topic (Publish-Subscribe)**:
- One producer → Multiple subscribers
- All subscribers receive message
- Use case: Events, notifications, logging
- Example: Order created event → email, SMS, analytics

### ✅ GOOD Queue Setup (RabbitMQ)

```yaml
# RabbitMQ Queues (point-to-point)
queues:
  order-processing:
    durable: true  # Survive broker restart
    arguments:
      x-dead-letter-exchange: "dlx"
      x-dead-letter-routing-key: "order-processing.dlq"
      x-message-ttl: 86400000  # 24 hours before auto-delete
      
  email-queue:
    durable: true
    arguments:
      x-dead-letter-exchange: "dlx"
      
  sms-queue:
    durable: true
    arguments:
      x-dead-letter-exchange: "dlx"
```

### ✅ GOOD Topic Setup (RabbitMQ)

```yaml
# RabbitMQ Topics (publish-subscribe)
exchanges:
  order-events:
    type: topic  # Topic exchange
    durable: true
    
bindings:
  - exchange: order-events
    routing_key: "order.#"  # Match order.created, order.paid, etc.
    queue: email-notifications
    
  - exchange: order-events
    routing_key: "order.#"
    queue: order-analytics
    
  - exchange: order-events
    routing_key: "order.paid"  # Only payment events
    queue: shipment-service
```

---

## RabbitMQ Patterns

**ALWAYS**:
- Use durable queues (survive broker restarts)
- Set dead letter exchange (handle failures)
- Implement message TTL (prevent infinite queuing)
- Acknowledge messages (only when processed)
- Use topic exchanges for events (multiple subscribers)
- Use direct exchanges for commands (single target)
- Limit concurrent consumers (prevent overload)

**NEVER**:
- Lose messages (use durable queues)
- Process messages multiple times (dedup or idempotent)
- Ignore dead letter queue (monitor failures)

### ✅ GOOD RabbitMQ Publisher & Consumer

```csharp
// Publisher (RabbitMQ using MassTransit)
public class OrderServicePublisher
{
    private readonly IPublishEndpoint _publishEndpoint;
    
    public async Task PublishOrderCreatedAsync(Order order)
    {
        // Publish event to all subscribers
        await _publishEndpoint.Publish<OrderCreatedEvent>(
            new OrderCreatedEvent
            {
                OrderId = order.Id,
                CustomerId = order.CustomerId,
                Amount = order.Amount,
                CreatedAt = DateTime.UtcNow
            }
        );
    }
}

// Subscriber 1: Email Notification
public class SendOrderEmailConsumer : IConsumer<OrderCreatedEvent>
{
    private readonly IEmailService _emailService;
    
    public async Task Consume(ConsumeContext<OrderCreatedEvent> context)
    {
        var @event = context.Message;
        
        try
        {
            // Send email
            await _emailService.SendOrderConfirmationAsync(
                @event.CustomerId,
                @event.Amount
            );
            
            // Message automatically acknowledged (removed from queue)
        }
        catch (EmailException ex)
        {
            // Nack (negative acknowledge) - requeue for retry
            throw;  // MassTransit will retry
        }
    }
}

// Subscriber 2: Order Analytics
public class RecordOrderAnalyticsConsumer : IConsumer<OrderCreatedEvent>
{
    private readonly IAnalyticsService _analyticsService;
    
    public async Task Consume(ConsumeContext<OrderCreatedEvent> context)
    {
        var @event = context.Message;
        
        // Record analytics event
        await _analyticsService.RecordOrderAsync(@event);
    }
}

// Configure RabbitMQ (MassTransit)
services.AddMassTransit(x =>
{
    // Configure consumers
    x.AddConsumer<SendOrderEmailConsumer>();
    x.AddConsumer<RecordOrderAnalyticsConsumer>();
    
    // RabbitMQ transport
    x.UsingRabbitMq((context, cfg) =>
    {
        cfg.Host("rabbitmq", h =>
        {
            h.Username("guest");
            h.Password("guest");
        });
        
        // Configure endpoints
        cfg.ConfigureEndpoints(context);
        
        // Configure consumer concurrency (max 10 parallel)
        cfg.ConfigureConsumer<SendOrderEmailConsumer>(ctx =>
        {
            ctx.ConcurrentMessageLimit = 10;
            ctx.ReceiveEndpoint(e =>
            {
                e.PrefetchCount = 10;  // Prefetch messages
            });
        });
    });
});
```

---

## Kafka Patterns

**ALWAYS**:
- Use topics with partitions (scale horizontally)
- Consumer groups (distribute load across consumers)
- Compacted topics for state (key-value log)
- Replication factor ≥ 3 (high availability)
- Retention period (7+ days for replay)
- Idempotent producers (prevent duplicates)

**NEVER**:
- Lose messages (configure replication & acks)
- Have single consumer (use consumer groups)
- Assume message ordering across partitions

### ✅ GOOD Kafka Setup

```yaml
# Kafka Topics
topics:
  order-events:
    partitions: 10  # Scale horizontally
    replication-factor: 3  # HA
    retention-ms: 604800000  # 7 days
    cleanup-policy: "delete"  # or "compact" for state topics
    config:
      compression.type: "snappy"
      min.insync.replicas: 2  # Write acks

  order-state:  # Compacted topic for state
    partitions: 1
    replication-factor: 3
    cleanup-policy: "compact"  # Keep latest per key
    segment-ms: 86400000  # 1 day segments
```

### ✅ GOOD Kafka Producer & Consumer

```csharp
// Kafka Producer using Confluent.Kafka
public class OrderEventProducer
{
    private readonly IProducer<string, string> _producer;
    
    public OrderEventProducer()
    {
        var config = new ProducerConfig
        {
            BootstrapServers = "kafka:9092",
            Acks = Acks.All,  // Wait for all replicas
            Retries = 3,
            EnableIdempotence = true,  // Prevent duplicates
            MessageTimeoutMs = 5000
        };
        
        _producer = new ProducerBuilder<string, string>(config).Build();
    }
    
    public async Task PublishOrderCreatedAsync(Order order)
    {
        var message = new Message<string, string>
        {
            Key = order.Id.ToString(),  // Partition key (orders for same customer → same partition)
            Value = JsonConvert.SerializeObject(new
            {
                order.Id,
                order.CustomerId,
                order.Amount,
                CreatedAt = DateTime.UtcNow
            })
        };
        
        var result = await _producer.ProduceAsync("order-events", message);
        
        if (result.Status == PersistenceStatus.Persisted)
        {
            _logger.LogInformation(
                "Order event published: {OrderId} to partition {Partition} at offset {Offset}",
                order.Id,
                result.Partition,
                result.Offset
            );
        }
        else
        {
            throw new Exception($"Failed to publish order event: {result.Status}");
        }
    }
}

// Kafka Consumer using Confluent.Kafka
public class OrderEventConsumer : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var config = new ConsumerConfig
        {
            BootstrapServers = "kafka:9092",
            GroupId = "email-notification-service",  // Consumer group
            AutoOffsetReset = AutoOffsetReset.Earliest,
            EnableAutoCommit = false,  // Manual commit
            StatisticsIntervalMs = 5000,
            SessionTimeoutMs = 6000,
            MaxPollIntervalMs = 300000
        };
        
        using (var consumer = new ConsumerBuilder<string, string>(config).Build())
        {
            consumer.Subscribe("order-events");
            
            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    var result = consumer.Consume(stoppingToken);
                    
                    if (result == null)
                        continue;
                    
                    // Deserialize message
                    var @event = JsonConvert.DeserializeObject<OrderCreatedEvent>(result.Value);
                    
                    // Process message
                    using (var scope = _serviceProvider.CreateScope())
                    {
                        var emailService = scope.ServiceProvider.GetRequiredService<IEmailService>();
                        await emailService.SendOrderConfirmationAsync(@event.CustomerId, @event.Amount);
                    }
                    
                    // Commit offset (only if processed successfully)
                    consumer.Commit(result);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error processing Kafka message");
                    // Message will be retried (offset not committed)
                }
            }
            
            consumer.Close();
        }
    }
}
```

---

## Dead Letter Queues (DLQ)

**ALWAYS**:
- Configure DLQ for every consumer queue
- Auto-route failed messages (after N retries)
- Monitor DLQ (alert on new messages)
- Implement retry logic (exponential backoff)
- Log all failures (for debugging)

**NEVER**:
- Ignore DLQ messages (poison pills)
- Retry forever (set max retries)
- Lose DLQ contents (keep for post-mortem)

### ✅ GOOD Dead Letter Queue Setup

```csharp
// Configure DLQ with retry logic
public class MessageConsumerConfiguration : IConsumer<OrderCreatedEvent>
{
    public async Task Consume(ConsumeContext<OrderCreatedEvent> context)
    {
        try
        {
            // Process message
            await ProcessOrderAsync(context.Message);
        }
        catch (TransientException ex)
        {
            // Transient error - retry with backoff
            await context.Defer(TimeSpan.FromSeconds(30));  // Retry after 30 sec
        }
        catch (Exception ex)
        {
            // Permanent error - send to DLQ
            _logger.LogError(ex, "Failed to process order event, moving to DLQ");
            
            // MassTransit automatically sends to DLQ after max retries
            throw;  // Nack
        }
    }
}

// Monitor DLQ
public class DeadLetterQueueMonitor : BackgroundService
{
    private readonly IConsumer<IEvent> _dlqConsumer;
    private readonly IAlertService _alertService;
    
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                // Consume DLQ messages (should be empty)
                var message = _dlqConsumer.Consume(TimeSpan.FromSeconds(5));
                
                if (message != null)
                {
                    // Alert: messages in DLQ
                    await _alertService.AlertAsync(
                        $"DLQ contains poison pill: {message.EventType}",
                        severity: AlertSeverity.Critical
                    );
                    
                    _logger.LogError(
                        "Poison pill in DLQ: {Message}",
                        JsonConvert.SerializeObject(message)
                    );
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "DLQ monitoring error");
            }
            
            await Task.Delay(TimeSpan.FromSeconds(30), stoppingToken);
        }
    }
}
```

---

## Message Ordering & Idempotency

**ALWAYS**:
- Process messages in order for same entity (use partition key)
- Make handlers idempotent (same message processed twice = same result)
- Use message deduplication (prevent duplicates)
- Track processing state (which messages processed)

**NEVER**:
- Assume parallel processing preserves order
- Process same message twice (expect duplicates)

### ✅ GOOD Message Ordering

```csharp
// Partition key ensures ordering for same customer
await _producer.ProduceAsync("order-events", new Message<string, string>
{
    Key = order.CustomerId.ToString(),  // Same customer → same partition → sequential
    Value = JsonConvert.SerializeObject(@event)
});

// Idempotent consumer (safe to process same message multiple times)
public class IdempotentConsumer : IConsumer<OrderCreatedEvent>
{
    private readonly IProcessedMessageStore _processedStore;
    
    public async Task Consume(ConsumeContext<OrderCreatedEvent> context)
    {
        // Check if already processed
        var messageId = context.Message.MessageId;
        var alreadyProcessed = await _processedStore.IsProcessedAsync(messageId);
        
        if (alreadyProcessed)
        {
            _logger.LogWarning("Duplicate message {MessageId}, skipping", messageId);
            return;  // Already processed, skip
        }
        
        // Process message
        await ProcessOrderAsync(context.Message);
        
        // Mark as processed
        await _processedStore.MarkProcessedAsync(messageId);
    }
}
```

---

## Message Queue Checklist

- [ ] Queue vs. topic chosen (point-to-point vs. publish-subscribe)
- [ ] Broker configured (RabbitMQ or Kafka)
- [ ] Durable queues/topics (survive failures)
- [ ] Dead letter queue configured (handle failures)
- [ ] Retry logic implemented (exponential backoff)
- [ ] Consumer groups configured (distribute load)
- [ ] Message deduplication enabled (prevent duplicates)
- [ ] Idempotent handlers (safe to replay)
- [ ] Message ordering ensured (partition keys)
- [ ] Concurrency limited (prevent overload)
- [ ] Monitoring & alerting (DLQ, consumer lag)
- [ ] Documentation (topics, routing, consumers)

---

## Summary

Good message queue patterns:
1. **Choose right pattern** — Queues for tasks, topics for events
2. **Durable delivery** — Configure queues, replicas, persistence
3. **Handle failures** — DLQ, retry logic, exponential backoff
4. **Idempotency** — Safe to process messages multiple times
5. **Ordering** — Partition keys for same-entity ordering
6. **Monitoring** — Watch consumer lag, DLQ, failures
7. **Scalability** — Horizontal consumer scaling with groups

Message queues decouple services and enable scalable, resilient systems.
