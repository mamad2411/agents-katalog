---
name: banking-api
description: "Banking API skill. Use when working with Banking for companies. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Banking API
API version: 3.0.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.codat.io

## Setup
1. Set your API key in the appropriate header
2. GET /companies/{companyId}/connections/{connectionId}/data/banking-accountBalances -- verify access

## Endpoints

8 endpoints across 1 groups. See references/api-spec.lap for full details.

### companies
| Method | Path | Description |
|--------|------|-------------|
| GET | /companies/{companyId}/connections/{connectionId}/data/banking-accountBalances | List account balances |
| GET | /companies/{companyId}/connections/{connectionId}/data/banking-accounts | List accounts |
| GET | /companies/{companyId}/connections/{connectionId}/data/banking-accounts/{accountId} | Get account |
| GET | /companies/{companyId}/connections/{connectionId}/data/banking-transactionCategories | List transaction categories |
| GET | /companies/{companyId}/connections/{connectionId}/data/banking-transactionCategories/{transactionCategoryId} | Get transaction category |
| GET | /companies/{companyId}/connections/{connectionId}/data/banking-transactions | List transactions |
| GET | /companies/{companyId}/data/banking-transactions | List banking transactions |
| GET | /companies/{companyId}/connections/{connectionId}/data/banking-transactions/{transactionId} | Get bank transaction |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search banking-accountBalances?" -> GET /companies/{companyId}/connections/{connectionId}/data/banking-accountBalances
- "Search banking-accounts?" -> GET /companies/{companyId}/connections/{connectionId}/data/banking-accounts
- "Get banking-account details?" -> GET /companies/{companyId}/connections/{connectionId}/data/banking-accounts/{accountId}
- "Search banking-transactionCategories?" -> GET /companies/{companyId}/connections/{connectionId}/data/banking-transactionCategories
- "Get banking-transactionCategory details?" -> GET /companies/{companyId}/connections/{connectionId}/data/banking-transactionCategories/{transactionCategoryId}
- "Search banking-transactions?" -> GET /companies/{companyId}/connections/{connectionId}/data/banking-transactions
- "Search banking-transactions?" -> GET /companies/{companyId}/data/banking-transactions
- "Get banking-transaction details?" -> GET /companies/{companyId}/connections/{connectionId}/data/banking-transactions/{transactionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
