---
name: payment-platform-readiness
description: Prepare payment platform integration for Apple Pay, Google Pay, Google Play Billing, App Store IAP, web checkout, subscriptions, one-time purchases, refunds, restore purchases, receipts, tax, entitlement grants, and support traces. Use when designing or auditing payment flows for apps, games, SaaS, desktop utilities, stores, or marketplaces.
---

# Payment Platform Readiness

Use this skill to make payments reliable, compliant, supportable, and product-friendly.

## Workflow

1. Identify payment channel, product type, billing model, and entitlement semantics.
2. Read `references/payment-platform-patterns.md`.
3. Map catalog, checkout, receipt/webhook processing, entitlement grant, refund/revoke, support, and reconciliation.
4. Check platform-specific constraints and fallback paths.
5. Produce blockers, event contract, and launch checklist.

## Guardrails

- Do not grant durable value from client-only confirmation.
- Keep payment records, entitlement state, and support cases reconcilable.
- Do not use payment confusion as retention.

## Output format

```text
Payment surfaces:
Billing model:

Readiness matrix:
- Catalog:
- Checkout:
- Confirmation:
- Entitlement:
- Refund/revoke:
- Support/reconciliation:

Blockers:
- <blocker>
```
