---
name: govuk-pay-api
description: "GOV.UK Pay API skill. Use when working with GOV.UK Pay for payments, refunds. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# GOV.UK Pay API
API version: 1.0.3

## Auth
ApiKey Authorization in header

## Base URL
https://publicapi.payments.service.gov.uk

## Setup
1. Set your API key in the appropriate header
2. GET /v1/payments -- verify access
3. POST /v1/payments -- create first payments

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/payments | Search payments |
| POST | /v1/payments | Create new payment |
| GET | /v1/payments/{paymentId} | Find payment by ID |
| POST | /v1/payments/{paymentId}/cancel | Cancel payment |
| POST | /v1/payments/{paymentId}/capture | Capture payment |
| GET | /v1/payments/{paymentId}/events | Return payment events by ID |
| GET | /v1/payments/{paymentId}/refunds | Get all refunds for a payment |
| POST | /v1/payments/{paymentId}/refunds | Submit a refund for a payment |
| GET | /v1/payments/{paymentId}/refunds/{refundId} | Find payment refund by ID |

### refunds
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/refunds | Search refunds |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all payments?" -> GET /v1/payments
- "Create a payment?" -> POST /v1/payments
- "Get payment details?" -> GET /v1/payments/{paymentId}
- "Create a cancel?" -> POST /v1/payments/{paymentId}/cancel
- "Create a capture?" -> POST /v1/payments/{paymentId}/capture
- "List all events?" -> GET /v1/payments/{paymentId}/events
- "List all refunds?" -> GET /v1/payments/{paymentId}/refunds
- "Create a refund?" -> POST /v1/payments/{paymentId}/refunds
- "Get refund details?" -> GET /v1/payments/{paymentId}/refunds/{refundId}
- "List all refunds?" -> GET /v1/refunds
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
