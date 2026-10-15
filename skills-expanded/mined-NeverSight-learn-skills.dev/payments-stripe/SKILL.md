---
name: payments-stripe
description: Use when integrating Stripe — set up Checkout for subscriptions, verify webhooks with the signing secret, handle events idempotently, and keep your database in sync with Stripe as the source of truth for billing state.
---

# Payments (Stripe)

## Overview

Stripe is the billing source of truth; your database is a **synced read-model**. The flow: send users to **Checkout**, then let **webhooks** drive every state change (subscription created/updated/cancelled, payment succeeded/failed). Never set a user to "paid" from the success-redirect — that's spoofable. Verify webhook signatures, process events idempotently, and reconcile to your DB.

## When to use

- Charging for subscriptions or one-time purchases.
- Reacting to payment/subscription lifecycle changes.
- Building an upgrade/downgrade or customer-portal flow.

## Checkout (start a subscription)

```ts
// server action / route handler
import Stripe from "stripe";
import { env } from "@/env";
const stripe = new Stripe(env.STRIPE_SECRET_KEY);

export async function createCheckout(orgId: string, priceId: string) {
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${env.NEXT_PUBLIC_APP_URL}/billing?success=1`,
    cancel_url: `${env.NEXT_PUBLIC_APP_URL}/billing`,
    client_reference_id: orgId,            // tie the session back to YOUR tenant
    metadata: { orgId },
  });
  return session.url!;
}
```

## Webhook (the source of truth)

```ts
// src/app/api/webhooks/stripe/route.ts
import Stripe from "stripe";
import { env } from "@/env";
const stripe = new Stripe(env.STRIPE_SECRET_KEY);

export async function POST(req: Request) {
  const body = await req.text();                       // RAW body, not parsed JSON
  const sig = req.headers.get("stripe-signature")!;
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig, env.STRIPE_WEBHOOK_SECRET);
  } catch {
    return new Response("Invalid signature", { status: 400 });
  }

  if (await alreadyProcessed(event.id)) return new Response("ok"); // idempotency

  switch (event.type) {
    case "checkout.session.completed":
    case "customer.subscription.updated":
    case "customer.subscription.deleted":
      await syncSubscriptionToDb(event);               // upsert plan/status/period
      break;
  }
  await markProcessed(event.id);
  return new Response("ok");
}
```

## Pitfalls

- **Granting access on the success redirect** — users can hit that URL without paying. Only webhooks grant access.
- **Parsing the body before verifying** — signature checks need the **raw** body; disable body parsing for this route.
- **No idempotency** — Stripe retries; store processed `event.id`s so retries don't double-apply.
- **Returning 500 on a handled event** — Stripe will retry forever. Return 2xx once you've safely recorded it.
- **Storing card data** — never; Stripe holds it. You store customer/subscription IDs only.
- **Trusting `metadata` you didn't set** — only read metadata you wrote (e.g. `orgId`).

## Hand-off

Stripe events synced into your DB. `subscription-billing` turns that synced state into plan limits and entitlements; the customer portal handles upgrades/cancellations.
