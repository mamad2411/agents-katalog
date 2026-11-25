---
name: pg-cron-scheduled-jobs
description: >-
  Use when scheduling Postgres jobs with pg_cron — installing the extension,
  writing cron expressions, scheduling SQL or function calls, monitoring runs,
  unscheduling, and avoiding overlap. Companion to background-jobs-and-cron;
  this is the deep dive.
---

# pg_cron deep dive: scheduled jobs inside Postgres

[`pg_cron`](https://github.com/citusdata/pg_cron) runs SQL on a cron schedule from inside Postgres. It is enabled on Supabase and most managed Postgres. Use it for recurring database maintenance, aggregations, soft-delete sweeps, and triggering edge functions via `pg_net`.

Companion skills: [`background-jobs-and-cron`](../background-jobs-and-cron/) (overview), [`pg-cron-with-pg-net-edge`](../pg-cron-with-pg-net-edge/) (calling HTTPS endpoints), [`pg-cron-recipes`](../pg-cron-recipes/) (cookbook), [`postgres-triggers-and-functions`](../postgres-triggers-and-functions/).

## Enable

```sql
create extension if not exists pg_cron;
-- Supabase: also enable in Dashboard → Database → Extensions
```

On Supabase, jobs run inside the `postgres` database. You can only schedule from a role with `cron.schedule` privileges (usually `postgres` / service role via SQL editor).

## Cron syntax (5 fields)

```
 ┌──────── minute (0-59)
 │ ┌────── hour (0-23, UTC)
 │ │ ┌──── day of month (1-31)
 │ │ │ ┌── month (1-12)
 │ │ │ │ ┌ day of week (0-6, Sun=0)
 │ │ │ │ │
 * * * * *
```

Common patterns:

| Schedule | Meaning |
|----------|---------|
| `* * * * *` | every minute |
| `*/5 * * * *` | every 5 minutes |
| `0 * * * *` | top of every hour |
| `0 9 * * *` | 09:00 UTC daily |
| `0 9 * * 1` | 09:00 UTC Mondays |
| `15 3 1 * *` | 03:15 UTC on the 1st of each month |

**All times are UTC.** Convert from your business timezone before writing the schedule.

## Schedule a job

```sql
select cron.schedule(
  job_name => 'cleanup-soft-deleted',
  schedule => '0 3 * * *',
  command  => $$ delete from posts where deleted_at < now() - interval '30 days' $$
);
```

Return value is the `jobid`. Re-running `cron.schedule` with the same `job_name` **replaces** the existing job — safe for idempotent migrations.

## Run a function (preferred)

Inline SQL is hard to test. Wrap logic in a `security definer` function and schedule a one-liner:

```sql
create or replace function public.cleanup_soft_deleted()
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  delete from posts where deleted_at < now() - interval '30 days';
  delete from comments where deleted_at < now() - interval '30 days';
end;
$$;

revoke all on function public.cleanup_soft_deleted() from public, anon, authenticated;

select cron.schedule('cleanup-soft-deleted', '0 3 * * *',
  $$ select public.cleanup_soft_deleted() $$);
```

Now you can unit-test the function directly with `select public.cleanup_soft_deleted();`.

## List and inspect jobs

```sql
-- definitions
select jobid, schedule, command, jobname, active from cron.job;

-- last 50 runs
select jobid, runid, job_pid, status, return_message, start_time, end_time
from cron.job_run_details
order by start_time desc
limit 50;

-- failed runs in the last day
select * from cron.job_run_details
where status = 'failed' and start_time > now() - interval '1 day'
order by start_time desc;
```

`cron.job_run_details` grows forever — schedule its own cleanup (see recipes).

## Update or remove

```sql
-- Re-schedule (replace existing by name)
select cron.schedule('cleanup-soft-deleted', '0 4 * * *',
  $$ select public.cleanup_soft_deleted() $$);

-- Pause / resume
update cron.job set active = false where jobname = 'cleanup-soft-deleted';
update cron.job set active = true  where jobname = 'cleanup-soft-deleted';

-- Delete
select cron.unschedule('cleanup-soft-deleted');
```

## Concurrency and overlapping runs

pg_cron does **not** prevent overlapping runs of the same job. If a job sometimes takes longer than its interval, add a lock:

```sql
create or replace function public.refresh_dashboard_stats()
returns void
language plpgsql
security definer
as $$
begin
  -- advisory lock; skip this run if another is in progress
  if not pg_try_advisory_lock(hashtext('refresh_dashboard_stats')) then
    raise notice 'previous run still in progress, skipping';
    return;
  end if;

  perform refresh_materialized_view_concurrently('public.dashboard_stats');

  perform pg_advisory_unlock(hashtext('refresh_dashboard_stats'));
exception when others then
  perform pg_advisory_unlock(hashtext('refresh_dashboard_stats'));
  raise;
end;
$$;
```

## Idempotency

Cron jobs **will** run twice eventually (restarts, manual triggers, race conditions). Make every job idempotent:

- `delete ... where deleted_at < ...` — safe, just deletes less the second time.
- `update ... where status = 'pending'` — safe, transitions only once.
- Sending an email? Use a `sent_at` column and `where sent_at is null` filter.

```sql
update notifications
   set sent_at = now()
 where scheduled_for <= now() and sent_at is null
 returning id;
-- then enqueue email send for returning ids
```

## Job naming convention

`{verb}-{noun}-{cadence}` or `{noun}-{verb}`:

- `cleanup-soft-deleted`
- `refresh-dashboard-stats`
- `digest-weekly`
- `expire-trials`

Stable names = idempotent re-runs of your migration.

## Migration discipline

Put `cron.schedule` calls in a versioned SQL migration so jobs are reproducible in every environment. Don't rely on the Supabase dashboard UI for the source of truth.

```sql
-- migrations/20260520_schedule_cleanup.sql
select cron.schedule('cleanup-soft-deleted', '0 3 * * *',
  $$ select public.cleanup_soft_deleted() $$);
```

## Time zones

- pg_cron schedules are UTC.
- Inside SQL you can still use `at time zone 'America/Los_Angeles'` for business logic.
- For "every Monday 9am Pacific" use the UTC equivalent (`0 17 * * 1` standard / `0 16 * * 1` daylight saving) — or use a daily 5‑min job that checks local time.

## What pg_cron is NOT good for

- Sub-minute schedules (minimum granularity is 1 minute).
- Long-running tasks (> a few minutes) — extract to an edge function and trigger via [`pg-cron-with-pg-net-edge`](../pg-cron-with-pg-net-edge/).
- Workloads that need retries, backoff, or DLQs — use a real queue (pgmq, Inngest, Trigger.dev).

## Avoid

- Inline multi-statement SQL in `cron.schedule` — wrap in a function.
- Running heavy aggregations during peak traffic windows; schedule off-peak UTC.
- Querying `cron.job_run_details` without a time filter (table grows unbounded).
- Forgetting to lock when a job can overlap itself.
- Storing the schedule only in the dashboard with no migration.

## Checklist

- [ ] `pg_cron` extension enabled.
- [ ] Each job calls a function, not inline SQL.
- [ ] Function is `security definer` with locked-down `search_path` and revoked public execute.
- [ ] Job is idempotent (safe to run twice).
- [ ] Long/overlapping jobs use `pg_try_advisory_lock`.
- [ ] Schedules are checked into migrations.
- [ ] `cron.job_run_details` has its own cleanup job (see recipes).
