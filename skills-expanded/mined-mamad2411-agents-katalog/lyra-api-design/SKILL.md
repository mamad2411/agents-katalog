---
name: lyra-api-design
description: Design APIs as contracts when the user mentions REST, GraphQL, gRPC, endpoints, OpenAPI, or status codes. OpenAPI-first, backwards-compatible.
compatibility: No tools required; pairs with lyra-nodejs for implementation and lyra-code-review for change review.
---

# lyra-api-design

## What it does

An API is a contract, not an afterthought. These rules cover resource modeling, HTTP semantics, OpenAPI-first contracts, pagination, errors, auth, and backwards compatibility across REST, GraphQL, and gRPC. Each rule states the consequence of breaking it and ships with a bad/good pair, because abstract advice doesn't survive contact with real clients. Breaking changes are treated as a last resort, and developer experience is treated as a design requirement. Use it before writing an endpoint, while reviewing an API change, or when choosing a protocol.

## The rules

### 1. Resources are nouns, not verbs

A URL names a thing — a user, an order, an invoice — not an action. If the URL contains a verb, you designed an RPC and labeled it REST.

```
bad:  POST /api/createOrder
good: POST /api/orders
```

### 2. Plural nouns, consistent casing, shallow nesting

Use `/users`, `/users/{id}`, `/users/{id}/orders`. Pick snake_case or kebab-case and stick to it. Stop nesting at one level — `/users/{id}/orders/{id}/items/{id}/variants` is a chain no client wants to build, so flatten to `/orders/{id}/items` and scope by query param.

### 3. HTTP methods are the verbs

GET reads, POST creates, PUT replaces, PATCH patches, DELETE removes. If you find yourself writing `/users/{id}/update` or `/users/{id}/delete`, the method is wrong.

```
bad:  POST /api/users/{id}/update
good: PATCH /api/users/{id}
```

### 4. Status codes encode outcomes

2xx is success, 4xx is a client problem, 5xx is a server problem. Proxies, monitors, and clients branch on the status first, so a 200 with an error body breaks every layer above your code.

```
bad:  200 OK  { "error": "not found" }
good: 404 Not Found  { "error": { "code": "NOT_FOUND", ... } }
```

### 5. Use the full status vocabulary

Don't compress every client error to 400. 409 Conflict for duplicates, 422 for valid JSON with bad semantics, 401 versus 403 for missing auth versus missing permission, 429 for rate limits, 410 for gone. Precision is what lets clients branch correctly.

### 6. The spec is the source of truth

Write or generate `openapi.yaml` first; code validates against it, clients generate from it, and every operation declares both its success and its error responses. Drift between spec and behavior is a bug — CI should catch it with contract tests.

```
bad:  code first, paste a stale Swagger doc later
good: openapi.yaml in the repo, CI fails if the live API doesn't match
```

### 7. Every field has a type, constraint, and description

JSON Schema with `required`, `format`, `minimum`, `maximum`, `pattern`, `maxLength` for every request and response field. Use the right JSON type — `"price": 9.99`, not `"price": "9.99"`; `"active": true`, not `"active": "1"`. No `any`, no "we'll document it later."

### 8. Every collection is paginated, prefer cursors

An unbounded `GET /api/users` that returns 100k rows is a DoS vector and a memory bomb. Enforce a default and maximum page size, and prefer cursor pagination (`?after=opaque_token`) over offset — offset shifts when rows are inserted between fetches, so clients see duplicates or gaps.

```
bad:  GET /api/users            → returns ALL users
good: GET /api/users?limit=50&after=cursor_xyz
```

### 9. Filter, sort, project via allowlisted params

`?status=active&sort=-created_at&fields=id,name` is fine; accepting raw DB column names from the client is not. Define the allowed filter, sort, and projection fields in the schema — otherwise you leak internals and open injection paths.

### 10. One error envelope, everywhere

Every error shares the same shape. Clients parse `code` to branch and show `message` to the human; a single envelope means they only write that logic once.

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "email must be a valid address; received 'foo@bar'",
    "details": [{ "field": "email", "code": "INVALID_FORMAT" }],
    "requestId": "req_abc123"
  }
}
```

### 11. Error messages are actionable

"Invalid input" tells the developer nothing. Name the field, the constraint violated, and the received value when it's safe to expose — "email must be a valid address; received 'foo@bar'" gets the next request right.

### 12. Auth is explicit and rate limits are visible

Every endpoint declares its auth scheme in the OpenAPI doc — bearer, API key, mTLS, OAuth2 scope — applied uniformly. Rate-limited requests return `429` with `Retry-After` and `X-RateLimit-*` headers; a silent throttle causes confusion, and a 429 without retry guidance causes retry storms. No undocumented endpoints as the only protection.

### 13. Idempotency keys for retried writes

POST and PUT that a client may retry should accept an `Idempotency-Key` header, with the server deduping by key. Without it, network retries create duplicate orders, duplicate charges, and duplicate emails.

```
POST /api/charges
Idempotency-Key: 9c1f3a2e-...
```

### 14. Expand, don't break

Safe changes add optional fields, new endpoints, or new optional params. Removing a field, changing a type, making optional required, or changing a status code breaks every client and requires a new version with a migration guide.

```
bad:  v1: { "name": "..." }  →  v1: { "fullName": "..." }
good: v1: { "name": "...", "fullName": "..." }  // name deprecated, sunset later
```

### 15. Version at the boundary, deprecate with a sunset

One version per API surface, bumped atomically — `/v1/...` or `Accept: application/vnd.api+json;version=1`. When deprecating, emit `Deprecation` and `Sunset` headers, document the migration, and keep the old behavior alive until the sunset date. A `410 Gone` with no warning is a betrayal, not a deprecation.

### 16. Time-to-first-call is the metric; docs and SDKs are generated

How long until a new developer makes a successful authenticated call? If it's over 15 minutes, the DX is broken. Render the OpenAPI spec into interactive try-it-out docs with worked examples for every endpoint and every error code, and generate client SDKs from the spec in TS, Python, Go, Java, Ruby — hand-maintained SDKs drift.

## Protocol selection

| Need                                                    | Protocol                       | Why                                              |
| ------------------------------------------------------- | ------------------------------ | ------------------------------------------------ |
| Public API, broad audience, cacheable reads             | **REST + JSON**                | Universal tooling, HTTP caching, easy onboarding |
| Internal service-to-service, low latency, schema-strict | **gRPC + protobuf**            | Binary, streaming, codegen contracts both sides  |
| Flexible client queries, over/under-fetching pain       | **GraphQL**                    | Client declares the shape, single endpoint       |
| Server pushes events to clients                         | **Webhooks / SSE / WebSocket** | Server-initiated delivery                        |

Default to REST. Reach for gRPC when you control both ends and need performance. Reach for GraphQL when many divergent clients fight over a fat REST payload. One protocol per boundary, unless you can document why you need two.

---

_Part of the [skill collection](../README.md)._