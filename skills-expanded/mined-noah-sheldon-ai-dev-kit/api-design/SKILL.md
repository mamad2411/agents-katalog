---
name: api-design
description: RESTful API design — resource naming, error envelopes, versioning, pagination strategies, rate limiting, idempotency keys, request/response validation with Pydantic/Zod, HATEOAS, OpenAPI generation, API documentation.
origin: AI Dev Kit
---

# API Design

Design RESTful APIs that are consistent, versioned, validated, and documented.
Covers resource modeling, error contracts, pagination, rate limiting, idempotency,
schema validation, HATEOAS, and OpenAPI/Swagger generation.

## When to Use

- Designing a new REST API or refactoring an existing one for consistency.
- Choosing pagination strategy (offset vs cursor vs keyset) for a dataset.
- Implementing API versioning (URL path vs header-based).
- Adding rate limiting, idempotency keys, or request validation.
- Generating OpenAPI specs and interactive documentation.
- Designing error response envelopes for client error handling.

## Core Concepts

### 1. RESTful Resource Naming

**Rules:**
- Use **nouns** for resources, **HTTP methods** for actions
- Use **plural nouns** for collections
- Use **kebab-case** for multi-word resource names
- Nest resources to express ownership, not to exceed 3 levels deep

```
# Good
GET    /api/v1/users              # List users
POST   /api/v1/users              # Create user
GET    /api/v1/users/{id}         # Get user
PUT    /api/v1/users/{id}         # Replace user
PATCH  /api/v1/users/{id}         # Update user fields
DELETE /api/v1/users/{id}         # Delete user
GET    /api/v1/users/{id}/orders  # List user's orders
POST   /api/v1/orders/{id}/cancel # Action on a resource (exception)

# Bad
GET    /api/v1/getUser            # Verb in URL
POST   /api/v1/createUser         # Verb in URL
GET    /api/v1/user               # Singular collection name
GET    /api/v1/users/{id}/orders/{oid}/items/{iid}/details  # Too deep
```

### 2. Error Envelope

Consistent error responses across all endpoints:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 422,
    "message": "Validation failed",
    "details": [
      { "field": "email", "reason": "Invalid email format" },
      { "field": "password", "reason": "Must be at least 8 characters" }
    ]
  }
}
```

**Success envelope with pagination:**

```json
{
  "success": true,
  "data": [
    { "id": "usr_123", "email": "user@example.com", "name": "Jane" }
  ],
  "error": null,
  "pagination": {
    "total": 150,
    "page": 1,
    "page_size": 20,
    "next_cursor": "eyJpZCI6MjB9"
  }
}
```

**Pydantic envelope models:**

```python
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetail(BaseModel):
    field: str
    reason: str


class ErrorEnvelope(BaseModel):
    code: int
    message: str
    details: Optional[list[ErrorDetail]] = None


class PaginationMeta(BaseModel):
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None


class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorEnvelope] = None
    pagination: Optional[PaginationMeta] = None
```

### 3. API Versioning

**URL Path Versioning (recommended):**

```
GET /api/v1/users
GET /api/v2/users
```

- Clear, cacheable, and easy to route
- Clients explicitly opt into a version
- Deprecate v1 by returning `Sunset` header

**Header-Based Versioning:**

```
GET /api/users
Header: API-Version: 2025-01-15
```

- Cleaner URLs, but harder to debug and cache
- Use when versioning by date is preferred (Stripe-style)

**Deprecation headers:**

```
Sunset: Sat, 01 Jan 2027 00:00:00 GMT
Deprecation: true
Link: </api/v2/users>; rel="successor-version"
```

### 4. Pagination Strategies

| Strategy | Best For | Example |
|---|---|---|
| **Offset/Limit** | Small datasets, admin dashboards | `?page=2&limit=20` |
| **Cursor-based** | Large datasets, real-time feeds | `?cursor=eyJpZCI6MjB9&limit=20` |
| **Keyset** | Ordered data with stable keys | `?after_id=42&limit=20` |

**Cursor-based pagination implementation:**

```python
import base64
import json
from typing import Optional


def encode_cursor(values: dict) -> str:
    return base64.urlsafe_b64encode(
        json.dumps(values).encode()
    ).decode()


def decode_cursor(cursor: str) -> dict:
    return json.loads(
        base64.urlsafe_b64decode(cursor.encode()).decode()
    )


async def list_users(
    cursor: Optional[str] = None,
    limit: int = 20,
) -> dict:
    decoded = decode_cursor(cursor) if cursor else {}
    last_id = decoded.get("id", 0)

    users = await db.query(
        "SELECT * FROM users WHERE id > $1 ORDER BY id ASC LIMIT $2",
        last_id, limit + 1,
    )

    has_next = len(users) > limit
    if has_next:
        users = users[:limit]

    next_cursor = encode_cursor({"id": users[-1]["id"]}) if has_next else None

    return {
        "data": users,
        "pagination": {
            "page_size": limit,
            "next_cursor": next_cursor,
            "has_more": has_next,
        },
    }
```

### 5. Rate Limiting

**Response headers:**

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1649000000
Retry-After: 60  (only on 429)
```

**Implementation (token bucket):**

