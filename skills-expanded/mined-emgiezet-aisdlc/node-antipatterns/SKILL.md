---
name: node-antipatterns
description: Forbidden Node.js backend patterns — prototype pollution, shell injection, path traversal, ReDoS, sync I/O in handlers. Applies when editing JS/TS Node files.
paths: ["**/*.cjs","**/*.js","**/*.mjs","**/*.ts"]
user-invocable: false
---

# Node.js anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-NODE-SEC-001 — Validate schemas before merging user objects; use `Object.create(null)` for hash maps.
- AP-NODE-SEC-002 — Use `execFile`/`spawn` with an argv array; never `exec` with a template literal.
- AP-NODE-SEC-004 — Avoid nested quantifiers in regexes; never construct `RegExp(userInput)` without length limits.
- AP-NODE-SEC-006 — Use `crypto.randomBytes(32)` or `crypto.randomUUID()` for tokens; never `Math.random()`.
- AP-NODE-SEC-009 — Always pass `{ algorithms: ['HS256'] }` (or your chosen alg) to `jwt.verify`.

## Errors
- AP-NODE-SEC-003 — Resolve paths with `path.resolve`, then verify the prefix matches your base directory.
- AP-NODE-SEC-005 — Compare secrets with `crypto.timingSafeEqual`; never `===` for HMAC or token values.
- AP-NODE-SEC-007 — Set `express.json({ limit: '1mb' })` and apply `helmet()` for security headers.
- AP-NODE-PERF-001 — Use async I/O (`fs.promises.*`, `util.promisify`) and async crypto in all request handlers.

## Warnings
- AP-NODE-PERF-002 — Limit JSON body size at the middleware layer; offload large payloads to a worker thread.
- AP-NODE-PERF-003 — Offload CPU-intensive work to `worker_threads`; limit parallel `fs.*` concurrency.
- AP-NODE-MAINT-001 — Register `process.on('unhandledRejection')` and `uncaughtException` handlers for graceful shutdown.

Details for any ID: `reference/<ID>.md`
