---
name: nodejs-standards
description: Node.js and backend coding standards, patterns, approved libraries, and anti-patterns. Load when writing, reviewing, or discussing any Node.js/Express backend code, APIs, services, or controllers.
user-invocable: false
stack: backend/node-express
paths:
  - "src/**/*.service.*"
  - "src/**/*.controller.*"
  - "src/**/*.route.*"
  - "src/**/*.middleware.*"
  - "server/**"
---

For the full reference see [nodejs.md](nodejs.md). Summary of rules that always apply:

**Libraries (use these, no alternatives):**
- Runtime: Node.js 20 LTS + TypeScript (strict)
- Framework: Express 4
- Validation: Zod (runtime + compile-time types from same schema)
- Logging: Pino (structured JSON — never raw stdout logging)
- Auth: `aws-jwt-verify` for Cognito JWT verification
- Security: `helmet` + `express-rate-limit`
- ORM: Prisma (SQL) or AWS DynamoDB DocumentClient v3 (NoSQL)
- Testing: Vitest + Supertest + MSW for external APIs
- API testing: Bruno collections

**Architecture layers (strict separation):**
```
Route → Controller → Service → Repository → DB
```
- Controller: validate input (Zod), call service, return response — nothing else
- Service: business logic only — no HTTP context objects (request/response) allowed
- Repository: DB access only — no business logic
- Middleware: auth, logging, rate limiting, error handling

**Non-negotiable patterns:**
- All async handlers: `asyncHandler(fn)` wrapper — never bare async arrow functions without wrapper
- All input: always `Schema.parse(req.body)` at controller boundary — never access raw body fields directly
- All responses: `json({ success: true, data: result })` or `json({ success: false, error: { code: 'ERR', message: '...' } })`
- All logging: use `logger.info(...)` / `logger.error(...)` (Pino) with `requestId`, `userId`, `action` fields — never stdout logging
- Centralized error middleware — never inline status 500 responses

**Anti-patterns (never do):**
- Raw stdout/stderr logging (use Pino `logger.*` methods instead)
- `any` type
- Unvalidated body fields without Zod parse
- DB calls in controllers
- Business logic in repositories
- Missing `asyncHandler` on route handlers
- Inline try/catch that swallows errors silently
- Hardcoded secrets or config values
