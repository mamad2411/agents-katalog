---
name: payment-failed-and-recovery
description: >-
  Use when handling failed Stripe payments: invoice.payment_failed,
  past_due subscriptions, dunning emails, grace periods, or billing recovery UX.
  Not for initial Checkout setup or webhook signature basics (use
  stripe-payment-webhooks).
---

# Payment failed and recovery

Failed renewals are normal. Handle via **webhooks** + clear UX, not silent lockout.

## Webhook events

| Event | Meaning |
|-------|---------|
| `invoice.payment_failed` | Charge failed; subscription often → `past_due` |
| `customer.subscription.updated` | Status may be `past_due`, `unpaid` |
| `invoice.paid` | Recovery successful — restore `active` |

Handler: upsert `subscriptions.status` from Stripe object; never invent status client-side.

## Entitlement policy (choose explicitly)

Document in code comments:

**Strict** — revoke pro immediately on `past_due`.

**Grace** — keep pro for N days while `past_due`; store `grace_until` on subscription row.

Default recommendation: **3–7 day grace** + banner; full revoke when status `canceled` or `unpaid`.

## UX

- Global banner for `past_due`: "Payment failed — update card" → Customer Portal link.
- `stripe.billingPortal.sessions.create({ customer, return_url })` from edge function or authenticated API.
- Do not delete user data on first failure.

## Email (optional)

On `invoice.payment_failed`, invoke `send-email` edge function (`email-and-notifications` skill) with idempotency key `event.id`.

## Stripe settings

- Smart Retries enabled in Stripe Billing settings.
- Configure dunning emails in Stripe or your app, not both blindly (duplicate emails).

## Avoid

- Ignoring `invoice.payment_failed`.
- Permanent ban without `subscription.deleted` or explicit cancel.
- Charging again from custom code instead of Stripe retry + Portal.

## Checklist

- [ ] `invoice.payment_failed` updates DB status
- [ ] Portal link in app for affected users
- [ ] `invoice.paid` restores access
- [ ] Idempotent on event replay
