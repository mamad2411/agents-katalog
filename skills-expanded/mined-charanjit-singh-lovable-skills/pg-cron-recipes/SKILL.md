---
name: pg-cron-recipes
description: >-
  Use when you need a copy-pasteable pg_cron recipe — cleanup of soft-deleted
  rows, expiring trials, materialized view refresh, retry queue, scheduled
  notifications, log table trimming. Cookbook companion to
  pg-cron-scheduled-jobs.
---

# pg_cron recipes (cookbook)

Battle-tested recipes for common scheduled jobs. All examples assume `pg_cron` and (where noted) `pg_net` are enabled. See [`pg-cron-scheduled-jobs`](../pg-cron-scheduled-jobs/) for the fundamentals and [`pg-cron-with-pg-net-edge`](../pg-cron-with-pg-net-edge/) for HTTPS calls.

Every recipe follows the same shape:

1. SQL function (`security definer`, idempotent).
2. `cron.schedule` call by stable name.
3. Notes on tuning the cadence.

---

## 1. Cleanup soft-deleted rows (daily)

```sql
create or replace function public.cleanup_soft_deleted()
returns table(table_name text, deleted_rows bigint)
language plpgsql
security definer
set search_path = public
as $$
declare
  rec record;
  n bigint;
begin
  for rec in
    select unnest(array['posts','comments','attachments']) as t
  loop
    execute format(
      'delete from %I where deleted_at < now() - interval ''30 days''',
      rec.t
    );
    get diagnostics n = row_count;
    table_name := rec.t;
    deleted_rows := n;
    return next;
  end loop;
end;
$$;

select cron.schedule('cleanup-soft-deleted', '0 3 * * *',
  $$ select public.cleanup_soft_deleted() $$);
```

Off-peak (03:00 UTC). Returns row counts per table for easy auditing.

---

## 2. Expire free trials (hourly)

```sql
create or replace function public.expire_trials()
returns int
language plpgsql
security definer
as $$
declare
  n int;
begin
  update organizations
     set plan = 'free',
         trial_expired_at = now()
   where plan = 'trial'
     and trial_ends_at < now()
     and trial_expired_at is null;
  get diagnostics n = row_count;
  return n;
end;
$$;

select cron.schedule('expire-trials', '5 * * * *',  -- 5 past every hour
  $$ select public.expire_trials() $$);
```

Off the hour boundary (`5 * * * *`) to avoid lock contention with other top-of-hour jobs.

---

## 3. Refresh materialized view (hourly, non-blocking)

```sql
create materialized view if not exists public.dashboard_stats as
select org_id,
       count(*)            as project_count,
       sum(monthly_revenue) as mrr
  from projects
 group by org_id;

create unique index if not exists dashboard_stats_org_id_idx
  on public.dashboard_stats(org_id);  -- required for concurrent refresh

create or replace function public.refresh_dashboard_stats()
returns void
language plpgsql
security definer
as $$
begin
  if not pg_try_advisory_lock(hashtext('refresh_dashboard_stats')) then
    return;
  end if;
  refresh materialized view concurrently public.dashboard_stats;
  perform pg_advisory_unlock(hashtext('refresh_dashboard_stats'));
exception when others then
  perform pg_advisory_unlock(hashtext('refresh_dashboard_stats'));
  raise;
end;
$$;

select cron.schedule('refresh-dashboard-stats', '*/15 * * * *',
  $$ select public.refresh_dashboard_stats() $$);
```

`concurrently` avoids locking readers; unique index is required. Advisory lock prevents overlap if a refresh takes > 15 min.

---

## 4. Scheduled notifications dispatch (every minute)

Notifications are inserted with `scheduled_for`. Cron sweeps due ones, marks them `sent`, and (optionally) calls an edge function to actually deliver.

```sql
create or replace function public.dispatch_due_notifications()
returns int
language plpgsql
security definer
as $$
declare
  ids uuid[];
begin
  with claimed as (
    select id from notifications
     where sent_at is null
       and scheduled_for <= now()
     order by scheduled_for
     limit 200
     for update skip locked
  )
  update notifications n
     set sent_at = now()
    from claimed
   where n.id = claimed.id
  returning n.id into ids;

  if array_length(ids, 1) is not null then
    perform net.http_post(
      url     := 'https://YOUR-PROJECT.functions.supabase.co/deliver-notifications',
      headers := jsonb_build_object(
        'Content-Type','application/json',
        'Authorization','Bearer ' || current_setting('app.cron_secret', true)
      ),
      body    := jsonb_build_object('ids', to_jsonb(ids))
    );
  end if;

  return coalesce(array_length(ids, 1), 0);
end;
$$;

select cron.schedule('dispatch-notifications', '* * * * *',
  $$ select public.dispatch_due_notifications() $$);
```

`for update skip locked` makes this safe even if two runs overlap. Batch size 200 keeps each tick cheap.

---

## 5. Retry failed webhook deliveries (every 5 min)

