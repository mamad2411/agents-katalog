---
name: account-and-transaction-api-specification
description: "Account and Transaction API Specification API skill. Use when working with Account and Transaction API Specification for account-access-consents, accounts, balances. Covers 29 endpoints."
version: 1.0.0
generator: lapsh
---

# Account and Transaction API Specification
API version: 4.0.0

## Auth
OAuth2 | OAuth2

## Base URL
/open-banking/v4.0/aisp

## Setup
1. Configure auth: OAuth2 | OAuth2
2. GET /accounts -- verify access
3. POST /account-access-consents -- create first account-access-consents

## Endpoints

29 endpoints across 12 groups. See references/api-spec.lap for full details.

### account-access-consents
| Method | Path | Description |
|--------|------|-------------|
| POST | /account-access-consents | Create Account Access Consents |
| GET | /account-access-consents/{ConsentId} | Get Account Access Consents |
| DELETE | /account-access-consents/{ConsentId} | Delete Account Access Consents |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | Get Accounts |
| GET | /accounts/{AccountId} | Get Accounts |
| GET | /accounts/{AccountId}/balances | Get Balances |
| GET | /accounts/{AccountId}/beneficiaries | Get Beneficiaries |
| GET | /accounts/{AccountId}/direct-debits | Get Direct Debits |
| GET | /accounts/{AccountId}/offers | Get Offers |
| GET | /accounts/{AccountId}/parties | Get Parties |
| GET | /accounts/{AccountId}/party | Get Parties |
| GET | /accounts/{AccountId}/product | Get Products |
| GET | /accounts/{AccountId}/scheduled-payments | Get Scheduled Payments |
| GET | /accounts/{AccountId}/standing-orders | Get Standing Orders |
| GET | /accounts/{AccountId}/statements | Get Statements |
| GET | /accounts/{AccountId}/statements/{StatementId} | Get Statements |
| GET | /accounts/{AccountId}/statements/{StatementId}/file | Get Statements |
| GET | /accounts/{AccountId}/statements/{StatementId}/transactions | Get Transactions |
| GET | /accounts/{AccountId}/transactions | Get Transactions |

### balances
| Method | Path | Description |
|--------|------|-------------|
| GET | /balances | Get Balances |

### beneficiaries
| Method | Path | Description |
|--------|------|-------------|
| GET | /beneficiaries | Get Beneficiaries |

### direct-debits
| Method | Path | Description |
|--------|------|-------------|
| GET | /direct-debits | Get Direct Debits |

### offers
| Method | Path | Description |
|--------|------|-------------|
| GET | /offers | Get Offers |

### party
| Method | Path | Description |
|--------|------|-------------|
| GET | /party | Get Parties |

### products
| Method | Path | Description |
|--------|------|-------------|
| GET | /products | Get Products |

### scheduled-payments
| Method | Path | Description |
|--------|------|-------------|
| GET | /scheduled-payments | Get Scheduled Payments |

### standing-orders
| Method | Path | Description |
|--------|------|-------------|
| GET | /standing-orders | Get Standing Orders |

### statements
| Method | Path | Description |
|--------|------|-------------|
| GET | /statements | Get Statements |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transactions | Get Transactions |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a account-access-consent?" -> POST /account-access-consents
- "Get account-access-consent details?" -> GET /account-access-consents/{ConsentId}
- "Delete a account-access-consent?" -> DELETE /account-access-consents/{ConsentId}
- "List all accounts?" -> GET /accounts
- "Get account details?" -> GET /accounts/{AccountId}
- "List all balances?" -> GET /accounts/{AccountId}/balances
- "List all beneficiaries?" -> GET /accounts/{AccountId}/beneficiaries
- "List all direct-debits?" -> GET /accounts/{AccountId}/direct-debits
- "List all offers?" -> GET /accounts/{AccountId}/offers
- "List all parties?" -> GET /accounts/{AccountId}/parties
- "List all party?" -> GET /accounts/{AccountId}/party
- "List all product?" -> GET /accounts/{AccountId}/product
- "List all scheduled-payments?" -> GET /accounts/{AccountId}/scheduled-payments
- "List all standing-orders?" -> GET /accounts/{AccountId}/standing-orders
- "List all statements?" -> GET /accounts/{AccountId}/statements
- "Get statement details?" -> GET /accounts/{AccountId}/statements/{StatementId}
- "List all file?" -> GET /accounts/{AccountId}/statements/{StatementId}/file
- "List all transactions?" -> GET /accounts/{AccountId}/statements/{StatementId}/transactions
- "List all transactions?" -> GET /accounts/{AccountId}/transactions
- "List all balances?" -> GET /balances
- "List all beneficiaries?" -> GET /beneficiaries
- "List all direct-debits?" -> GET /direct-debits
- "List all offers?" -> GET /offers
- "List all party?" -> GET /party
- "List all products?" -> GET /products
- "List all scheduled-payments?" -> GET /scheduled-payments
- "List all standing-orders?" -> GET /standing-orders
- "List all statements?" -> GET /statements
- "List all transactions?" -> GET /transactions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
