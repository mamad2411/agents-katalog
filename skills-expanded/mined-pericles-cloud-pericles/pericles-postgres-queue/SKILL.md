---
name: pericles-postgres-queue
version: 2026.05.1
description: >
  How to do queueing and key-value storage on PostgreSQL in Pericles — the
  deliberate replacement for Kafka and Redis. Use this WHENEVER you need a job
  queue, background processing, scheduled work, notification dispatch, inter-agent
  messaging, rate limiting, or a cache/KV store, and ALWAYS push back when Kafka,
  Redis, RabbitMQ, Bull, or Celery is proposed. Reflects the existing MessageQueue
  model + monitoring/queue-client.ts and the KeyValueStore model.
doctrine_refs: [§2]
depends_on: [pericles-data-model, pericles-tech-stack]
last_reconciled: 2026-05-28
---

# Pericles Postgres Queue & KV (build skill)

Postgres-based queueing is the deliberate choice for current scale (§2) — one
datastore to run, back up, and reason about. This is already built; use the existing
pieces rather than inventing parallel ones.

## When to use this skill

Any background job, scheduled task, notification/event dispatch, inter-agent message,
rate limiter, or cache/KV need — and any time Kafka/Redis is proposed.

## What already exists (use it)

- **Model `MessageQueue`** (`backend/prisma/schema.prisma`): `queue_name`,
  `message_type` (`event | incident | notification`), `payload` Json, `status`
  (`MessageStatus`, default PENDING), `attempts` / `max_attempts` (default 3),
  `scheduled_at`, `processed_at`, `failed_at`, `error_message`. Indexes
  `[queue_name, status]`, `[organization_id, queue_name]`, `[status, scheduled_at]`.
- **Client `backend/src/monitoring/queue-client.ts`**: `publishToQueue(queueName,
  message)`, `publishBatchToQueue(...)`, `consumeFromQueue(queueName, …, handler)`.
  `QueueMessage = { type, payload, timestamp, organizationId }`. Publishing
  deliberately **does not throw** ("queue publishing should not block main
  operations") — it logs and continues.
- **Model `KeyValueStore`**: namespaced KV (`namespace` default "default", e.g.
  "cache"/"queue"/"session") with `expires_at` TTL; unique `[organization_id,
  namespace, key]`.

Publish/consume through these. Add new queues by choosing a `queue_name` (e.g.
`events-queue`, `validation-queue`, `notifications-queue`), not a new table.

## Hardening the consumer (recommended)

The current `consumeFromQueue` uses `findMany` + `update`, which is fine for a single
worker but can double-process under concurrency. When you add concurrent workers,
claim atomically with `FOR UPDATE SKIP LOCKED`:

```sql
UPDATE "MessageQueue" SET status='PROCESSING', attempts=attempts+1
WHERE id = (
  SELECT id FROM "MessageQueue"
  WHERE queue_name = $1 AND status='PENDING' AND scheduled_at <= now()
  ORDER BY scheduled_at FOR UPDATE SKIP LOCKED LIMIT 1
) RETURNING *;
```

## Retries with backoff

`MessageQueue` already has `attempts`/`max_attempts`. On failure, set a future
`scheduled_at` and bump `attempts`; at `max_attempts` set `status='FAILED'`,
`failed_at`, `error_message`, and alert. `availableAt = now() + base * 2^(attempts-1)`.
Notification delivery specifically retries up to 3 times before alerting the Plan
Admin (`pericles-notifications`).

## Priority & scheduling

Use `scheduled_at` for delayed/scheduled work; a sweeper promotes due rows. For
Critical work (e.g. plan activation) give it a dedicated `queue_name` and process it
first. Note the monitoring loop runs on an interval (`MONITORING_DEFAULT_INTERVAL_MS`,
default 15000) — recurring scans are interval-driven; durable hand-offs go through
`MessageQueue`.

## KV on Postgres

Use `KeyValueStore` with a `namespace` and optional `expires_at` instead of Redis. A
periodic sweep deletes expired rows (the `data-retention-cleanup` job pattern). Rely
on Postgres + indexing before any external cache.

## What this forbids

Introducing Kafka/Redis/RabbitMQ/Bull/Celery without an approved ADR; creating a new
job/cache table alongside `MessageQueue`/`KeyValueStore`; non-atomic claiming under
concurrency (use `SKIP LOCKED`); consequential-action jobs that bypass the Execution
Node (the queue dispatches, the Execution Node commits — `pericles-execution-node`);
unbounded retries.

## Verification

New work uses `MessageQueue`/`KeyValueStore` via `queue-client.ts`; concurrent
consumers use `SKIP LOCKED`; retries back off and cap at `max_attempts` then alert;
KV TTLs swept; no Kafka/Redis imports in `package.json`.

## Existing standards (read alongside)

`CLAUDE.md` (env note: "PostgreSQL-based queue/KV store - no Redis required");
`backend/src/monitoring/queue-client.ts`; `.claude/rules/05-database.md`,
`.claude/rules/13-infrastructure.md`.

## Open questions

- Whether to centralize a generic worker/claim helper (with SKIP LOCKED) so every
  queue consumer is concurrency-safe by default — propose to the platform team.

## Changelog

- 2026.05.1 — Reconciled to the real MessageQueue + KeyValueStore models and
  monitoring/queue-client.ts; documented existing publish/consume and the
  non-blocking-publish design; reframed claim/lease as recommended hardening.
- 2026.05.0 — Initial draft.
