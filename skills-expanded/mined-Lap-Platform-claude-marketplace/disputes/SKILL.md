---
name: disputes
description: "Disputes API skill. Use when working with Disputes for customer. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Disputes
API version: 1.11

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v1/customer/disputes -- verify access
3. POST /v1/customer/disputes/{id}/provide-evidence -- create first provide-evidence

## Endpoints

15 endpoints across 1 groups. See references/api-spec.lap for full details.

### customer
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/customer/disputes | List disputes |
| GET | /v1/customer/disputes/{id} | Show dispute details |
| PATCH | /v1/customer/disputes/{id} | Partially update dispute |
| POST | /v1/customer/disputes/{id}/provide-evidence | Provide evidence |
| POST | /v1/customer/disputes/{id}/appeal | Appeal dispute |
| POST | /v1/customer/disputes/{id}/accept-claim | Accept claim |
| POST | /v1/customer/disputes/{id}/adjudicate | Settle dispute |
| POST | /v1/customer/disputes/{id}/require-evidence | Update dispute status |
| POST | /v1/customer/disputes/{id}/escalate | Escalate dispute to claim |
| POST | /v1/customer/disputes/{id}/send-message | Send message about dispute to other party |
| POST | /v1/customer/disputes/{id}/make-offer | Make offer to resolve dispute |
| POST | /v1/customer/disputes/{id}/accept-offer | Accept offer to resolve dispute |
| POST | /v1/customer/disputes/{id}/deny-offer | Deny offer to resolve dispute |
| POST | /v1/customer/disputes/{id}/acknowledge-return-item | Acknowledge returned item |
| POST | /v1/customer/disputes/{id}/provide-supporting-info | Provide supporting information for dispute |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all disputes?" -> GET /v1/customer/disputes
- "Get dispute details?" -> GET /v1/customer/disputes/{id}
- "Partially update a dispute?" -> PATCH /v1/customer/disputes/{id}
- "Create a provide-evidence?" -> POST /v1/customer/disputes/{id}/provide-evidence
- "Create a appeal?" -> POST /v1/customer/disputes/{id}/appeal
- "Create a accept-claim?" -> POST /v1/customer/disputes/{id}/accept-claim
- "Create a adjudicate?" -> POST /v1/customer/disputes/{id}/adjudicate
- "Create a require-evidence?" -> POST /v1/customer/disputes/{id}/require-evidence
- "Create a escalate?" -> POST /v1/customer/disputes/{id}/escalate
- "Create a send-message?" -> POST /v1/customer/disputes/{id}/send-message
- "Create a make-offer?" -> POST /v1/customer/disputes/{id}/make-offer
- "Create a accept-offer?" -> POST /v1/customer/disputes/{id}/accept-offer
- "Create a deny-offer?" -> POST /v1/customer/disputes/{id}/deny-offer
- "Create a acknowledge-return-item?" -> POST /v1/customer/disputes/{id}/acknowledge-return-item
- "Create a provide-supporting-info?" -> POST /v1/customer/disputes/{id}/provide-supporting-info
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