```python
import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
        self.buckets: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_id: str) -> tuple[bool, dict]:
        now = time.time()
        window_start = now - self.window

        # Prune expired entries
        self.buckets[client_id] = [
            t for t in self.buckets[client_id] if t > window_start
        ]

        remaining = self.max_requests - len(self.buckets[client_id])
        reset_at = now + self.window

        if remaining <= 0:
            return False, {
                "X-RateLimit-Limit": str(self.max_requests),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(reset_at)),
                "Retry-After": str(self.window),
            }

        self.buckets[client_id].append(now)
        return True, {
            "X-RateLimit-Limit": str(self.max_requests),
            "X-RateLimit-Remaining": str(remaining - 1),
            "X-RateLimit-Reset": str(int(reset_at)),
        }
```

### 6. Idempotency Keys

For POST/PUT/PATCH operations that must be safe to retry:

```python
import hashlib
from typing import Optional

idempotency_store: dict[str, tuple[int, dict]] = {}


def get_idempotency_key(key: Optional[str], request_body: bytes) -> str:
    if key:
        return key
    return hashlib.sha256(request_body).hexdigest()[:16]


async def handle_idempotent_request(
    key: str,
    handler,
    *args,
    **kwargs,
) -> tuple[int, dict]:
    if key in idempotency_store:
        status, response = idempotency_store[key]
        return status, response

    status, response = await handler(*args, **kwargs)
    idempotency_store[key] = (status, response)
    return status, response
```

**Client usage:**

```
POST /api/v1/payments
Idempotency-Key: req_abc123
{"amount": 100, "currency": "USD"}
# Retry with same key → returns original response, no duplicate charge
```

### 7. Request/Response Validation

**Python with Pydantic:**

```python
from pydantic import BaseModel, Field, field_validator, EmailStr


class CreateUserRequest(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=150)
    role: str = Field(default="user", pattern="^(user|admin|editor)$")

    model_config = {
        "str_strip_whitespace": True,
        "json_schema_extra": {
            "examples": [{
                "email": "user@example.com",
                "name": "Jane Doe",
                "role": "user",
            }]
        },
    }

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v


class CreateUserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str
    created_at: str

    model_config = {"from_attributes": True}
```

**TypeScript with Zod:**

```typescript
import { z } from "zod";

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(150).trim(),
  role: z.enum(["user", "admin", "editor"]).default("user"),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

function validateCreateUser(body: unknown): CreateUserInput {
  return CreateUserSchema.parse(body);
}
```

### 8. HATEOAS (Hypermedia as the Engine of Application State)

```json
{
  "success": true,
  "data": {
    "id": "usr_123",
    "email": "user@example.com",
    "name": "Jane Doe",
    "_links": {
      "self": { "href": "/api/v1/users/usr_123" },
      "orders": { "href": "/api/v1/users/usr_123/orders" },
      "update": { "href": "/api/v1/users/usr_123", "method": "PATCH" },
      "delete": { "href": "/api/v1/users/usr_123", "method": "DELETE" }
    }
  }
}
```

### 9. OpenAPI/Swagger Generation

**FastAPI auto-generates from type hints:**

```python
from fastapi import FastAPI, APIRouter
from app.schemas.user import CreateUserRequest, CreateUserResponse, APIResponse

router = APIRouter(tags=["users"])


@router.post(
    "/users",
    response_model=APIResponse[CreateUserResponse],
    status_code=201,
    summary="Create a new user",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User with this email already exists"},
        422: {"description": "Validation error"},
    },
)
async def create_user(payload: CreateUserRequest):
    ...
```

**Generate static OpenAPI spec:**

```bash
# Export OpenAPI 3.1 JSON
python -c "from app.main import create_app; import json; print(json.dumps(create_app().openapi()))" > openapi.json

# Generate TypeScript client from OpenAPI
npx openapi-typescript openapi.json -o src/api/types.ts

# Generate Python client
openapi-python-client generate --path openapi.json --meta setup
```

## Anti-Patterns

- **Verbs in URLs** — `GET /getUser` instead of `GET /users/{id}`
- **Inconsistent error formats** — Different endpoints return different error shapes
- **No versioning** — Breaking changes force all clients to update simultaneously
- **Offset pagination on huge tables** — Slow queries; use cursor-based pagination
- **Missing idempotency on payments** — Retries cause duplicate charges
- **No rate limiting** — API vulnerable to abuse and overload
- **Validation only on the client** — Always validate server-side
- **Leaking stack traces in 500 errors** — Exposes internals; return generic messages
- **Ignoring HTTP status codes** — Returning 200 for errors with `error: true` in body

## Best Practices

1. **Use noun-based plural URLs** — `/users`, `/users/{id}/orders`
2. **Always wrap responses in a consistent envelope** — `{success, data, error, pagination}`
3. **Version in the URL path** — `/api/v1/...`, `/api/v2/...`
4. **Validate every input** with Pydantic/Zod — reject early, fail fast
5. **Use cursor-based pagination** for any collection that grows beyond 10K rows
6. **Implement idempotency keys** for all mutating operations that clients may retry
7. **Return proper HTTP status codes** — 200/201 for success, 4xx for client errors, 5xx for server errors
8. **Add rate limit headers** so clients can self-regulate
9. **Generate OpenAPI specs from code** — never maintain Swagger by hand
10. **Document with examples** — every endpoint should show request and response samples

## Related Skills

- `backend-patterns` — FastAPI implementation patterns with DI, middleware, and testing
- `api-integrations` — Consuming third-party APIs with retries, auth, and circuit breakers
- `skill-authoring` — Documenting API conventions as reusable skills
