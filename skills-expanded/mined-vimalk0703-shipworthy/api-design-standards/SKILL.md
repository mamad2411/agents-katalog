---
name: api-design-standards
description: REST API conventions — consistent naming, proper HTTP methods/status codes, pagination, versioning, error responses, and type-safe contracts.
invoke_when: Use when creating API routes, controllers, endpoint handlers, or designing API contracts.
---

# API Design Standards

## URL Conventions
- **Resources are plural nouns**: `/users`, `/orders`, `/products`
- **Nested for relationships**: `/users/:id/orders`
- **Lowercase, hyphen-separated**: `/order-items` not `/orderItems`
- **No trailing slashes**

## HTTP Methods

| Method | Purpose | Idempotent | Body |
|--------|---------|------------|------|
| GET | Read | Yes | No |
| POST | Create | No | Yes |
| PUT | Full replace | Yes | Yes |
| PATCH | Partial update | Yes | Yes |
| DELETE | Remove | Yes | No |

## Status Codes
- `200` OK, `201` Created, `204` No Content
- `400` Bad Request, `401` Unauthorized, `403` Forbidden, `404` Not Found, `409` Conflict, `422` Unprocessable, `429` Rate Limited
- `500` Internal Error, `503` Unavailable

## Error Response Format (consistent across ALL endpoints)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email address is invalid",
    "details": [{ "field": "email", "message": "Must be a valid email" }]
  }
}
```

## Pagination
```
GET /users?page=1&limit=20
```
Response: `{ "data": [...], "pagination": { "total": 150, "page": 1, "limit": 20, "hasMore": true } }`

## Requirements
- Every endpoint MUST have request and response types defined
- Choose one versioning strategy per project (`/api/v1/` or header-based)
- Keep API documentation in sync with code
