---
name: api-design-patterns
description: >
  REST and GraphQL API design patterns. Resource naming, HTTP methods, status codes, error formats,
  pagination, versioning, and rate limiting. Use when designing APIs, reviewing endpoints, or
  writing OpenAPI specs.
---

# api-design-patterns

REST and GraphQL API design patterns.

## Mandatory Rules (Blocking — violating any is an error)

1. **Every endpoint MUST return a consistent error envelope**: `{ "error": { "code": "...", "message": "...", "details": [...] } }`
2. **Never expose internal IDs in URLs without validation** — all path params must be validated (UUID format, existence check)
3. **Never return 200 for errors** — use proper 4xx/5xx status codes
4. **Every collection endpoint MUST support pagination** — no unbounded lists
5. **Every mutating endpoint MUST be idempotent or document why not** — include Idempotency-Key header support for POST
6. **Never break backwards compatibility** — additive changes only without version bump
7. **Every endpoint MUST have rate limiting** — return 429 with Retry-After header
8. **No sensitive data in URLs** — tokens, passwords, PII go in headers or body, never query params
9. **All responses MUST include request-id header** — for tracing and debugging
10. **OpenAPI spec MUST exist** — no endpoint without a spec entry

## Forbidden Patterns (Anti-patterns to reject on sight)

- `GET /getUsers` — verb in resource name
- `POST /users/delete` — using POST for deletion
- `200 OK` with `{ "success": false }` — lying status codes
- Nested resources deeper than 2 levels: `/a/{id}/b/{id}/c/{id}/d`
- Mixed casing: `/userProfiles` and `/user-profiles` in same API
- Returning full objects on DELETE (use 204 No Content)
- Pagination without total count or next-page cursor
- Error responses without machine-readable error codes

## Decision Matrix — When to Use What

| Scenario | Use | Not |
|----------|-----|-----|
| Need items 1-100 of 10K | Cursor pagination | Offset pagination |
| Sub-resource of a parent | Nested URL `/users/{id}/orders` | Flat URL `/orders?user_id=X` |
| Long-running operation | 202 Accepted + polling endpoint | Synchronous wait |
| Bulk operations | POST /bulk with array body | Multiple individual calls |
| Search across types | GET /search?q=... | GET on each resource separately |
| File upload | multipart/form-data | Base64 in JSON body |
| Versioning | URL prefix `/v2/` | Header-based (harder to test) |
| Auth | Bearer token in Authorization header | API key in query param |

## how to use

- `/api-design-patterns`
  Apply these API conventions to all endpoint design in this conversation.

- `/api-design-patterns <endpoint>`
  Review the endpoint against rules below and suggest improvements.

## when to apply

Reference these guidelines when:
- designing new API endpoints or resources
- choosing HTTP methods and status codes
- implementing error handling for APIs
- adding pagination, filtering, or sorting
- writing OpenAPI/Swagger specifications
- implementing rate limiting or auth
- reviewing API designs for consistency

## rule categories by priority

| priority | category | impact |
|----------|----------|--------|
| 1 | resource naming | critical |
| 2 | HTTP methods | critical |
| 3 | status codes | high |
| 4 | error responses | high |
| 5 | pagination | high |
| 6 | versioning | medium |
| 7 | rate limiting | medium |
| 8 | idempotency | medium |

## quick reference

### 1. resource naming (critical)

- use nouns, not verbs: `/users` not `/getUsers`
- use plural nouns: `/users`, `/orders`, `/products`
- use lowercase with hyphens: `/user-profiles` not `/userProfiles`
- nest for relationships: `/users/{id}/orders`
- limit nesting to 2 levels max
- use query params for filtering: `/users?role=admin&status=active`
- avoid trailing slashes; be consistent

### 2. HTTP methods (critical)

| Method | Action | Idempotent | Safe | Request Body |
|--------|--------|------------|------|-------------|
| GET | Read resource(s) | Yes | Yes | No |
| POST | Create resource | No | No | Yes |
| PUT | Replace resource entirely | Yes | No | Yes |
| PATCH | Partial update | No | No | Yes |
| DELETE | Remove resource | Yes | No | Optional |

- GET must never modify state
- POST for actions that don't map to CRUD: `/orders/{id}/cancel`
- PUT requires full resource representation
- PATCH sends only changed fields

### 3. status codes (high)

**Success**:
| Code | Use |
|------|-----|
| 200 | Successful GET, PUT, PATCH, DELETE |
| 201 | Successful POST (resource created); include Location header |
| 204 | Successful DELETE or action with no response body |

**Client errors**:
| Code | Use |
|------|-----|
| 400 | Malformed request, validation failure |
| 401 | Missing or invalid authentication |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state conflict) |
| 422 | Valid syntax but unprocessable content |
| 429 | Rate limit exceeded |

**Server errors**:
| Code | Use |
|------|-----|
| 500 | Unexpected server error |
| 502 | Bad gateway (upstream failure) |
| 503 | Service unavailable (maintenance, overload) |

### 4. error responses (high)

Use a consistent error format across all endpoints:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "INVALID_FORMAT"
      }
    ],
    "request_id": "req_abc123"
  }
}
```

- always include a machine-readable error code
- always include a human-readable message
- include field-level details for validation errors
- include request_id for traceability
- never expose stack traces or internal details in production

### 5. pagination (high)

**Prefer cursor-based pagination** for large or frequently changing datasets:
```json
{
  "data": [],
  "pagination": {
    "next_cursor": "eyJpZCI6MTAwfQ==",
    "has_more": true,
    "limit": 25
  }
}
```

**Offset-based** acceptable for small, static datasets:
```
GET /users?offset=20&limit=10
```

Rules:
- default page size: 25; max: 100
- always return pagination metadata
- include total count only when cheap to compute
- return empty array (not null) for no results

### 6. versioning (medium)

**Preferred**: URL path versioning: `/api/v1/users`
- simple, explicit, cacheable
- increment major version only for breaking changes

**Alternative**: Header versioning: `Accept: application/vnd.api+json;version=2`

Rules:
- support at most 2 concurrent versions
- deprecation notice 6+ months before removal
- document breaking changes in changelog
- never break existing clients silently

### 7. rate limiting (medium)

- return rate limit headers on every response:
  - `X-RateLimit-Limit`: max requests per window
  - `X-RateLimit-Remaining`: remaining in current window
  - `X-RateLimit-Reset`: UTC epoch seconds when window resets
- return 429 with `Retry-After` header when exceeded
- rate limit by API key, not just IP
- different limits for different endpoint tiers

### 8. idempotency (medium)

- GET, PUT, DELETE are naturally idempotent
- make POST idempotent with idempotency keys: `Idempotency-Key: <uuid>`
- store idempotency results for replay (24h minimum)
- return cached result for duplicate idempotency keys
- critical for payment and financial endpoints

## common fixes

| problem | fix |
|---------|-----|
| verb in URL (`/getUser`) | rename to noun (`/users/{id}`) |
| 200 for errors | use appropriate 4xx/5xx status codes |
| inconsistent error format | adopt standard error envelope |
| no pagination | add cursor-based pagination |
| breaking change without version bump | increment API version |
| missing rate limiting | add rate limiter middleware |
