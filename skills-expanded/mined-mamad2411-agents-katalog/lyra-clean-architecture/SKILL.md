---
name: lyra-clean-architecture
description: "Pick the lightest architecture that fits — NONE, Layered, Hexagonal, or DDD — and justify each layer before adding it."
metadata:
  version: "1.0.0"
  author: "Alexandru Miron"
compatibility: "No tools required. Optional: invoke lyra-clean-code for class-level quality, lyra-tdd for the test-first workflow."
---

# lyra-clean-architecture

## What it does

Architecture is a liability, not a virtue. Every port, layer, and adapter is a maintenance cost you pay forever. This skill walks a top-down decision tree — NONE → Layered → Hexagonal → DDD — so you reach for more only when the cost of not having it is real. The Dependency Rule (dependencies point inward, toward business policy) is the one principle that unifies all four levels. If a unit test for a business rule needs a running database or framework, the boundary is wrong — fix the boundary, don't mock harder.

## The decision tree

Walk top-down. Default to the lighter option. Descend only when the cost of not having the architecture exceeds the cost of maintaining it.

```
1. NONE — simple layered
   Lifespan < 6 months AND ≤ ~8 endpoints AND business rules are thin?
   → 3 flat folders: web/, service/, data/. No ports. No interfaces.
     The Dependency Rule still applies: service/ never imports web/;
     data/ never imports service/. Folder discipline, not ceremony.
   → Throwaway prototype, internal admin tool, hackathon project.

2. LAYERED — Clean Architecture lite
   CRUD-dominated AND business rules are real but localized AND
   single delivery channel?
   → 3 layers with one boundary: web → use_case → repository_interface.
     The repository interface lives in the use_case layer; data/ implements it.
     No separate domain layer yet — entities are plain records/structs.
   → Standard SaaS CRUD app, REST API with a few non-trivial rules.

3. HEXAGONAL — Ports & Adapters
   Multiple delivery channels for the same logic (HTTP + CLI + queue + cron) OR
   you will swap DB / external API / framework within 2 years OR
   you need to unit-test business logic with zero infra running?
   → Define inbound ports (use case interfaces) and outbound ports
     (dependency interfaces). All infra lives in adapters. One composition root.
   → Payment service, multi-tenant SaaS with queue workers.

4. DDD — Bounded Contexts + Rich Domain
   Complex domain with deep invariants AND multiple subdomains that don't share
   a model AND the domain is a strategic differentiator AND lifespan 5+ years?
   → Bounded contexts, aggregates, value objects, domain events.
     Ubiquitous language enforced in code. Hexagonal delivery inside each context.
   → Insurance underwriting, trading systems, complex logistics.
```

When two options tie, take the lighter one. You can always add architecture later; removing it is a rewrite.

## The rules

### 1. Default to less.

Architecture has no off switch by default — supply one. Make the case to add a layer, not to remove it. If you can't cite the specific cost of not having it, don't add it.

### 2. The Dependency Rule always applies.

Source dependencies point inward, toward higher-level policy. Inner code never names outer code. Define the interface in the inner layer; implement it in the outer. Data crossing a boundary uses the form most convenient for the inner layer — never an ORM entity, never an HTTP request object.

bad: use case imports the ORM entity and passes it straight through.
good: use case defines its own `CreateOrderInput`; the adapter maps from the ORM row.

### 3. A port without two implementations is a premature port.

Real plus fake-for-tests counts. Real plus "we might add Kafka later" does not. Delete the port until the second implementation is real. Same for wrapping `Logger`, `Clock`, or `UUID` — wrap only when a test actually exercises the seam.

### 4. Don't extract for CRUD.

A Use Case class for a one-line delegation is ceremony — inline it in the controller. A domain entity for CRUD is premature — a plain record or struct is correct until business rules appear. Wait until logic exists.

### 5. Don't reuse the persistence model as the domain model.

Schema changes will rewrite business rules. Keep a persistence model and a domain entity; map between them at the adapter.

bad: passing the ORM `User` row into the use case, which reads `passwordHash` directly.
good: adapter maps the `User` row → a `User` domain entity that never exposes `passwordHash` to callers.

### 6. Confine `new` for adapters to the composition root.

One place wires real adapters to ports. Everything else takes dependencies as arguments. A microservice with a shared database is not an architecture — it's a distributed monolith. Either share nothing, or stay monolithic with clean internal boundaries.

### 7. Never introduce a bounded context for a single team.

Bounded contexts exist to bound team boundaries and model divergence. One team, one model. Split when teams split.

### 8. Strangler, not big-bang.

Don't rewrite a working system to Clean Architecture in one pass. Move one slice at a time, behavior-preserving tests first. The Dependency Rule is language-agnostic — `Protocol` in Python, interface-at-consumer in Go, interface in the port package in Java/Kotlin.

## Worked example

A Hexagonal use case with one inbound port (`CreateOrder`) and two outbound ports. The inner layer owns the contracts; the outer layer implements them; the composition root is the only place that wires real adapters.

```typescript
// application/ports.ts — INNER, owns the contracts
export interface OrderRepository {
  save(order: Order): Promise<void>;
}
export interface PaymentGateway {
  authorize(
    orderId: string,
    amountCents: number,
  ): Promise<{ authorizationId: string }>;
}

// application/CreateOrder.ts — INNER, depends only on ports + domain
export class CreateOrder {
  constructor(
    private orders: OrderRepository,
    private payments: PaymentGateway,
  ) {}
  async execute(input: {
    orderId: string;
    amountCents: number;
  }): Promise<{ authorizationId: string }> {
    const order = Order.create(input.orderId, input.amountCents);
    const auth = await this.payments.authorize(order.id, order.amountCents);
    await this.orders.save(order.markAuthorized(auth.authorizationId));
    return { authorizationId: auth.authorizationId };
  }
}

// adapters/PostgresOrderRepository.ts — OUTER, implements port
export class PostgresOrderRepository implements OrderRepository {
  constructor(private db: SqlClient) {}
  async save(order: Order): Promise<void> {
    await this.db.query(
      "insert into orders (id, amount_cents, status, auth_id) values ($1,$2,$3,$4)",
      [order.id, order.amountCents, order.status, order.authorizationId],
    );
  }
}

// composition.ts — the only place `new` happens for adapters
export const buildCreateOrder = ({ db, stripe }) =>
  new CreateOrder(
    new PostgresOrderRepository(db),
    new StripePaymentGateway(stripe),
  );
```

The same shape works in Python (`Protocol`), Go (interface at consumer), Java/Kotlin (interface in the port package). The Dependency Rule is language-agnostic.

---

_Part of the [skill collection](../README.md)._