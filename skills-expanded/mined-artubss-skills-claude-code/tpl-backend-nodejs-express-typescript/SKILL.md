---
name: tpl-backend-nodejs-express-typescript
description: Template do pack (backend/01-nodejs-express-typescript.md). Orienta o agente em APIs, servicos e arquitetura backend alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: backend/01-nodejs-express-typescript.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Node.js REST API

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `backend/01-nodejs-express-typescript.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK

| Technology | Version | Purpose |
|------------|---------|---------|
| Node.js | 22.x | Runtime |
| TypeScript | 5.4+ | Language |
| Express | 5.x | HTTP framework |
| PostgreSQL | 16 | Primary database |
| Drizzle ORM | 0.30+ | Type-safe query builder |
| Zod | 3.x | Runtime validation |
| JWT (jsonwebtoken) | 9.x | Auth tokens |
| Vitest | 1.x | Unit + integration tests |
| Supertest | 7.x | HTTP integration tests |
| tsx | 4.x | Dev runner (no build needed in dev) |
| tsup | 8.x | Production bundler |

---

## PROJECT STRUCTURE

```
src/
├── config/
│   ├── env.ts            # Zod-validated environment variables
│   ├── database.ts       # Drizzle client + connection pool
│   └── app.ts            # Express app factory (no listen here)
├── modules/
│   └── users/
│       ├── users.router.ts       # Route definitions only
│       ├── users.controller.ts   # Request/response handling
│       ├── users.service.ts      # Business logic
│       ├── users.repository.ts   # Database queries
│       ├── users.schema.ts       # Zod schemas for validation
│       └── users.types.ts        # TypeScript interfaces
├── middlewares/
│   ├── auth.middleware.ts        # JWT verification
│   ├── validate.middleware.ts    # Zod validation factory
│   └── error.middleware.ts       # Global error handler
├── db/
│   ├── schema/
│   │   ├── users.ts              # Drizzle table definitions
│   │   └── index.ts              # Re-export all schemas
│   └── migrations/               # Drizzle migration files
├── shared/
│   ├── types/
│   │   ├── express.d.ts          # Augmented Request type
│   │   └── common.ts             # Shared interfaces
│   └── errors/
│       ├── AppError.ts           # Base error class
│       └── HttpError.ts          # HTTP-specific errors
├── server.ts             # Entry point (app.listen here)
tests/
├── unit/
│   └── users/
│       └── users.service.test.ts
├── integration/
│   └── users/
│       └── users.routes.test.ts
└── helpers/
    ├── test-db.ts                # Test database setup/teardown
    └── test-app.ts               # Supertest app factory
```

---

## ARCHITECTURE RULES

### LAYERED ARCHITECTURE

```
HTTP Request
     │
     ▼
[Router]          → defines route path + method, attaches middlewares
     │
     ▼
[Middleware]       → auth check, body validation (Zod), rate limiting
     │
     ▼
[Controller]       → extracts validated data, calls service, formats response
     │
     ▼
[Service]          → business logic, transactions, calls repository
     │
     ▼
[Repository]       → SQL queries via Drizzle, no business logic here
     │
     ▼
[Database]         → PostgreSQL
```

**Rules:**
- Controllers NEVER import repositories directly — always go through service
- Services NEVER import Express types (`Request`, `Response`)
- Repositories NEVER contain `if/else` business logic — pure data access
- Each module is self-contained: router, controller, service, repository, schema, types
- Cross-module communication happens via service-to-service calls, never repo-to-repo

---

## MIDDLEWARE PATTERNS

### JWT Auth Middleware

```typescript
// src/middlewares/auth.middleware.ts
import type { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'
import { env } from '../config/env'
import { HttpError } from '../shared/errors/HttpError'

export interface JwtPayload {
  sub: string
  email: string
  role: 'admin' | 'user'
  iat: number
  exp: number
}

declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload
    }
  }
}

export function authenticate(req: Request, _res: Response, next: NextFunction): void {
  const header = req.headers.authorization
  if (!header?.startsWith('Bearer ')) {
    throw new HttpError(401, 'Missing or invalid Authorization header')
  }

  const token = header.slice(7)
  try {
    const payload = jwt.verify(token, env.JWT_ACCESS_SECRET) as JwtPayload
    req.user = payload
    next()
  } catch {
    throw new HttpError(401, 'Token expired or invalid')
  }
}

export function authorize(...roles: JwtPayload['role'][]) {
  return (req: Request, _res: Response, next: NextFunction): void => {
    if (!req.user || !roles.includes(req.user.role)) {
      throw new HttpError(403, 'Insufficient permissions')
    }
    next()
  }
}
```

### Zod Validation Middleware

```typescript
// src/middlewares/validate.middleware.ts
import type { Request, Response, NextFunction } from 'express'
import { ZodSchema, ZodError } from 'zod'
import { HttpError } from '../shared/errors/HttpError'

