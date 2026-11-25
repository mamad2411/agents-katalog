---
name: rest-essentials
description: Use when designing or reviewing REST APIs — resource modeling, OpenAPI contracts, versioning, rate limiting, error shapes.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: protocol
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [graphql-essentials, websocket-essentials, observability-essentials, security]
---

# REST Essentials

**Iron Law: resource-oriented URLs, status codes carry semantics, OpenAPI is your contract. Version in the URL when breaking; deprecate before deleting.**

## Resource design

URLs name **resources** (nouns), HTTP methods carry **verbs**. If your URL has a verb in it, you're doing RPC, not REST.

```
GET    /orders                # list
GET    /orders/{id}           # read one
POST   /orders                # create
PATCH  /orders/{id}           # partial update
PUT    /orders/{id}           # full replace (rare)
DELETE /orders/{id}           # remove
GET    /orders/{id}/items     # sub-resource
```

| Symptom                     | Fix                                                  |
| --------------------------- | ---------------------------------------------------- |
| `/getOrders`, `/createUser` | rename to noun + method                              |
| `/orders?action=cancel`     | `POST /orders/{id}/cancel` (controller sub-resource) |
| Deeply nested `/a/b/c/d/e`  | flatten; add filter query params                     |
| Returning entire DB row     | shape DTO; never leak internal columns               |
| Pluralize inconsistently    | always plural for collections                        |

## Status codes (semantics matter)

| Code | Meaning           | Use when                                                   |
| ---- | ----------------- | ---------------------------------------------------------- |
| 200  | OK                | GET/PUT/PATCH success with body                            |
| 201  | Created           | POST created a resource; `Location:` header pointing to it |
| 202  | Accepted          | async — work queued, not done                              |
| 204  | No Content        | DELETE success, or PUT/PATCH with no body                  |
| 400  | Bad Request       | malformed payload, missing required field                  |
| 401  | Unauthorized      | no/invalid auth — you don't know who's calling             |
| 403  | Forbidden         | known caller, denied                                       |
| 404  | Not Found         | resource doesn't exist (or you don't want to admit it)     |
| 409  | Conflict          | concurrent edit, unique constraint, version mismatch       |
| 422  | Unprocessable     | well-formed but semantically invalid                       |
| 429  | Too Many Requests | rate-limited — include `Retry-After`                       |
| 500  | Internal Error    | your bug; never leak details                               |
| 503  | Unavailable       | dependency down, maintenance — include `Retry-After`       |

**Status 200 with `{"error": ...}` in the body is a sin.** The caller can't trust the protocol layer; every client must inspect the body to know success. Use the right code.

## OpenAPI is the contract

Schema-first. Generate clients and server stubs from one OpenAPI document; never hand-write both sides.

```yaml
paths:
  /orders/{id}:
    get:
      operationId: getOrder
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        "200":
          description: order found
          content:
            application/json:
              schema: { $ref: "#/components/schemas/Order" }
        "404": { $ref: "#/components/responses/NotFound" }
```

- `operationId` becomes the generated function name — make it readable.
- Reuse via `$ref`; duplicating schemas is how contracts drift.
- Lint with Spectral or Redocly in CI. Block PRs that break the contract.
- Publish the spec at `/openapi.json` or `/.well-known/openapi`.

## Versioning

| Strategy     | Looks like                                   | Verdict                                                      |
| ------------ | -------------------------------------------- | ------------------------------------------------------------ |
| **URL path** | `/v1/orders`, `/v2/orders`                   | **Default.** Visible in logs, easy to route, cache-friendly. |
| Header       | `Accept: application/vnd.api+json;version=2` | Hidden, breaks browsers, complicates CDN caching.            |
| Query        | `/orders?v=2`                                | Pollutes cache keys, leaks into bookmarks.                   |
| Media type   | `Accept: application/vnd.acme.v2+json`       | "Hypermedia-pure" but operationally painful.                 |

**Bump major versions only for breaking changes.** Additive changes (new field, new optional param, new endpoint) don't need a new version. Use `Deprecation:` and `Sunset:` headers (RFC 9745/8594) — give consumers ≥ 6 months notice before deleting v1.

## Rate limiting

Token bucket per client identity (API key, user ID, IP fallback). Two layers: a fast bucket for burst protection, a slow quota for daily volume.

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 994
X-RateLimit-Reset: 1747503600   # unix seconds
Retry-After: 30                  # only on 429/503
```

- Redis/Dragonfly for shared state across instances.
- Different limits per route class (writes < reads; auth endpoints stricter).
- Return 429 with `Retry-After` — clients with sane SDKs will back off.
- Document limits in OpenAPI under each operation.

## Error shape (consistent across every route)

```json
{
  "error": "validation_failed",
  "message": "field 'email' must be a valid email",
  "request_id": "req_01HZ...",
  "retryable": false,
  "details": [{ "field": "email", "code": "format" }]
}
```

- `error` is a stable machine code; clients switch on it.
- `message` is human-readable; never leak stack traces or internal SQL.
- `request_id` echoes the trace ID — paste it into logs to find the event.
- `retryable` tells the client whether to back off and retry vs. fail fast.

Same shape on every error response. Lock it down in OpenAPI with a `$ref` and validate in middleware.

## Pagination

Default to **cursor** pagination. Offset breaks under writes (rows shift), and on large tables it scans the whole prefix every page.

```
GET /orders?limit=50&cursor=eyJpZCI6ImFiYyJ9
→ { items: [...], next_cursor: "eyJpZCI6Inh5eiJ9", has_more: true }
```

Encode the cursor (opaque base64 of `{id, sort_key}`). Document max `limit`. Return `has_more` so the client knows when to stop.

## Anti-patterns

- RPC verbs in URLs (`/getOrder`, `/cancelInvoice`)
- 200 OK with `{ "error": ... }` body
- Returning DB models directly — versioning hell, info leakage
- No pagination on list endpoints — works at 10 rows, OOMs at 100k
- Surprise breaking changes (rename a field in v1 without bumping)
- Hand-written client AND server with no shared schema
- Missing `request_id` in errors — debugging by guessing
- 401 vs 403 confusion (no auth = 401; wrong auth = 403)
- One global rate limit across all routes

## Red flags

| Thought                                   | Reality                                                            |
| ----------------------------------------- | ------------------------------------------------------------------ |
| "We'll document it later"                 | Consumers will reverse-engineer it. Their guess becomes your spec. |
| "Just one breaking change"                | Two months later, six clients are broken in production.            |
| "Headers are cleaner than URL versioning" | Cleaner for the spec, hell for caching, debugging, and routing.    |
| "Rate limits aren't needed yet"           | First abusive client says hi.                                      |

## Hand-off

For GraphQL when REST doesn't fit: `Skill(graphql-essentials)`. For real-time push: `Skill(websocket-essentials)`. For trace-ID propagation feeding `request_id`: `Skill(observability-essentials)`. For authn/authz on routes: `Skill(security)`.
