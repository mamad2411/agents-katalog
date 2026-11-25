---
name: sync-for-expenses-api
description: "Sync for Expenses API skill. Use when working with Sync for Expenses for companies. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Sync for Expenses API
API version: prealpha

## Auth
ApiKey Authorization in header

## Base URL
https://api.codat.io

## Setup
1. Set your API key in the appropriate header
2. GET /companies/{companyId}/sync/expenses/config -- verify access
3. POST /companies/{companyId}/sync/expenses/config -- create first config

## Endpoints

14 endpoints across 1 groups. See references/api-spec.lap for full details.

### companies
| Method | Path | Description |
|--------|------|-------------|
| GET | /companies/{companyId}/sync/expenses/config | Get company configuration |
| POST | /companies/{companyId}/sync/expenses/config | Set company configuration |
| POST | /companies/{companyId}/sync/expenses/connections/partnerExpense | Create Partner Expense connection |
| GET | /companies/{companyId}/sync/expenses/mappingOptions | Mapping options |
| POST | /companies/{companyId}/sync/expenses/syncs | Initiate sync |
| GET | /companies/{companyId}/sync/expenses/syncs/lastSuccessful/status | Last successful sync |
| GET | /companies/{companyId}/sync/expenses/syncs/latest/status | Latest sync status |
| GET | /companies/{companyId}/sync/expenses/syncs/list/status | List sync statuses |
| GET | /companies/{companyId}/sync/expenses/syncs/{syncId}/status | Get Sync status |
| GET | /companies/{companyId}/sync/expenses/syncs/{syncId}/transactions | Get Sync transactions |
| GET | /companies/{companyId}/sync/expenses/syncs/{syncId}/transactions/{transactionId} | Get Sync Transaction |
| POST | /companies/{companyId}/sync/expenses/data/expense-transactions | Create expense-transactions |
| PUT | /companies/{companyId}/sync/expenses/expense-transactions/{transactionId} | Update expense-transactions |
| POST | /companies/{companyId}/sync/expenses/syncs/{syncId}/transactions/{transactionId}/attachments | Upload attachment |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all config?" -> GET /companies/{companyId}/sync/expenses/config
- "Create a config?" -> POST /companies/{companyId}/sync/expenses/config
- "Create a partnerExpense?" -> POST /companies/{companyId}/sync/expenses/connections/partnerExpense
- "List all mappingOptions?" -> GET /companies/{companyId}/sync/expenses/mappingOptions
- "Create a sync?" -> POST /companies/{companyId}/sync/expenses/syncs
- "List all status?" -> GET /companies/{companyId}/sync/expenses/syncs/lastSuccessful/status
- "List all status?" -> GET /companies/{companyId}/sync/expenses/syncs/latest/status
- "List all status?" -> GET /companies/{companyId}/sync/expenses/syncs/list/status
- "List all status?" -> GET /companies/{companyId}/sync/expenses/syncs/{syncId}/status
- "List all transactions?" -> GET /companies/{companyId}/sync/expenses/syncs/{syncId}/transactions
- "Get transaction details?" -> GET /companies/{companyId}/sync/expenses/syncs/{syncId}/transactions/{transactionId}
- "Create a expense-transaction?" -> POST /companies/{companyId}/sync/expenses/data/expense-transactions
- "Update a expense-transaction?" -> PUT /companies/{companyId}/sync/expenses/expense-transactions/{transactionId}
- "Create a attachment?" -> POST /companies/{companyId}/sync/expenses/syncs/{syncId}/transactions/{transactionId}/attachments
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
