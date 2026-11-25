---
name: backend-graphql
description: "GraphQL servers done well: when GraphQL fits, schema design (types, nullability, connections for pagination, input types, errors), resolvers and DataLoader against N+1, authorisation per type and field, query depth and cost limits, persisted queries, caching, subscriptions, code generation, choosing a server library, and evolving a schema by deprecation. Read before building or changing a GraphQL API."
---

# GraphQL

The generated GraphQL server exposes every table as a type with every
column, resolves `orders { customer { orders } }` with one query per row,
checks permissions only on the top-level field, lets anyone send a query 40
levels deep, reports every failure as a string in `errors`, and renames a
field while a mobile app still in the stores depends on it. This skill gives
the decision, the schema shape, the resolver pattern and the limits that
keep a GraphQL API fast and safe. One part of the backend; the whole is in
the `backend` skill.

## 1. When GraphQL fits

- Fits: several clients (web, iOS, Android, partners) that need different
  slices of the same data; a graph-shaped domain (products, variants,
  sellers, reviews); frontend teams that change screens without waiting for
  new endpoints; one entry point over several services.
- Does not: a public CRUD API for third parties (REST with OpenAPI is easier
  to cache, rate-limit and document); one web app and one TypeScript team
  (tRPC or server actions carry less machinery); file transfer; webhooks.
- Keep the project's choice. GraphQL beside a working REST API doubles the
  surface to secure: add it for a real consumer.

## 2. The server library

| Stack | Library |
|---|---|
| TypeScript | GraphQL Yoga as the server, Pothos for a typed code-first schema; Apollo Server where the project uses Apollo's platform |
| Go | gqlgen (schema-first, generates types and resolver stubs) |
| Rust | async-graphql |
| Python | Strawberry (code-first with type hints); Graphene only where it already is |
| Java and Kotlin | Spring for GraphQL, or Netflix DGS (`backend-stack-java`) |
| .NET | Hot Chocolate (`backend-stack-dotnet`) |
| Ruby | graphql-ruby (`backend-stack-rails`) |

- Code-first (types from code, SDL printed) cannot drift from the
  resolvers; schema-first (SDL written, code generated) keeps the contract
  in front. Either way, the SDL is printed to a committed `schema.graphql`
  that reviews and CI diff.
- Nexus sees little maintenance now, and hand-written resolver maps full of
  `any` are where untyped servers come from: Pothos for new TypeScript.

## 3. Schema design

```graphql
type Query {
  order(id: ID!): Order
  orders(first: Int = 25, after: String, filter: OrderFilter): OrderConnection!
}

type Order implements Node {
  id: ID!
  number: String!
  status: OrderStatus!
  total: Money!
  customer: Customer              # nullable: deleted, or hidden from this viewer
  items(first: Int = 50, after: String): OrderItemConnection!
  createdAt: DateTime!
}

type Money {
  amount: String!                 # minor units; Int is only 32 bits
  currency: CurrencyCode!
}
```

- Names: types in `PascalCase`, fields and arguments in `camelCase`, enum
  values in `SCREAMING_SNAKE_CASE`; mutations as verb plus noun
  (`placeOrder`) or noun plus verb (`orderCreate`), whichever the schema
  already uses, never both.
- Model the domain, not the tables: no join tables as types, a `customer`
  field instead of `customerId`, no internal columns.
- Nullability on purpose. Non-null for what always exists (`id`, `status`);
  nullable for what can fail or be hidden on its own (a record from another
  service, a field this viewer may not see). An error in a non-null field
  nulls its parent, up to the nearest nullable field: too many `!` and one
  failing field blanks the page. Lists as `[Item!]!`.
- Scalars: `ID` for ids (opaque strings); `DateTime` as ISO 8601 in UTC
  (graphql-scalars); money in minor units as a string or a custom scalar,
  since `Int` stops at 2,147,483,647 and `Float` loses cents.
- Enums for closed sets; document that new values can appear, so clients
  keep a default branch.

## 4. Pagination with connections

- Lists that grow are connections (the Relay spec): `first` and `after`
  (`last` and `before` only when needed), `edges { cursor node }`,
  `pageInfo { hasNextPage endCursor }`, and a `nodes` shortcut if clients
  want it. The cursor is opaque (the encoded sort key and id,
  `backend-api`); `first` defaults to 25 and the server refuses more than
  100.
