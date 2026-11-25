---
name: stripe-one-time-payment-webhooks
description: >-
  Use when webhooks for one-time Stripe payments: Checkout mode payment, Payment
  Links, payment_intent.succeeded, orders table, credits, or lifetime purchases.
  Not for recurring subscriptions (use stripe-payment-webhooks and
  pricing-and-billing).
---

# Stripe one-time payment webhooks

Separate **orders** / **purchases** from **subscriptions**. Different events and tables.

## Checkout `mode: "payment"`

Handle `checkout.session.completed`:

- `session.mode === "payment"`
- `session.payment_intent` — retrieve for amount, status
- `client_reference_id` / `metadata.user_id` → app user

```ts
case "checkout.session.completed": {
  const session = event.data.object as Stripe.Checkout.Session;
  if (session.mode !== "payment") break;
  const userId = session.client_reference_id ?? session.metadata?.user_id;
  if (!userId || !session.payment_intent) break;
  await upsertOrder({
    user_id: userId,
    stripe_payment_intent_id: session.payment_intent as string,
    stripe_checkout_session_id: session.id,
    amount_total: session.amount_total,
    currency: session.currency,
    status: "paid",
  });
  break;
}
```

Also handle `payment_intent.succeeded` if you create PaymentIntents without Checkout — **same upsert** keyed on `payment_intent.id` (idempotency).

## Schema

```sql
create table public.orders (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id),
  stripe_payment_intent_id text unique,
  stripe_checkout_session_id text unique,
  amount_total bigint,
  currency text,
  status text not null check (status in ('paid', 'refunded', 'failed')),
  product_id text,
  created_at timestamptz default now()
);
```

## Refunds

- `charge.refunded` or `payment_intent.canceled` → set `orders.status = 'refunded'`; revoke credits if applicable.

## Credits / lifetime license

Grant in webhook **after** idempotency check:

```ts
await supabase.rpc("grant_credits", { p_user_id: userId, p_amount: 100 });
```

RPC must be idempotent or guarded by `stripe_payment_intent_id` unique constraint.

## Avoid

- Storing one-time purchase only in `subscriptions` table.
- Fulfilling order on `success_url` without webhook.
- Double grant on `checkout.session.completed` + `payment_intent.succeeded` without shared idempotency key (use same `payment_intent_id` unique key).

## Related

- `stripe-payment-webhooks` — signature and hosting
- `payment-webhook-idempotency` — duplicate events
