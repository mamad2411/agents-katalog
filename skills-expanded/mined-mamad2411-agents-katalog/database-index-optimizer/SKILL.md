---
name: database-index-optimizer
description: Audits the Pitch CRM Supabase/Postgres database for missing, duplicate, and unused indexes and slow queries, then proposes safe, reviewable migrations. Auto-loads on requests about slow queries, query plans, EXPLAIN/ANALYZE, pg_stat_statements, pg_stat_user_indexes, index bloat, missing indexes on tenant_id/company_id/contact_id/job_id/project_id/phone/email/property_address/status/created_at/updated_at, queue tables, webhook/message event id lookups, sequential scans on large tables, or general database performance tuning.
---

# Database Index Optimizer

Audit-only by default. NEVER run `DROP INDEX`, `CREATE INDEX` (non-concurrent), or `REINDEX` directly against production. Always emit a migration file for human review.

## When this skill applies

Triggers: "slow query", "missing index", "query plan", "EXPLAIN", "pg_stat", "seq scan", "index bloat", "duplicate index", "unused index", "tune database", "why is X page slow", "timeouts on Y endpoint", "queue is backing up", "webhook lookups slow".

## Hard rules

1. **Read-only audit first.** Use `supabase--read_query` and `supabase--analytics_query` to gather evidence before proposing anything.
2. **Migrations only via `supabase--migration`.** Every index change is a reviewable SQL migration. No ad-hoc DDL.
3. **`CREATE INDEX CONCURRENTLY` always** on tables with >10k rows or any tenant-facing table. Never block writes on `contacts`, `jobs`, `pipeline_entries`, `roof_measurements`, `sms_messages`, `call_sessions`, `photos`, `webhook_events`, `function_cache`, or any queue table.
4. **Partial + composite over wide.** Prefer `(tenant_id, <hot column>)` composites and partial indexes (`WHERE deleted_at IS NULL`, `WHERE status IN (...)`) over single-column or covering-everything indexes.
5. **Tenant-leading.** Every multi-tenant table's hot index MUST lead with `tenant_id` (or `company_id` where that is the scoping column). This matches the project's `useEffectiveTenantId()` + `.eq('tenant_id', …)` query pattern. A non-tenant-leading index on a tenant-scoped table is a finding, not a fix.
6. **Never drop in the same migration as create.** Drops go in a follow-up migration after the new index has been observed in production for ≥7 days.
7. **No `DROP INDEX` without proof.** Require `idx_scan = 0` in `pg_stat_user_indexes` over a meaningful window AND confirmation the index is not enforcing a unique constraint, FK, or RLS predicate.
8. **Respect existing memory.** `pipeline_entries ↔ contacts` joins must keep the `contacts!pipeline_entries_contact_id_fkey` FK intact — never drop indexes backing that FK.

## Audit checklist (run in order)

### Gate 1 — Missing indexes on canonical hot columns

For every table in `public`, check whether an index exists leading with the relevant column. Canonical hot columns:

- Tenant scoping: `tenant_id`, `company_id`
- Foreign keys: `contact_id`, `job_id`, `project_id`, `lead_id`, `estimate_id`, `invoice_id`, `pipeline_entry_id`, `user_id`, `assigned_to`, `created_by`, `brand_id`, `location_id`
- Lookup keys: `phone`, `email`, `property_address`, `address_line1 + zip_code`, `external_id`, `telnyx_call_id`, `telnyx_message_id`, `stripe_payment_intent_id`, `webhook_event_id`, `idempotency_key`
- Filtering: `status`, `stage`, `result_state`, `deleted_at`
- Time: `created_at`, `updated_at`, `scheduled_at`, `next_attempt_at`, `expires_at`

Query to enumerate FK columns missing a leading index:

```sql
SELECT c.conrelid::regclass AS table_name,
       a.attname             AS column_name
FROM pg_constraint c
JOIN pg_attribute a
  ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND c.connamespace = 'public'::regnamespace
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid
      AND i.indkey[0] = a.attnum
  )
ORDER BY 1, 2;
```

