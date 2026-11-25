---
name: domain-driven-design
description: "Strategic and tactical Domain-Driven Design reference: context-map relationships, aggregate rules and sizing, value objects vs entities, domain event guidelines, event storming conventions, and code patterns (aggregate root, Money value object, outbox event publishing, anticorruption layer) with the common mistakes to avoid. Use when modeling a domain, splitting bounded contexts, or reviewing aggregates."
---

# DDD pattern library

## Strategic patterns

### Context map relationships

| Pattern | Relationship | When |
|---|---|---|
| Partnership | Equal teams, mutual dependency | Sister teams in a single product |
| Customer-Supplier | Downstream depends on upstream | Common; upstream prioritizes downstream needs |
| Conformist | Downstream conforms to upstream | Downstream has no negotiating power |
| Anti-Corruption Layer | Translation layer | Integrating legacy / external systems |
| Shared Kernel | Small shared model | Rare; high coordination cost |
| Open Host Service | Well-defined API for many consumers | Platform / shared services |
| Published Language | Shared schema (events, formats) | Cross-context integration |
| Separate Ways | No integration | Independent contexts |

### When bounded contexts mismatch teams

If two contexts span one team, the team has internal coordination overhead. If one context spans two teams, you have Shared Kernel costs.

Ideal: one team per context (Conway's Law inverse).

## Tactical patterns

### Aggregate rules

1. **One transaction = one aggregate**
2. **Reference other aggregates by ID**
3. **Aggregate root enforces all internal invariants**
4. **Use domain events for cross-aggregate coordination**

### Aggregate sizing

When in doubt, smaller. Big aggregates cause:
- Lock contention
- Large transactions
- Slow loads (load everything for one change)
- Difficult tests

If invariants don't span objects, they belong in separate aggregates with eventual consistency.

### Value object vs entity

| | Entity | Value object |
|---|---|---|
| Identity | Has it (persistent ID) | None; defined by attributes |
| Mutability | Lifecycle of attribute changes | Immutable |
| Equality | By ID | By attributes |
| Examples | Customer, Order, Account | Money, Address, DateRange |

Most things are value objects. Entity is the lifecycle exception.

### Domain event guidelines

- **Past tense**: `OrderConfirmed`, not `ConfirmOrder`
- **Business-meaningful**: not `CustomerRecordUpdated`
- **Immutable**: a fact, not a state
- **Self-contained**: include the data downstream needs
- **Versioned**: schema evolves

## Common mistakes catalog

### Anemic domain model

```python
# Bad: data class with no behavior
class Order:
    id: str
    status: str
    line_items: list

# Business logic scattered in services:
def confirm_order(order: Order):
    if order.status != "pending":
        raise ...
    order.status = "confirmed"
```

Behavior should live in the aggregate, not in service classes that orchestrate it from the outside.

### God aggregate

```python
class Customer:
    orders: list[Order]
    payment_methods: list[PaymentMethod]
    addresses: list[Address]
    support_tickets: list[Ticket]
    # ...
```

This holds too much. Loading a Customer loads everything. Breaking into separate aggregates (Customer, Order, PaymentMethod, etc.) is correct.

### Object references between aggregates

```python
# Bad
class Order:
    customer: Customer  # full object

# Good
class Order:
    customer_id: CustomerId  # just the ID
```

Object references invite traversal; traversal breaks aggregate boundaries.

### Same word, conflated meaning

If "Customer" means "person who placed an order" in one place and "person with a support account" in another, you have two bounded contexts. Force-fitting them into one model produces conflicting requirements.

## Event storming output format

Sticky-note color convention:
- ORANGE = domain events
- BLUE = commands
- YELLOW = aggregates
- PINK = external systems
- PURPLE = policies (when X, do Y)
- GREEN = read models / projections

## Code patterns (Java, TypeScript)

> Named patterns with code for aggregate root design, value objects, domain events, anticorruption layer, bounded context integration, and ubiquitous language.

### Pattern: Aggregate Root with Invariant Enforcement

```java
public class ShoppingCart {
    private final CartId id;
    private final CustomerId customerId;
    private final Map<ProductId, CartItem> items;
    private CartStatus status;

    // Maximum items enforced within aggregate
    private static final int MAX_ITEMS = 50;

    public static ShoppingCart create(CustomerId customerId) {
        return new ShoppingCart(CartId.generate(), customerId, new HashMap<>(), CartStatus.ACTIVE);
    }

    public void addItem(ProductId productId, int quantity, Money unitPrice) {
        // Invariant 1: Cart must be active
        if (this.status != CartStatus.ACTIVE)
            throw new DomainException("Cannot modify a checked-out cart");

        // Invariant 2: Quantity must be positive
        if (quantity <= 0)
            throw new DomainException("Quantity must be positive");

        // Invariant 3: Maximum item types
        if (!items.containsKey(productId) && items.size() >= MAX_ITEMS)
            throw new DomainException("Cart cannot contain more than " + MAX_ITEMS + " distinct items");

        // Merge with existing quantity if already in cart
        items.merge(productId,
            new CartItem(productId, quantity, unitPrice),
            (existing, newItem) -> new CartItem(
                productId,
                existing.quantity() + quantity,  // Add quantities
                unitPrice  // Use latest price
            )
        );
    }

    public void removeItem(ProductId productId) {
        if (this.status != CartStatus.ACTIVE)
            throw new DomainException("Cannot modify a checked-out cart");
        items.remove(productId);
    }

    public OrderRequest checkout() {
        if (this.status != CartStatus.ACTIVE)
            throw new DomainException("Cart already checked out");
        if (items.isEmpty())
            throw new DomainException("Cannot checkout an empty cart");

        this.status = CartStatus.CHECKED_OUT;

        return new OrderRequest(
            this.customerId,
            items.values().stream().map(CartItem::toOrderLine).toList()
        );
    }

    // No direct access to items collection — only through business methods
    public Money totalValue() {
        return items.values().stream()
            .map(CartItem::subtotal)
            .reduce(Money.zero("USD"), Money::add);
    }

    public int itemCount() { return items.values().stream().mapToInt(CartItem::quantity).sum(); }
}
```

### Pattern: Value Object (Money)

```typescript
// TypeScript value object — immutable, equality by value
export class Money {
  private constructor(
    private readonly _amount: number,
    private readonly _currency: string,
  ) {
    if (_amount < 0) throw new Error('Amount cannot be negative');
    if (!_currency.match(/^[A-Z]{3}$/)) throw new Error('Invalid currency code');
  }

  static of(amount: number, currency: string): Money {
    return new Money(Math.round(amount * 100) / 100, currency);  // 2 decimal places
  }

  static zero(currency: string): Money {
    return new Money(0, currency);
  }

  add(other: Money): Money {
    if (this._currency !== other._currency) {
      throw new Error(`Cannot add ${this._currency} and ${other._currency}`);
    }
    return Money.of(this._amount + other._amount, this._currency);
  }

  multiply(factor: number): Money {
    return Money.of(this._amount * factor, this._currency);
  }

  isGreaterThan(other: Money): boolean {
    this.assertSameCurrency(other);
    return this._amount > other._amount;
  }

  equals(other: Money): boolean {
    return this._amount === other._amount && this._currency === other._currency;
  }

  get amount(): number { return this._amount; }
  get currency(): string { return this._currency; }
  toString(): string { return `${this._amount} ${this._currency}`; }

  private assertSameCurrency(other: Money): void {
    if (this._currency !== other._currency) {
      throw new Error(`Currency mismatch: ${this._currency} vs ${other._currency}`);
    }
  }
}
```

### Pattern: Domain Event Publishing with Outbox

```java
// Domain event collection and publishing via outbox
public abstract class AggregateRoot {
    private final List<DomainEvent> uncommittedEvents = new ArrayList<>();

    protected void registerEvent(DomainEvent event) {
        this.uncommittedEvents.add(event);
    }

    public List<DomainEvent> collectEvents() {
        List<DomainEvent> events = List.copyOf(uncommittedEvents);
        uncommittedEvents.clear();
        return events;
    }
}

public class Order extends AggregateRoot {
    // ...

    public void confirm() {
        if (this.status != OrderStatus.PENDING)
            throw new DomainException("Only pending orders can be confirmed");
        this.status = OrderStatus.CONFIRMED;
        // Register event — to be collected and published by application service
        registerEvent(OrderConfirmedEvent.from(this));
    }
}

// Application service: save aggregate + publish events in same transaction (outbox pattern)
@Service
@Transactional
public class OrderApplicationService {

    private final OrderRepository orders;
    private final OutboxRepository outbox;

    public void confirmOrder(ConfirmOrderCommand cmd) {
        Order order = orders.findById(new OrderId(cmd.orderId())).orElseThrow();
        order.confirm();
        orders.save(order);

        // Write events to outbox in same transaction — guaranteed delivery
        List<DomainEvent> events = order.collectEvents();
        events.forEach(event -> outbox.save(new OutboxMessage(event)));

        // Outbox relay (separate process) reads outbox and publishes to Kafka/RabbitMQ
    }
}
```

### Pattern: Anticorruption Layer

```typescript
// Order context ACL — protecting domain from legacy shipping system model
interface LegacyShipmentSystem {
  createShipment(req: {
    ord_no: string;
    cust_cd: string;
    dlvry_addr: string;
    items: Array<{ prod_cd: string; qty: number; wgt_kg: number }>;
    prioty: 0 | 1 | 2;  // 0=low, 1=normal, 2=urgent
  }): Promise<{ shipment_no: string; eta_days: number }>;
}

// Domain model — clean, using ubiquitous language
interface ShipmentRequest {
  orderId: OrderId;
  customerId: CustomerId;
  deliveryAddress: Address;
  items: Array<{ productId: ProductId; quantity: number; weightKg: number }>;
  priority: 'STANDARD' | 'EXPRESS' | 'OVERNIGHT';
}

// ACL: translates between domain model and legacy system
class ShippingServiceAcl {
  constructor(private readonly legacy: LegacyShipmentSystem) {}

  async scheduleShipment(request: ShipmentRequest): Promise<ShipmentConfirmation> {
    // Translate priority (domain language → legacy codes)
    const priorityMap: Record<string, 0 | 1 | 2> = {
      STANDARD: 0,
      EXPRESS: 1,
      OVERNIGHT: 2,
    };

    const legacyResponse = await this.legacy.createShipment({
      ord_no: request.orderId.value,
      cust_cd: request.customerId.value,
      dlvry_addr: this.formatAddress(request.deliveryAddress),
      items: request.items.map(item => ({
        prod_cd: item.productId.value,
        qty: item.quantity,
        wgt_kg: item.weightKg,
      })),
      prioty: priorityMap[request.priority],
    });

    // Translate legacy response to domain model
    return new ShipmentConfirmation(
      new ShipmentId(legacyResponse.shipment_no),
      request.orderId,
      new Date(Date.now() + legacyResponse.eta_days * 24 * 60 * 60 * 1000),
    );
  }

  private formatAddress(addr: Address): string {
    return `${addr.street}, ${addr.city}, ${addr.postalCode}, ${addr.country}`;
  }
}
```

## More anti-patterns in code (Java)

### Anti-Pattern: Anemic Domain Model

```java
// All behavior in a service, entities are just data bags
@Entity
public class Order {
    private String status;
    private List<OrderItem> items;
    // Only getters and setters
}

@Service
public class OrderService {
    public void addItem(Order order, OrderItem item) {
        // Business logic in service, not entity
        if (order.getStatus().equals("DRAFT")) {
            order.getItems().add(item);
        }
    }
}
```

The Order entity has no behavior — no invariant enforcement, no self-protection. OrderService duplicates business logic that belongs in Order. Multiple services can bypass each other's rules by directly manipulating the entity's state.

Fix: move business behavior into the entity. The entity is responsible for maintaining its own invariants.

### Anti-Pattern: Aggregate with Foreign Key References

```java
// VIOLATION: Order holds a reference to Customer object (crosses aggregate boundary)
public class Order {
    private Customer customer;  // Wrong — creates tight coupling, breaks aggregate boundary
    private List<OrderItem> items;
}

// Correct: reference by ID only
public class Order {
    private CustomerId customerId;  // Only the ID — load Customer separately when needed
    private List<OrderItem> items;
}
```

Holding object references across aggregate boundaries creates coupling that breaks independent persistence and scalability. Reference aggregates by their IDs. Load them via repositories when the application layer needs to coordinate between aggregates.

### Anti-Pattern: One Aggregate for Everything

```java
// One giant aggregate trying to maintain consistency across the entire domain
public class ECommerceDomain {
    private Customer customer;
    private List<Order> orders;
    private List<Product> products;
    private ShoppingCart cart;
    // ... everything
}
```

This is an aggregate that is the entire domain model. All writes are serialized. All concurrent accesses conflict. Size aggregates by their invariants. Customer, Order, Product, and Cart are separate aggregates because their invariants don't span each other.

## References

- Evans, Eric. _Domain-Driven Design_. Addison-Wesley, 2003. Aggregate (Chapter 6), Value Object (Chapter 5), Domain Event.
- Vernon, Vaughn. _Implementing Domain-Driven Design_. Addison-Wesley, 2013. Chapter 10 (Aggregates).
- Brandolini, Alberto. _Introducing Event Storming_. Leanpub, 2021.
- Vernon, Vaughn. "Effective Aggregate Design." DDD Community articles. dddcommunity.org.
- DDD Crew: context-mapping. github.com/ddd-crew/context-mapping.

## Cross-references
- `microservices` plugin — for service boundaries from bounded contexts
- `event-driven` plugin — for event design at scale
- `cqrs-event-sourcing` plugin — for the event-sourcing variant
- `migration-strategies` plugin — for strangler-fig + ACL patterns
