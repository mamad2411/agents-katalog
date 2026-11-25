---
name: payments
description: "Payments API skill. Use when working with Payments for payments. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Payments
API version: 2.8

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v2/payments/authorizations/{authorization_id} -- verify access
3. POST /v2/payments/authorizations/{authorization_id}/capture -- create first capture

## Endpoints

7 endpoints across 1 groups. See references/api-spec.lap for full details.

### payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/payments/authorizations/{authorization_id} | Show details for authorized payment |
| POST | /v2/payments/authorizations/{authorization_id}/capture | Capture authorized payment |
| POST | /v2/payments/authorizations/{authorization_id}/reauthorize | Reauthorize authorized payment |
| POST | /v2/payments/authorizations/{authorization_id}/void | Void authorized payment |
| GET | /v2/payments/captures/{capture_id} | Show captured payment details |
| POST | /v2/payments/captures/{capture_id}/refund | Refund captured payment |
| GET | /v2/payments/refunds/{refund_id} | Show refund details |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get authorization details?" -> GET /v2/payments/authorizations/{authorization_id}
- "Create a capture?" -> POST /v2/payments/authorizations/{authorization_id}/capture
- "Create a reauthorize?" -> POST /v2/payments/authorizations/{authorization_id}/reauthorize
- "Create a void?" -> POST /v2/payments/authorizations/{authorization_id}/void
- "Get capture details?" -> GET /v2/payments/captures/{capture_id}
- "Create a refund?" -> POST /v2/payments/captures/{capture_id}/refund
- "Get refund details?" -> GET /v2/payments/refunds/{refund_id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
