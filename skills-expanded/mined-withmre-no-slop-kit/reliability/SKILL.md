---
name: reliability
description: Reliability, performance and cost rules for any web project. Use whenever a task touches data fetching, API endpoints, database queries or schema, calls to external or paid APIs, forms and submissions, caching, file handling, error handling, logging, monitoring, backups or deployment, and before any production release.
---

# Reliability

A site that works on your machine with three test rows is not ready. Plan for slow networks, failing APIs, empty tables, impatient users, bots and growth. Apply the items relevant to the task. Lazy still applies: add a mechanism when the need exists. At the end, one line: items checked, items left.

## 1. Limits and costs

- Rate limit every public endpoint per IP and per user. Stricter on expensive ones: auth, search, uploads, exports, contact forms, anything that sends email or SMS or calls AI. Return `429` with `Retry-After`.
- Cap calls to paid APIs: per-user quota, global daily ceiling enforced in code, and billing alerts on the provider's side. A bot or a loop must never drain the account.
- LLM calls: max tokens per request, per-user quota, and a hard stop when the monthly budget is reached.
- Request body size limit. Pagination with a maximum page size on every list endpoint. Timeouts on database queries.

## 2. Every request can fail

- Every outbound call has a timeout. `fetch` has none by default: use `AbortSignal.timeout(ms)` or the client library's option.
- Retry only transient failures (network error, `429`, `502`, `503`, `504`), only for idempotent operations, with exponential backoff, jitter and a max of three attempts.
- Writes that must not happen twice (payments, orders, emails) carry an idempotency key checked server-side.
- External API down or slow: show cached data when it exists, otherwise a clear message. The rest of the page keeps working.
- Every failure the user can hit has a visible outcome: a human message saying what happened and what to do, with a retry button when retrying makes sense. Never a blank page, an infinite spinner or a raw error.
- Framework error boundaries and error pages in place (`error.tsx`, `+error.svelte`, `ErrorBoundary`, custom 500).
- Optimistic updates are rolled back with a message when the server refuses.

## 3. The interface handles every state

For every component that loads data, handle each case explicitly:

- Loading: a skeleton shaped like the content, or a spinner for short actions.
- Empty: what would be here and the next action (« Aucun devis pour l'instant. Créer un devis »).
- Error: section 2.
- Partial: some items failed, the rest still shows.
- Success.

Submissions: button disabled and showing progress while sending, so double clicks send once. The server also deduplicates (idempotency key or unique constraint), because a disabled button is only a client-side check.

## 4. Load only what you display

- Select the columns you need. Never `select *` sent to the client.
- Paginate or virtualize long lists. Never fetch a whole table to filter or count client-side.
- No N+1 queries: join, batch or preload.
- Fetch on the server when the framework allows, and send the page only the data it renders.
- Heavy or slow work (exports, image processing, bulk emails) goes to a background job, only when it would block the request for more than a few seconds.

## 5. Indexes

- Index columns used in frequent `WHERE`, `JOIN` and `ORDER BY` clauses. Postgres does not index foreign keys automatically: index the ones you join or filter on.
- Unique constraints for what must be unique (email, slug, idempotency key). Let the database enforce it.
- Text search: a proper index (trigram or full-text), never `LIKE '%term%'` on a large table.
- Check a slow query with `EXPLAIN ANALYZE` before and after. Don't add indexes blindly: each one slows writes.

## 6. Files and weight

- Images: WebP or AVIF, resized to their display size, `width` and `height` set, lazy-loaded below the fold. Use the framework's image component when there is one.
- Upload limits on size and count, enforced server-side. Large uploads go straight to storage through signed URLs.
- Text compression (Brotli or gzip) on: check the response headers, most hosts do it.
- JavaScript bundle checked. Split heavy routes. No large library for a small job (dates: `Intl` before a date library).
- Fonts self-hosted, only the weights used.

## 7. Cache what doesn't change

- Static assets with hashed filenames: `Cache-Control: public, max-age=31536000, immutable`.
- HTML and API responses: short or no cache unless the data allows more.
- Server-side cache for expensive, rarely changing data (config, reference lists, external API results), with an explicit expiry or invalidation.
- Responses containing user-specific data: `Cache-Control: private` or `no-store`. Never cached by a CDN.

## 8. Know when it breaks

- Error tracking on front and back (Sentry or equivalent). Personal data scrubbed. Source maps uploaded privately to the tracker.
- Server logs structured (JSON), with a request ID, the route and the user ID. Each caught error logged once with its context. No secrets.
- Uptime monitoring on the home page and a `/health` endpoint that checks the DB, with an alert sent by email or phone.
- Billing alerts on every provider.
- Production browser console: no errors.

## 9. Backups that restore

- Automatic backups of the database and of user files (storage buckets are often forgotten), daily at least, with a defined retention.
- Stored separately from production: another account, another region or another provider.
- Restore tested for real before launch and at least once a quarter: restore into a scratch database, check row counts and a few records. Write the restore procedure in the project's CLAUDE.md.
- Point-in-time recovery enabled when the provider offers it and the data justifies it.
- Backup taken before any risky migration.

## 10. Deploy and roll back

- Migrations backward-compatible with the running code: add, deploy, then remove in a later release.
- Known rollback path: previous deployment one click away, and the migration plan for undoing.
- Preview and production use separate databases.
- Serverless or edge: use a connection pooler for the database (Supabase pooler, PgBouncer, Prisma Accelerate or the host's equivalent). Each function instance opening its own connections exhausts the database.
- Scheduled jobs (cron) report each run to a heartbeat monitor, so a job that silently stops is noticed.
- Environment variables checked at startup: the app refuses to boot with a missing required variable instead of failing on first use.
