---
name: payouts
description: "Payouts API skill. Use when working with Payouts for payments. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Payouts
API version: 1.9

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v1/payments/payouts/{id} -- verify access
3. POST /v1/payments/payouts -- create first payouts

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### payments
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/payments/payouts | Create batch payout |
| GET | /v1/payments/payouts/{id} | Show payout batch details |
| GET | /v1/payments/payouts-item/{payout_item_id} | Show payout item details |
| POST | /v1/payments/payouts-item/{payout_item_id}/cancel | Cancel unclaimed payout item |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a payout?" -> POST /v1/payments/payouts
- "Get payout details?" -> GET /v1/payments/payouts/{id}
- "Get payouts-item details?" -> GET /v1/payments/payouts-item/{payout_item_id}
- "Create a cancel?" -> POST /v1/payments/payouts-item/{payout_item_id}/cancel
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
