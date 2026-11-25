---
name: "cqrs-patterns"
description: "CQRS and event sourcing patterns with code: command handlers, event-sourced aggregate roots, PostgreSQL read model projections, snapshots, event upcasting, and optimistic concurrency retries. Use when implementing or reviewing an event-sourced system."
---

# CQRS/Event Sourcing Patterns

> Named patterns with code for command handlers, event store append with optimistic concurrency, projection design, snapshot strategy, aggregate reconstitution, and event upcasting.

## Patterns

### Pattern: Command Handler with Aggregate Load

```java
// Full command handler flow: validate → load → execute → persist
@CommandHandler
public class ConfirmOrderCommandHandler {

    private final EventStore eventStore;

    public void handle(ConfirmOrderCommand command) {
        String streamId = "order-" + command.orderId();

        // 1. Load aggregate by replaying event stream
        List<RecordedEvent> rawEvents = eventStore.readStream(streamId);
        if (rawEvents.isEmpty()) {
            throw new OrderNotFoundException(command.orderId());
        }

        List<DomainEvent> events = rawEvents.stream()
            .map(this::deserialize)
            .toList();

        long currentVersion = rawEvents.get(rawEvents.size() - 1).getStreamRevision().getValueUnsigned();
        Order order = Order.reconstitute(events);

        // 2. Execute business logic — entity enforces invariants
        List<DomainEvent> newEvents = order.confirm(command.confirmedBy());

        // 3. Persist with optimistic concurrency check
        // If another process wrote to this stream between our read and write,
        // WrongExpectedVersionException is thrown — caller retries or fails
        eventStore.appendToStream(
            streamId,
            ExpectedRevision.expectedRevision(currentVersion),
            newEvents.stream().map(this::serialize).toList()
        );
    }
}
```

### Pattern: Event-Sourced Aggregate Root

```java
public class Order {
    // State — rebuilt from events
    private OrderId id;
    private OrderStatus status;
    private CustomerId customerId;
    private List<OrderItem> items;
    private long version = 0;

    // Uncommitted events — to be persisted by the command handler
    private final List<DomainEvent> uncommittedEvents = new ArrayList<>();

    // Reconstitution — pure event replay, no side effects
    public static Order reconstitute(List<DomainEvent> history) {
        Order order = new Order();
        history.forEach(event -> {
            order.applyEvent(event);
            order.version++;
        });
        return order;
    }

    // Business method — raises events, does not modify state directly
    public List<DomainEvent> confirm(String confirmedBy) {
        if (this.status != OrderStatus.PENDING) {
            throw new DomainException("Only pending orders can be confirmed");
        }

        OrderConfirmedEvent event = new OrderConfirmedEvent(
            this.id, confirmedBy, Instant.now()
        );
        this.applyEvent(event);  // Apply to state immediately
        this.uncommittedEvents.add(event);
        return List.of(event);
    }

    // State transition — called by reconstitution AND by business methods
    // Must be side-effect free (no DB calls, no external calls)
    private void applyEvent(DomainEvent event) {
        switch (event) {
            case OrderCreatedEvent e -> {
                this.id = e.orderId();
                this.customerId = e.customerId();
                this.items = new ArrayList<>(e.items());
                this.status = OrderStatus.PENDING;
            }
            case OrderConfirmedEvent e -> this.status = OrderStatus.CONFIRMED;
            case OrderCancelledEvent e -> this.status = OrderStatus.CANCELLED;
            case OrderDispatchedEvent e -> this.status = OrderStatus.DISPATCHED;
            default -> log.warn("Unknown event type: {}", event.getClass().getSimpleName());
        }
    }
}
```

### Pattern: Read Model Projection (PostgreSQL)

```java
// Projection handles domain events and maintains a denormalized read model
@Component
public class OrderListProjection {

    private final OrderListRepository repo;  // JPA repository for read model table

    @EventHandler
    public void on(OrderCreatedEvent event) {
        repo.save(OrderListEntry.builder()
            .orderId(event.orderId().value())
            .customerId(event.customerId().value())
            .status("PENDING")
            .itemCount(event.items().size())
            .total(event.total().amount())
            .currency(event.total().currency())
            .placedAt(event.timestamp())
            .build());
    }

    @EventHandler
    public void on(OrderConfirmedEvent event) {
        repo.updateStatus(event.orderId().value(), "CONFIRMED", event.timestamp());
    }

    @EventHandler
    public void on(OrderDispatchedEvent event) {
        repo.updateStatusAndTracking(
            event.orderId().value(),
            "DISPATCHED",
            event.trackingId(),
            event.timestamp()
        );
    }

    // READ SIDE: pre-joined query — no joins needed at query time
    public Page<OrderListDto> findByCustomer(String customerId, Pageable pageable) {
        return repo.findByCustomerIdOrderByPlacedAtDesc(customerId, pageable)
            .map(this::toDto);
    }
}
```

### Pattern: Snapshot Storage and Retrieval (Marten / PostgreSQL)

