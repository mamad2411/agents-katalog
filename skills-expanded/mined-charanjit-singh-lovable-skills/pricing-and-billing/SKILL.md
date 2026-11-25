---
name: pricing-and-billing
description: >-
  Use when implementing Stripe subscriptions, checkout, customer portal,
  trials, invoices, or plan gating. Not for one-time tips without Stripe or
  display-only pricing tables with no payment.
---

# Pricing and billing (Stripe)

This skill is the **entry point** for Stripe work. Pair with:

- `stripe-payment-webhooks` — handler and event matrix
- `payment-webhook-idempotency` — duplicate event safety
- `payment-webhook-testing` — Stripe CLI, local debug
- `payment-failed-and-recovery` — dunning UX
- `stripe-one-time-payment-webhooks` — non-subscription products

## Architecture

- **Checkout** or **Pricing Table** for subscribe; **Customer Portal** for manage/cancel.
- Webhooks in an **edge function** are the source of truth for `subscription.status`.
- DB: `subscriptions(user_id, stripe_customer_id, stripe_subscription_id, status, price_id, current_period_end)`.

## Client

- Never use secret key in frontend. Publishable key only for Checkout/Elements if needed.
- After checkout success, **wait for webhook** before unlocking pro features (or poll subscription row with timeout UX).

## Webhook events (handle at minimum)

- `checkout.session.completed`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `invoice.payment_failed`

Update DB idempotently; log event id processed.

## Plan gating

```ts
const isPro = subscription?.status === "active" || subscription?.status === "trialing";
```

Gate routes and server policies — UI-only gates are insufficient.

## UX

- Pricing page: clear plan comparison, annual/monthly toggle if offered.
- Failed payment: banner + link to portal.
- Trial end: remind before charge when Stripe trial configured.

## Avoid

- Setting `is_pro=true` from client query params.
- Missing webhook signature verification.
- Hardcoding price IDs without env config per environment.
