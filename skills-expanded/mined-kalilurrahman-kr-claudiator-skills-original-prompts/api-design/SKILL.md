---
name: api-design
description: Design a complete REST or GraphQL API from requirements. Outputs endpoints, request/response schemas, error handling, authentication, and versioning strategy.
argument-hint: [API purpose, resources, and key operations]
allowed-tools: Read, Write, Bash
---

# API Design

Design a production-ready API specification from requirements. No ambiguity — every endpoint, field, and error code must be defined with enough detail for engineers to implement and consumers to integrate.

## Process

1. **Parse requirements.** Identify resources, operations, and business constraints.
2. **Choose API style.** REST for resource-oriented, GraphQL for complex data fetching, gRPC for internal services.
3. **Model resources.** Define entities, relationships, and key attributes.
4. **Design endpoints.** Map operations to HTTP methods and paths (REST) or queries/mutations (GraphQL).
5. **Define schemas.** Request bodies, response structures, query parameters, headers.
6. **Plan authentication.** OAuth 2.0, API keys, JWT — pick one and specify flow.
7. **Design error handling.** HTTP status codes, error response format, error codes.
8. **Add versioning strategy.** URL versioning (/v1/), header versioning, or content negotiation.
9. **Document rate limits.** Per-user, per-endpoint, time windows.
10. **Save to OpenAPI/GraphQL schema** file.

## Output Format

### API Overview
- **Purpose:** [One sentence]
- **Style:** REST | GraphQL | gRPC
- **Base URL:** `https://api.example.com/v1`
- **Authentication:** [Method + brief description]

### Resources
| Resource | Description | Key Operations |
|----------|-------------|----------------|
| User | User account | Create, Read, Update, Delete |
| Product | Product catalog | List, Read, Search |
| Order | Purchase order | Create, Read, List |

### Endpoints (REST)

#### GET /users/{id}
**Description:** Retrieve user by ID  
**Auth Required:** Yes  
**Path Parameters:**
- `id` (string, required) — User UUID

**Response 200:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- 404: User not found
- 401: Unauthorized

#### POST /users
**Description:** Create new user  
**Auth Required:** No (public registration)  
**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "string",
  "name": "string"
}
```

**Response 201:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors:**
- 400: Validation error (email format, password strength)
- 409: Email already exists

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email format is invalid",
    "field": "email",
    "details": {}
  }
}
```

### Error Codes
| Code | HTTP Status | Meaning |
|------|-------------|---------|
| VALIDATION_ERROR | 400 | Input validation failed |
| UNAUTHORIZED | 401 | Missing or invalid token |
| FORBIDDEN | 403 | Valid token, insufficient permissions |
| NOT_FOUND | 404 | Resource does not exist |
| CONFLICT | 409 | Resource already exists |
| RATE_LIMIT | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Server error |

### Authentication Flow (OAuth 2.0)
1. Client redirects user to `/oauth/authorize`
2. User grants permission
3. Server redirects back with authorization code
4. Client exchanges code for access token at `/oauth/token`
5. Client includes token in `Authorization: Bearer {token}` header

### Rate Limits
- Default: 1000 requests/hour per user
- Burst: 100 requests/minute
- Headers returned:
  - `X-RateLimit-Limit: 1000`
  - `X-RateLimit-Remaining: 847`
  - `X-RateLimit-Reset: 1640000000`

### Versioning
- URL-based: `/v1/`, `/v2/`
- Breaking changes require new version
- Non-breaking changes (new optional fields) added to current version
- Deprecation: 6-month notice, sunset timeline announced

### Pagination
```
GET /users?page=2&limit=50
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 50,
    "total": 487,
    "pages": 10
  }
}
```

## Rules

- Every endpoint must have explicit authentication requirement (Yes/No).
- Error responses must include machine-readable error codes, not just HTTP status.
- Required vs optional fields must be clearly marked.
- Rate limits are mandatory for public APIs.
- Include realistic examples with actual data, not placeholder text.
- If requirements are vague, list specific questions before designing.
- Choose appropriate HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove).
- Use plural nouns for collections: `/users` not `/user`.
- Save final output as OpenAPI 3.0 YAML if REST, or GraphQL schema if GraphQL.