```csharp
// Marten (C#) — PostgreSQL-backed event store with built-in snapshot support
public class OrderRepository
{
    private readonly IDocumentStore _store;

    public async Task<Order> LoadAsync(Guid orderId)
    {
        await using var session = _store.OpenSession();

        // Marten automatically uses the latest snapshot as the starting point
        // and replays only events after the snapshot version
        return await session.Events.AggregateStreamAsync<Order>(orderId);
    }

    // Configure snapshotting — Marten takes snapshot every 50 events
    public static void ConfigureStore(StoreOptions opts)
    {
        opts.Events.AddEventType<OrderCreated>();
        opts.Events.AddEventType<OrderConfirmed>();
        opts.Events.AddEventType<OrderDispatched>();

        opts.Events.Projections.SelfAggregate<Order>(ProjectionLifecycle.Inline);
        opts.Events.UseOptimisticConcurrency = true;

        // Snapshot threshold
        opts.Events.Projections
            .Snapshot<Order>(SnapshotLifecycle.Inline)
            .SnapshotEvery(50);
    }
}
```

### Pattern: Event Upcasting Pipeline

```java
// EventStore reads V1 events; upcaster converts to V2 before handlers receive them
public class EventDeserializer {

    private final ObjectMapper mapper;

    public DomainEvent deserialize(RecordedEvent rawEvent) {
        String eventType = rawEvent.getEventType();
        String json = rawEvent.getEventDataAsString();

        return switch (eventType) {
            case "OrderCreated_V1" -> upcastOrderCreatedV1(mapper.readValue(json, OrderCreatedV1.class));
            case "OrderCreated_V2" -> mapper.readValue(json, OrderCreatedV2.class);
            case "OrderConfirmed" -> mapper.readValue(json, OrderConfirmedEvent.class);
            default -> throw new UnknownEventTypeException(eventType);
        };
    }

    // Upcast V1 → V2: fill in currency default for pre-multicurrency orders
    private OrderCreatedV2 upcastOrderCreatedV1(OrderCreatedV1 v1) {
        return new OrderCreatedV2(
            v1.orderId(),
            v1.customerId(),
            new Money(BigDecimal.valueOf(v1.amount()), "USD"),  // V1 was USD-only
            v1.items(),
            v1.timestamp()
        );
    }
}
```

### Pattern: Optimistic Concurrency — Retry on Conflict

```java
// Handle WrongExpectedVersionException by retrying the command
@Service
public class CommandBus {

    private static final int MAX_RETRIES = 3;

    public void dispatch(Command command) {
        int attempt = 0;
        while (true) {
            try {
                findHandler(command).handle(command);
                return;
            } catch (ConcurrencyException e) {
                attempt++;
                if (attempt >= MAX_RETRIES) {
                    throw new CommandProcessingException(
                        "Failed after " + MAX_RETRIES + " retries due to concurrency conflicts", e
                    );
                }
                log.warn("Concurrency conflict on attempt {}. Retrying...", attempt);
            }
        }
    }
}
```

## Anti-Patterns

### Anti-Pattern: Anemic Command — Command That Is Really a DTO Passed to a Service

```java
// This is not CQRS — it is just a service method with a renamed parameter
public class UpdateOrderService {
    public void update(UpdateOrderCommand command) {  // command is just a DTO
        order.setStatus(command.status());
        order.setItems(command.items());
        repo.save(order);  // Directly mutating state — no events raised
    }
}
```

In event sourcing, commands go through command handlers that produce domain events. The command does not mutate state directly — events do. If there are no events, it is not event sourcing.

### Anti-Pattern: Projections That Are Just Entity Copies

```java
// Anti-pattern: projection mirrors the write model exactly — no denormalization
@EventHandler
public void on(OrderCreatedEvent event) {
    readModel.save(new Order(event.orderId(), event.customerId(), event.items()));
    // This projection is as hard to query as the event-sourced aggregate itself
}
```

Projections should be optimized for specific query patterns. A single `orders` read table that mirrors the write model provides no advantage over a simple CRUD database. Design projections around actual query patterns: order list by customer (flat, pre-sorted), order detail (all data for one order, no joins), order analytics (aggregated by day/product).

### Anti-Pattern: Event Sourcing for Simple CRUD

A user settings table. Fields: theme (light/dark), language, notification preferences. Users change these occasionally. No audit trail required. No business invariants that need event history.

Applying event sourcing here means storing `ThemeChanged`, `LanguageChanged`, `NotificationsEnabled`, and `NotificationsDisabled` events and replaying them to get current settings. The complexity cost is enormous relative to the benefit (there is none for this use case).

Event sourcing is justified by: audit trail requirements, regulatory compliance, complex domain behavior, event-driven integration where downstream consumers need the change history, or temporal queries.

### Anti-Pattern: Long-Running Aggregates Without Snapshots

An order processing aggregate accumulates events over its lifetime: created, item added × 20, confirmed, payment received × 3 (retries), shipping label generated, dispatched, delivered, return requested, return received, refund issued. That is 30+ events for one order.

At 1 million orders and 30 events each, loading any order requires reading 30 events from the event store. Still manageable. But a subscription that accumulates events for 3 years without snapshots may require reading thousands of events. Snapshot every 50–100 events for aggregates with long lifetimes.

## References

- Young, Greg. CQRS Documents. cqrs.files.wordpress.com, 2010.
- Fowler, Martin. "Event Sourcing." martinfowler.com/eaaDev/EventSourcing.html. 2005.
- Vernon, Vaughn. _Implementing Domain-Driven Design_. Addison-Wesley, 2013.
- EventStoreDB: developers.eventstore.com.
- Marten: martendb.io.
- Axon Framework: docs.axoniq.io.
