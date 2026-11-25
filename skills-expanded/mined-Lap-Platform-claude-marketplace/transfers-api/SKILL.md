---
name: transfers-api
description: "Transfers API skill. Use when working with Transfers for grants, transactions, transfers. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# Transfers API
API version: 3

## Auth
ApiKey X-API-Key in header | Bearer basic | ApiKey clientKey in query

## Base URL
https://balanceplatform-api-test.adyen.com/btl/v3

## Setup
1. Set Authorization header with your Bearer token
2. GET /grants -- verify access
3. POST /grants -- create first grants

## Endpoints

9 endpoints across 3 groups. See references/api-spec.lap for full details.

### grants
| Method | Path | Description |
|--------|------|-------------|
| GET | /grants | Get a capital account |
| POST | /grants | Request a grant payout |
| GET | /grants/{id} | Get grant reference details |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transactions | Get all transactions |
| GET | /transactions/{id} | Get a transaction |

### transfers
| Method | Path | Description |
|--------|------|-------------|
| POST | /transfers | Transfer funds |
| POST | /transfers/approve | Approve initiated transfers |
| POST | /transfers/cancel | Cancel initiated transfers |
| POST | /transfers/{transferId}/returns | Return a transfer |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all grants?" -> GET /grants
- "Create a grant?" -> POST /grants
- "Get grant details?" -> GET /grants/{id}
- "List all transactions?" -> GET /transactions
- "Get transaction details?" -> GET /transactions/{id}
- "Create a transfer?" -> POST /transfers
- "Create a approve?" -> POST /transfers/approve
- "Create a cancel?" -> POST /transfers/cancel
- "Create a return?" -> POST /transfers/{transferId}/returns
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
