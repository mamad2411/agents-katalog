---
name: expressjs
description: "Unified Express.js skill index — covers API security, authentication & authorization, database integration with Prisma, environment configuration, error handling, input validation with Zod, logging & monitoring with Pino, middleware architecture, modular project structure, REST API design, and Swagger/OpenAPI documentation. Use this as the entry point; it delegates to focused sub-skill files for each domain."
---

# Express.js Skill

## Overview

This file is the top-level entry point for all Express.js-related topics. It identifies the right sub-skill file to consult based on what the user is trying to accomplish. Each sub-skill file contains detailed patterns, examples, and best practices for its domain.

---

## Sub-Skills Reference

| Domain                         | File                                                               | When to use                                                                                                                                                                                                                                 |
| ------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| API Security                   | [api-security.md](api-security.md)                                 | Setting up Helmet, CORS, rate limiting, CSRF protection; sanitizing user input; preventing injection attacks (SQL, NoSQL, XSS, command injection); securing HTTP headers; implementing request size limits; applying OWASP best practices   |
| Authentication & Authorization | [authentication-authorization.md](authentication-authorization.md) | Setting up login/register flows; generating and verifying JWTs; implementing refresh tokens; configuring Passport.js strategies; building auth middleware; implementing RBAC or ABAC; protecting routes by role or permission               |
| Database Integration           | [database-integration.md](database-integration.md)                 | Connecting Express to PostgreSQL/MySQL/SQLite via Prisma; writing CRUD operations; managing database client lifecycle; structuring data access layers; handling connection pooling and error handling                                       |
| Environment Configuration      | [env-configuration.md](env-configuration.md)                       | Setting up .env files; validating env vars at startup; structuring config modules; managing dev/staging/production configs; using dotenv or env validation libraries; handling secrets securely                                             |
| Error Handling                 | [error-handling.md](error-handling.md)                             | Building error handling middleware; creating custom AppError classes; wrapping async route handlers; mapping third-party errors to HTTP responses; logging errors; handling 404s and unhandled rejections                                   |
| Input Validation               | [input-validation.md](input-validation.md)                         | Creating validation schemas for API endpoints; building validation middleware; validating nested objects, arrays, enums, dates; transforming and coercing input; reusing schemas across routes; generating TypeScript types from schemas    |
| Logging & Monitoring           | [logging-monitoring.md](logging-monitoring.md)                     | Setting up application logging; building request logging middleware; adding correlation/request IDs; configuring log levels per environment; implementing health check endpoints; collecting API metrics; integrating with monitoring tools |
| Middleware Architecture        | [middleware-architecture.md](middleware-architecture.md)           | Building custom middleware; understanding request/response lifecycle; ordering middleware correctly; composing reusable middleware; creating middleware factories; applying middleware per-route or globally                                |
| Modular Architecture           | [modular-architecture.md](modular-architecture.md)                 | Organizing routes, services, repositories, middleware into modules; scaling project structure; separating business logic from HTTP layer; creating feature-based or domain-driven folder structures                                         |
| REST API Design                | [rest-api-design.md](rest-api-design.md)                           | Designing API endpoints; choosing HTTP methods and status codes; structuring JSON responses; implementing pagination and filtering; versioning APIs; following REST conventions                                                             |
| Swagger / OpenAPI              | [swagger-implementation.md](swagger-implementation.md)             | Adding API documentation; generating OpenAPI specs from existing Zod DTOs; registering routes programmatically; serving Swagger UI; documenting auth, pagination, error responses                                                           |

---

## Quick Decision Guide

```
What are you trying to do?
│
├── Harden the API against attacks or set security headers?
│   └── → api-security.md
│
├── Implement login, JWT, refresh tokens, or role-based access?
│   └── → authentication-authorization.md
│
├── Connect to a database with Prisma (CRUD, repos, transactions)?
│   └── → database-integration.md
│
├── Manage environment variables, .env files, or secrets?
│   └── → env-configuration.md
│
├── Handle errors centrally, create custom error classes, or catch async errors?
│   └── → error-handling.md
│
├── Validate request body, params, query, or headers with Zod?
│   └── → input-validation.md
│
├── Set up structured logging (Pino), request logs, or health checks?
│   └── → logging-monitoring.md
│
├── Build custom middleware, understand pipeline order, or compose middleware chains?
│   └── → middleware-architecture.md
│
├── Structure the project into modules (routes / services / repos / controllers)?
│   └── → modular-architecture.md
│
├── Design REST endpoints, choose status codes, or implement pagination/sorting?
│   └── → rest-api-design.md
│
└── Generate OpenAPI/Swagger docs from Zod schemas?
    └── → swagger-implementation.md
```

---

## How to Use This Skill

1. **Identify the goal** using the Quick Decision Guide above.
2. **Load the corresponding sub-skill file** with `read_file` (e.g., `error-handling.md`).
3. **Follow the patterns and examples** in that file to produce the response.
4. **Load multiple sub-skill files** when the task spans domains — for example, building a new feature module typically involves `modular-architecture.md` + `input-validation.md` + `error-handling.md`.
