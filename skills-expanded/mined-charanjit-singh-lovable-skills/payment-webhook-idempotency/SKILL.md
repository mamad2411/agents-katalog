---
name: payment-webhook-idempotency
description: >-
  Use when Stripe or payment webhooks fire twice, need duplicate event handling,
  stripe_webhook_events table, ordering, or safe retries. Not for first-time
  webhook setup without idempotency concerns (use stripe-payment-webhooks).
---

# Payment webhook idempotency

Stripe **retries** webhooks on non-2xx, slow responses, or network blips. Handlers must be safe to run multiple times for the same `event.id`.

## Rules

1. **Insert `event.id` first** (or check existence) before side effects.
2. On duplicate `event.id`, return **200** immediately — do not re-grant credits or extend subscription twice.
3. Side effects (DB upsert, emails, credits) must be **upserts** keyed by stable IDs (`subscription_id`, `payment_intent_id`), not blind inserts.

## Table

```sql
create table public.stripe_webhook_events (
  id text primary key,
  type text not null,
  livemode boolean,
  processed_at timestamptz not null default now()
);

-- RLS: no client access; edge function uses service role only
alter table public.stripe_webhook_events enable row level security;
-- no policies for anon/authenticated
```

## Handler flow

```
receive event
  → verify signature
  → if event.id exists in stripe_webhook_events → 200 OK (duplicate)
  → begin logical work
  → upsert subscription / order (idempotent on stripe_subscription_id)
  → insert stripe_webhook_events
  → 200 OK
```

If work fails **after** partial writes, prefer:

- Transaction where possible, or
- Compensating upsert on retry, or
- Insert event id only after success (accept rare double-work on crash — mitigate with unique constraints on business keys)

## Unique constraints (business layer)

```sql
alter table public.subscriptions
  add constraint subscriptions_stripe_sub_id_unique unique (stripe_subscription_id);

create table public.orders (
  id uuid primary key default gen_random_uuid(),
  stripe_payment_intent_id text unique,
  user_id uuid not null,
  amount_cents int not null,
  status text not null
);
```

## Ordering

Events may arrive out of order (`subscription.updated` before `checkout.session.completed`). Upsert from **latest Stripe object** via API retrieve when unsure, or handle both paths to the same upsert function.

## Avoid

- `insert into credits (amount) values (100)` without idempotency key per event.
- Returning 500 after successfully granting access (causes retry + duplicate grant).
- Deleting webhook event rows in production.

## Checklist

- [ ] Primary key = Stripe `event.id`
- [ ] Duplicate returns 200
- [ ] Business tables have unique Stripe IDs
