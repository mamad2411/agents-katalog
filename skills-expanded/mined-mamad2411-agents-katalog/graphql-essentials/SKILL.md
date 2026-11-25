---
name: graphql-essentials
description: Use when building or reviewing GraphQL APIs — schema design, DataLoader, federation, subscriptions, field-level authz.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: protocol
  status: active
  invokes_shell: false
  shell_reviewed: valksor 2026-05-17
  related:
    - rest-essentials
    - websocket-essentials
    - observability-essentials
    - security
---

# GraphQL Essentials

**Iron Law: schema is the contract. DataLoader to kill N+1. Authorize per field, not per type.**

## When GraphQL beats REST

| Situation                               | Pick                                               |
| --------------------------------------- | -------------------------------------------------- |
| Mobile clients with varying view shapes | **GraphQL** — fetch exactly what each screen needs |
| Single team, simple CRUD                | **REST** — less ceremony, better caching           |
| Federated graph across N teams          | **GraphQL** (federation)                           |
| File upload / streaming                 | **REST** — multipart over GraphQL is awkward       |
| Heavily aggregated dashboards           | **GraphQL** — one round-trip, many resources       |

GraphQL pays for itself when clients vary or data is graph-shaped. Don't reach for it because it's trendy.

## Schema design

```graphql
type Order {
  id: ID!
  customer: Customer! # non-null because every order has one
  items: [OrderItem!]! # non-null list of non-null items
  status: OrderStatus!
  createdAt: DateTime!
}

input CreateOrderInput { # always wrap mutation args in Input
  customerId: ID!
  items: [OrderItemInput!]!
}

type CreateOrderPayload { # always return a Payload type, not the entity
  order: Order
  userErrors: [UserError!]! # validation/business errors live here
}

enum OrderStatus {
  PENDING
  PAID
  SHIPPED
  CANCELLED
}
```

**Nullability rules:**

- `T!` = field guaranteed present. If resolver returns null, request errors out.
- `[T!]!` = non-null list of non-null items (the right default).
- `[T]` = nullable list of nullable items (almost never what you want).
- Only mark nullable what's genuinely optional (deleted records, pending lookups).

**Input vs Payload:** every mutation takes one Input, returns one Payload. Never accept loose args; never return the bare entity. Payloads let you add fields (warnings, related entities) without breaking the schema.

**Error model:** transport errors → `errors[]` at root. Business errors → typed `userErrors` on the payload. Clients switch on a stable `code` field.

## DataLoader — kill N+1 dead

Naive resolver: fetch order → for each item resolve product → 1 + N queries. With 50 items, 51 queries.

```typescript
// Batch loads per request, keyed by ID
const productLoader = new DataLoader<string, Product>(async (ids) => {
  const rows = await db.product.findMany({ where: { id: { in: ids } } });
  return ids.map(id => rows.find(r => r.id === id) ?? null);
});

// Resolver:
OrderItem: {
  product: (item, _, ctx) => ctx.loaders.product.load(item.productId),
}
```

| Pattern                   | When                                                      |
| ------------------------- | --------------------------------------------------------- |
| **By ID**                 | direct foreign key — most common                          |
| **By relation**           | `loadMany` returns a list per parent (e.g., user → posts) |
| **Cached across request** | default; never share a DataLoader across requests         |

One loader instance **per request**, attached to ctx. Sharing across requests cross-contaminates auth.

## Federation v2 (when you have multiple teams)

Each subgraph owns part of the type. The gateway stitches them.

```graphql
# Orders subgraph
type Order @key(fields: "id") {
  id: ID!
  total: Money!
  customerId: ID!
}

# Customers subgraph
type Customer @key(fields: "id") {
  id: ID!
  email: String!
}

# Orders extends with a reference resolver:
type Order @key(fields: "id") {
  customer: Customer! @requires(fields: "customerId")
}
```

- Use `@key` to mark entity boundaries; gateway uses it for entity fetches.
- `@external` + `@requires` when a field needs data from another subgraph.
- Compose & validate via Rover or Apollo Studio in CI — broken composition = down API.

Don't federate prematurely. One team = one monolithic schema.

## Subscriptions

Real-time over WebSocket (`graphql-ws` protocol — `subscriptions-transport-ws` is deprecated).

```graphql
type Subscription {
  orderUpdated(customerId: ID!): Order!
}
```

- Authorize on **subscribe**, re-check on each push if scope can change.
- Filter at the publisher, not in JS — don't fan-out to 10k connections then drop 9999.
- Pub-sub via Redis/Dragonfly across instances.
- Cap concurrent subscriptions per connection; close idle ones.

See `Skill(websocket-essentials)` for the transport layer.

## Field-level authorization

Type-level checks (`@auth(role: ADMIN)`) leak metadata: a forbidden field still appears in introspection and validates. **Real authz lives in the resolver**, on the resolved value, against ctx.

```typescript
Order: {
  pricingNotes: (order, _, ctx) => {
    if (!ctx.user.can('read', 'order.internal', order)) {
      throw new ForbiddenError(); // returned as typed userError or top-level error
    }
    return order.pricingNotes;
  },
}
```

- Authorize based on **the actual record**, not just role. Row-level rules need the row.
- Don't rely solely on directives for hot paths — they fire after resolution.
- Pair with persisted queries: clients send a hash, server resolves to a known operation. Kills introspection-based attacks.

## Operational guards

| Risk                                | Guard                                             |
| ----------------------------------- | ------------------------------------------------- |
| Depth-DoS query (`a.b.c.d.e.f...`)  | depth limit (e.g. 10)                             |
| Breadth-DoS (`items(limit: 99999)`) | per-field `limit` validators + complexity scoring |
| Introspection abuse                 | disable in production OR require auth             |
| Slow resolvers tanking p95          | per-field tracing (Apollo plugin or OTel)         |

## Pagination

Relay-style cursor connections — and actually emit cursors.

```graphql
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
}
type OrderEdge {
  node: Order!
  cursor: String!
}
type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

## Anti-patterns

- N+1 resolvers without DataLoader
- Returning bare entities from mutations instead of Payload
- Nullable everything "for flexibility" — clients defensive-code forever
- Authorization in directives only, never re-checked against the row
- One DataLoader instance shared across requests
- Federating with 2 teams "for future-proofing"

## Red flags

| Thought                   | Reality                                                                           |
| ------------------------- | --------------------------------------------------------------------------------- |
| "GraphQL handles caching" | Not without persisted queries + careful cache keys. REST/HTTP caching is simpler. |
| "Directives cover authz"  | Directives gate visibility, not access. Resolvers enforce.                        |
| "We need federation"      | Usually you need module boundaries in one schema.                                 |

## Hand-off

For request/response APIs that don't need a graph: `Skill(rest-essentials)`. For subscription transport details: `Skill(websocket-essentials)`. For trace propagation through resolvers: `Skill(observability-essentials)`. For authn token validation: `Skill(security)`.