- `totalCount` only when it is cheap or truly needed: counting a big table
  on every page is the API's slowest query.
- Short fixed lists (a product's three images) stay plain lists.

## 5. Mutations and errors

- One input type and one payload type per mutation
  (`placeOrder(input: PlaceOrderInput!): PlaceOrderPayload!`), so either can
  gain fields without breaking callers.
- Expected business failures are typed data the client must handle: a
  result union, or a `userErrors` list in the payload. One style per schema.

```graphql
union PlaceOrderResult = PlaceOrderSuccess | OutOfStock | ValidationFailed

type PlaceOrderSuccess { order: Order! }
type OutOfStock { productId: ID!, available: Int! }
type ValidationFailed { fields: [FieldError!]! }
type FieldError { field: String!, code: String! }
```

- The top-level `errors` array is for the unexpected and for protocol
  failures (not signed in, too costly, rate limited), each with a stable
  `extensions.code` (`UNAUTHENTICATED`, `FORBIDDEN`, `BAD_USER_INPUT`,
  `INTERNAL_SERVER_ERROR`) and a request id. Unexpected errors are masked in
  production: Yoga masks by default; Apollo Server needs `formatError` and
  `includeStacktraceInErrorResponses: false`.
- HTTP: `POST` for everything, `GET` for queries only, never a mutation.
  With the GraphQL over HTTP media type (`application/graphql-response+json`),
  a document that fails to parse or validate gets a `4xx`; partial data with
  field errors is a `200`.
- With cookie auth, refuse requests a browser can send cross-site without a
  preflight (form or `text/plain` bodies, `GET` without a custom header):
  Apollo's `csrfPrevention` (on by default), Yoga's CSRF prevention plugin.

## 6. Resolvers and DataLoader

- Resolvers are thin: read the arguments, call a service (the same services
  REST uses), map the result. Rules and authorisation live in services.
- N+1 is GraphQL's default: `orders { customer }` calls the `customer`
  resolver once per order. Every field that loads by key goes through a
  DataLoader created per request in the context; it gathers the keys asked
  for in one tick and loads them in one query:

```ts
import DataLoader from "dataloader";

export function makeLoaders(db: Db, viewer: Viewer) {
  return {
    customerById: new DataLoader<string, Customer | null>(async (ids) => {
      const rows = await db.customers.findMany({ ids, tenantId: viewer.tenantId });
      const byId = new Map(rows.map((c) => [c.id, c]));
      return ids.map((id) => byId.get(id) ?? null); // same length, same order
    }),
  };
}
```

- Per request, never global: its cache holds what this viewer may see, and
  a shared one leaks between users and grows forever.
- One-to-many (each order's items) batches by parent id and groups the rows;
  paginated children per parent use a window query
  (`row_number() OVER (PARTITION BY order_id ...)`) or are offered only on
  the single-record field.
- Elsewhere: `GraphQL::Dataloader` in graphql-ruby, Hot Chocolate's and
  async-graphql's DataLoader, dataloadgen with gqlgen, Strawberry's
  `DataLoader`, `@BatchMapping` in Spring for GraphQL.

## 7. Authorisation

- Authenticate once per request while building the context (the session or
  token, `backend-auth`); every resolver sees the `viewer`.
- Authorise where data is loaded: the service checks the viewer may see
  this order, and loaders scope queries by tenant. A check only on
  `Query.order` is bypassed through `customer { orders }`, `node(id:)` or a
  nested connection; every path to a type ends in the same check.
- Rules on sensitive fields (a customer's email, cost prices, internal
  notes): Pothos's scope-auth plugin, graphql-ruby's `authorized?`, Hot
  Chocolate's `[Authorize]` with policies, or a directive the server
  actually enforces. The field returns `null` with an error, or is hidden
  for that role.
- Introspection shows every type and field: fine for a public API. For a
  private one, turn it off in production with field suggestions (they leak
  names too), but never count on that as security.

## 8. Limits against expensive queries

One request can ask for millions of rows. Limits in the server, before
execution (GraphQL Armor bundles most of these for Yoga and Apollo):

| Limit | Start at |
|---|---|
| Depth | 10 to 12 |
| Cost: each field 1, connections multiplied by `first` | 1,000 to 5,000 points, tuned on real operations |
| Page size (`first`, `last`) | 100 |
| Aliases per operation | 15 to 30 (aliases repeat a costly field, or try 500 passwords in one request) |
| Operations per batched request | 5 to 10, or batching off |
| Document size | 100 KB |
| Execution time | 10 to 15 s |

- Public APIs rate-limit by cost, not by request count (as GitHub and
  Shopify do), and return the cost so clients learn their budget.
- Sign-in and other sensitive mutations keep per-account rate limits
  (`backend-security`), since aliases and batching slip past per-request
  limits.

## 9. Persisted queries and trusted documents

- First-party clients use trusted documents: the build extracts every
  operation from the client code (GraphQL Code Generator's client preset
  with persisted documents, Relay's persisted queries), the server stores
  them by hash, and in production it runs only those hashes. Arbitrary
  queries are refused, which ends most cost and depth abuse and shrinks
  requests.
- Automatic persisted queries (the client sends the hash, and the text on a
  miss) only save bandwidth: anyone can register any query. Public APIs
  cannot allow-list at all; they live on the limits in section 8.

## 10. Caching

- Inside a request, DataLoader; across requests, the services' application
  cache (`backend-caching`). Whole-response caching (Yoga's response cache,
  Apollo's `@cacheControl` hints) keyed by the session for anything
  per-user, and invalidated by type and id when mutations run.
- CDN caching needs `GET`: persisted queries sent as `GET` with the hash and
  variables in the URL, public data only, `Cache-Control` from the lowest
  `maxAge` in the operation.
- Client caches (Apollo Client, urql's Graphcache, Relay) normalise by
  `__typename` and `id`: every type with identity has `id: ID!`, and
  mutations return the objects they changed, so no refetch is needed.

## 11. Subscriptions

- For events a client must see at once (a message, a finished job), over
  WebSockets with the `graphql-ws` protocol (`subscriptions-transport-ws` is
  abandoned) or over SSE (`graphql-sse`). Auth on connect, pub/sub across
  instances and limits: `backend-realtime`.
- Authorise each event per subscriber at delivery, not only at subscribe
  time. A list that only needs refreshing every minute is a polled query.

## 12. Tooling and evolution

- Clients get types from the schema: GraphQL Code Generator (client
  preset), gql.tada (types inferred, no build step), the Relay compiler,
  Apollo's iOS and Kotlin generators.
- The schema is linted (graphql-eslint) and diffed in CI against the one in
  production (GraphQL Inspector, or the Apollo GraphOS or Hive registry),
  failing on breaking changes.
- Federation (Apollo Federation, Hive Gateway, Cosmo) only when many teams
  own parts of one graph; one service with modules is simpler.
- Add, never change: new fields, types and optional arguments are safe.
  Removing or renaming a field, changing its type, making a field nullable
  or an argument required breaks clients.
- Deprecate first: `@deprecated(reason: "Use totalPrice.")` on the old field
  with the new one beside it; watch field usage per client (clients send
  their name and version, such as `apollographql-client-name`); remove after
  the window, which for mobile apps is months.

## Check it

- The diff of `schema.graphql` is what you meant, and the breaking-change
  check passes.
- The clients' real operations run in tests with a query counter: counts
  stay flat as page sizes grow.
- As another tenant, and as a user without rights: `order(id:)`,
  `node(id:)` and the nested path (`customer { orders }`) return nothing of
  the other; sensitive fields are null or refused.
- A query 30 levels deep, 500 aliases, `first: 100000`, a batch of 100
  operations and a mutation over `GET`: each refused before execution with a
  clear code.
- In production mode, an unexpected error shows a masked message, a code and
  a request id; introspection is in the state you chose.

## Avoid

Tables exposed as types; `Int` for money or large ids; everything non-null,
or everything nullable; lists without pagination; business rules or SQL in
resolvers; related records loaded one at a time; a DataLoader shared across
requests; permissions checked only at the top-level field; no depth, cost or
alias limits; automatic persisted queries treated as security; errors as
bare strings; stack traces in `errors`; mutations over `GET`; a field renamed
without a deprecation window.
