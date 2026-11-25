---
name: nowpayments-api
description: "NOWPayments API skill. Use when working with NOWPayments for {{api-host}}, {{api-host}}o. Covers 35 endpoints."
version: 1.0.0
generator: lapsh
---

# NOWPayments API

## Auth
ApiKey x-api-key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /{{api-host}}/v1/subscriptions/plans/{plan}-id -- verify access
3. POST /{{api-host}}/v1/subscriptions/plans -- create first plans

## Endpoints

35 endpoints across 2 groups. See references/api-spec.lap for full details.

### {{api-host}}
| Method | Path | Description |
|--------|------|-------------|
| POST | /{{api-host}}/v1/subscriptions/plans | Create plan |
| PATCH | /{{api-host}}/v1/subscriptions/plans/{plan}-id | Update plan |
| GET | /{{api-host}}/v1/subscriptions/plans/{plan}-id | Get one plan |
| GET | /{{api-host}}/v1/subscriptions/plans | Get many plans |
| POST | /{{api-host}}/v1/subscriptions | Create an email subscription |
| GET | /{{api-host}}/v1/subscriptions | Get many recurring payments |
| GET | /{{api-host}}/v1/subscriptions/{sub_id} | Get one recurring payment |
| DELETE | /{{api-host}}/v1/subscriptions/{sub_id} | Delete recurring payment |
| POST | /{{api-host}}/v1/sub-partner/balance | Create new sub-partner |
| POST | /{{api-host}}/v1/subscriptions | Create sub-partner recurring payments |
| GET | /{{api-host}}/v1/sub-partner/balance/{id} | Get sub-partner balance |
| GET | /{{api-host}}/v1/sub-partner/transfers | Get all transfers |
| GET | /{{api-host}}/v1/sub-partner/transfer/{id} | Get transfer |
| POST | /{{api-host}}/v1/sub-partner/transfer | Transfer |
| POST | /{{api-host}}/v1/sub-partner/payment | Deposit with payment |
| POST | /{{api-host}}/v1/sub-partner/deposit | Deposit from master account |
| POST | /{{api-host}}/v1/sub-partner/write-off | Write off on master account |
| GET | /{{api-host}}/v1/estimate | Get estimated price |
| POST | /{{api-host}}/v1/payment | Create payment |
| POST | /{{api-host}}/v1/invoice-payment | Create payment by invoice |
| POST | /{{api-host}}/v1/payment/{id}/update-merchant-estimate | Get/Update payment estimate |
| GET | /{{api-host}}/v1/payment/{payment_id} | Get payment status |
| GET | /{{api-host}}/v1/min-amount | Get the minimum payment amount |
| GET | /{{api-host}}/v1/payment/ | Get list of payments |
| POST | /{{api-host}}/v1/invoice | Create invoice |
| GET | /{{api-host}}/v1/currencies | Get available currencies |
| GET | /{{api-host}}/v1/full-currencies | Get available currencies (2nd method) |
| GET | /{{api-host}}/v1/merchant/coins | Get available checked currencies |
| POST | /{{api-host}}/v1/payout | Create payout |
| GET | /{{api-host}}/v1/payout/<payout_id> | Get payout status |
| GET | /{{api-host}}/v1/balance | Get balance |
| POST | /{{api-host}}/v1/payout/{withdrawals}-id/verify | Verify payout |
| GET | /{{api-host}}/v1/status | Get API status |
| POST | /{{api-host}}/v1/auth | Authentication |

### {{api-host}}o
| Method | Path | Description |
|--------|------|-------------|
| GET | /{{api-host}}o/v1/sub-partner | Get sub-partners |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a plan?" -> POST /{{api-host}}/v1/subscriptions/plans
- "Partially update a plan?" -> PATCH /{{api-host}}/v1/subscriptions/plans/{plan}-id
- "Get plan details?" -> GET /{{api-host}}/v1/subscriptions/plans/{plan}-id
- "List all plans?" -> GET /{{api-host}}/v1/subscriptions/plans
- "Create a subscription?" -> POST /{{api-host}}/v1/subscriptions
- "List all subscriptions?" -> GET /{{api-host}}/v1/subscriptions
- "Get subscription details?" -> GET /{{api-host}}/v1/subscriptions/{sub_id}
- "Delete a subscription?" -> DELETE /{{api-host}}/v1/subscriptions/{sub_id}
- "Create a balance?" -> POST /{{api-host}}/v1/sub-partner/balance
- "Get balance details?" -> GET /{{api-host}}/v1/sub-partner/balance/{id}
- "List all sub-partner?" -> GET /{{api-host}}o/v1/sub-partner
- "List all transfers?" -> GET /{{api-host}}/v1/sub-partner/transfers
- "Get transfer details?" -> GET /{{api-host}}/v1/sub-partner/transfer/{id}
- "Create a transfer?" -> POST /{{api-host}}/v1/sub-partner/transfer
- "Create a payment?" -> POST /{{api-host}}/v1/sub-partner/payment
- "Create a deposit?" -> POST /{{api-host}}/v1/sub-partner/deposit
- "Create a write-off?" -> POST /{{api-host}}/v1/sub-partner/write-off
- "List all estimate?" -> GET /{{api-host}}/v1/estimate
- "Create a payment?" -> POST /{{api-host}}/v1/payment
- "Create a invoice-payment?" -> POST /{{api-host}}/v1/invoice-payment
- "Create a update-merchant-estimate?" -> POST /{{api-host}}/v1/payment/{id}/update-merchant-estimate
- "Get payment details?" -> GET /{{api-host}}/v1/payment/{payment_id}
- "List all min-amount?" -> GET /{{api-host}}/v1/min-amount
- "List all payment?" -> GET /{{api-host}}/v1/payment/
- "Create a invoice?" -> POST /{{api-host}}/v1/invoice
- "List all currencies?" -> GET /{{api-host}}/v1/currencies
- "List all full-currencies?" -> GET /{{api-host}}/v1/full-currencies
- "List all coins?" -> GET /{{api-host}}/v1/merchant/coins
- "Create a payout?" -> POST /{{api-host}}/v1/payout
- "List all <payout_id>?" -> GET /{{api-host}}/v1/payout/<payout_id>
- "List all balance?" -> GET /{{api-host}}/v1/balance
- "Create a verify?" -> POST /{{api-host}}/v1/payout/{withdrawals}-id/verify
- "List all status?" -> GET /{{api-host}}/v1/status
- "Create a auth?" -> POST /{{api-host}}/v1/auth
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
