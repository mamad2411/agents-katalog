---
name: backend-mean
description: "Node.js + Express + MongoDB backend development for MEAN stack apps. Use when implementing server code: models, routes, controllers, middleware, config, and database connections."
---

# Backend Mean

## Purpose

Implement Node.js + Express + MongoDB backends for MEAN stack applications. Translate database schemas and API contracts from architects into working server code: Mongoose models, Express routes, controllers, middleware, authentication, validation, and error handling.

## Key Patterns

### Project Structure
- server/config/ — DB connection, env validation, CORS config
- server/models/ — Mongoose model files
- server/routes/ — Express router files with index.js mount
- server/controllers/ — Business logic handlers
- server/middleware/ — auth.js, validate.js, errorHandler.js, asyncHandler.js
- server/utils/ — ApiError.js, ApiResponse.js, validators/

### Model Pattern
- Mongoose schema with fields, types, validators, required, enum, match
- timestamps: true on every schema
- toJSON transform removing __v and converting _id to id
- Pre-save middleware for password hashing (bcrypt, 12 rounds)
- Instance methods: comparePassword for auth
- select: false on password field

### Controller Pattern
- Every handler wrapped with asyncHandler (no try/catch needed)
- ApiError class for throwing errors with status codes
- All list endpoints: pagination with page, limit, total, pages
- Standard response: { success: true, data: {...} }
- Promise.all for parallel queries (count + find)

### Auth Pattern
- JWT signed with { id: user._id }, expiry 7d
- protect middleware: extract token from Authorization header, verify, attach user to req
- authorize middleware: check req.user.role against allowed roles
- Refresh token: separate longer-lived token (30d)

### Error Handler Pattern
- Global error middleware as last Express middleware
- Handles: Mongoose ValidationError (422), CastError (400), duplicate key 11000 (409)
- Stack trace only in development mode

## Conventions

- async/await everywhere with asyncHandler wrapper
- Custom ApiError class — throw instead of res.status().json()
- Environment variables in .env — validate on startup
- Passwords: bcryptjs with 12 salt rounds, select: false, never return in responses
- Use express-rate-limit on auth routes
- Use helmet for security headers, cors for cross-origin, morgan for logging
- NEVER return stack traces in production
- NEVER hardcode secrets

## Knowledge Strategy

- **Patterns to capture:** Working controller patterns, middleware chains, auth implementations
- **Examples to collect:** Complete server setup files, model definitions, route files
- **Update permission:** Agents may freely add/update files in `references/`. Changes to `SKILL.md` or `scripts/` require user approval.
