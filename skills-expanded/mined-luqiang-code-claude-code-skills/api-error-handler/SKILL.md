---
name: api-error-handler
description: |
  Add consistent error handling to API routes. Creates standardized error responses,
  logging, and error classes. Triggers on "add error handling", "error handling",
  "standardize errors".
metadata:
  type: tool
  version: "1.0.0"
  author: community
  tags: [api, error-handling, express, fastify]
triggers:
  - "add error handling"
  - "standardize errors"
  - "error handler"
  - "consistent error responses"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# API Error Handler

Add consistent, production-grade error handling to API routes.

## When to Use
- API routes lack standardized error responses
- Error handling is inconsistent across endpoints
- User mentions "error handling", "error responses", "error middleware"

## When NOT to Use
- GraphQL APIs (different error format)
- WebSocket endpoints (different patterns)
- The project already has a mature error handling layer

## Workflow
1. Scan API routes to understand current error handling patterns
2. Identify the framework (Express, Fastify, Koa, etc.)
3. Create an `AppError` class with: statusCode, code, message, details
4. Create error middleware that catches all errors and returns JSON:
   ```json
   { "error": { "code": "VALIDATION_ERROR", "message": "...", "details": [...] } }
   ```
5. Add error categories: ValidationError, AuthError, NotFoundError, RateLimitError
6. Wire into existing routes — replace bare `throw new Error()` with `AppError` subclasses
7. Add request ID to error responses for traceability
8. Run existing tests to verify nothing breaks

## Output Structure
```
src/
├── errors/
│   ├── AppError.ts           # Base error class
│   ├── ValidationError.ts    # 400
│   ├── AuthError.ts          # 401
│   ├── ForbiddenError.ts     # 403
│   ├── NotFoundError.ts      # 404
│   └── RateLimitError.ts     # 429
├── middleware/
│   └── errorHandler.ts       # Error middleware
```

## Key Principles
- Never leak stack traces in production
- Always include a machine-readable `code` field
- Log errors with request ID for debugging
- DON'T catch errors you can't handle — let the middleware do it
- Use HTTP status codes semantically

## Notes
- Don't wrap every route in try-catch — use the error middleware
- Production errors should NOT include internal details
- Add `NODE_ENV` check: include stack traces only in development
