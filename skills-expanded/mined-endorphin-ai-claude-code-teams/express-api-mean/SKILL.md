---
name: express-api-mean
description: "Express.js API architecture for MEAN stack apps. Use when designing REST endpoints, middleware chains, authentication flows, error handling contracts, and request/response schemas."
---

# Express Api Mean

## Purpose

Design REST API architectures for MEAN stack applications using Express.js. Produce endpoint contracts, middleware chains, authentication flows, error handling patterns, and request/response schemas that backend developers implement directly.

## Key Patterns

### REST Endpoint Design
- Resource-based URLs: /api/users, /api/posts, /api/posts/:id/comments
- HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove)
- Consistent success response: `{ success: true, data: {...}, pagination: {...} }`
- Consistent error response: `{ success: false, error: { code, message, details } }`

### Middleware Architecture
Request flow: CORS -> Body Parser -> Rate Limiter -> Auth -> Validation -> Controller -> Response
- Global middleware: CORS, body-parser, morgan (logging), helmet (security headers), compression
- Route middleware: auth (JWT verify), validate (Joi/express-validator), authorize (role check)
- Error middleware: Global error handler as last middleware

### Authentication Flow (JWT)
1. POST /api/auth/register -> hash password -> save user -> return JWT
2. POST /api/auth/login -> verify credentials -> return JWT + refresh token
3. POST /api/auth/refresh -> verify refresh token -> return new JWT
4. Protected routes: Authorization: Bearer <token> header -> verify middleware

### Controller Pattern
- Use asyncHandler wrapper to avoid try/catch boilerplate
- Use ApiError class for consistent error throwing
- All list endpoints include pagination (page, limit, total, pages)
- Sort by -createdAt by default (newest first)

## Conventions

- All routes prefixed with /api/
- Use plural nouns for resources: /users not /user
- Nested resources max 2 levels: /posts/:id/comments
- HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 409 (Conflict), 422 (Validation), 500 (Server Error)
- Validate request body with Joi or express-validator
- Pagination on all list endpoints (default: page=1, limit=20)
- Use express-rate-limit on auth routes (max 10 attempts per 15 min)
- Use helmet for security headers

## Knowledge Strategy

- **Patterns to capture:** Endpoint designs that worked well, middleware chains for common scenarios, auth patterns
- **Examples to collect:** Complete route files, controller patterns, middleware implementations
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