type Target = 'body' | 'query' | 'params'

export function validate(schema: ZodSchema, target: Target = 'body') {
  return (req: Request, _res: Response, next: NextFunction): void => {
    const result = schema.safeParse(req[target])
    if (!result.success) {
      const messages = result.error.errors.map(e => `${e.path.join('.')}: ${e.message}`)
      throw new HttpError(422, 'Validation failed', messages)
    }
    req[target] = result.data // replace with parsed/coerced data
    next()
  }
}
```

### Global Error Handler

```typescript
// src/middlewares/error.middleware.ts
import type { Request, Response, NextFunction } from 'express'
import { HttpError } from '../shared/errors/HttpError'
import { env } from '../config/env'

export function errorHandler(
  err: unknown,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  if (err instanceof HttpError) {
    res.status(err.statusCode).json({
      error: err.message,
      ...(err.details && { details: err.details }),
      ...(env.NODE_ENV === 'development' && { stack: err.stack }),
    })
    return
  }

  console.error('[Unhandled Error]', err)
  res.status(500).json({
    error: 'Internal server error',
    ...(env.NODE_ENV === 'development' && { raw: String(err) }),
  })
}
```

### JWT Token Service

```typescript
// src/modules/auth/auth.service.ts
import jwt from 'jsonwebtoken'
import { env } from '../../config/env'
import type { JwtPayload } from '../../middlewares/auth.middleware'

export function signAccessToken(payload: Omit<JwtPayload, 'iat' | 'exp'>): string {
  return jwt.sign(payload, env.JWT_ACCESS_SECRET, { expiresIn: '15m' })
}

export function signRefreshToken(userId: string): string {
  return jwt.sign({ sub: userId }, env.JWT_REFRESH_SECRET, { expiresIn: '7d' })
}

export function verifyRefreshToken(token: string): { sub: string } {
  return jwt.verify(token, env.JWT_REFRESH_SECRET) as { sub: string }
}
```

---

## ENVIRONMENT VARIABLES

```typescript
// src/config/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_ACCESS_SECRET: z.string().min(32),
  JWT_REFRESH_SECRET: z.string().min(32),
  CORS_ORIGIN: z.string().default('http://localhost:5173'),
})

const parsed = envSchema.safeParse(process.env)
if (!parsed.success) {
  console.error('❌ Invalid environment variables:', parsed.error.format())
  process.exit(1)
}

export const env = parsed.data
```

---

## ROUTING TABLE

| Trigger | Method | Route | Middleware | Controller Action |
|---------|--------|-------|-----------|-------------------|
| Register | POST | `/api/v1/auth/register` | validate(registerSchema) | AuthController.register |
| Login | POST | `/api/v1/auth/login` | validate(loginSchema) | AuthController.login |
| Refresh token | POST | `/api/v1/auth/refresh` | validate(refreshSchema) | AuthController.refresh |
| Logout | DELETE | `/api/v1/auth/logout` | authenticate | AuthController.logout |
| List users | GET | `/api/v1/users` | authenticate, authorize('admin') | UsersController.list |
| Get profile | GET | `/api/v1/users/me` | authenticate | UsersController.me |
| Update profile | PATCH | `/api/v1/users/me` | authenticate, validate(updateSchema) | UsersController.update |
| Delete account | DELETE | `/api/v1/users/me` | authenticate | UsersController.delete |
| Health check | GET | `/api/health` | — | HealthController.check |

---

## QUALITY GATES

Before opening a PR, verify ALL of the following:

- [ ] `npx tsc --noEmit` passes with zero errors
- [ ] `vitest run` passes with zero failures
- [ ] Coverage ≥ 80% for new service/repository files
- [ ] All new routes have a corresponding integration test
- [ ] No raw `console.log` in production code (use a logger)
- [ ] Environment variables added to `env.ts` schema, not hardcoded
- [ ] No `any` type — use `unknown` and narrow it
- [ ] All async route handlers are wrapped or use Express 5 auto-catch
- [ ] Error responses use `HttpError`, not manual `res.status(500).json(...)`
- [ ] API changes documented in OpenAPI spec or README routing table

---

## FORBIDDEN

- **NEVER** put SQL queries or `db.*` calls inside controllers or services — only repositories
- **NEVER** store JWT secrets in code — always from `env.ts`
- **NEVER** return stack traces in production responses
- **NEVER** use `express-async-errors` patch hack — use Express 5 native async error propagation
- **NEVER** skip Zod validation on incoming request data
- **NEVER** use `parseInt`/`parseFloat` on user input without schema coercion
- **NEVER** return passwords or token hashes in any API response
- **NEVER** commit `.env` files — use `.env.example`
- **NEVER** bypass the layer hierarchy (e.g., controller importing repository directly)
- **NEVER** use `require()` — this is a pure ESM project (`"type": "module"` in package.json)
