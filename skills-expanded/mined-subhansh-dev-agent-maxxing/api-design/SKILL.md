---
name: api-design
description: REST API design patterns — naming, versioning, error handling, pagination, authentication.
---

# API Design Patterns

## Naming

- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural: `/users` not `/user`
- Use kebab-case for multi-word: `/user-profiles`
- Nest for relationships: `/users/123/posts`

## HTTP Methods

- `GET` — read (idempotent)
- `POST` — create
- `PUT` — replace (idempotent)
- `PATCH` — partial update
- `DELETE` — remove (idempotent)

## Status Codes

- `200` — OK
- `201` — Created
- `204` — No Content (successful DELETE)
- `400` — Bad Request (validation error)
- `401` — Unauthorized (no token)
- `403` — Forbidden (no permission)
- `404` — Not Found
- `409` — Conflict (duplicate)
- `422` — Unprocessable (valid JSON, invalid data)
- `429` — Too Many Requests
- `500` — Internal Server Error

## Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [
      { "field": "email", "message": "Required" }
    ]
  }
}
```

## Pagination

```
GET /users?page=2&limit=20

{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

## Authentication

- Use Bearer tokens: `Authorization: Bearer <token>`
- Return `401` for missing/invalid tokens
- Return `403` for insufficient permissions

## Versioning

- URL path: `/v1/users` (simplest, most common)
- Header: `Accept: application/vnd.api.v1+json`

## Rate Limiting

Return headers:
- `X-RateLimit-Limit`: max requests per window
- `X-RateLimit-Remaining`: requests left
- `X-RateLimit-Reset`: when the window resets
