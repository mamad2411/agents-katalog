---
name: dev-detailed-design
description: Guides the agent through low-level detailed design of a module or component — type/class models, API contracts, sequence diagrams, state machines, and database schemas — before implementation begins.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior Engineer doing detailed design**. Your job is to make every structural decision explicit before code is written, so implementation becomes mechanical. Do NOT spawn a subagent for this.

Design the module/component for: $ARGUMENTS

> **Scope distinction:** [`dev-system-design`](../dev-system-design/SKILL.md) decides *what components exist and how they connect*. This skill decides *how each component is structured internally* — its types, its public API contract, its data model, its state machine, its key flows. Its output is `docs/design-docs/<feature_id>/detailed-design.md`.

> **Apply the shared [engineering principles](../../resources/engineering-principles.md) throughout**, especially §1 (trace to the requirement), §2 (architecture before code), and §3 (design patterns deliberately).

---

## Step 0: Prerequisites
Before starting detailed design, confirm these inputs exist:
- [ ] The US acceptance criteria are listed (from `user_visible_behavior` in `.harness/features.json`).
- [ ] The component's boundary is defined (from `docs/SYSTEM_ARCHITECTURE.md` or a `system-design.md` note).
- [ ] The public interface / API this component must satisfy is known (even if it needs to be designed here).

If any are missing, resolve them before continuing.

---

## Step 1: Define the Public API Contract
The public API is the component's promise to the rest of the system. Define it completely before writing any implementation.

### For HTTP/REST endpoints:
```
POST /api/v1/orders
Authorization: Bearer <token>

Request body:
{
  "customerId": "uuid",
  "items": [{ "productId": "uuid", "quantity": 2 }]
}

Response 201:
{
  "orderId": "uuid",
  "status": "pending",
  "createdAt": "ISO8601"
}

Errors:
  400 – validation failed (list fields)
  401 – unauthenticated
  422 – business rule violation (e.g. insufficient stock)
```

### For a function / module interface:
```typescript
// Define the interface contract before the implementation
interface OrderService {
  placeOrder(cmd: PlaceOrderCommand): Promise<Result<Order, OrderError>>
  cancelOrder(id: OrderId, reason: string): Promise<Result<void, OrderError>>
  getOrder(id: OrderId): Promise<Option<Order>>
}
```

### For a message/event schema:
```json
// Event: order.placed  (published to: orders-topic)
{
  "eventId": "uuid",
  "eventType": "order.placed",
  "occurredAt": "ISO8601",
  "payload": {
    "orderId": "uuid",
    "customerId": "uuid",
    "totalAmount": 9900
  }
}
```

**Rule**: the contract is reviewed and locked before implementation. Changes to the contract after implementation starts are breaking changes and require explicit sign-off.

---

## Step 2: Domain / Type Model
Define the core types, entities, and value objects. Use the language of the domain (see `docs/DOMAIN_GLOSSARY.md` if it exists):

```typescript
// Entity — has identity, lifecycle, invariants
type OrderId = Brand<string, 'OrderId'>
type CustomerId = Brand<string, 'CustomerId'>

interface Order {
  readonly id: OrderId
  readonly customerId: CustomerId
  readonly items: readonly OrderItem[]
  readonly status: OrderStatus
  readonly createdAt: Date
  readonly updatedAt: Date
}

// Value object — no identity, equality by value
interface OrderItem {
  readonly productId: ProductId
  readonly quantity: Quantity  // branded: 1..999
  readonly unitPrice: Money    // branded: non-negative
}

// Bounded set → discriminated union, not open string
type OrderStatus = 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled'
```

Rules:
- **Branded types** for IDs and constrained values — prevent mixing `UserId` with `OrderId` at compile time.
- **Immutable value objects** — no setters. Mutations produce a new instance.
- **Entities** own their invariants — expose methods that transition state validly; never expose raw setters.
- **No anemic domain model** — an `Order` object must be able to reject an invalid transition, not just hold data.

---

## Step 3: State Machine (when applicable)
For entities with lifecycle (Order, Payment, Subscription, Workflow), draw the state machine explicitly:

```
States:       pending → confirmed → shipped → delivered
                   ↘ cancelled ←────────────────┘
                   (cancelled from any pre-delivered state)

Transitions:
  pending    --[confirmOrder]-->  confirmed   (guard: stock available)
  confirmed  --[shipOrder]-->     shipped     (guard: address validated)
  shipped    --[deliverOrder]-->  delivered   (guard: courier confirms)
  *          --[cancelOrder]-->   cancelled   (guard: not already delivered)

Illegal transitions:
  delivered  --[cancelOrder]-->   (throws DomainError)
  cancelled  --[*]-->             (throws DomainError)
```

For each transition, document:
- **Trigger**: command or event that causes it.
- **Guard**: precondition that must hold.
- **Side effects**: events emitted, notifications sent, records created.

---

## Step 4: Sequence Diagrams (key flows)
Draw the two most important flows: the **happy path** and the **primary failure path**.

```
POST /orders — happy path

Client → API Gateway → OrderController → OrderService → InventoryService (sync gRPC)
                                                     → OrderRepository (write)
                                                     → EventBus (publish order.placed)
       ← 201 Created ←──────────────────────────────

POST /orders — insufficient stock

Client → API Gateway → OrderController → OrderService → InventoryService (returns insufficient)
       ← 422 Unprocessable ←──────────────────────────
```

Rules:
- Show every hop across a boundary (network call, DB query, cache lookup, event publish).
- Name each arrow with the operation, not just an arrow.
- Show the failure path — what rolls back, what compensates.

---

## Step 5: Data Model / Schema
For every new table or collection, write the schema with field types, nullability, and constraints:

```sql
-- orders
CREATE TABLE orders (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(id),
  status      TEXT NOT NULL CHECK (status IN ('pending','confirmed','shipped','delivered','cancelled')),
  total_cents INTEGER NOT NULL CHECK (total_cents >= 0),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status      ON orders(status) WHERE status NOT IN ('delivered','cancelled');

-- order_items
CREATE TABLE order_items (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id   UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id),
  quantity   INTEGER NOT NULL CHECK (quantity BETWEEN 1 AND 999),
  unit_cents INTEGER NOT NULL CHECK (unit_cents >= 0)
);
```

For each table document:
- **Write patterns**: insert-only? append-only? soft-delete?
- **Read patterns**: what queries hit this table — are the indexes correct?
- **Cardinality**: one-to-many, many-to-many (junction table needed)?
- **Migration strategy**: how does this change get applied to production without downtime?

---

## Step 6: Error Taxonomy
Define the error types the component can produce and map them to HTTP status codes or error codes:

| Error | Cause | HTTP | Retry? |
|---|---|---|---|
| `ValidationError` | Invalid input field | 400 | No — fix the input |
| `NotFoundError` | Resource does not exist | 404 | No |
| `BusinessRuleError` | Rule violation (e.g. cancel delivered order) | 422 | No — business constraint |
| `ConflictError` | Concurrent modification / duplicate | 409 | Maybe — with new idempotency key |
| `ExternalServiceError` | Downstream unavailable | 502 | Yes — with backoff |
| `InternalError` | Unexpected / programmer error | 500 | No — fix the bug |

---

## Step 7: Identify Invariants & Edge Cases
List what must ALWAYS be true (invariants) and what must NEVER happen (anti-invariants). Implementation will be tested against these:

- **INV-1**: `order.total_cents == sum(item.unit_cents * item.quantity)` — always.
- **INV-2**: An order in `cancelled` status cannot transition to any other status.
- **INV-3**: `order_items` cannot exist without a parent `orders` row (enforced by FK + CASCADE).
- **EDGE-1**: Empty cart (zero items) must be rejected at the API layer before any DB write.
- **EDGE-2**: Concurrent `placeOrder` for the same customer must not double-decrement stock — use `SELECT ... FOR UPDATE` or optimistic locking.

---

## Step 8: Output — Design Note + Handoff
Write `docs/design-docs/<feature_id>/detailed-design.md` with sections mirroring Steps 1–7.

Then hand off to the coding skill with an explicit pointer:
- Coding skill: [`dev-be-developer`](../dev-be-developer/SKILL.md), [`dev-go-developer`](../dev-go-developer/SKILL.md), [`dev-js-ts-developer`](../dev-js-ts-developer/SKILL.md), etc.
- Tell the coding skill: "Implement according to `docs/design-docs/<id>/detailed-design.md`. The API contract, type model, and DB schema are locked — do not deviate without raising a new design decision."
