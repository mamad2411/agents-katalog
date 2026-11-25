---
name: rest-api-design
description: "Apply when designing or implementing REST APIs. Covers: URL conventions, HTTP methods, status codes, versioning, pagination, error responses, OpenAPI spec. Trigger for: REST, API design, endpoints, HTTP, routes, OpenAPI, Swagger."
---

# REST API DESIGN — Production Standards

## URL Conventions
```
# Resources (nouns, plural, lowercase, hyphens)
GET    /jobs                    # list
POST   /jobs                    # create
GET    /jobs/{id}               # read one
PATCH  /jobs/{id}               # partial update
DELETE /jobs/{id}               # delete
POST   /jobs/{id}/retry         # action (verb after resource)
GET    /users/{id}/jobs         # nested resource

# ❌ Wrong
GET /getJob, POST /createJob, GET /job_list
```

## HTTP Status Codes (use correctly)
```
200 OK              — successful GET, PATCH
201 Created         — successful POST (with Location header)
204 No Content      — successful DELETE
400 Bad Request     — validation error (return field details)
401 Unauthorized    — not authenticated
403 Forbidden       — authenticated but not allowed
404 Not Found       — resource doesn't exist
409 Conflict        — duplicate, state conflict
422 Unprocessable   — semantic validation error
429 Too Many Requests
500 Internal Error  — unexpected server error
503 Service Unavailable — dependency down
```

## Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {"field": "email", "message": "Invalid email format"},
      {"field": "age", "message": "Must be between 18 and 120"}
    ],
    "request_id": "req_abc123",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

## Pagination (cursor-based)
```json
GET /jobs?limit=20&cursor=eyJpZCI6MTAwfQ

{
  "data": [...],
  "pagination": {
    "limit": 20,
    "next_cursor": "eyJpZCI6MTIwfQ",
    "has_more": true
  }
}
```

## Versioning
```
/v1/jobs    # URL versioning (simplest, recommended)
# NOT: Accept: application/vnd.api+json;version=2 (complex)
```

## OpenAPI Spec (always)
```python
# FastAPI generates it automatically
app = FastAPI(
    title="Jobs API",
    version="1.0.0",
    description="Async job processing API",
)
# Accessible at /docs and /openapi.json
```

## Forbidden
❌ Verbs in URLs (/getJob, /createUser)
❌ Returning 200 for errors
❌ No error details in response body
❌ Inconsistent naming (camelCase + snake_case mixed)
❌ Sensitive data in URL params (use body or headers)
