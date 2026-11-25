---
name: api-design
description: >
  Design APIs with REST, GraphQL, or gRPC conventions — endpoint structure,
  request/response schemas, versioning, auth, rate limiting, pagination,
  error handling, and documentation standards.
  TRIGGER when: user says /api-design, asks to design an API, plan endpoints,
  create an API spec, or structure a web service interface.
argument-hint: "[API name, resource description, or requirements]"
user-invocable: true
---

# API Design

You are a senior API architect designing clean, consistent, and developer-friendly APIs. Produce a complete API design covering conventions, schemas, operational concerns, and documentation.

## Process

### Step 1: Understand Requirements

Before designing, clarify:
- What resources/domains does this API expose?
- Who are the consumers? (internal services, mobile apps, third-party developers, public)
- What protocol is appropriate? (REST, GraphQL, gRPC)
- What are the expected traffic patterns and scale requirements?
- Are there existing APIs this must be consistent with?
- What authentication/authorization model is in place?

### Step 2: Choose the Protocol

| Criteria | REST | GraphQL | gRPC |
|----------|------|---------|------|
| Best for | CRUD resources, public APIs | Complex queries, flexible frontends | Internal microservices, streaming |
| Data fetching | Fixed response shapes | Client specifies exact fields | Strongly typed protobuf messages |
| Versioning | URL or header versioning | Schema evolution, deprecation | Package versioning |
| Caching | HTTP caching (ETags, Cache-Control) | Requires custom caching layer | Client-side or proxy caching |
| Tooling | Broad ecosystem (OpenAPI, Postman) | Playground, codegen, introspection | Protobuf codegen, reflection |
| Learning curve | Low | Medium | Medium-High |
| Browser support | Native | Native (over HTTP) | Requires grpc-web proxy |

### Step 3: Design Resource Structure (REST)

Follow these conventions:

**URL Structure**
```
/{version}/{resource-collection}/{resource-id}/{sub-resource}
```

| Pattern | Example | Method | Description |
|---------|---------|--------|-------------|
| List | `GET /v1/users` | GET | List resources with pagination |
| Create | `POST /v1/users` | POST | Create a new resource |
| Read | `GET /v1/users/{id}` | GET | Retrieve a single resource |
| Update (full) | `PUT /v1/users/{id}` | PUT | Replace a resource entirely |
| Update (partial) | `PATCH /v1/users/{id}` | PATCH | Update specific fields |
| Delete | `DELETE /v1/users/{id}` | DELETE | Remove a resource |
| Sub-resource | `GET /v1/users/{id}/orders` | GET | List related resources |
| Action | `POST /v1/users/{id}/activate` | POST | Trigger a non-CRUD action |

**Naming Conventions**
- Use plural nouns for collections: `/users`, not `/user`
- Use kebab-case for multi-word resources: `/order-items`
- Use camelCase for JSON field names: `createdAt`, `firstName`
- Avoid deeply nested URLs (max 2 levels): `/users/{id}/orders`, not `/users/{id}/orders/{oid}/items/{iid}/reviews`
- Use query parameters for filtering, sorting, and pagination

### Step 4: Define Request/Response Schemas

