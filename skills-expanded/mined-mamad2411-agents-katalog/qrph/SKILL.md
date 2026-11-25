---
name: "qrph"
description: "Use when the task involves generating or integrating NextPay QRPH collection flows, especially choosing between dynamic one-time payment intents and static reusable funding methods, explaining QRPH webhook timing, or producing request and response examples from the NextPay Partners API v2 contract."
---

# NextPay QRPH

## Overview

Use this skill for QRPH money-in flows on NextPay Partners API v2. Start with `references/README.md` to choose between dynamic and static QRPH, then read the matching reference file, and use the live OpenAPI URL when exact request fields, enums, or response shapes matter.

Use `$nextapi` instead when the task goes beyond QRPH collection into merchants, accounts, payouts, or general integration work.

## Freshness

Treat the markdown references as workflow guides. Use `https://api.partners.nextpay.world/v2/openapi` as the source of truth for current wire shapes and enum values.

## Quick Decision Tree

```text
Need a one-time QR with a fixed merchant amount and expiry?
└─ references/payment-intents.md

Need a reusable QR where the customer chooses the amount?
└─ references/funding-methods.md

Need to understand checkout, settlement, or expiry webhook behavior?
└─ references/webhooks.md

Need exact request or response fields?
└─ `https://api.partners.nextpay.world/v2/openapi`
```

## Workflow

1. Use `https://api.partners.nextpay.world` as the API base URL.
2. Use HTTP Basic Auth with the Client ID as the username and the Client Secret as the password.
3. Read `references/README.md` to choose between dynamic QRPH and static QRPH.
4. Read `references/payment-intents.md` or `references/funding-methods.md` for the route shortlist and operational model.
5. Read `references/webhooks.md` when the task involves checkout UX, payout readiness, or settlement timing.
6. Read the live OpenAPI URL for exact current request bodies, enums, headers, and response fields.
7. Explain `PHP/2` whenever it appears. Precision notation means the integer amount stores minor units, so `10000` means PHP 100.00.

## QRPH Rules

- Payment intents are dynamic QRPH flows: one use, fixed amount, expiring.
- Funding methods are static QRPH flows: reusable, customer-entered amount, non-expiring.
- Payment intent creation currently supports `automatic`, `ph_netbank`, and `ph_coins` provider selection for `qrph_p2m_reference`.
- Funding method creation is narrower in the current public schema and should be documented as `ph_netbank` plus `qrph_p2m_reference`.
- Prefer `X-Idempotency-Key` on QRPH create endpoints to avoid duplicate side effects on retries.
- Do not promise an expiry webhook. Expiry is represented by `expires_at`, so fetch the resource if confirmation is needed.
- Treat `v2.payment_instrument.payment_received` as the earliest positive payment acknowledgment, `v2.payment_instrument.payment_settled` as the stronger settlement signal, and `v2.payment_intent.succeeded` as the one-time business completion event.

## References

- Read `references/README.md` first for dynamic versus static QRPH routing.
- Read `references/payment-intents.md` for one-time QRPH generation and lookup.
- Read `references/funding-methods.md` for reusable QRPH generation and lookup.
- Read `references/webhooks.md` for QRPH webhook semantics and timing nuance.
- Read `https://api.partners.nextpay.world/v2/openapi` for the live current contract.