### Gate 2 — Tenant-leading composite check

For each tenant-scoped table, the hottest filter combinations must have a `(tenant_id, …)` composite. Common required composites in this project:

- `contacts (tenant_id, phone)`, `contacts (tenant_id, email)`, `contacts (tenant_id, created_at DESC)`, `contacts (tenant_id, status) WHERE deleted_at IS NULL`
- `jobs (tenant_id, status, updated_at DESC)`
- `pipeline_entries (tenant_id, stage_id, updated_at DESC)`, `pipeline_entries (tenant_id, contact_id)`
- `sms_messages (tenant_id, contact_id, created_at DESC)`, `sms_messages (tenant_id, telnyx_message_id)`
- `call_sessions (tenant_id, contact_id, started_at DESC)`, `call_sessions (tenant_id, telnyx_call_id)`
- `photos (tenant_id, job_id, taken_at DESC)`
- `roof_measurements (tenant_id, job_id, created_at DESC)`
- `webhook_events / *_webhook_events (tenant_id, event_id)` UNIQUE — also serves idempotency
- `function_cache (cache_key)` UNIQUE + `(expires_at)` for the cleanup worker
- Queue tables (`*_queue`, `dialer_leads`, `ai_measurement_jobs`, `pdf_jobs`): `(status, next_attempt_at)` partial `WHERE status IN ('pending','queued','retry')`

### Gate 3 — Duplicate indexes

```sql
SELECT n.nspname, t.relname AS table, array_agg(c.relname) AS duplicate_indexes,
       pg_get_indexdef(i.indexrelid) AS def
FROM pg_index i
JOIN pg_class c ON c.oid = i.indexrelid
JOIN pg_class t ON t.oid = i.indrelid
JOIN pg_namespace n ON n.oid = t.relnamespace
WHERE n.nspname = 'public'
GROUP BY n.nspname, t.relname, i.indkey, i.indpred, i.indclass, pg_get_indexdef(i.indexrelid)
HAVING count(*) > 1;
```

