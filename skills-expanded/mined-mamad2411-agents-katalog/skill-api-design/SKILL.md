---
name: skill-api-design
description: REST/gRPC API design, versioning strategies, error codes, request/response contracts, backward compatibility, rate limiting, OpenAPI specifications. Use when designing APIs, defining contracts, planning versioning, or ensuring API consistency.
version: 1.0.0
---

# Skill: API Design

Design APIs as contracts. Versions matter. Backward compatibility is non-negotiable.

## REST Principles

- **Noun-based URLs**: `/users` not `/getUsers`
- **HTTP methods**: GET (read), POST (create), PUT (update), DELETE (remove)
- **Status codes**: 200 (OK), 201 (created), 400 (bad request), 401 (auth), 404 (not found), 500 (error)
- **Consistency**: Same patterns across all endpoints

## Versioning Strategy

**URL path** (explicit, clear):
```
GET /api/v1/users   # v1 API
GET /api/v2/users   # v2 API (breaking change)
```

**Header** (less visible, prefer path):
```
GET /api/users
Header: API-Version: 2
```

## Breaking Changes = Major Version

```
v1.0 → v2.0: User response format changed
v1.1 → v1.2: New optional field added (backward-compatible)
v1.0 → v1.1: Bug fix (patch)
```

## API Contract (OpenAPI/Swagger)

```yaml
paths:
  /users/{id}:
    get:
      summary: Get user
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string }
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: Not found
```

## Error Responses

```json
{
  "error": "not_found",
  "message": "User not found",
  "code": 404,
  "details": {
    "resource": "user",
    "id": "user-123"
  }
}
```

## Rate Limiting

```
Header: X-RateLimit-Limit: 1000
Header: X-RateLimit-Remaining: 999
Header: X-RateLimit-Reset: 1640000000
```

## Pagination

```
GET /users?page=2&page_size=10

Response:
{
  "items": [...],
  "total": 245,
  "page": 2,
  "page_size": 10,
  "has_next": true
}
```

## Deprecation Plan

```
1. Announce: Email, docs, API response header
2. Timeline: 6 months before removal
3. Header: X-API-Warn: "endpoint deprecated, use /v2/..."
4. Support: v1 and v2 endpoints run in parallel
5. Remove: After timeline expires
```

---

**Status**: Ready for API design  
**Best for**: API contracts, versioning, error handling
