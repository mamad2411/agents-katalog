---
name: subscriptions
description: "Subscriptions API skill. Use when working with Subscriptions for billing. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Subscriptions
API version: 1.8

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v1/billing/plans -- verify access
3. POST /v1/billing/plans -- create first plans

## Endpoints

16 endpoints across 1 groups. See references/api-spec.lap for full details.

### billing
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/billing/plans | Create plan |
| GET | /v1/billing/plans | List plans |
| GET | /v1/billing/plans/{id} | Show plan details |
| PATCH | /v1/billing/plans/{id} | Update plan |
| POST | /v1/billing/plans/{id}/activate | Activate plan |
| POST | /v1/billing/plans/{id}/deactivate | Deactivate plan |
| POST | /v1/billing/plans/{id}/update-pricing-schemes | Update pricing |
| POST | /v1/billing/subscriptions | Create subscription |
| GET | /v1/billing/subscriptions/{id} | Show subscription details |
| PATCH | /v1/billing/subscriptions/{id} | Update subscription |
| POST | /v1/billing/subscriptions/{id}/revise | Revise plan or quantity of subscription |
| POST | /v1/billing/subscriptions/{id}/suspend | Suspend subscription |
| POST | /v1/billing/subscriptions/{id}/cancel | Cancel subscription |
| POST | /v1/billing/subscriptions/{id}/activate | Activate subscription |
| POST | /v1/billing/subscriptions/{id}/capture | Capture authorized payment on subscription |
| GET | /v1/billing/subscriptions/{id}/transactions | List transactions for subscription |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a plan?" -> POST /v1/billing/plans
- "List all plans?" -> GET /v1/billing/plans
- "Get plan details?" -> GET /v1/billing/plans/{id}
- "Partially update a plan?" -> PATCH /v1/billing/plans/{id}
- "Create a activate?" -> POST /v1/billing/plans/{id}/activate
- "Create a deactivate?" -> POST /v1/billing/plans/{id}/deactivate
- "Create a update-pricing-scheme?" -> POST /v1/billing/plans/{id}/update-pricing-schemes
- "Create a subscription?" -> POST /v1/billing/subscriptions
- "Get subscription details?" -> GET /v1/billing/subscriptions/{id}
- "Partially update a subscription?" -> PATCH /v1/billing/subscriptions/{id}
- "Create a revise?" -> POST /v1/billing/subscriptions/{id}/revise
- "Create a suspend?" -> POST /v1/billing/subscriptions/{id}/suspend
- "Create a cancel?" -> POST /v1/billing/subscriptions/{id}/cancel
- "Create a activate?" -> POST /v1/billing/subscriptions/{id}/activate
- "Create a capture?" -> POST /v1/billing/subscriptions/{id}/capture
- "List all transactions?" -> GET /v1/billing/subscriptions/{id}/transactions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