```sql
create or replace function public.retry_failed_webhooks()
returns int
language plpgsql
security definer
as $$
declare
  n int;
begin
  with due as (
    select id from webhook_deliveries
     where status = 'failed'
       and attempts < 5
       and next_attempt_at <= now()
     for update skip locked
     limit 50
  )
  update webhook_deliveries w
     set status = 'pending',
         attempts = attempts + 1,
         next_attempt_at = now() + (power(2, attempts) || ' minutes')::interval
    from due
   where w.id = due.id;
  get diagnostics n = row_count;
  return n;
end;
$$;

select cron.schedule('retry-webhooks', '*/5 * * * *',
  $$ select public.retry_failed_webhooks() $$);
```

Exponential backoff in SQL: 2, 4, 8, 16, 32 minutes between attempts.

---

## 6. Trim audit / log tables (daily)

```sql
create or replace function public.trim_audit_log(keep_days int default 90)
returns bigint
language plpgsql
security definer
as $$
declare
  n bigint;
begin
  delete from audit_log where created_at < now() - (keep_days || ' days')::interval;
  get diagnostics n = row_count;
  return n;
end;
$$;

select cron.schedule('trim-audit-log', '30 3 * * *',
  $$ select public.trim_audit_log(90) $$);
```

Pair with table partitioning by month for cheaper bulk drops once tables get large.

---

## 7. Trim pg_cron and pg_net history (daily)

These tables grow forever unless you trim:

```sql
create or replace function public.trim_cron_history()
returns void
language sql
security definer
as $$
  delete from cron.job_run_details where end_time < now() - interval '14 days';
  delete from net._http_response   where created  < now() - interval '7 days';
$$;

select cron.schedule('trim-cron-history', '45 3 * * *',
  $$ select public.trim_cron_history() $$);
```

---

## 8. Weekly digest fan-out (Mondays 14:00 UTC)

```sql
create or replace function public.enqueue_weekly_digest()
returns int
language plpgsql
security definer
as $$
declare
  n int;
begin
  insert into notifications (user_id, kind, payload, scheduled_for)
  select u.id,
         'weekly_digest',
         jsonb_build_object('week_of', date_trunc('week', now())),
         now()
    from users u
   where u.email_digest_optin
     and u.last_digest_sent_at < now() - interval '6 days';
  get diagnostics n = row_count;
  update users
     set last_digest_sent_at = now()
   where email_digest_optin
     and last_digest_sent_at < now() - interval '6 days';
  return n;
end;
$$;

select cron.schedule('enqueue-weekly-digest', '0 14 * * 1',
  $$ select public.enqueue_weekly_digest() $$);
```

Notice this only **enqueues** — actual sending goes through the per-minute dispatcher (#4).

---

## 9. Heartbeat / liveness ping (every minute)

```sql
create table if not exists ops.heartbeat (
  id int primary key default 1,
  last_seen timestamptz not null
);
insert into ops.heartbeat values (1, now()) on conflict (id) do nothing;

create or replace function ops.heartbeat_tick()
returns void
language sql
security definer
as $$
  update ops.heartbeat set last_seen = now() where id = 1;
$$;

select cron.schedule('heartbeat', '* * * * *', $$ select ops.heartbeat_tick() $$);
```

External monitor can alert if `now() - last_seen > 5 minutes`.

---

## 10. Anonymize PII on inactive accounts (weekly)

```sql
create or replace function public.anonymize_inactive_users(after_days int default 365)
returns int
language plpgsql
security definer
as $$
declare
  n int;
begin
  update users
     set email = 'deleted+' || id || '@example.invalid',
         full_name = 'Deleted user',
         avatar_url = null,
         phone = null,
         anonymized_at = now()
   where last_active_at < now() - (after_days || ' days')::interval
     and anonymized_at is null
     and deleted_at is not null;
  get diagnostics n = row_count;
  return n;
end;
$$;

select cron.schedule('anonymize-inactive', '0 4 * * 0',  -- Sunday 04:00 UTC
  $$ select public.anonymize_inactive_users(365) $$);
```

Helps meet GDPR / data minimization obligations.

---

## Cadence quick-reference

| Job class | Suggested cron |
|-----------|----------------|
| Hot queue dispatch | `* * * * *` |
| Retries / backoff | `*/5 * * * *` |
| Aggregation refresh | `*/15 * * * *` or `0 * * * *` |
| Expiration sweeps | `5 * * * *` |
| Daily cleanups | `0 3 * * *` (off-peak UTC) |
| Trims / log retention | `30 3 * * *` |
| Weekly digests | `0 14 * * 1` |
| Heavy reports | `0 5 * * 0` (Sunday early) |

## Avoid

- Running all daily jobs at `0 0 * * *` — they pile up. Stagger by 15–30 minutes.
- Skipping `for update skip locked` on queue-style sweeps (causes double-sends).
- Letting `cron.job_run_details` / `net._http_response` grow forever.
- Writing one giant function that does five unrelated things — split per concern.

## Checklist

- [ ] Each recipe is wrapped in a `security definer` function.
- [ ] Schedules staggered across the hour and day.
- [ ] Queue sweeps use `for update skip locked` + batch size.
- [ ] History tables (cron, pg_net) have their own trim job.
- [ ] Heartbeat or external alert on long-running / failed jobs.
