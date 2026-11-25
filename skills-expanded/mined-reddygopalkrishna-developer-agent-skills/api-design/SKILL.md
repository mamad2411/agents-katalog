---
name: api-design
description: Designs and reviews HTTP/REST APIs that are consistent, evolvable and safe to retry - resource naming, method semantics, status codes, RFC 9457 errors, pagination, versioning, idempotency keys, ETags, rate limits, long-running operations, webhooks and OpenAPI contracts. Use when creating or changing endpoints, writing an OpenAPI spec, reviewing an API PR, deciding if a change is breaking, or choosing between REST, GraphQL and gRPC.
license: MIT
---

# API Design

An API is a contract you cannot take back. Design it so clients can retry safely, evolve without breaking, and understand every failure from the response alone.

## When to use

- Adding or changing an endpoint, request/response shape, or error format.
- Writing or reviewing an OpenAPI document or an API pull request.
- Deciding whether a change is breaking and how to ship it.
- Choosing REST vs GraphQL vs gRPC for a new interface.

Not for: internal function signatures.

Pair with schema work: the API and the tables behind it are designed together. Use the database-schema-design skill for the tables if it is installed. If it is not, at minimum give every table a primary key, enforce NOT NULL, UNIQUE and foreign keys in the database, store times as `timestamptz` (or the database's UTC timestamp type) and money as `numeric`/`decimal`, and index every column the API filters or sorts on.

## Workflow

1. **Find the existing conventions first.** Read the current OpenAPI spec, two or three existing endpoints, and the error format. Consistency with the existing API beats any rule below; flag conflicts instead of silently diverging.
2. **Model resources, not actions.** List the nouns, their identifiers, and their relationships. Map operations to HTTP methods (table below). Only fall back to an action sub-resource (`POST /orders/{id}/cancel`) when the operation is not a state change you can express with PUT/PATCH.
3. **Write the contract before the code.** Add or update the OpenAPI (3.1+) definition: paths, schemas, required fields, examples, every error response. Run a linter (for example Spectral) if the repo has one.
4. **Decide failure behavior explicitly:** which status codes, which are retryable, what the problem-details `type` is for each error.
5. **Check compatibility.** Compare against the previous spec (for example `oasdiff breaking old.yaml new.yaml`) and against the breaking-change rules below. If breaking, stop and agree a versioning or migration plan with the user.
6. **Implement and test the contract:** request validation, error mapping, pagination edges (empty, last page), idempotent retries, and conditional requests.
7. Run the review checklist in [references/review-checklist.md](references/review-checklist.md) before calling it done.

## Resource naming

- Plural nouns, lowercase, hyphenated paths: `/v1/payment-methods/{paymentMethodId}`.
- Nest only for true ownership and at most one level: `/orders/{id}/items`. Otherwise use filters: `/items?orderId=...`.
- IDs are opaque strings in the contract even if they are integers today.
- JSON field names: pick one case (camelCase or snake_case) and never mix. Match the existing API.
- Timestamps: RFC 3339 in UTC (`2026-11-03T14:05:00Z`). Durations: ISO 8601 or explicit units in the field name (`timeoutSeconds`).
- Money: integer minor units or a decimal string, always with an ISO 4217 currency code. Never binary floats.
- Enums: strings, documented as extensible; clients must tolerate unknown values.

## Method semantics

| Method | Use for | Safe | Idempotent | Typical success |
|---|---|---|---|---|
| GET | Read a resource or collection | Yes | Yes | 200, 304 |
| HEAD | Headers only (existence, ETag) | Yes | Yes | 200, 304 |
| POST | Create in a collection, or non-idempotent action | No | No (make it so with an Idempotency-Key) | 201 + `Location`, 202, 200 |
| PUT | Full replace at a known URI (or create at client-chosen URI) | No | Yes | 200, 204, 201 |
| PATCH | Partial update | No | Not by default | 200, 204 |
| DELETE | Remove | No | Yes | 204, 202, 200 |

- GET never changes state. No `GET /users/{id}/delete`.
- PATCH body format must be declared: JSON Merge Patch (RFC 7396, `application/merge-patch+json`) for simple cases, JSON Patch (RFC 6902, `application/json-patch+json`) when you need array operations or test-and-set.
- Repeating a DELETE on an already-deleted resource may return 404; that is still idempotent (the server state is the same).

## Status codes

| Code | Meaning | Notes |
|---|---|---|
| 200 OK | Success with body | |
| 201 Created | Resource created | Include `Location` header and usually the resource |
| 202 Accepted | Work queued, not done | Return a status resource (see long-running operations) |
| 204 No Content | Success, no body | |
| 304 Not Modified | Conditional GET matched | No body |
| 400 Bad Request | Malformed syntax, invalid JSON, wrong types | |
| 401 Unauthorized | Missing or invalid credentials | Send `WWW-Authenticate` |
| 403 Forbidden | Authenticated but not allowed | Use 404 instead when existence itself is secret |
| 404 Not Found | No such resource (for this caller) | |
| 405 Method Not Allowed | Method not supported on the resource | Send `Allow` |
| 409 Conflict | State conflict (duplicate, invalid transition) | |
| 412 Precondition Failed | `If-Match` did not match | Lost-update protection |
| 415 Unsupported Media Type | Wrong `Content-Type` | |
| 422 Unprocessable Content | Well-formed but fails validation | Pick 400 or 422 for validation and use it everywhere |
| 428 Precondition Required | Server requires `If-Match` | |
| 429 Too Many Requests | Rate limited | Send `Retry-After` |
| 500 Internal Server Error | Unexpected bug | Never leak stack traces |
| 502 / 504 | Upstream failed / timed out | Retryable for idempotent requests |
| 503 Service Unavailable | Overloaded or in maintenance | Send `Retry-After` |

Never return 200 with an error payload.

## Errors: RFC 9457 problem details

Return `Content-Type: application/problem+json` for every 4xx/5xx:

```json
{
  "type": "https://api.example.com/problems/insufficient-funds",
  "title": "Insufficient funds",
  "status": 422,
  "detail": "Balance is 30.00 USD; the transfer needs 50.00 USD.",
  "instance": "/v1/transfers/tr_123",
  "errors": [{ "pointer": "/amount", "detail": "exceeds available balance" }]
}
```

- `type` is a stable identifier clients branch on; `title` is constant per type; `detail` is for humans and may change.
- Extension members (like `errors` above, or `traceId`) are allowed; document them.
- Put field-level validation errors in one response, not one error per round trip.
- Never include secrets, SQL, stack traces or internal hostnames.

## Pagination, filtering, sorting

| | Cursor (keyset) | Offset |
|---|---|---|
| Stable under inserts/deletes | Yes | No (items skip or repeat) |
| Performance on deep pages | Constant | Degrades with offset size |
| Jump to page N | No | Yes |
| Default choice | Yes, for feeds, large or changing data | Small, static admin lists |

- Cursor responses: `{ "data": [...], "nextCursor": "opaque-string-or-null" }`. The cursor is opaque (encode the sort key and ID); clients must not parse it.
- Always cap `limit` (for example default 20, max 100) and document both.
- Sort must be deterministic: add the ID as a tiebreaker.
- Filters as query parameters with documented operators: `?status=active&createdAfter=2026-01-01T00:00:00Z`.
- Sort parameter: `?sort=-createdAt,name` with an allowlist of sortable fields.
- Optionally expose `Link` headers (RFC 8288) with `rel="next"`.

## Versioning and compatibility

**Non-breaking (ship anytime):** adding an endpoint; adding an optional request field; adding a response field; adding an enum value *if* clients were told enums are extensible; relaxing validation.

**Breaking (needs a new version or a migration plan):** removing or renaming a field, endpoint or enum value; making an optional field required; changing a type or format; changing default behavior or sort order; tightening validation; changing status codes or error `type`s clients rely on; changing auth requirements; changing pagination style.

Strategies:

| Strategy | Example | When |
|---|---|---|
| URL major version | `/v1/orders` | Default for public APIs; simple to route and cache |
| Header or media type | `Accept: application/vnd.example.v2+json` | When URLs must stay stable |
| Date-based versions | `Api-Version: 2026-11-01` | Many small changes; per-client pinning |

Deprecate before removing: announce, mark `deprecated: true` in OpenAPI, optionally send a `Deprecation` header (RFC 9745) and a `Sunset` header (RFC 8594), measure remaining traffic, then remove.

## Idempotency keys for POST

Clients retry after timeouts. Without idempotency, a retried `POST /payments` charges twice.

1. Client sends `Idempotency-Key: <uuid>` (the header is an IETF draft and is widely used, for example by Stripe).
2. Server stores key + request fingerprint + response, scoped to the caller, with a TTL (for example 24 hours).
3. Same key, same body: return the stored response. Same key, different body: 422 (or 409). Key still in progress: 409.
4. Store the key in the same transaction as the side effect, or use a unique constraint, so concurrent duplicates cannot both succeed.

## Conditional requests (ETags)

- Return `ETag` on GET. Clients send `If-None-Match` and get 304 when unchanged (saves bandwidth).
- For updates, require `If-Match: "<etag>"`; return 412 on mismatch to prevent lost updates. Return 428 if the header is missing and you require it.
- A version number or `updated_at` hash is a fine ETag source.

## Rate limiting

- Return 429 with `Retry-After` (seconds or HTTP date). 503 + `Retry-After` for overload.
- Advertise limits. `RateLimit` / `RateLimit-Policy` headers are an IETF draft; `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` are the common legacy form. Match what the API already uses.
- Limit per credential, not only per IP.

## Long-running operations

1. `POST /v1/reports` returns `202 Accepted`, `Location: /v1/operations/op_123`.
2. `GET /v1/operations/op_123` returns `{ "status": "running" | "succeeded" | "failed", "result": ..., "error": <problem details> }`.
3. On success, link to the created resource (or `303 See Other` to it).
4. Optionally offer a webhook on completion. Never hold an HTTP request open for minutes.

## Webhooks

- **Sign every delivery:** HMAC-SHA256 over `id + timestamp + raw body` with a per-endpoint secret. Consider following the Standard Webhooks specification (standardwebhooks.com); it uses headers along the lines of `webhook-id`, `webhook-timestamp` and `webhook-signature`, but check the exact header names and signed-payload format against the current spec before implementing.
- Receivers: verify the signature on the raw bytes with a constant-time compare; reject timestamps older than a few minutes (replay protection).
- Delivery is at-least-once: include a unique event ID, retry with exponential backoff, and tell consumers to dedupe by ID.
- Order is not guaranteed: include the resource version or timestamp, or send thin events ("order.updated, id=...") and let receivers fetch current state.
- Receivers should return 2xx fast and process asynchronously.

## REST vs GraphQL vs gRPC

| Choose | When |
|---|---|
| REST + OpenAPI | Public or partner APIs, broad client support, HTTP caching matters |
| GraphQL | Many client types with different data needs over one graph; a team that will own schema governance |
| gRPC | Internal service-to-service calls, streaming, strict schemas, polyglot codegen |

Read [references/graphql-and-grpc.md](references/graphql-and-grpc.md) when the API is GraphQL or gRPC, or when choosing between them.

## Anti-patterns

- **Verbs in paths** (`/getUser`, `/createOrder`) — use methods on resources.
- **200 with `{"error": ...}`** — breaks every client, proxy and monitor.
- **Leaking the database schema** — internal column names and join tables become a contract you can never change.
- **Unbounded lists** — every collection endpoint paginates from day one.
- **Silent breaking change "because no one uses that field"** — prove it with traffic data or version it.
- **Retry-unsafe POSTs for money or messages** — require an Idempotency-Key.
- **Different error shapes per endpoint** — one problem-details format everywhere.
- **Booleans that will become states** (`isActive`) — prefer a `status` enum when a third state is plausible.

## Done when

- OpenAPI spec updated, linted, with examples and every error response documented.
- Breaking-change check run against the previous spec; any breaking change has an agreed plan.
- Errors use problem details; codes match the table; no stack traces leak.
- Collections paginate with a capped limit and deterministic sort.
- Non-idempotent writes that matter accept an Idempotency-Key; updates that can race use ETags.
- Tests cover validation errors, auth failures, pagination edges and retries.

## References

- [references/review-checklist.md](references/review-checklist.md) — read when reviewing an API PR or before finishing a design.
- [references/graphql-and-grpc.md](references/graphql-and-grpc.md) — read when the interface is GraphQL or gRPC.
