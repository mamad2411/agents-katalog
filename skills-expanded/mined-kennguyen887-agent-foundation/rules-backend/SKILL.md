---
name: rules-backend
description: Binding personal rules for backend data — load before adding config/env vars, writing migrations/SQL/transactions/money fields, or building consumers, crons, retries, timeouts or backfills.
---

# rules-backend

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## Config & Env — `21-config-environment-rules.md`
- Never hardcode config; new env vars → `.env.example` + Joi/Zod schema (fail boot if missing); no `process.env.X` in business logic.

## Database — `22-database-migration-rules.md`
- Follow database-migrations skill; never alter schema manually; migrations immutable once merged, reversible; filters in SQL.
- ACID: 2+ dependent writes in ONE trx, every query uses the trx, no external calls inside; invariants in schema (unique index > check-then-insert, map violations to 4xx); derived data in same trx or computed on read; locks only for read-decide-write under concurrency — atomic conditional UPDATE + affected rows > atomic arithmetic > `FOR UPDATE` inside the same trx; short trx, retry whole trx on deadlock; report success only after commit; durable state in DB (outbox for critical side effects).
- Money never FLOAT — `DECIMAL(p,2)`/cents, no float math, round once.
- Avoid OR across columns in WHERE (kill NULLs with NOT NULL DEFAULT, same-column → IN, else UNION ALL/derived column); sargable predicates + index; never column-vs-column selection — use a constant recency window.

## Reliability — `23-reliability-rules-idempotency-bounded-everything.md`
- Every consumer idempotent (natural-key upsert / atomic status transition / processed marker in same trx); crons need overlap guard + max tries; migrations/backfills idempotent.
- Everything bounded: explicit timeouts under the caller's deadline; paginate/chunk growing scans, select only needed columns; retries capped with backoff + jitter.
