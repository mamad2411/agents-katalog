---
name: pg-cron-with-pg-net-edge
description: >-
  Use when pg_cron needs to call an HTTPS endpoint — typically a Supabase Edge
  Function — for work too heavy or external for plain SQL. Covers pg_net setup,
  authentication, payload signing, and reading async responses.
---

# Calling edge functions from pg_cron via pg_net

pg_cron only runs SQL. When you need to send email, hit a third-party API, or run code that doesn't belong in the database, schedule a SQL job that **calls an HTTPS endpoint** using the `pg_net` extension. The standard target is a Supabase Edge Function.

Companion skills: [`pg-cron-scheduled-jobs`](../pg-cron-scheduled-jobs/), [`pg-cron-recipes`](../pg-cron-recipes/), [`edge-functions-and-webhooks`](../edge-functions-and-webhooks/), [`server-input-validation`](../server-input-validation/), [`rate-limiting-edge`](../rate-limiting-edge/).

## Enable pg_net

```sql
create extension if not exists pg_net;
-- Supabase: also enable in Dashboard → Database → Extensions
```

`pg_net` exposes `net.http_post`, `net.http_get`, etc. Requests are **asynchronous** — the SQL function returns a `request_id` immediately and the worker processes the call out-of-band. Responses land in `net._http_response`.

## Minimal pattern

```sql
select net.http_post(
  url     := 'https://YOUR-PROJECT.functions.supabase.co/send-digest',
  headers := jsonb_build_object(
    'Content-Type',  'application/json',
    'Authorization', 'Bearer ' || current_setting('app.cron_secret', true)
  ),
  body    := jsonb_build_object('window', 'daily')
) as request_id;
```

Set the secret once per database:

```sql
-- Run as superuser / via Supabase SQL editor
alter database postgres set app.cron_secret = 'long-random-string-shared-with-the-function';
```

Restart the connection (or use `set local`) for the new GUC to take effect.

## Edge function side: verify the shared secret

```ts
// supabase/functions/send-digest/index.ts
import { createClient } from "npm:@supabase/supabase-js@2";

Deno.serve(async (req) => {
  const auth = req.headers.get("authorization") ?? "";
  if (auth !== `Bearer ${Deno.env.get("CRON_SECRET")}`) {
    return new Response("unauthorized", { status: 401 });
  }
  const { window } = await req.json();

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
  // ... do the heavy work
  return Response.json({ ok: true });
});
```

Set `CRON_SECRET` in Supabase function secrets to the **same** value as `app.cron_secret`. Without this check, anyone can hit the public URL.

## Wrap in a function + schedule

```sql
create or replace function public.invoke_send_digest(window text)
returns bigint
language plpgsql
security definer
as $$
declare
  req_id bigint;
begin
  select net.http_post(
    url     := 'https://YOUR-PROJECT.functions.supabase.co/send-digest',
    headers := jsonb_build_object(
      'Content-Type',  'application/json',
      'Authorization', 'Bearer ' || current_setting('app.cron_secret', true)
    ),
    body    := jsonb_build_object('window', window),
    timeout_milliseconds := 10000
  ) into req_id;
  return req_id;
end;
$$;

revoke all on function public.invoke_send_digest(text) from public, anon, authenticated;

select cron.schedule('send-daily-digest', '0 14 * * *',  -- 14:00 UTC daily
  $$ select public.invoke_send_digest('daily') $$);
```

## Reading responses

```sql
-- Last 20 responses
select id, status_code, content, created
from net._http_response
order by created desc
limit 20;

-- Failures only
select r.id, r.status_code, r.content, r.created
from net._http_response r
where r.status_code is null or r.status_code >= 400
order by r.created desc;
```

`net._http_response` grows unboundedly. Schedule a daily cleanup (`pg-cron-recipes` has one).

## Polling for completion (when you must)

In most flows, fire-and-forget is enough. If you need to react to the response inside SQL, poll:

```sql
create or replace function public.wait_for_response(req_id bigint, max_ms int default 30000)
returns net._http_response
language plpgsql
as $$
declare
  deadline timestamptz := clock_timestamp() + (max_ms || ' milliseconds')::interval;
  r net._http_response;
begin
  loop
    select * into r from net._http_response where id = req_id;
    exit when r.id is not null;
    exit when clock_timestamp() > deadline;
    perform pg_sleep(0.25);
  end loop;
  return r;
end;
$$;
```

Use sparingly — polling blocks the connection.

## Payload signing (defense in depth)

For sensitive payloads, sign with HMAC and verify in the function:

```sql
create or replace function public.invoke_signed(url text, payload jsonb)
returns bigint
language plpgsql
security definer
as $$
declare
  body_text text := payload::text;
  signature text := encode(
    hmac(body_text, current_setting('app.cron_secret', true), 'sha256'),
    'hex'
  );
begin
  return net.http_post(
    url     := url,
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'X-Signature',  signature
    ),
    body    := payload
  );
end;
$$;
```

In the function, recompute HMAC over the raw body and `timingSafeEqual` compare.

## Common targets

| Scenario | Target endpoint |
|----------|------------------|
| Daily digest emails | `send-digest` edge function |
| Stripe sync | `sync-stripe-subscriptions` |
| Webhook re-delivery | `replay-failed-webhooks` |
| AI batch summarization | `summarize-pending` |
| Recompute aggregates from event store | `rebuild-stats` |

## Avoid

- Hardcoding the bearer secret in SQL — use a database GUC (`alter database ... set`).
- Calling slow endpoints **synchronously** from page-blocking SQL.
- Not cleaning up `net._http_response` (it grows forever).
- Ignoring `status_code` — set up an alert on > 0 failed responses in the last hour.
- Sending PII in unsigned, unencrypted bodies to non-Supabase hosts.
- Calling the same edge function from cron and from clients without a way to distinguish (add a header like `X-Source: cron`).

## Checklist

- [ ] `pg_net` extension enabled.
- [ ] Shared secret stored as a database GUC, not in code.
- [ ] Edge function verifies `Authorization: Bearer ...` against `CRON_SECRET`.
- [ ] Cron job calls a wrapper SQL function, not `net.http_post` inline.
- [ ] `net._http_response` cleanup job scheduled.
- [ ] Failure alert (manual or via monitoring) on `status_code >= 400` or null.
