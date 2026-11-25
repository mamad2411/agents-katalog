---
name: express-middleware-design
description: Orders Express and Fastify middleware correctly, centralizes error handling and validates requests at the edge, so handlers only see clean input.
---

# Express middleware design

Treat the middleware stack as a pipeline with a fixed order. Read the entry file and every `app.use` call before editing.

## Order, outside in

1. Request id and structured logging.
2. Security headers (`helmet`) and CORS with an explicit origin list.
3. Body parsers with a size limit (`express.json({ limit: '100kb' })`).
4. Rate limiting on auth and write routes.
5. Authentication, then authorization per route.
6. Validation of `params`, `query` and `body` with a schema library such as zod, before any handler runs.
7. Route handlers.
8. A 404 handler, then one error handler with four arguments, registered last.

## Steps

1. Wrap async handlers so rejections reach `next(err)`. Express 5 does this itself; on Express 4 add a small `asyncHandler` wrapper. In Fastify, throw and let the error handler catch it.
2. Define an `AppError` class carrying `status`, a stable `code` and a safe message. Handlers throw it; they never call `res.status(500)` themselves.
3. In the error handler, map `AppError` and validation errors to their status, log everything else with the request id, and answer 500 with a generic body. Never send stack traces.
4. Validate once, write the parsed result back to `req`, and type it so handlers trust it.

## Rules

- Never call `next()` after sending a response.
- Do not put business logic in middleware; it parses, checks and passes on.
- Keep each middleware in its own file with a single job.

## Report

Show the final stack order, the files changed, and routes that still lack validation.
