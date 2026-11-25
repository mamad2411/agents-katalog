---
name: backend-dev
description: Use this skill for backend development — server logic, authentication, microservices, serverless functions, middleware, background jobs, caching strategies, and backend architecture patterns. Trigger on keywords: backend, server, API endpoint, middleware, authentication, authorization, microservice, serverless, background job, queue, caching, session.
---

# Backend Development

## Core Principles

- **Stateless services** — don't store session state in memory; use Redis or a DB
- **Fail fast** — validate inputs at the boundary, return errors early
- **Idempotency** — POST/PUT endpoints that can be called multiple times safely
- **Observability** — every service needs logs, metrics, and traces

---

## API Endpoint Structure

### Request Lifecycle
```text
Request → Rate Limiting → Authentication → Authorization → Validation → Business Logic → Response
```

Never skip this order. Auth before business logic. Validation before processing.

### Response Standards
```json
// Success
{ "data": { ... }, "meta": { "page": 1, "total": 100 } }

// Error
{ 
  "error": { 
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [{ "field": "email", "issue": "Invalid format" }]
  }
}
```

---

## Authentication Patterns

### JWT Best Practices
- Short access token TTL (15 min) + long refresh token (7 days)
- Store refresh token in httpOnly cookie (not localStorage)
- Validate signature, expiry, issuer, and audience
- Rotate refresh tokens on use
- Maintain a revocation list or use short-lived tokens only

### Session-Based Auth
- Store session ID in httpOnly, Secure, SameSite cookie
- Store session data in Redis with TTL
- Regenerate session ID after login (session fixation prevention)

### Authorization
```typescript
// Check authorization at the service layer, not just the route
async function getOrder(userId: string, orderId: string) {
  const order = await db.orders.findById(orderId)
  if (!order) throw new NotFoundError()
  // Authorization check — user can only see their own orders
  if (order.userId !== userId) throw new ForbiddenError()
  return order
}
```

---

## Background Jobs & Queues

Use queues for:
- Email sending
- Image/file processing
- External API calls that don't need to be synchronous
- Long-running tasks

### Job Patterns
```text
Fire-and-forget: Enqueue and return immediately
Scheduled: Run at specific time (cron)
Delayed: Run after X minutes/hours
Retry: Re-attempt on failure with backoff
```

Always implement:
- Dead letter queue for failed jobs
- Idempotency key to prevent duplicate processing
- Timeout per job
- Max retry count

---

## Error Handling

```typescript
// Structured error hierarchy
class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number,
    public code: string
  ) { super(message) }
}

class ValidationError extends AppError {
  constructor(details: ValidationDetail[]) {
    super('Validation failed', 400, 'VALIDATION_ERROR')
    this.details = details
  }
}

// Global error handler
app.use((err, req, res, next) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({ error: err })
  }
  // Log unexpected errors
  logger.error('Unexpected error', { err, req })
  res.status(500).json({ error: { code: 'INTERNAL_ERROR' } })
})
```

---

## Middleware Checklist

Every production API needs:
- [ ] Request logging (method, path, status, duration)
- [ ] Rate limiting (per IP, per user, per endpoint)
- [ ] CORS configuration (explicit whitelist)
- [ ] Helmet / security headers
- [ ] Request ID propagation (for distributed tracing)
- [ ] Body size limits
- [ ] Timeout handling

---

## Environment Configuration

```typescript
// Never hardcode configuration — always from environment
const config = {
  db: {
    url: process.env.DATABASE_URL,      // required
    poolSize: parseInt(process.env.DB_POOL_SIZE ?? '10')
  },
  jwt: {
    secret: process.env.JWT_SECRET,     // required
    expiresIn: process.env.JWT_TTL ?? '15m'
  }
}

// Validate required config at startup — fail fast
const required = ['DATABASE_URL', 'JWT_SECRET']
for (const key of required) {
  if (!process.env[key]) throw new Error(`Missing required env: ${key}`)
}
```
