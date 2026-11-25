---
name: express-api-backend
description: How to build and review Node.js + Express + MongoDB/Mongoose backends (MERN) in TypeScript — project structure, routes/controllers/services, Zod validation, central error handling, auth with httpOnly cookies/JWT, role-based access, helmet/CORS/rate limits, env config, logging. Use when creating or changing an Express API, REST endpoints, Mongoose models, auth/login, middleware, or any MERN backend code.
---

# Express API Backend (MERN, TypeScript)

Written for this agent-kit; versions checked Sep 2026: **Express 5.2**, **Mongoose 9.x**, **Zod 4.x**, helmet 8, express-rate-limit 8. Always match what the project already has in `package.json` — if it is on older majors, follow those APIs (see "Version gotchas"). Pair with: `owasp-security` (review), `mongodb-schema-design`, `mongodb-query-optimizer`, `mongodb-connection`, `launch-readiness-audit` group 6.

## 1. Structure (feature-based)

```
src/
  app.ts              # builds the express app (middleware, routes, error handler) — no listen()
  server.ts           # connects DB, calls app.listen(), graceful shutdown
  config/env.ts       # Zod-validated env; the ONLY place that reads process.env
  lib/                # db.ts, logger.ts, http-error.ts
  middleware/         # auth.ts, validate.ts, error-handler.ts, rate-limit.ts
  modules/
    user/
      user.model.ts
      user.schema.ts      # Zod schemas for body/query/params
      user.service.ts     # business logic + DB calls (no req/res here)
      user.controller.ts  # thin: parse → call service → send response
      user.routes.ts
```

Rules: controllers stay thin, services hold logic, models hold schema only. Don't add repository layers, DI containers or base classes unless the project already uses them.

## 2. Env config — fail fast

```ts
// config/env.ts
import { z } from 'zod'
const Env = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().default(4000),
  MONGODB_URI: z.string().min(1),
  JWT_SECRET: z.string().min(32),
  CLIENT_ORIGIN: z.url(),
})
export const env = Env.parse(process.env) // crashes at boot if something is missing
```

Keep `.env` out of git; commit `.env.example` with names only.

## 3. App setup (order matters)

```ts
// app.ts
import express from 'express'
import helmet from 'helmet'
import cors from 'cors'
import cookieParser from 'cookie-parser'
import { rateLimit } from 'express-rate-limit'

export const app = express()
app.set('trust proxy', 1)                 // behind Render/Railway/Vercel/Nginx — needed for correct client IPs
app.disable('x-powered-by')
app.use(helmet())
app.use(cors({ origin: env.CLIENT_ORIGIN, credentials: true })) // never origin: '*' with credentials
app.use(express.json({ limit: '100kb' }))
app.use(cookieParser())
app.use('/api', rateLimit({ windowMs: 15 * 60 * 1000, limit: 300, standardHeaders: 'draft-8', legacyHeaders: false }))

app.get('/health', (_req, res) => { res.json({ ok: true }) })
app.use('/api/users', userRoutes)
app.use((_req, res) => { res.status(404).json({ error: 'Not found' }) })
app.use(errorHandler)                     // LAST
```

Stricter limiter on auth routes (login, signup, OTP, reset): e.g. `limit: 10` per 15 min. For multiple server instances use a shared store (Redis) — the default memory store is per-process.

## 4. Validation — every input, on the server

```ts
// middleware/validate.ts
import type { RequestHandler } from 'express'
import { z } from 'zod'
export const validate = (schema: { body?: z.ZodType; query?: z.ZodType; params?: z.ZodType }): RequestHandler =>
  (req, res, next) => {
    for (const key of ['body', 'query', 'params'] as const) {
      const s = schema[key]; if (!s) continue
      const r = s.safeParse(req[key])
      if (!r.success) return res.status(400).json({ error: 'Invalid input', details: z.flattenError(r.error) })
      res.locals[key] = r.data              // Express 5: req.query is read-only — store parsed data in res.locals
    }
    next()
  }
```

