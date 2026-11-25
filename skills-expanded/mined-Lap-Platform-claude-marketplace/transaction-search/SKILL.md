---
name: transaction-search
description: "Transaction Search API skill. Use when working with Transaction Search for reporting. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Transaction Search
API version: 1.9

## Auth
OAuth2

## Base URL
https://api-m.sandbox.paypal.com

## Setup
1. Configure auth: OAuth2
2. GET /v1/reporting/transactions -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### reporting
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/reporting/transactions | List transactions |
| GET | /v1/reporting/balances | List all balances |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all transactions?" -> GET /v1/reporting/transactions
- "List all balances?" -> GET /v1/reporting/balances
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
