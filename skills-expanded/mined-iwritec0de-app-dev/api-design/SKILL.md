---
name: api-design
description: >-
  This skill should be used when the user asks to "design a REST API", "structure
  API endpoints", "choose HTTP status codes", "set up API versioning", "implement
  API pagination", or mentions "REST API", "API design", "endpoint design",
  "OpenAPI", "Swagger", "API versioning", "HTTP status codes", "API authentication",
  "rate limiting", "pagination", "HATEOAS". Provides REST API design patterns,
  OpenAPI specification guidance, authentication strategies, and API versioning.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# API Design Patterns

## REST Resource Design

### URL Structure
```
GET    /api/v1/resources          — List (with pagination)
GET    /api/v1/resources/:id      — Get single
POST   /api/v1/resources          — Create
PUT    /api/v1/resources/:id      — Full update
PATCH  /api/v1/resources/:id      — Partial update
DELETE /api/v1/resources/:id      — Delete

# Nested resources
GET    /api/v1/users/:id/posts    — User's posts
POST   /api/v1/users/:id/posts    — Create post for user

# Actions (non-CRUD)
POST   /api/v1/orders/:id/cancel  — Action on resource
POST   /api/v1/auth/login         — Authentication
POST   /api/v1/auth/refresh       — Token refresh
```

### Naming Rules
- Plural nouns for resources (`/users`, not `/user`)
- Kebab-case for multi-word (`/user-profiles`, not `/userProfiles`)
- No verbs in URLs (`/users`, not `/getUsers`)
- No trailing slashes

## HTTP Status Codes

| Code | When to Use |
|------|-------------|
| 200 | Successful GET, PUT, PATCH, or DELETE |
| 201 | Successful POST (resource created). Include `Location` header. |
| 204 | Successful DELETE with no response body |
| 400 | Invalid request (validation error, malformed JSON) |
| 401 | Not authenticated (missing or invalid credentials) |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict (duplicate resource, version mismatch) |
| 422 | Semantically invalid (valid JSON, but business logic rejects it) |
| 429 | Rate limit exceeded. Include `Retry-After` header. |
| 500 | Server error (never expose internals) |

## Response Formats

### Success (Direct)
```json
{
  "id": "uuid",
  "name": "Example",
  "createdAt": "2025-01-01T00:00:00Z"
}
```

### Success (Envelope)
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "perPage": 20,
    "total": 150
  }
}
```

### Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

## Pagination

### Cursor-Based (Recommended)
```
GET /api/users?cursor=abc123&limit=20

Response:
{
  "data": [...],
  "pagination": {
    "nextCursor": "def456",
    "hasMore": true
  }
}
```

### Offset-Based
```
GET /api/users?page=2&perPage=20

Response:
{
  "data": [...],
  "pagination": {
    "page": 2,
    "perPage": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

## Authentication Patterns

### JWT Bearer Token
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...

Access token: short-lived (15-60 min)
Refresh token: long-lived (7-30 days), stored securely
```

### API Key
```
X-API-Key: sk_live_abc123...

Use for: server-to-server, public data APIs
Never for: user-facing authentication
```

### OAuth 2.0 Flows
- **Authorization Code** — Web apps (most secure)
- **PKCE** — SPAs and mobile apps
- **Client Credentials** — Service-to-service
- **Device Code** — CLI tools and IoT

## Rate Limiting

Include headers in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1672531200
Retry-After: 60
```

Common limits:
- Anonymous: 60 requests/minute
- Authenticated: 1000 requests/minute
- Auth endpoints (login): 10 requests/minute (brute-force prevention)

## Versioning

### URL Path (Recommended)
```
/api/v1/users
/api/v2/users
```

### Header
```
Accept: application/vnd.myapi.v2+json
```

### Query Parameter
```
/api/users?version=2
```

## Caching

```
# Immutable resources
Cache-Control: public, max-age=31536000, immutable

# Dynamic but cacheable
Cache-Control: public, max-age=60, stale-while-revalidate=30

# Never cache
Cache-Control: no-store

# ETag for conditional requests
ETag: "abc123"
If-None-Match: "abc123"  → 304 Not Modified
```

## Security Headers

```
Content-Type: application/json
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000
```

## Input Validation Rules

- Validate ALL input (body, query, params, headers)
- Whitelist allowed fields (don't pass raw input to DB)
- Set max lengths on strings
- Set min/max on numbers
- Validate email, URL, UUID formats
- Sanitize HTML in text fields
- Reject unknown fields (strict mode)
