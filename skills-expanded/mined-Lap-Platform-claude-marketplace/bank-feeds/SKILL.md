---
name: bank-feeds
description: "Bank Feeds API skill. Use when working with Bank Feeds for companies. Covers 32 endpoints."
version: 1.0.0
generator: lapsh
---

# Bank Feeds
API version: 3.0.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.codat.io

## Setup
1. Set your API key in the appropriate header
2. GET /companies -- verify access
3. POST /companies -- create first companies

## Endpoints

32 endpoints across 1 groups. See references/api-spec.lap for full details.

### companies
| Method | Path | Description |
|--------|------|-------------|
| POST | /companies | Create company |
| GET | /companies | List companies |
| GET | /companies/{companyId} | Get company |
| DELETE | /companies/{companyId} | Delete a company |
| PUT | /companies/{companyId} | Replace company |
| PATCH | /companies/{companyId} | Update company |
| GET | /companies/{companyId}/accessToken | Get company access token |
| GET | /companies/{companyId}/connections | List connections |
| POST | /companies/{companyId}/connections | Create connection |
| GET | /companies/{companyId}/connections/{connectionId} | Get connection |
| DELETE | /companies/{companyId}/connections/{connectionId} | Delete connection |
| PATCH | /companies/{companyId}/connections/{connectionId} | Unlink connection |
| GET | /companies/{companyId}/connections/{connectionId}/data/bankAccounts | List bank accounts |
| GET | /companies/{companyId}/connections/{connectionId}/options/bankAccounts | Get create/update bank account model |
| POST | /companies/{companyId}/connections/{connectionId}/push/bankAccounts | Create bank account |
| POST | /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/batch | Create source accounts |
| POST | /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts | Create single source account |
| GET | /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts | List source accounts |
| PATCH | /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/{accountId} | Update source account |
| DELETE | /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/{accountId} | Delete source account |
| POST | /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/credentials | Generate source account credentials |
| DELETE | /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/credentials | Delete all source account credentials |
| GET | /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/mapping | List bank feed accounts |
| POST | /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/mapping | Create bank feed account mapping |
| GET | /companies/{companyId}/connections/{connectionId}/bankFeeds/info | Get company information |
| POST | /companies/{companyId}/connections/{connectionId}/push/bankAccounts/{accountId}/bankTransactions | Create bank transactions |
| GET | /companies/{companyId}/connections/{connectionId}/options/bankAccounts/{accountId}/bankTransactions | Get create bank transactions model |
| GET | /companies/{companyId}/push/{pushOperationKey} | Get create operation |
| GET | /companies/{companyId}/push | List create operations |
| GET | /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/{sourceAccountId}/managedBankFeeds/syncs/{syncId} | Get sync |
| GET | /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/{sourceAccountId}/managedBankFeeds/syncs/latest | Get latest sync |
| POST | /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/{sourceAccountId}/managedBankFeeds/syncs | Run ad-hoc sync |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a company?" -> POST /companies
- "Search companies?" -> GET /companies
- "Get company details?" -> GET /companies/{companyId}
- "Delete a company?" -> DELETE /companies/{companyId}
- "Update a company?" -> PUT /companies/{companyId}
- "Partially update a company?" -> PATCH /companies/{companyId}
- "List all accessToken?" -> GET /companies/{companyId}/accessToken
- "Search connections?" -> GET /companies/{companyId}/connections
- "Create a connection?" -> POST /companies/{companyId}/connections
- "Get connection details?" -> GET /companies/{companyId}/connections/{connectionId}
- "Delete a connection?" -> DELETE /companies/{companyId}/connections/{connectionId}
- "Partially update a connection?" -> PATCH /companies/{companyId}/connections/{connectionId}
- "Search bankAccounts?" -> GET /companies/{companyId}/connections/{connectionId}/data/bankAccounts
- "List all bankAccounts?" -> GET /companies/{companyId}/connections/{connectionId}/options/bankAccounts
- "Create a bankAccount?" -> POST /companies/{companyId}/connections/{connectionId}/push/bankAccounts
- "Create a batch?" -> POST /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/batch
- "Create a bankFeedAccount?" -> POST /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts
- "List all bankFeedAccounts?" -> GET /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts
- "Partially update a bankFeedAccount?" -> PATCH /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/{accountId}
- "Delete a bankFeedAccount?" -> DELETE /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/{accountId}
- "Create a credential?" -> POST /companies/{companyId}/connections/{connectionId}/connectionInfo/bankFeedAccounts/credentials
- "List all mapping?" -> GET /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/mapping
- "Create a mapping?" -> POST /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/mapping
- "List all info?" -> GET /companies/{companyId}/connections/{connectionId}/bankFeeds/info
- "Create a bankTransaction?" -> POST /companies/{companyId}/connections/{connectionId}/push/bankAccounts/{accountId}/bankTransactions
- "List all bankTransactions?" -> GET /companies/{companyId}/connections/{connectionId}/options/bankAccounts/{accountId}/bankTransactions
- "Get push details?" -> GET /companies/{companyId}/push/{pushOperationKey}
- "Search push?" -> GET /companies/{companyId}/push
- "Get sync details?" -> GET /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/{sourceAccountId}/managedBankFeeds/syncs/{syncId}
- "List all latest?" -> GET /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/{sourceAccountId}/managedBankFeeds/syncs/latest
- "Create a sync?" -> POST /companies/{companyId}/connections/{connectionId}/bankFeedAccounts/{sourceAccountId}/managedBankFeeds/syncs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
