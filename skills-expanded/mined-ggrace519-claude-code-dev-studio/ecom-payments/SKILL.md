---
name: ecom-payments
description: Payments integration specialist. Owns gateway integration (Stripe, Adyen, Braintree, PayPal), 3DS / SCA, tokenization, auth/capture/void/refund, chargebacks, and PCI scope minimization. Auto-invoked for any payment code path.
---

# E-commerce Payments

Money moves here, and mistakes surface on customer statements and audit
reports. Double-charges, orphan auths, and mis-captured amounts are production
outages with a finance ticket attached.

## When to reach for this

- Integrating a gateway (Stripe, Adyen, Braintree, PayPal) or a local payment method
- Implementing auth / capture / void / refund / partial-refund flows
- Handling 3DS2 / SCA challenges or payment webhooks
- Reviewing anything that could expand PCI scope

## Principles

1. **Hosted fields or provider SDK only.** Raw PAN must never touch your
   servers — that single rule keeps you at PCI SAQ-A / SAQ-A-EP instead of a
   full assessment. Never log request bodies on payment routes.
2. **Idempotency key on every write.** Auth, capture, void, refund — all keyed
   on an order-derived stable ID, so a retried request cannot double-charge.
   Gateways honor the key (Stripe: `Idempotency-Key` header, 24h window).
3. **Webhooks are the truth; redirects are hints.** A customer closing the tab
   after paying still paid. Drive order state from verified webhooks (raw-body
   signature check; Stripe tolerance 5 min) and treat the return URL as UX only.
4. **Split auth and capture when fulfillment is async.** Authorize at order,
   capture at ship. Card auths typically expire in ~7 days — schedule
   reauthorization or capture before expiry, and void what you won't capture.
5. **Reconcile daily.** Gateway settlement report vs internal order ledger, by
   transaction ID. Flag every delta automatically; unexplained drift is how
   orphan auths and missed refunds are actually found.

## Payment state machine

| State | Entered via | Allowed transitions |
|---|---|---|
| `requires_action` | 3DS challenge issued | `authorized`, `failed` |
| `authorized` | auth success webhook | `captured`, `partially_captured`, `voided`, `expired` |
| `captured` | capture success webhook | `refunded`, `partially_refunded`, `disputed` |
| `failed` / `voided` / `expired` | terminal | re-attempt creates a *new* payment intent |
| `disputed` | chargeback webhook | `dispute_won`, `dispute_lost` (evidence due-date is a hard deadline) |

Enforce transitions in one place; an out-of-order webhook must not move a
`refunded` payment back to `captured`. A worked integration skeleton
(idempotent capture, webhook reconciliation, refund paths) is in
[`references/payment-flow.md`](references/payment-flow.md).

## Pitfalls

- Capturing more than the authorized amount, or after auth expiry
- Refunds issued without checking prior partial refunds (over-refund)
- Trusting the redirect/return URL to mark an order paid
- JSON body-parser re-serializing the webhook body and breaking signature checks
- Storing gateway tokens without scoping them to the customer who created them
- Tests covering only happy-path capture — the branches that matter are
  duplicate webhook, failed capture after auth, partial refund, and chargeback

---
*Related: `ecom-inventory` (allocate on auth, release on failure), `ecom-tax`
(tax committed at capture, reversed on refund), `security-checklist` (PCI-scope
and secrets self-check) · domain agent: `ecom-architect` (provider selection,
payment strategy) · output/ADR format: `playbook-conventions`*
