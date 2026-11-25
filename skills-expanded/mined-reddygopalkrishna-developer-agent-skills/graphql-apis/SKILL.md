---
name: graphql-apis
description: Builds and reviews GraphQL APIs - schema design (nullability, connections, input and payload types, errors as data), per-request DataLoader batching for N+1, depth and cost limits, persisted queries, field-level authorization, schema evolution with deprecation and usage data, caching, subscriptions, federation and type codegen. Use when designing or changing a GraphQL schema or resolvers, a GraphQL server is slow or overloaded, adding auth to a graph, or planning a breaking schema change. Not for choosing between REST, GraphQL and gRPC (see api-design).
license: MIT
---

# GraphQL APIs

A GraphQL schema is a public contract that clients can query in shapes you never planned for. Design it for client use cases, make every resolver safe and cheap to call many times, and never trust the shape or size of an incoming query.

## When to use

- Designing a new schema, or adding types, fields, queries or mutations.
- Writing or reviewing resolvers.
- The GraphQL server is slow, issues too many database queries, or is being abused with heavy queries.
- Adding authentication or authorization to a graph.
- Removing or changing fields that clients use.

Not for: deciding whether to use GraphQL at all (the api-design skill has the REST vs GraphQL vs gRPC table), or general HTTP API conventions.

## Workflow

1. **Start from client operations.** Write the queries and mutations the UI actually needs, then design types to serve them. Do not mirror database tables.
2. **Design the types** with the schema rules below. Run the schema linter and a schema diff against the current production schema.
3. **Implement resolvers** with per-request batching from day one.
4. **Add protection:** depth and cost limits, timeouts, pagination caps, and persisted queries for first-party clients.
5. **Add authorization** in the business layer for every object and field.
6. **Generate types** for server and clients from the schema.
7. **Test:** resolver unit tests, operation-level integration tests against a real schema, and a test that counts database queries for a representative nested query.
8. **Instrument** per-operation and per-field latency and errors before shipping.

## Schema design rules

| Topic | Rule |
| --- | --- |
| Naming | Types `PascalCase`, fields and arguments `camelCase`, enum values `SCREAMING_SNAKE_CASE`. Mutations are verbs: `createOrder`, `cancelOrder`. |
| IDs | Opaque, globally unique `ID!` if clients normalize their cache by ID (the `Node` interface with `node(id:)`). Never expose sequential database IDs as the only identifier if enumeration matters. |
| Nullability | Nullable by default for fields that load from other services or may be denied. Non-null (`!`) only when the field cannot fail. An error in a non-null field nulls its parent, up to the nearest nullable field. |
| Lists | Paginate any list that can grow, using cursor connections (`first`/`after`, `edges { node cursor }`, `pageInfo`). Cap `first` on the server. Use plain lists only for small, bounded sets. |
| Inputs | Each mutation takes one `input: XxxInput!` argument and returns a `XxxPayload` type, so fields can be added later without breaking callers. |
| Expected errors | Return them as data: a `userErrors` field on the payload, or a result union (`CreateOrderResult = CreateOrderSuccess \| OutOfStock \| InvalidAddress`). Clients must handle them. |
| Unexpected errors | Top-level `errors` array with a stable `extensions.code`. Never put stack traces or SQL in messages returned to clients. |
| Enums vs strings | Enums for closed sets the client branches on. Adding an enum value can break clients with exhaustive switches; announce it. |
| Scalars | Custom scalars (`DateTime`, `URL`, `EmailAddress`) with documented formats. Validate them in the scalar parser. |
| Descriptions | Every type and field gets a description. They are the API documentation. |

## Resolvers and N+1

A nested query like `orders { customer { name } }` calls the `customer` resolver once per order. Without batching, 100 orders means 101 database queries.

- Use a DataLoader-style loader for every relation: collect keys during one tick, load them in one query (`WHERE id IN (...)`), and return results **in the same order as the keys**, with `null` or an error for missing ones.
- Create loaders **per request**, in the request context. A loader shared across requests leaks data between users through its cache.
- Batch by the access key, including tenant or permission scope, if results differ by user.
- Resolvers stay thin: parse arguments, call a service or loader, map the result. Business rules and authorization live in the service layer, shared with any REST or job code.
- Measure: log the number of database queries per operation in development and fail a test when a representative query exceeds a budget.

For ORM-level N+1 fixes, see the orm-patterns skill.

## Protecting the server

Any client can send an arbitrarily deep or wide query. Add all of these:

