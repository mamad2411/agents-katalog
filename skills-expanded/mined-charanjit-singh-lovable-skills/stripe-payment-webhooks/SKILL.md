---
name: stripe-payment-webhooks
description: >-
  Use when implementing or fixing Stripe payment webhooks: signature verification,
  event handlers, syncing subscriptions or Checkout to Supabase, webhook endpoint
  setup. Not for pricing page UI only, non-Stripe providers, or generic edge
  functions without payment events (see edge-functions-and-webhooks).
---

# Stripe payment webhooks

Webhooks are the **source of truth** for paid state. Checkout success URLs and client callbacks are not sufficient alone.

Related: `edge-functions-and-webhooks` (hosting), `payment-webhook-idempotency`, `payment-webhook-testing`, `payment-failed-and-recovery`, `pricing-and-billing`.

## Endpoint

- Supabase Edge Function: `supabase/functions/stripe-webhook/index.ts`
- Stripe Dashboard → Webhooks → endpoint URL → signing secret in `STRIPE_WEBHOOK_SECRET`
- Use **raw body** for signature verification (do not parse JSON first).

```ts
import Stripe from "npm:stripe@17";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, {
  apiVersion: "2024-11-20.acacia",
  httpClient: Stripe.createFetchHttpClient(),
});
const cryptoProvider = Stripe.createSubtleCryptoProvider();

const signature = req.headers.get("stripe-signature");
const body = await req.text();

let event: Stripe.Event;
try {
  event = await stripe.webhooks.constructEventAsync(
    body,
    signature!,
    Deno.env.get("STRIPE_WEBHOOK_SECRET")!,
    undefined,
    cryptoProvider
  );
} catch {
  return new Response("Invalid signature", { status: 400 });
}
```

Return **2xx quickly** after enqueue or DB write; Stripe retries on non-2xx.

## Database (service role inside function)

```sql
-- Processed events (idempotency) — see payment-webhook-idempotency skill
create table public.stripe_webhook_events (
  id text primary key,  -- Stripe event id evt_...
  type text not null,
  processed_at timestamptz default now()
);

create table public.subscriptions (
  user_id uuid primary key references auth.users(id),
  stripe_customer_id text unique,
  stripe_subscription_id text unique,
  status text not null,
  price_id text,
  current_period_end timestamptz,
  cancel_at_period_end boolean default false,
  updated_at timestamptz default now()
);
```

Map `user_id` via `client_reference_id` on Checkout or `metadata.user_id` on Customer/Subscription.

## Event handlers (subscriptions)

| Event | Action |
|-------|--------|
| `checkout.session.completed` | Read `subscription` or `mode`; link `customer` to `user_id`; upsert subscription row |
| `customer.subscription.created` | Upsert status, `price_id`, period end |
| `customer.subscription.updated` | Same; handle plan change, `cancel_at_period_end` |
| `customer.subscription.deleted` | Set status `canceled`; revoke entitlements |
| `invoice.paid` | Confirm period; optional receipt email |
| `invoice.payment_failed` | See `payment-failed-and-recovery` |

```ts
switch (event.type) {
  case "checkout.session.completed": {
    const session = event.data.object as Stripe.Checkout.Session;
    const userId = session.client_reference_id ?? session.metadata?.user_id;
    if (!userId) break;
    // retrieve subscription if mode=subscription
    break;
  }
  case "customer.subscription.updated":
  case "customer.subscription.deleted": {
    const sub = event.data.object as Stripe.Subscription;
    await upsertSubscriptionFromStripe(sub);
    break;
  }
  default:
    // unhandled — still return 200 if intentionally ignored
}
```

## One-time payments

For `mode: "payment"` Checkout or Payment Links, handle:

- `checkout.session.completed` (check `mode === "payment"`)
- `payment_intent.succeeded`

Store `orders` or `purchases` table; do not reuse subscription row without clear schema.

## Metadata contract

Always set on Checkout Session creation (server or Stripe Dashboard template):

- `client_reference_id`: Supabase `auth.users.id`
- `metadata.user_id`: same (backup)

Never trust webhook to grant access without resolving user from metadata you control at session creation.

## Entitlements

After DB upsert, app reads `subscriptions.status`:

- Pro: `active`, `trialing`
- Not pro: `canceled`, `unpaid`, `past_due`, `incomplete`, missing row

## Avoid

- Skipping signature verification in production.
- Using Checkout `success_url` alone to set `is_pro`.
- Logging full card or customer PII.
- 4xx on duplicate events (use idempotency — return 200 if already processed).

## Checklist

- [ ] Raw body + `constructEvent` / `constructEventAsync`
- [ ] `stripe_webhook_events` insert before side effects
- [ ] Service role client only inside function
- [ ] Test mode vs live mode secrets separated

Templates: [examples.md](examples.md).