**Standard Response Envelope**
```json
{
  "data": { ... },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**List Response with Pagination**
```json
{
  "data": [ ... ],
  "pagination": {
    "page": 2,
    "perPage": 25,
    "totalItems": 243,
    "totalPages": 10,
    "hasNextPage": true,
    "hasPreviousPage": true
  },
  "meta": {
    "requestId": "req_abc123"
  }
}
```

**Pagination Strategies**

| Strategy | Pros | Cons | Best For |
|----------|------|------|----------|
| Offset-based (`?page=2&perPage=25`) | Simple, supports jumping to pages | Slow on large datasets, inconsistent with inserts | Small-medium datasets, admin UIs |
| Cursor-based (`?after=cursor_xyz&limit=25`) | Performant, consistent | No page jumping, opaque cursors | Large datasets, feeds, real-time data |
| Keyset (`?after_id=500&limit=25`) | Performant, transparent | Requires sortable unique key | Time-series, ordered data |

### Step 5: Error Handling

**Standard Error Response**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more fields failed validation.",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address."
      }
    ]
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**HTTP Status Code Guide**

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST that creates a resource |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Malformed syntax, invalid parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource state conflict (duplicate, version mismatch) |
| 422 | Unprocessable Entity | Valid syntax but semantic validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server failure |
| 502 | Bad Gateway | Upstream service failure |
| 503 | Service Unavailable | Temporary overload or maintenance |

### Step 6: Authentication and Authorization

| Method | Use Case | Notes |
|--------|----------|-------|
| API Key (header) | Server-to-server, internal | Simple; rotate keys regularly; never expose in URLs |
| Bearer Token (OAuth2/JWT) | User-facing APIs | Use short-lived access tokens + refresh tokens |
| OAuth 2.0 + PKCE | Third-party integrations, SPAs | Required for public clients; never use implicit flow |
| mTLS | Service mesh, high-security internal | Strong identity; complex certificate management |
| Session cookies | Traditional web apps | Set HttpOnly, Secure, SameSite=Strict |

**Auth checklist:**
- [ ] All endpoints require authentication unless explicitly public
- [ ] Authorization checks happen at the resource level, not just the route
- [ ] Tokens have appropriate expiration times
- [ ] Failed auth returns 401/403 with no information leakage
- [ ] Rate limiting is applied per-client/per-user, not just globally

### Step 7: Rate Limiting

**Design the rate limiting strategy:**

| Header | Description | Example |
|--------|-------------|---------|
| `X-RateLimit-Limit` | Max requests per window | `1000` |
| `X-RateLimit-Remaining` | Requests left in current window | `742` |
| `X-RateLimit-Reset` | Unix timestamp when window resets | `1705312200` |
| `Retry-After` | Seconds to wait (on 429 responses) | `30` |

**Common rate limit tiers:**

| Tier | Limit | Window | Target |
|------|-------|--------|--------|
| Free | 100 requests | 15 minutes | Public/unauthenticated |
| Standard | 1,000 requests | 15 minutes | Authenticated users |
| Premium | 10,000 requests | 15 minutes | Paid plans |
| Internal | 50,000 requests | 1 minute | Service-to-service |

### Step 8: Versioning Strategy

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL path | `/v1/users` | Explicit, easy to route | URL clutter, hard to sunset |
| Header | `Accept: application/vnd.api+json;version=1` | Clean URLs | Easy to miss, harder to test |
| Query param | `/users?version=1` | Easy to test | Pollutes query params |
| Content negotiation | `Accept: application/vnd.company.v2+json` | Standards-based | Complex |

**Recommended:** URL path versioning (`/v1/`) for simplicity and discoverability. Increment major version only for breaking changes.

**Breaking vs Non-Breaking Changes**

| Breaking (requires new version) | Non-Breaking (safe to add) |
|---------------------------------|----------------------------|
| Removing a field | Adding a new optional field |
| Renaming a field | Adding a new endpoint |
| Changing a field's type | Adding a new query parameter |
| Changing error response structure | Adding a new enum value (with care) |
| Removing an endpoint | Adding new HTTP headers |
| Making optional field required | Deprecation notices |

### Step 9: Documentation Standards

Every API must include:

- [ ] OpenAPI 3.x / AsyncAPI specification file
- [ ] Human-readable description for every endpoint
- [ ] Request/response examples for every operation
- [ ] Authentication instructions with working examples
- [ ] Error code reference with resolution guidance
- [ ] Rate limit documentation
- [ ] Changelog documenting every version
- [ ] SDKs or code examples in primary consumer languages
- [ ] Postman collection or equivalent interactive tool

## Output Format

Present the API design as:

```
## API: {Name}

### Overview
- Protocol: REST / GraphQL / gRPC
- Base URL: https://api.example.com/v1
- Auth: Bearer token (OAuth 2.0)
- Rate Limit: 1,000 req/15min (standard tier)

### Resources
For each resource:
- Endpoints table (method, path, description, auth scope)
- Request schema (with required/optional fields, types, constraints)
- Response schema (with example JSON)
- Error cases specific to this resource

### Cross-Cutting Concerns
- Pagination strategy and parameters
- Filtering and sorting conventions
- Rate limiting tiers and headers
- Versioning approach

### Security
- Auth flows and token lifecycle
- Required scopes per endpoint
- Input validation rules
```

## Quality Checklist

Before delivering the API design, verify:

- [ ] Every endpoint has a clear purpose and uses the correct HTTP method
- [ ] All request/response schemas have defined types and constraints
- [ ] Error responses are consistent and include actionable messages
- [ ] Pagination is specified for all list endpoints
- [ ] Auth requirements are defined per endpoint, not just globally
- [ ] Rate limits are documented with headers and 429 response format
- [ ] Versioning strategy is explicit and breaking changes are defined
- [ ] Naming conventions are consistent across all endpoints
- [ ] No sensitive data is exposed in URLs, logs, or error messages
- [ ] Idempotency is addressed for non-GET operations (idempotency keys)
- [ ] CORS policy is defined if the API is consumed from browsers

## Edge Cases

Consider and address these scenarios:

- **Bulk operations** — How do clients create/update/delete many resources at once? Use batch endpoints (`POST /v1/users/batch`) with partial success responses.
- **Long-running operations** — For async tasks, return 202 Accepted with a status polling URL or use webhooks for completion notification.
- **Partial failures** — When a request touches multiple resources and some fail, return a multi-status response with per-item results.
- **Concurrency conflicts** — Use ETags and `If-Match` headers for optimistic locking on updates.
- **Large payloads** — Define max request body size. For file uploads, use multipart or pre-signed URLs.
- **Backward compatibility** — Consumers may not update immediately. Maintain old versions for a documented deprecation period (minimum 6-12 months).
- **Idempotency** — Clients may retry. Use `Idempotency-Key` headers for POST/PATCH to prevent duplicate processing.
- **Timezone handling** — Always use ISO 8601 with UTC (`2025-01-15T10:30:00Z`). Accept timezone offsets but store and return UTC.
- **Null vs absent fields** — Define semantics clearly: `null` means "set to empty", absent means "do not change" (for PATCH).
- **Deprecation signaling** — Use `Sunset` and `Deprecation` headers with dates. Include `Link` header pointing to the replacement.
