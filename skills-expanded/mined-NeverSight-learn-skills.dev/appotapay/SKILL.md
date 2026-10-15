---
name: appotapay
description: >-
  Router skill for integrating the AppotaPay payment gateway (Vietnamese fintech, docs.appotapay.com).
  Use when the user wants to integrate AppotaPay, accept online payments through AppotaPay, build an
  AppotaPay checkout/redirect flow, handle AppotaPay IPN / payment callbacks, build the X-APPOTAPAY-AUTH
  JWT token, sign requests, check transaction status, or issue refunds. This skill explains the overall
  flow and routes you to the correct sub-skill (appotapay-auth, appotapay-payment).
license: MIT
metadata:
  version: "0.1.0"
  source: https://docs.appotapay.com
---

# AppotaPay integration — start here

AppotaPay is a Vietnamese payment platform. Partners call REST APIs (JSON) authenticated
with a JWT in the `X-APPOTAPAY-AUTH` header. This router tells you which sub-skill to load.

## Source of truth — fetch the LIVE docs first

The bundled `references/*.md` are an **offline snapshot and may lag** the real documentation.
AppotaPay publishes always-current machine-readable docs as `llms-*.txt` files. **Before you
finalize endpoints, fields, codes, or base URLs in generated code, fetch the live doc and reconcile
— if they disagree, the live doc wins.**

- Discover everything: `https://docs.appotapay.com/llms.txt`
- One page, e.g. create-payment: `https://docs.appotapay.com/llms-v2.0-payment-payment-full.txt`
- Full guide & URL scheme: **`references/live-docs.md`** · helper: `scripts/fetch-doc.mjs`

## Decision: which sub-skill to load

| The user wants to…                                                        | Load this skill        |
|---------------------------------------------------------------------------|------------------------|
| Build/refresh the `X-APPOTAPAY-AUTH` JWT, or sign request params           | **appotapay-auth**     |
| Accept a payment, create an order/checkout, handle IPN/redirect, refund, check status | **appotapay-payment** |

Almost every flow needs **appotapay-auth** first (the JWT is required on every request),
then a product skill. For the standard "accept a payment" task, load **appotapay-auth**
and **appotapay-payment** together.

## Credentials (from the AppotaPay Partner portal)

Register at https://partner.appotapay.com and create an application to get three secrets:

- `PARTNER_CODE` — your partner identifier (JWT `iss`)
- `API_KEY` — public key (JWT `api_key`, and part of `jti`)
- `SECRET_KEY` — secret, used to **sign the JWT** and **verify IPN/redirect signatures**. Never expose it client-side.

Store these as environment variables (e.g. `APPOTAPAY_PARTNER_CODE`, `APPOTAPAY_API_KEY`,
`APPOTAPAY_SECRET_KEY`). Never hard-code or commit secrets.

## Base URLs

| Environment | Gateway base URL                      |
|-------------|---------------------------------------|
| Sandbox     | `https://gateway.dev.appotapay.com`   |
| Production  | `https://gateway.appotapay.com`       |

> The sandbox host is documented explicitly. Confirm the production host and your account's
> IP allow-list with AppotaPay before going live.

### Sandbox test credentials

```
PARTNER_CODE = APPOTAPAY
API_KEY      = FJcmF8uj2ISveL5FvvNk4pnp8xrhINz8
SECRET_KEY   = XAonJgy14YhtePEITXhyBS2unjfJLAV3
```

## Product areas (beyond v1 of this skill)

The AppotaPay platform also covers: e-wallet (OAuth2 wallet linking), subscription
(recurring billing), virtual-account (bank-transfer collection), firm-banking, bill payment,
buy-card, charging-card, mobile-topup, credit-card (auth→capture), merchant-hosted, and POS.
This skill version ships **auth** + **payment**; other areas follow the same auth + signature model.

## Golden rules

1. **JWT on every request** — see appotapay-auth.
2. **Always verify the IPN/redirect `signature`** = `HMAC_SHA256(data, SECRET_KEY)` before trusting a result.
3. **Re-check status via the API** (`GET /api/v2/orders/transaction`) before fulfilling an order — never trust the redirect alone.
4. **Amounts are integers in VND** (no decimals). `currency` must be `VND`.
5. Keep `SECRET_KEY` server-side only.