| Control | What to do |
| --- | --- |
| Depth limit | Reject queries deeper than a fixed limit (often around 10, tune to your schema). |
| Cost / complexity limit | Give fields a cost (higher for lists and remote calls, multiplied by `first`) and reject queries over a budget before executing. |
| Pagination caps | Enforce a maximum `first`/`last` per connection on the server. |
| Timeouts | A server-side execution timeout per operation, and timeouts on every downstream call (see the resilience-patterns skill). |
| Rate limiting | Limit by client and by cost, not only by request count. One request can be very expensive. |
| Batching and aliases | Limit operations per HTTP request and aliases per query. Attackers hide brute-force attempts (e.g. many `login` aliases) inside one request. |
| Persisted queries / trusted documents | For first-party clients, register operations at build time and accept only known hashes in production. This blocks arbitrary queries and enables GET and CDN caching. |
| Introspection | Disabling it in production for private APIs reduces discovery. It is defense in depth, not access control: the schema can still be inferred. |

## Authorization

- Authenticate at the HTTP layer and put the user or principal in the request context.
- **Authorize in the business layer**, on every object load and on sensitive fields, not only at the gateway or on root fields. Any object can be reached through many paths (`order.customer.orders.payments`).
- Return `null` plus an error for forbidden nullable fields, or omit the object from lists. Decide whether "not found" and "forbidden" should look the same to avoid leaking existence.
- Never use loaders to bypass permission checks: check after loading, or batch-load only what the user may see.
- Treat arguments as untrusted input: validate formats and bound sizes (string lengths, list lengths, `first`).

For general access-control checks, see the security-audit and auth-implementation skills.

## Evolving the schema

GraphQL APIs are usually versionless. Change them additively:

1. Add the new field or type.
2. Mark the old one `@deprecated(reason: "Use totalPrice. Removal after 2027-03-01.")`.
3. Watch **field-level usage** (from your server's operation metrics or a schema registry) per client.
4. Remove only when usage is zero or the clients have agreed. Removal is a breaking change: get explicit confirmation from the API owner before shipping it.

Breaking changes include: removing or renaming a field, type, argument or enum value; changing a field's type; making an output field nullable that was non-null; making an argument or input field required. Run a schema diff tool in CI (for example GraphQL Inspector, or your schema registry's check command) to block them.

## Caching

- Most GraphQL traffic is POST, which HTTP caches and CDNs ignore. Persisted queries sent as GET make CDN caching possible for public, non-personalized data.
- Clients usually rely on a normalized cache keyed by `__typename` + `id`. Return `id` on every object type that has one, and return the changed objects from mutations so caches update.
- Server-side: cache in loaders (per request) and in the service layer (shared, with care for per-user data). See the caching-strategies skill.

## Subscriptions

- Use subscriptions for small, frequent updates the client is watching (order status, chat). For one-off "tell me when the export is ready", polling or a notification is simpler.
- Transport is usually WebSocket-based; check which protocol your server and client libraries share. For scaling connections, auth on connect and reconnect behavior, see the realtime-apis skill.
- Re-check authorization for each event, not just at subscribe time. Permissions can change during a long connection.
- Publish events from the service layer through a pub/sub system so any server instance can deliver them.

## Federation and multiple teams

- Federation (or schema stitching) lets several services own parts of one graph. Use it when separate teams must deploy their parts independently. A single team usually does better with one schema in one service.
- Each entity has a clear owning service. Other services extend it by key.
- The router adds a hop and a planning step. Monitor query plans and per-subgraph latency.
- Run composition checks in CI for every subgraph change.

## Code generation

- Generate server resolver types and client operation types from the schema (for example GraphQL Code Generator for TypeScript, or your language's equivalent). Hand-written types drift.
- Commit the schema file (SDL) so diffs show in reviews.
- Generate clients from the operations they use, so removing a field fails the client build.

## Anti-patterns

- **Database-shaped schema**: types that mirror tables and expose join tables, making clients do the modeling.
- **No batching**: N+1 queries on every nested list.
- **Shared loader instances** across requests: cross-user data leaks.
- **Auth only on root fields**: nested paths expose data.
- **Unbounded lists** and no cost limits: one query takes down the database.
- **Everything non-null**: one failing field blanks the whole response.
- **Errors only in the `errors` array** for expected business failures: clients can't handle them in a typed way.
- **Monitoring HTTP status only**: GraphQL often returns 200 with errors. Monitor the `errors` field per operation.
- **Removing deprecated fields by date alone**, without checking usage.

## Done when

- The schema is designed from client operations, with descriptions, connections for growing lists, and input/payload types for mutations.
- Every relation resolver uses per-request batching, and a test bounds database queries for a representative nested query.
- Depth, cost, pagination and timeout limits are enforced; first-party clients use persisted queries.
- Authorization is enforced in the business layer for every object and sensitive field.
- A schema diff runs in CI and blocks unapproved breaking changes.
- Per-operation latency, errors and field usage are monitored.
