---
name: express-api-design
description: Conventions for structuring Express APIs — layering, async error handling, edge validation, error envelopes, middleware ordering, and hardening. Use when writing or reviewing Express routers, controllers, services, or middleware.
---

# Express API Design

Apply when building or reviewing Express (v4/v5) HTTP APIs.

## Layering

Separate three responsibilities; do not collapse them into fat route handlers:

- **Router** — declares paths and attaches middleware/controllers. No logic.
- **Controller** — reads/validates the request, calls a service, formats the response. No business rules, no direct DB access.
- **Service** — business logic, transaction boundaries, calls repositories/clients. Framework-agnostic (no `req`/`res`).

```ts
router.post('/users', validate(createUserSchema), asyncHandler(usersController.create));
```

## Async error handling

Unhandled promise rejections in handlers are the most common Express bug. Pick one and apply everywhere:

- **Express 5**: rejected promises returned from handlers are forwarded to the error middleware automatically — still be explicit and consistent.
- **Express 4**: wrap every async handler:

```ts
const asyncHandler = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
```

Never leave an `await` in a handler without a path to `next(err)`. Do not send responses from inside `catch` per-handler — let the central error handler do it.

## Input validation at the edge

- Validate and coerce every request (body, query, params) with **zod** or **joi** in middleware before the controller runs. Reject unknown fields.
- Treat validated output as the typed input; do not re-read raw `req.body` downstream.

```ts
const validate = (schema) => (req, res, next) => {
  const r = schema.safeParse({ body: req.body, query: req.query, params: req.params });
  if (!r.success) return next(new ValidationError(r.error.issues));
  req.data = r.data;
  next();
};
```

## Consistent error envelope

- Define a single error class hierarchy carrying an HTTP status and a machine-readable `code`.
- One **error-handling middleware, registered last**, converts everything to the shared envelope (see `api-contract-design`) and logs with context. Map unknown errors to 500 without leaking stack traces to clients.

```ts
app.use((err, req, res, next) => {
  const status = err.status ?? 500;
  logger.error({ err, requestId: req.id }, 'request failed');
  res.status(status).json({ error: { code: err.code ?? 'INTERNAL', message: status === 500 ? 'Internal error' : err.message } });
});
```

## Middleware order

Order matters. Register in this sequence:

1. Security headers (`helmet`)
2. CORS
3. Request id + logging
4. Body parsing (`express.json` with a `limit`)
5. Rate limiting
6. Authentication / authorization
7. Routes
8. **404 handler**
9. **Error handler (always last, 4-arg signature)**

## Hardening basics

- `helmet()` for security headers; set an explicit `express.json({ limit: '100kb' })` to bound payloads.
- **CORS**: allowlist specific origins; never reflect arbitrary `Origin` with credentials.
- **Rate limit** public and auth endpoints (`express-rate-limit`), keyed by IP or user.
- Set `trust proxy` correctly behind a load balancer so IP-based logic and rate limiting work.

## Graceful shutdown

Drain in-flight requests on `SIGTERM`, then close DB/queue connections, then exit. Add a timeout to force-exit if draining stalls.

```ts
process.on('SIGTERM', async () => {
  server.close(async () => { await db.close(); process.exit(0); });
  setTimeout(() => process.exit(1), 10_000).unref();
});
```

## Anti-patterns

- Business logic or DB queries in route handlers.
- `try/catch` in every handler duplicating error responses instead of a central handler.
- Error middleware registered before routes (it won't catch them).
- No payload size limit; permissive CORS (`origin: true` with credentials).
- Swallowing rejections; sending `err.stack` to clients.
