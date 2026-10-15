---
name: "nextapi"
description: "Use when the task involves general NextPay Partners API v2 integration work, especially setting up Basic Auth, choosing between merchant, account, funding-method, payment-intent, payout, webhook, or sandbox simulation endpoints, generating request or response examples, or explaining integration behavior from the OpenAPI spec."
---

# NextPay Partners API

## Overview

Use this as the broad integration skill for NextPay Partners API v2. Start with `references/README.md` for routing, then read the topic directory that matches the task, and use the live OpenAPI URL for exact current endpoints, schemas, enums, and parameter details.

## Freshness

Treat the markdown references as routing guides, not the source of truth for current wire shapes. Use `https://api.partners.nextpay.world/v2/openapi` when exact fields, enums, endpoint availability, or behavior matter.

## Quick Decision Tree

```text
Need merchant or account work?
└─ references/core/

Need to collect money?
└─ references/money-in/

Need to disburse money?
└─ references/money-out/

Need webhooks or event delivery?
└─ references/integration/

Need sandbox testing?
└─ references/sandbox/

Need exact wire shapes?
└─ `https://api.partners.nextpay.world/v2/openapi`
```

## Workflow

1. Use `https://api.partners.nextpay.world` as the API base URL.
2. Use HTTP Basic Auth with the Client ID as the username and the Client Secret as the password.
3. Read `references/README.md` to choose the right resource family before writing code.
4. Read the matching topic directory under `references/` for the operational model and endpoint shortlist.
5. Read targeted sections of `https://api.partners.nextpay.world/v2/openapi` for exact request bodies, enums, headers, and response fields.
6. Explain `PHP/2` whenever it appears. Precision notation means the integer amount stores minor units, so `10000` means PHP 100.00.

## Resource Selection

- Use merchants for legal-entity level onboarding and updates.
- Use accounts for balances, postings, and account-to-account transfers.
- Use funding methods for reusable receiving instruments.
- Use payment intents for one-time collection flows tied to a payment instrument lifecycle.
- Use payout requests to initiate disbursements. A payout request can fan out into multiple payouts when rail limits require splitting.
- Use payouts to inspect the individual disbursement records created from a payout request.
- Use webhooks to register event delivery endpoints and manage `active` or `inactive` status.
- Use payment simulation only in test environments to exercise the real payment-processing and webhook paths without live provider traffic.

## Integration Notes

- Prefer idempotency keys on create endpoints that expose `X-Idempotency-Key`. Idempotency means a retry can avoid creating duplicate side effects.
- Do not promise a payment-intent expiry webhook. The spec says expiry is represented by `expires_at`, so fetch the resource if confirmation is needed.
- When event timing matters, read `references/integration/webhooks.md`. `v2.payment_instrument.payment_received` is the earliest positive payment signal, `v2.payment_instrument.payment_settled` is the stronger settlement signal, and `v2.payment_intent.succeeded` is the one-time business completion event.
- Expect mixed error payloads. Rate limits often use Problem Details fields such as `type`, `title`, `status`, `detail`, and `code`, while some validation or not-found responses use simpler `error` and `code` fields.
- Read the live OpenAPI event enum before hard-coding handlers, because the allowed values include both older event names and v2-specific event names.
- Use sandbox payment simulation to test success, failure, and idempotent replay behavior. The simulation response can return `payment_processed`, `payment_failed`, or `already_processed`.

## Quick Start

```bash
curl -u "$NEXTPAY_CLIENT_ID:$NEXTPAY_CLIENT_SECRET" \
  https://api.partners.nextpay.world/v2/merchants
```

## References

- Read `references/README.md` first for routing and domain differences.
- Read `references/core/`, `references/money-in/`, `references/money-out/`, `references/integration/`, or `references/sandbox/` for topic-specific guidance.
- Read `references/integration/webhooks.md` when webhook event meaning or timing matters.
- Read `https://api.partners.nextpay.world/v2/openapi` for the live current contract.
