---
name: stripe
description: Stripe payments on the web — Checkout Sessions, Elements, webhook signature verification, test mode/CLI, and the entitlements table pattern. Use when adding billing, implementing subscription flows, or debugging payment events.
---

Stripe on the web bills through Checkout Sessions (hosted) or Elements (embedded). Webhooks — not the browser — are the source of truth for payment state. This is direct Stripe integration; RevenueCat is a mobile-store concern and does not apply here.

## Required env vars (Doppler)

| Var | Scope | Notes |
| --- | --- | --- |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | client | Safe to expose in the browser bundle |
| `STRIPE_SECRET_KEY` | server only | Route handlers / server actions only — never `NEXT_PUBLIC_` |
| `STRIPE_WEBHOOK_SECRET` | server only | For webhook signature verification; differs per env (and per `stripe listen` session) |

## PCI rules — non-negotiable

- **Never handle raw card data** — Checkout's hosted page or Elements' iframe inputs only; card details never touch your DOM or server
- **Never log** card numbers, CVVs, or full PANs anywhere
- **Never store** payment method details in your database — store Stripe ids (`cus_…`, `sub_…`, `pm_…`) only
- The Stripe SDK instance lives in a server-only module:

```ts
// src/lib/stripe.ts
import 'server-only';
import Stripe from 'stripe';
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
```

## Canonical Checkout flow (subscriptions)

```ts
// server action or route handler
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  customer: customerId,                       // create the customer on signup, store cus_… on the tenant
  line_items: [{ price: priceId, quantity: 1 }],
  success_url: `${origin}/settings/billing?status=success`,
  cancel_url: `${origin}/settings/billing`,
  metadata: { business_id: businessId },       // how webhooks map back to the tenant
  subscription_data: { metadata: { business_id: businessId } },
});
redirect(session.url!);
```

For self-serve plan changes, payment-method updates, and cancellation, send users to the **Billing Portal** instead of building UI:

```ts
const portal = await stripe.billingPortal.sessions.create({
  customer: customerId,
  return_url: `${origin}/settings/billing`,
});
redirect(portal.url);
```

Use **Elements** (`@stripe/stripe-js` + `@stripe/react-stripe-js`, PaymentIntent + `client_secret`) only when the flow must stay fully in-app; Checkout is less code and Stripe maintains the compliance surface.

## Webhook handler — raw body or nothing

Signature verification is an HMAC over the exact raw bytes. Read `request.text()`, never `request.json()`:

```ts
// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const body = await request.text(); // RAW body — required
  const sig = request.headers.get('stripe-signature');
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig!, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch {
    return new NextResponse('Invalid signature', { status: 400 });
  }
  // handle event, return 200 fast
}
```

- Exclude this route from the auth middleware matcher — Stripe's request carries no session cookie
- Handlers must be idempotent (Stripe retries; events can arrive out of order) — upsert keyed on the subscription id
- Return `200` quickly; do slow work after acknowledging

## Entitlements table pattern

One row per tenant, written **only** by the webhook handler (service-role client); the app reads it and never writes it:

```sql
create table api.entitlements (
  business_id uuid primary key references api.businesses(id) on delete cascade,
  stripe_customer_id text unique,
  stripe_subscription_id text unique,
  plan text not null default 'free',
  status text not null default 'inactive',   -- active | trialing | past_due | canceled
  current_period_end timestamptz,
  updated_at timestamptz not null default now()
);
```

Sync it from `checkout.session.completed` + `customer.subscription.created/updated/deleted` + `invoice.payment_failed`. Gate features on `status in ('active','trialing')`. Server-side checks (route handlers, server actions, RLS) enforce the gate — client-side checks are cosmetic.

## Test mode / CLI

```bash
stripe login
stripe listen --forward-to localhost:3000/api/webhooks/stripe
# copy the printed whsec_… into the dev config as STRIPE_WEBHOOK_SECRET
stripe trigger checkout.session.completed    # simulate the full event flow
stripe events resend evt_…                   # replay a real event while debugging
```

Test cards: `4242 4242 4242 4242` (success), `4000 0000 0000 9995` (insufficient funds), `4000 0025 0000 3155` (requires 3DS).

## Rules

- Always verify webhook signatures — a handler that skips `constructEvent` is a blocker in review
- The webhook updates the database; the success page only reads it — never flip entitlements from client-side redirect state
- Prices/products are created in the Stripe dashboard or a checked-in seed script — reference `price_…` ids from env/config, never hardcode amounts in the app
- Test the full loop in stg with `stripe listen` before touching live mode
- Run `tsc --noEmit` after any payment flow change