Also flag indexes whose key columns are a strict prefix of another index on the same table (the shorter one is usually redundant — but verify it isn't backing a UNIQUE/PK/FK constraint).

### Gate 4 — Unused indexes

```sql
SELECT s.schemaname, s.relname AS table, s.indexrelname AS index,
       s.idx_scan, pg_size_pretty(pg_relation_size(s.indexrelid)) AS size
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE s.schemaname = 'public'
  AND s.idx_scan = 0
  AND NOT i.indisunique
  AND NOT i.indisprimary
ORDER BY pg_relation_size(s.indexrelid) DESC;
```

Cross-check: never propose dropping an index that backs a FK, UNIQUE constraint, or is referenced in an RLS policy's `USING`/`WITH CHECK`. Confirm uptime since last `pg_stat_reset()` is sufficient (`SELECT stats_reset FROM pg_stat_database WHERE datname = current_database();`).

### Gate 5 — Slow queries

If `pg_stat_statements` is enabled:

```sql
SELECT round(mean_exec_time::numeric, 1) AS mean_ms,
       calls,
       round((total_exec_time/1000)::numeric, 1) AS total_s,
       round(rows::numeric / NULLIF(calls,0), 1) AS rows_per_call,
       left(regexp_replace(query, '\s+', ' ', 'g'), 240) AS query
FROM pg_stat_statements
WHERE query NOT ILIKE '%pg_stat_statements%'
ORDER BY total_exec_time DESC
LIMIT 25;
```

For the top offenders, run `EXPLAIN (ANALYZE, BUFFERS)` (read-only, on a representative query) and look for: `Seq Scan` on >10k-row tables, `Rows Removed by Filter` ≫ rows returned, sort spills to disk, nested-loop with >1k outer rows, or index used but with `Filter` doing the real work (wrong index leading column).

Also pull Postgres logs for slow statements:

```sql
SELECT identifier, postgres_logs.timestamp, event_message, parsed.error_severity
FROM postgres_logs
CROSS JOIN unnest(metadata) AS m
CROSS JOIN unnest(m.parsed) AS parsed
WHERE event_message ILIKE '%duration:%'
ORDER BY timestamp DESC
LIMIT 100;
```

### Gate 6 — Queue / webhook / cache tables

These need specialized indexes because of polling patterns:

- Queue tables: partial `(next_attempt_at)` `WHERE status IN ('pending','queued','retry') AND attempts_count < max_attempts`
- Webhook events: `UNIQUE (provider, event_id)` for idempotency; `(tenant_id, received_at DESC)` for inbox views
- `function_cache`: `UNIQUE (cache_key)`, plus `(expires_at)` partial `WHERE expires_at IS NOT NULL` for the cleanup worker (pairs with the backend-auto-cleanup-worker skill)
- `sms_messages` / `call_sessions`: lookup by provider id (`telnyx_message_id`, `telnyx_call_id`) needs UNIQUE for webhook idempotency

## Output: the audit report

Always deliver a single report with six sections (matching the gates above). Each finding has:

- **Severity**: `critical` (timeouts in prod), `high` (>500ms p95), `medium` (>100ms p95 or seq scan on tenant table), `low` (cleanup)
- **Evidence**: query plan snippet, `idx_scan` count, `pg_stat_statements` mean time, or absence of matching `pg_index` row
- **Proposed SQL** (CREATE in one migration, DROP in a separate follow-up migration)
- **Risk notes**: lock behavior, disk size estimate, RLS impact, FK/UNIQUE backing

## Migration template

```sql
-- Migration: add_index_<table>_<columns>
-- Evidence: <p95 ms, calls/day, EXPLAIN snippet, or FK without backing index>
-- Expected impact: <e.g. removes Seq Scan on contacts (~480k rows)>
-- Lock behavior: CONCURRENTLY — non-blocking, requires running outside a transaction

CREATE INDEX CONCURRENTLY IF NOT EXISTS
  idx_<table>_<cols>_<predicate>
  ON public.<table> (tenant_id, <col>, <col2> DESC)
  WHERE deleted_at IS NULL;

-- Verify after deploy:
--   SELECT idx_scan FROM pg_stat_user_indexes WHERE indexrelname = 'idx_<table>_<cols>_<predicate>';
--   Re-run EXPLAIN (ANALYZE, BUFFERS) on the offending query and confirm Index Scan.
```

For drops (separate migration, ≥7 days later):

```sql
-- Migration: drop_unused_index_<name>
-- Evidence: idx_scan = 0 since <stats_reset date>; not backing FK/UNIQUE/RLS.
DROP INDEX CONCURRENTLY IF EXISTS public.<index_name>;
```

## Refusal triggers

Refuse and surface a finding instead of "fixing" when:

- Asked to add an index without first reading `pg_stat_user_indexes` / query plan.
- Asked to `DROP INDEX` without 7+ days of `idx_scan = 0` evidence.
- A proposed index would lead with a non-tenant column on a tenant-scoped table.
- A proposed index duplicates an existing one (same leading columns + predicate).
- Asked to run DDL outside a `supabase--migration` call.
- Asked to add `CREATE INDEX` (non-concurrent) on any table with >10k rows.

## Done definition

An optimization pass is complete only when:

1. A six-gate report has been delivered.
2. Each `critical`/`high` finding has either a migration PR or an explicit reason to defer.
3. The migration uses `CREATE INDEX CONCURRENTLY IF NOT EXISTS` with tenant-leading composite + partial predicate where applicable.
4. Post-deploy verification query is included as a SQL comment.
5. Any proposed DROPs are scheduled as a separate follow-up migration, not bundled with creates.
