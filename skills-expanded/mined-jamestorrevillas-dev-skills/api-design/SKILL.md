---
name: api-design
description: Use this skill when designing or reviewing APIs — REST, GraphQL, tRPC, or gRPC. Trigger on keywords: API design, REST, GraphQL, tRPC, gRPC, endpoint, schema, route, OpenAPI, Swagger, API versioning, pagination, API contract, HTTP methods.
---

# API Design

## Choosing the Right API Type

| Type | Best For | Avoid When |
|---|---|---|
| **REST** | Public APIs, CRUD, simple clients, IoT | Complex nested data, rapid schema iteration |
| **GraphQL** | Mobile apps, complex nested data, multiple clients | Simple CRUD, small teams new to it |
| **tRPC** | TypeScript monorepos, internal full-stack TS APIs | Non-TypeScript clients, public APIs |
| **gRPC** | High-performance microservice comms, streaming | Browser clients, simple use cases |

---

## REST API Design

### URL Conventions
```text
GET    /users              ← list
GET    /users/{id}         ← single
POST   /users              ← create
PUT    /users/{id}         ← replace
PATCH  /users/{id}         ← partial update
DELETE /users/{id}         ← delete

# Nested resources
GET    /users/{id}/orders
POST   /users/{id}/orders

# Actions (when REST verbs aren't enough)
POST   /orders/{id}/cancel
POST   /users/{id}/activate
```

### HTTP Status Codes
| Code | Use When |
|---|---|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST that creates |
| 204 | Successful DELETE (no body) |
| 400 | Validation failure, bad request |
| 401 | Missing/invalid authentication |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate, version mismatch) |
| 422 | Unprocessable entity (semantic errors) |
| 429 | Rate limit exceeded |
| 500 | Unexpected server error |

### Response Envelope
```json
// Collection
{
  "data": [...],
  "meta": { "total": 100, "page": 1, "perPage": 20 }
}

// Single resource
{ "data": { "id": "1", "name": "James" } }

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [{ "field": "email", "issue": "Invalid format" }]
  }
}
```

---

## API Design Principles

### Versioning Strategy
```text
# URL versioning (most visible, easiest to route)
/v1/users
/v2/users

# Header versioning (cleaner URLs)
Accept: application/vnd.api+json;version=2
```text

Never break existing clients. Deprecate, then remove.

### Pagination
```text
# Offset (simple, good for small datasets)
GET /posts?page=2&perPage=20

# Cursor (fast for large datasets, use for infinite scroll)
GET /posts?cursor=eyJpZCI6MTAwfQ&limit=20
```text

### Filtering & Sorting
```text
GET /orders?status=pending&userId=123
GET /products?sort=-price,name    # - prefix = descending
GET /products?fields=id,name,price  # sparse fieldsets
```text

### Idempotency
```text
# Include idempotency key for non-idempotent operations
POST /payments
Idempotency-Key: unique-client-generated-uuid
```text

---

## GraphQL Design

### Schema Design Rules
- Describe business domain, not DB structure
- Use connections pattern for lists (pagination-ready)
- Mutations return the modified object
- Use enums for finite value sets
- Add descriptions to all types and fields

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, pagination: PaginationInput): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
```

---

## API Security Checklist

- [ ] All endpoints require authentication (unless explicitly public)
- [ ] Authorization checked per resource, not just per route
- [ ] Rate limiting on all endpoints, stricter on auth endpoints
- [ ] Input validation on every parameter and body field
- [ ] Sensitive data not returned unless explicitly needed
- [ ] CORS configured with explicit whitelist
- [ ] API versioning strategy defined before going public
