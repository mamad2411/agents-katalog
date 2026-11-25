---
name: background-jobs-and-cron
description: >-
  Use when scheduling background work: cron jobs, digest emails, cleanup tasks,
  pg_cron, Supabase scheduled edge functions, or job queues. Not for synchronous
  user-facing API in the request path.
---

# Background jobs and cron

This is the overview / decision guide. Once you've picked an approach, the deep dives are:

- [`pg-cron-scheduled-jobs`](../pg-cron-scheduled-jobs/) — pg_cron syntax, monitoring, locking, idempotency.
- [`pg-cron-with-pg-net-edge`](../pg-cron-with-pg-net-edge/) — cron jobs that call edge functions via HTTPS.
- [`pg-cron-recipes`](../pg-cron-recipes/) — copy-pasteable cookbook (cleanup, retries, digests, expirations).

## Choose mechanism

| Need | Approach |
|------|----------|
| Simple periodic task (daily cleanup) | `pg_cron` or Supabase **scheduled Edge Function** |
| Heavy / external APIs | Edge function invoked on schedule |
| User-specific delayed work | `scheduled_at` column + cron polls due rows |
| High volume queue | External queue (future); start with `jobs` table |

## `jobs` table pattern

```sql
create table public.jobs (
  id uuid primary key default gen_random_uuid(),
  type text not null,
  payload jsonb not null default '{}',
  run_at timestamptz not null default now(),
  status text not null default 'pending' check (status in ('pending','running','done','failed')),
  attempts int not null default 0,
  last_error text,
  created_at timestamptz default now()
);
create index jobs_pending_run_at_idx on public.jobs (status, run_at) where status = 'pending';
```

Cron edge function (every minute):

1. `select * from jobs where status = 'pending' and run_at <= now() limit 10 for update skip locked`
2. Process; set `done` or `failed` with backoff (`run_at = now() + interval '5 minutes'`, `attempts + 1`).

## pg_cron (SQL-only tasks)

```sql
select cron.schedule('purge-old-logs', '0 3 * * *', $$ delete from public.logs where created_at < now() - interval '90 days' $$);
```

Enable extension per Supabase project docs; prefer edge function if logic needs secrets/SDKs.

## Scheduled edge function

Supabase dashboard → Edge Functions → schedule, or `supabase functions deploy` with cron config per platform docs.

## Rules

- **Idempotent** job handlers (safe retry).
- Max attempts then `failed` + alert.
- No long blocking in HTTP request — enqueue job instead.

## Avoid

- `setInterval` in browser for server work.
- Duplicate cron without leader lock (`for update skip locked` or single scheduler).

## Checklist

- [ ] Secrets only in edge env
- [ ] Failed jobs visible (admin table or logs)
- [ ] RLS: `jobs` not client-writable
