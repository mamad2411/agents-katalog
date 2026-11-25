---
name: domain-driven-design
description: Apply Domain-Driven Design concepts — bounded contexts, aggregates, entities, value objects, domain events, and ubiquitous language — when modeling complex business domains or designing service boundaries. Use when designing domain models, service boundaries, event-driven systems, or when the user asks about DDD, bounded contexts, aggregates, or domain modeling.
---

# Domain-Driven Design (DDD)

Drawn from: *Domain-Driven Design by Example* and Eric Evans' foundational DDD work.

## Core Vocabulary (Ubiquitous Language)

The most important DDD principle: domain experts and developers use **the same words** in conversation and in code. If the business says "order", the code has `Order`, not `SalesTransaction` or `PurchaseRecord`.

**Apply:**
- Rename code to match business language when they diverge
- Use domain terms in class names, method names, variable names, API paths
- If you need a translation layer between business terms and code terms, the model is wrong

## Strategic Design: Bounded Contexts

A **Bounded Context** is an explicit boundary within which a domain model applies. The same concept (e.g., "Customer") can mean different things in different contexts.

```
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│  Sales Context    │   │ Shipping Context   │   │ Billing Context   │
│                   │   │                   │   │                   │
│  Customer         │   │  Recipient         │   │  Payer            │
│  (name, preferences│  │  (address, delivery│  │  (payment methods,│
│   purchase history)│  │   instructions)   │   │   invoices)       │
└───────────────────┘   └───────────────────┘   └───────────────────┘
```

Each context owns its model. Don't try to unify into one global Customer model — it collapses under the weight of everyone's requirements.

**Context Map patterns:**
- **Shared Kernel** — two contexts share a small common model; changes require both teams
- **Customer/Supplier** — downstream context depends on upstream; upstream sets the terms
- **Anticorruption Layer (ACL)** — translation layer that protects your model from external models
- **Published Language** — a well-documented shared format for cross-context communication

## Tactical Design: Building Blocks

### Entities
Objects with a unique identity that persists over time and through state changes.

```typescript
class Order {
  constructor(
    private readonly id: OrderId,    // identity — never changes
    private status: OrderStatus,     // state — changes over time
    private items: OrderItem[],
  ) {}

  getId(): OrderId { return this.id; }

  // Behaviour lives on the entity, not on a service
  addItem(item: OrderItem): void {
    if (this.status !== OrderStatus.Draft) {
      throw new Error('Cannot add items to a non-draft order');
    }
    this.items.push(item);
  }
}
```

**Rule:** Two entities are the same if they have the same identity, regardless of attribute differences.

### Value Objects
Objects defined entirely by their attributes — no identity, immutable.

```typescript
class Money {
  constructor(
    private readonly amount: number,
    private readonly currency: string,
  ) {}

  add(other: Money): Money {
    if (this.currency !== other.currency) throw new Error('Currency mismatch');
    return new Money(this.amount + other.amount, this.currency); // new instance — immutable
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}
```

**Rule:** Two value objects are the same if all their attributes are equal. Replace them instead of mutating.

**Prefer value objects** for: money, addresses, date ranges, coordinates, phone numbers, email addresses, quantities.

### Aggregates
A cluster of entities and value objects with a single **Aggregate Root** as the entry point.

```typescript
// Order is the aggregate root — all access goes through it
class Order {
  private items: OrderItem[] = [];   // OrderItem is inside the aggregate
  private readonly id: OrderId;

  // ✅ External code calls methods on the root
  addItem(productId: ProductId, quantity: number, price: Money): void {
    const item = new OrderItem(productId, quantity, price);
    this.items.push(item);
  }

  // ❌ External code never holds a direct reference to OrderItem
  // and mutates it directly — that bypasses invariant enforcement
}
```

**Aggregate rules:**
1. External objects reference the aggregate root only, never internal entities directly
2. The root enforces all invariants for the aggregate
3. Keep aggregates small — one or a few entities maximum
4. Load aggregates in full; don't partially load them

### Domain Services
Logic that doesn't naturally belong on any entity or value object.

```typescript
// ✅ Good — logic spans multiple aggregates; belongs in a domain service
class TransferService {
  transfer(from: Account, to: Account, amount: Money): void {
    from.debit(amount);
    to.credit(amount);
  }
}

// ❌ Bad — putting cross-aggregate logic on one of the aggregates
class Account {
  transferTo(to: Account, amount: Money): void { ... } // Account shouldn't know about other accounts
}
```

### Domain Events
Something meaningful that happened in the domain — named in past tense.

```typescript
class OrderPlaced {
  constructor(
    public readonly orderId: OrderId,
    public readonly customerId: CustomerId,
    public readonly placedAt: Date,
    public readonly totalAmount: Money,
  ) {}
}

// Aggregate raises events
class Order {
  private domainEvents: DomainEvent[] = [];

  place(): void {
    if (this.items.length === 0) throw new Error('Cannot place empty order');
    this.status = OrderStatus.Placed;
    this.domainEvents.push(new OrderPlaced(this.id, this.customerId, new Date(), this.total()));
  }

  pullEvents(): DomainEvent[] {
    const events = [...this.domainEvents];
    this.domainEvents = [];
    return events;
  }
}
```

Use domain events to:
- Decouple bounded contexts (publish events, let other contexts subscribe)
- Trigger side effects (send email when `OrderPlaced` fires)
- Build audit logs and event sourcing

### Repositories
Provide collection-like access to aggregates; hide persistence details.

```typescript
interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  save(order: Order): Promise<void>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
}

// Infrastructure layer implements the interface
class PostgresOrderRepository implements OrderRepository {
  async findById(id: OrderId): Promise<Order | null> {
    const row = await this.db.query('SELECT * FROM orders WHERE id = $1', [id.value]);
    return row ? this.toDomain(row) : null;
  }
}
```

**Rule:** One repository per aggregate root. Repositories return fully-constructed aggregates — never partial domain objects.

## Layered Architecture for DDD

```
Presentation / API     →  Controllers, DTOs, request/response mapping
Application            →  Use cases, orchestration, transaction boundaries
Domain                 →  Entities, value objects, aggregates, domain services, domain events
Infrastructure         →  Repositories (impl), email, external APIs, database
```

- Domain layer has **zero dependencies** on infrastructure
- Application layer orchestrates domain objects but contains no business rules itself
- Infrastructure implements interfaces defined in domain/application layers

## DDD Decision Guide

| Situation | DDD building block |
|---|---|
| Has unique identity, changes state | Entity |
| Defined by values, immutable | Value Object |
| Cluster of objects with single entry point | Aggregate |
| Logic spans multiple aggregates | Domain Service |
| Something happened in the domain | Domain Event |
| Access aggregates, hide persistence | Repository |
| Clear business subdomain boundary | Bounded Context |

## When NOT to Use DDD

DDD overhead is justified for complex domains. For simple CRUD:

- Simple CRUD apps with no real business rules → active record pattern is fine
- Reporting/analytics → optimize for queries, not rich domain models
- When the domain is well-understood and stable → YAGNI applies

Start with simpler patterns. Introduce DDD tactical patterns as domain complexity grows.

## Refactoring Toward DDD

1. Find the domain experts and establish ubiquitous language
2. Draw context boundaries — where do concepts mean different things?
3. Identify aggregates — what are the consistency boundaries?
4. Move business rules from services into entities/value objects
5. Replace primitive obsession (strings for IDs, prices) with value objects
6. Introduce domain events for side effects and cross-context communication
