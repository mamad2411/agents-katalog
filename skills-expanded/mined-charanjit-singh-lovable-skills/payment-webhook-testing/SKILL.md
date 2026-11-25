---
name: payment-webhook-testing
description: >-
  Use when testing Stripe payment webhooks locally, debugging webhook failures,
  Stripe CLI forward, replaying events, or webhook logs. Not for production
  deploy only or writing marketing copy.
---

# Payment webhook testing

## Stripe CLI (local)

```bash
stripe login
stripe listen --forward-to http://127.0.0.1:54321/functions/v1/stripe-webhook
```

Copy the **webhook signing secret** CLI prints (`whsec_...`) into local `STRIPE_WEBHOOK_SECRET` (not production secret).

Trigger test events:

```bash
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
```

For custom metadata (`user_id`), create sessions via API in test mode, then complete Checkout in browser, or use `stripe trigger` with fixtures where supported.

## Supabase local functions

```bash
supabase functions serve stripe-webhook --env-file ./supabase/.env.local
```

Env file must include:

- `STRIPE_SECRET_KEY` (sk_test_...)
- `STRIPE_WEBHOOK_SECRET` (from `stripe listen`)
- `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`

## Verify checklist

| Check | How |
|-------|-----|
| Signature | Wrong secret → 400; correct → 200 |
| Idempotency | Send same `event.id` twice → second 200, no double DB row |
| DB write | Row in `subscriptions` / `orders` matches Stripe Dashboard |
| Live vs test | `event.livemode` matches environment |

## Dashboard debugging

- Stripe → Developers → Webhooks → select endpoint → **Recent deliveries**
- Read response body and status; fix 4xx/5xx before shipping
- Use **Resend** after fix to replay (still idempotent on `event.id`)

## Common failures

| Symptom | Fix |
|---------|-----|
| Invalid signature | Raw body parsing; wrong `whsec`; body parsed as JSON before verify |
| 500 timeout | Return 200 after DB write; move email to async |
| User not linked | Missing `client_reference_id` / `metadata.user_id` on Checkout |
| Pro not unlocked | Client gating before webhook; add polling or Realtime on `subscriptions` |

## Test mode data

- Use test cards: `4242 4242 4242 4242`
- Never use live keys in Lovable preview or git.

## Avoid

- Disabling signature verification locally "temporarily" and shipping it.
- Testing only via `success_url` without firing webhook.