- Use strict object schemas; never pass `req.body` straight into `Model.create()` / `updateOne()` (mass assignment → users setting `role: 'admin'`).
- Validate ObjectIds (`mongoose.isValidObjectId`) before querying.
- Reject unknown query operators: never build filters from raw `req.query` objects (NoSQL injection like `{ "$ne": null }`). Mongoose `sanitizeFilter` or explicit field picking.

## 5. Errors — one handler, no leaks

```ts
// lib/http-error.ts
export class HttpError extends Error { constructor(public status: number, message: string) { super(message) } }

// middleware/error-handler.ts
import type { ErrorRequestHandler } from 'express'
export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  const status = err instanceof HttpError ? err.status : 500
  if (status >= 500) logger.error({ err, path: req.path }, 'Unhandled error')
  res.status(status).json({ error: status >= 500 ? 'Something went wrong' : err.message })
}
```

- Express 5 forwards rejected promises from async handlers to the error handler automatically — no `asyncHandler` wrapper or try/catch in every controller needed.
- Never send stack traces, Mongo errors or env values to the client. Map known cases: duplicate key (code 11000) → 409, CastError → 400, validation → 400.
- Use a structured logger (`pino`) instead of `console.log`; never log passwords, tokens or full request bodies.

## 6. Auth & permissions

- Passwords: `argon2` (argon2id) or `bcrypt` (cost ≥ 12). Never store or log plain passwords.
- Session token in an **httpOnly, Secure, SameSite=Lax (or Strict)** cookie — not in `localStorage`. Short-lived access token (e.g. 15 min) + rotating refresh token stored hashed in DB, so logout/revocation works.
- Cross-site frontend + cookie auth → need `SameSite=None; Secure` and CSRF protection (or keep API and frontend on the same site).
- `requireAuth` middleware verifies the token and loads the user; `requireRole('admin')` checks roles. Apply them on the **router**, server-side — UI hiding is not security.
- **Ownership check on every resource** (`Order.findOne({ _id, userId: req.user.id })`), otherwise user A can read user B's data by changing the id (IDOR).
- Login errors are generic ("Invalid email or password"); same response time path for unknown users where practical.
- Password reset/verify tokens: random (`crypto.randomBytes(32)`), stored hashed, single-use, expire (≤ 1h).

## 7. Mongoose

- One connection per process, created in `server.ts` before `listen()`; on serverless, cache the connection on `globalThis` (see `mongodb-connection`).
- Schemas: `timestamps: true`, required fields, enums, `select: false` on `password`, indexes for every query pattern (`unique: true` for email, compound indexes for filters + sort).
- Use `.lean()` for read-only queries, projection to return only needed fields, and **pagination** (limit + cursor/`_id` or page) on every list endpoint — never return unbounded lists.
- Never return raw documents with secrets; shape the response (DTO) or use `toJSON` transform.
- Transactions only when multiple documents must change atomically (needs a replica set / Atlas).

## 8. Version gotchas (verify against installed versions)

- **Mongoose 9:** pre middleware no longer gets `next()` — write `schema.pre('save', async function () { ... })`. `findOneAndUpdate(..., { new: true })` is deprecated → `{ returnDocument: 'after' }`. Requires Node ≥ 20.19. TypeScript: `FilterQuery` renamed to `QueryFilter`.
- **Express 5:** async errors auto-forwarded; `req.query` is a read-only getter; wildcard routes need names (`/*splat`, not `*`); `res.status()` only accepts valid integer codes.
- **Zod 4:** `z.email()` / `z.url()` top-level helpers exist; use `z.flattenError(err)` / `z.treeifyError(err)` instead of v3's `err.flatten()` when on v4.
- **express-rate-limit 7+:** option is `limit` (old name `max`).

## 9. Done checklist (backend)

- [ ] Every route has validation, auth where needed, and an ownership/role check.
- [ ] Rate limits on API + stricter on auth/OTP/AI endpoints.
- [ ] No secrets in code; env validated at boot.
- [ ] Error handler returns safe messages; logs have no secrets.
- [ ] List endpoints paginated; indexes exist for the queries.
- [ ] Health endpoint, graceful shutdown (close server + DB on SIGTERM).
- [ ] `npm audit --omit=dev` clean; run `owasp-security` review on new auth/data code.
