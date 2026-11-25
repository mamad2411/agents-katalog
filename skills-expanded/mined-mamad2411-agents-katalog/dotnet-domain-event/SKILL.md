---
name: dotnet-domain-event
description: Create domain events and MassTransit consumers for event-driven architecture with RabbitMQ. Use when user says "add event", "create consumer", "domain event", "publish event", "MassTransit", "message handler", "event-driven", "RabbitMQ", or asks about asynchronous communication between services. Do NOT use for synchronous command handling.
metadata:
  author: Claude-DotNet-Ultimate
  version: 1.0.0
  category: messaging
---

# Domain Events & MassTransit Consumers

## Architecture

```
Domain Event raised in Entity
    ↓
Collected in AggregateRoot._domainEvents
    ↓
Extracted after SaveChanges via ExtractDomainEvents()
    ↓
Published via IMessageBus (MassTransit IPublishEndpoint)
    ↓
Delivered to RabbitMQ exchange
    ↓
Consumed by MassTransit IConsumer<T>
```

## Step 1: Define Domain Event

Place in `src/Core/Domain/Events/`:

```csharp
namespace ClaudeDotNetUltimate.Core.Domain.Events;

public sealed record ProductCreatedEvent(
    ProductId ProductId,
    string Name,
    decimal Price) : DomainEvent;

public sealed record ProductPriceChangedEvent(
    ProductId ProductId,
    decimal OldPrice,
    decimal NewPrice) : DomainEvent;
```

**Rules for domain events:**
- Always a `sealed record` extending `DomainEvent`
- Named in past tense: `OrderCreated`, `ItemAdded`, `PriceChanged`
- Contains only the data needed by consumers
- No infrastructure references (no RabbitMQ topics, no queue names)
- Immutable — all properties in constructor

## Step 2: Raise Event in Entity

```csharp
public sealed class Product : AggregateRoot<ProductId>
{
    public static Product Create(string name, Money price)
    {
        var product = new Product { Id = ProductId.New(), Name = name, Price = price };
        product.AddDomainEvent(new ProductCreatedEvent(product.Id, name, price.Amount));
        return product;
    }

    public void UpdatePrice(Money newPrice)
    {
        var oldPrice = Price.Amount;
        Price = newPrice;
        AddDomainEvent(new ProductPriceChangedEvent(Id, oldPrice, newPrice.Amount));
    }
}
```

## Step 3: Create MassTransit Consumer

Place in `src/Infrastructure/Messaging/Consumers/`:

```csharp
namespace ClaudeDotNetUltimate.Infrastructure.Messaging.Consumers;

public sealed class ProductCreatedConsumer(
    ILogger<ProductCreatedConsumer> logger) : IConsumer<ProductCreatedEvent>
{
    public Task Consume(ConsumeContext<ProductCreatedEvent> context)
    {
        logger.LogInformation(
            "Product created: {ProductId} - {Name} at {Price}",
            context.Message.ProductId,
            context.Message.Name,
            context.Message.Price);

        return Task.CompletedTask;
    }
}
```

## Step 4: Register Consumer

In `src/Infrastructure/Messaging/MassTransitConfig.cs`, add the receive endpoint:

```csharp
cfg.ReceiveEndpoint("product-created", e =>
{
    e.ConfigureConsumer<ProductCreatedConsumer>(context);
    e.UseMessageRetry(r => r.Exponential(
        retryLimit: 3,
        minInterval: TimeSpan.FromSeconds(1),
        maxInterval: TimeSpan.FromSeconds(30),
        intervalDelta: TimeSpan.FromSeconds(5)));
});
```

## Step 5: Publish in Command Handler

```csharp
public async Task<Result<ProductDto>> Handle(
    CreateProductCommand request, CancellationToken ct)
{
    var product = Product.Create(request.Name, Money.From(request.Price, request.Currency));

    await unitOfWork.Products.AddAsync(product, ct);
    var saveResult = await unitOfWork.SaveChangesWithResultAsync(ct);

    if (saveResult.IsFailure)
        return Result<ProductDto>.Failure(saveResult.Error!);

    foreach (var domainEvent in product.ExtractDomainEvents())
        await messageBus.PublishAsync(domainEvent, ct);

    return /* ... */;
}
```

## MassTransit Configuration Patterns

### Retry Policies
```csharp
e.UseMessageRetry(r => r.Exponential(3, TimeSpan.FromSeconds(1),
    TimeSpan.FromSeconds(30), TimeSpan.FromSeconds(5)));
```

### Dead Letter Queue
Failed messages after all retries automatically go to `_error` queue.

### Outbox Pattern
Already configured: in-memory outbox with bus outbox for deduplication.

### Concurrency
```csharp
e.ConcurrentMessageLimit = 10;
e.PrefetchCount = 16;
```

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Event | Past tense record | `OrderConfirmedEvent` |
| Consumer | Event name + Consumer | `OrderConfirmedConsumer` |
| Queue | kebab-case | `order-confirmed` |
| Exchange | Auto from MassTransit | `ClaudeDotNetUltimate.Core.Domain.Events:OrderConfirmedEvent` |

## Checklist

- [ ] Domain event record defined in `Core/Domain/Events/`
- [ ] Event raised in aggregate root method
- [ ] Consumer created in `Infrastructure/Messaging/Consumers/`
- [ ] Receive endpoint registered in `MassTransitConfig`
- [ ] Retry policy configured
- [ ] Integration test with MassTransit test harness
