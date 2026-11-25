---
name: api-design
description: REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs.
---

# API Design Patterns

Conventions and best practices for designing consistent, developer-friendly REST APIs.

## When to Activate

- Designing new API endpoints
- Reviewing existing API contracts
- Adding pagination, filtering, or sorting
- Implementing error handling for APIs
- Planning API versioning strategy

## Resource Design

### URL Structure

```
# Resources are nouns, plural, lowercase, kebab-case
GET    /api/v1/assets
GET    /api/v1/assets/:id
POST   /api/v1/assets
PUT    /api/v1/assets/:id
PATCH  /api/v1/assets/:id
DELETE /api/v1/assets/:id

# Sub-resources for relationships
GET    /api/v1/users/:id/assets
POST   /api/v1/users/:id/assets

# Actions that don't map to CRUD (use verbs sparingly)
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
```

### Naming Rules

```
# GOOD
/api/v1/asset-prices          # kebab-case for multi-word resources
/api/v1/assets?status=active  # query params for filtering
/api/v1/users/123/assets      # nested resources for ownership

# BAD
/api/v1/getAssets              # verb in URL
/api/v1/asset                  # singular (use plural)
/api/v1/asset_prices           # snake_case in URLs
```

## HTTP Methods and Status Codes

### Method Semantics

| Method | Idempotent | Safe | Use For |
|--------|-----------|------|---------|
| GET | Yes | Yes | Retrieve resources |
| POST | No | No | Create resources, trigger actions |
| PUT | Yes | No | Full replacement of a resource |
| PATCH | No* | No | Partial update of a resource |
| DELETE | Yes | No | Remove a resource |

### Status Code Reference

```
# Success
200 OK                    — GET, PUT, PATCH (with response body)
201 Created               — POST (include Location header)
204 No Content            — DELETE, PUT (no response body)

# Client Errors
400 Bad Request           — Validation failure, malformed JSON
401 Unauthorized          — Missing or invalid authentication
403 Forbidden             — Authenticated but not authorized
404 Not Found             — Resource doesn't exist
409 Conflict              — Duplicate entry, state conflict
422 Unprocessable Entity  — Semantically invalid (valid JSON, bad data)
429 Too Many Requests     — Rate limit exceeded

# Server Errors
500 Internal Server Error — Unexpected failure (never expose details)
503 Service Unavailable   — Temporary overload, include Retry-After
```

### Common Mistakes

```
# BAD: 200 for everything
{ "status": 200, "success": false, "error": "Not found" }

# GOOD: Use HTTP status codes semantically
HTTP/1.1 404 Not Found
{ "error": { "code": "not_found", "message": "Asset not found" } }

# BAD: 200 for created resources
# GOOD: 201 with Location header
HTTP/1.1 201 Created
Location: /api/v1/assets/abc-123
```

## Response Format

### Success Response

```json
{
  "data": {
    "id": "abc-123",
    "name": "Bitcoin",
    "ticker": "BTC",
    "quantity": 0.5,
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### Collection Response (with Pagination)

```json
{
  "data": [
    { "id": "abc-123", "name": "Bitcoin", "ticker": "BTC" },
    { "id": "def-456", "name": "Ethereum", "ticker": "ETH" }
  ],
  "meta": {
    "total": 42,
    "page": 1,
    "per_page": 20,
    "total_pages": 3
  },
  "links": {
    "self": "/api/v1/assets?page=1&per_page=20",
    "next": "/api/v1/assets?page=2&per_page=20",
    "last": "/api/v1/assets?page=3&per_page=20"
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      {
        "field": "ticker",
        "message": "Must be uppercase letters only",
        "code": "invalid_format"
      },
      {
        "field": "quantity",
        "message": "Must be greater than 0",
        "code": "out_of_range"
      }
    ]
  }
}
```

## Pagination

### Offset-Based (Simple)

```
GET /api/v1/assets?page=2&per_page=20

# Implementation (GORM)
db.Offset((page-1)*perPage).Limit(perPage).Find(&assets)
```

**Pros:** Easy to implement, supports "jump to page N"
**Cons:** Slow on large offsets, inconsistent with concurrent inserts

### Cursor-Based (Scalable)

```
GET /api/v1/assets?cursor=eyJpZCI6MTIzfQ&limit=20

# Implementation
SELECT * FROM assets WHERE id > :cursor_id ORDER BY id ASC LIMIT 21;
```

**Pros:** Consistent performance, stable with concurrent inserts
**Cons:** Cannot jump to arbitrary page

### When to Use Which

| Use Case | Pagination Type |
|----------|----------------|
| Admin dashboards, small datasets (<10K) | Offset |
| Infinite scroll, feeds, large datasets | Cursor |
| Public APIs | Cursor (default) |
| Search results | Offset (users expect page numbers) |

## Filtering, Sorting, and Search

### Filtering

```
# Simple equality
GET /api/v1/assets?currency=USD&status=active

# Comparison operators
GET /api/v1/assets?value[gte]=1000&value[lte]=50000

# Multiple values
GET /api/v1/assets?currency=USD,TWD,JPY
```

### Sorting

```
# Single field (prefix - for descending)
GET /api/v1/assets?sort=-value

# Multiple fields
GET /api/v1/assets?sort=-value,name
```

### Sparse Fieldsets

```
# Return only specified fields
GET /api/v1/assets?fields=id,name,ticker,value
```

## Rate Limiting

### Headers

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000

# When exceeded
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

### Rate Limit Tiers

| Tier | Limit | Window | Use Case |
|------|-------|--------|----------|
| Anonymous | 30/min | Per IP | Public endpoints |
| Authenticated | 100/min | Per user | Standard API access |
| Internal | 10000/min | Per service | Service-to-service |

## Implementation (Go/Gin)

```go
func (h *AssetHandler) Create(c *gin.Context) {
    var req CreateAssetRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusUnprocessableEntity, gin.H{
            "error": gin.H{
                "code":    "validation_error",
                "message": err.Error(),
            },
        })
        return
    }

    userID := c.GetString("userID")
    asset, err := h.service.Create(c.Request.Context(), userID, &req)
    if err != nil {
        switch {
        case errors.Is(err, ErrDuplicate):
            c.JSON(http.StatusConflict, gin.H{
                "error": gin.H{"code": "duplicate", "message": "Asset already exists"},
            })
        default:
            c.JSON(http.StatusInternalServerError, gin.H{
                "error": gin.H{"code": "internal_error", "message": "Internal error"},
            })
        }
        return
    }

    c.Header("Location", fmt.Sprintf("/api/v1/assets/%d", asset.ID))
    c.JSON(http.StatusCreated, gin.H{"data": asset})
}
```

## API Design Checklist

Before shipping a new endpoint:

- [ ] Resource URL follows naming conventions (plural, kebab-case, no verbs)
- [ ] Correct HTTP method used (GET for reads, POST for creates, etc.)
- [ ] Appropriate status codes returned (not 200 for everything)
- [ ] Input validated with schema (Gin binding tags / Zod)
- [ ] Error responses follow standard format with codes and messages
- [ ] Pagination implemented for list endpoints
- [ ] Authentication required (or explicitly marked as public)
- [ ] Authorization checked (user can only access their own resources)
- [ ] Rate limiting configured
- [ ] Response does not leak internal details (stack traces, SQL errors)
- [ ] Consistent naming with existing endpoints

---

**Remember**: A well-designed API is a contract. Breaking changes should be avoided; new capabilities should be additive.
