---
name: api-design-restful
description: Design RESTful APIs following best practices, conventions, and standards. Use when creating API endpoints, designing API contracts, documenting APIs, or when the user asks about REST, API design, HTTP methods, or API versioning.
---

# API Design & RESTful Best Practices

Design clean, consistent, and maintainable RESTful APIs following industry standards and best practices.

## RESTful Principles

### Resource Naming

**Use nouns, not verbs:**

- ✅ `/users`, `/orders`, `/products`
- ❌ `/getUsers`, `/createOrder`, `/deleteProduct`

**Use plural nouns:**

- ✅ `/users/123`, `/orders/456`
- ❌ `/user/123`, `/order/456`

**Use hierarchical structure:**

- ✅ `/users/123/orders` (user's orders)
- ✅ `/stores/456/products` (store's products)
- ❌ `/user-orders/123` (avoid flat structure when hierarchy exists)

**Use kebab-case for multi-word resources:**

- ✅ `/order-items`, `/user-addresses`
- ❌ `/orderItems`, `/user_addresses`

### HTTP Methods

**GET** - Retrieve resources (idempotent, safe)

```typescript
GET / users; // List users
GET / users / 123; // Get specific user
GET / users / 123 / orders; // Get user's orders
```

**POST** - Create resources (not idempotent)

```typescript
POST / users; // Create new user
POST / orders; // Create new order
POST / orders / 123 / cancel; // Action (when no better verb exists)
```

**PUT** - Replace entire resource (idempotent)

```typescript
PUT / users / 123; // Replace entire user
```

**PATCH** - Partial update (idempotent)

```typescript
PATCH / users / 123; // Update specific fields
```

**DELETE** - Remove resource (idempotent)

```typescript
DELETE / users / 123; // Delete user
```

### HTTP Status Codes

**2xx Success:**

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST (include Location header)
- `204 No Content` - Successful DELETE

**4xx Client Error:**

- `400 Bad Request` - Invalid request syntax/validation
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Authenticated but not authorized
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Resource conflict (e.g., duplicate)
- `422 Unprocessable Entity` - Validation errors

**5xx Server Error:**

- `500 Internal Server Error` - Generic server error
- `502 Bad Gateway` - Upstream server error
- `503 Service Unavailable` - Temporary unavailability

## Request/Response Patterns

### Request Headers

```typescript
// Required
Content-Type: application/json
Authorization: Bearer <token>

// Optional but recommended
X-Request-ID: <uuid>        // Request tracing
X-Client-Version: 1.0.0     // Client version
Accept: application/json    // Response format
```

### Response Structure

**Success Response:**

```typescript
// Single resource
{
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  }
}

// Collection
{
  "data": [
    { "id": 1, "name": "User 1" },
    { "id": 2, "name": "User 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}

// With links (HATEOAS)
{
  "data": { ... },
  "links": {
    "self": "/users/123",
    "orders": "/users/123/orders"
  }
}
```

**Error Response:**

```typescript
{
  "error": {
    "message": "Validation failed",
    "code": "VALIDATION_ERROR",
    "errors": {
      "email": ["Email is required", "Email is invalid"],
      "password": ["Password must be at least 8 characters"]
    }
  }
}
```

### Pagination

**Offset-based:**

```typescript
GET /users?page=1&limit=20

Response:
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

**Cursor-based (for large datasets):**

```typescript
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20

Response:
{
  "data": [...],
  "meta": {
    "limit": 20,
    "hasMore": true,
    "nextCursor": "eyJpZCI6MTQzfQ"
  }
}
```

### Filtering & Sorting

```typescript
// Filtering
GET /users?status=active&role=admin

// Sorting
GET /users?sort=name&order=asc
GET /users?sort=-createdAt  // descending

// Multiple filters
GET /orders?status=pending&storeId=123&createdAfter=2024-01-01
```

## API Versioning

### URL Versioning (Recommended)

```typescript
GET / v1 / users;
GET / v2 / users;
```

### Header Versioning

```typescript
GET /users
Headers: API-Version: 2
```

### Implementation:

```typescript
// routes/index.ts
router.use("/v1", v1Routes);
router.use("/v2", v2Routes);

// Default to latest
router.use("/", v2Routes);
```

## API Documentation (Swagger/OpenAPI)

### Swagger Annotations

```typescript
/**
 * @swagger
 * /users:
 *   post:
 *     summary: Create a new user
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - password
 *             properties:
 *               email:
 *                 type: string
 *                 format: email
 *               password:
 *                 type: string
 *                 minLength: 8
 *     responses:
 *       201:
 *         description: User created successfully
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/User'
 *       400:
 *         description: Validation error
 */
```

## Best Practices

### 1. Use Consistent Response Format

```typescript
// Success helper
class ResponseFormatter {
  static success(res: Response, data: any, message?: string, statusCode = 200) {
    return res.status(statusCode).json({
      data,
      ...(message && { message }),
    });
  }

  static error(res: Response, message: string, statusCode = 400, errors?: any) {
    return res.status(statusCode).json({
      error: {
        message,
        ...(errors && { errors }),
      },
    });
  }
}
```

### 2. Validate All Inputs

```typescript
// Use validation middleware
router.post(
  "/users",
  validate({
    body: {
      email: ["required", "email"],
      password: ["required", (v) => v.length >= 8 || "Password too short"],
    },
  }),
  createUser,
);
```

### 3. Use Proper HTTP Methods

- GET for retrieval (idempotent, cacheable)
- POST for creation
- PUT for full replacement
- PATCH for partial updates
- DELETE for removal

### 4. Implement Rate Limiting

```typescript
// Rate limit middleware
const rateLimit = require("express-rate-limit");

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});

router.use("/api/", limiter);
```

### 5. Include Request IDs

```typescript
// Request ID middleware
app.use((req, res, next) => {
  req.id = uuidv4();
  res.setHeader("X-Request-ID", req.id);
  next();
});
```

### 6. Use Proper Status Codes

- Don't always return 200 for errors
- Use 201 for created resources
- Use 204 for successful deletions
- Use 422 for validation errors

### 7. Support Content Negotiation

```typescript
// Accept header handling
app.use((req, res, next) => {
  const accept = req.headers.accept || "application/json";
  if (!accept.includes("application/json")) {
    return res.status(406).json({ error: "Only JSON supported" });
  }
  next();
});
```

## Anti-Patterns to Avoid

- ❌ Using verbs in URLs (`/getUsers`, `/createOrder`)
- ❌ Returning 200 for errors
- ❌ Inconsistent response formats
- ❌ No pagination for collections
- ❌ Exposing internal errors to clients
- ❌ No API versioning strategy
- ❌ Inconsistent naming conventions
- ❌ Missing request validation
- ❌ No rate limiting
- ❌ Returning sensitive data in responses

## When Creating APIs

1. **Design the contract first** - Define request/response schemas
2. **Use RESTful conventions** - Follow HTTP method semantics
3. **Validate all inputs** - Never trust client data
4. **Return consistent responses** - Use standard response format
5. **Document with Swagger** - Keep documentation in sync with code
6. **Version your APIs** - Plan for future changes
7. **Handle errors gracefully** - User-friendly error messages
8. **Implement pagination** - For all list endpoints
9. **Add rate limiting** - Protect your API
10. **Include request tracing** - For debugging and monitoring
