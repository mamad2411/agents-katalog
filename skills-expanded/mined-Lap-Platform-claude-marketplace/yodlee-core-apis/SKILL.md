---
name: yodlee-core-apis
description: "Yodlee Core APIs API skill. Use when working with Yodlee Core APIs for transactions, cobrand, dataExtracts. Covers 70 endpoints."
version: 1.0.0
generator: lapsh
---

# Yodlee Core APIs
API version: 1.1.0

## Auth
Requires API key (key parameter)

## Base URL
/

## Setup
1. Include your API key via the key parameter
2. GET /transactions -- verify access
3. POST /cobrand/login -- create first login

## Endpoints

70 endpoints across 15 groups. See references/api-spec.lap for full details.

### transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transactions | Get Transactions |
| PUT | /transactions/categories/rules/{ruleId} | Update Transaction Categorization Rule |
| POST | /transactions/categories/rules/{ruleId} | Run Transaction Categorization Rule |
| DELETE | /transactions/categories/rules/{ruleId} | Delete Transaction Categorization Rule |
| GET | /transactions/count | Get Transactions Count |
| GET | /transactions/categories/txnRules | Get Transaction Categorization Rules |
| DELETE | /transactions/categories/{categoryId} | Delete Category |
| GET | /transactions/categories | Get Transaction Category List |
| PUT | /transactions/categories | Update Category |
| POST | /transactions/categories | Create Category |
| GET | /transactions/categories/rules | Get Transaction Categorization Rules |
| POST | /transactions/categories/rules | Create or Run Transaction Categorization Rule |
| PUT | /transactions/{transactionId} | Update Transaction |

### cobrand
| Method | Path | Description |
|--------|------|-------------|
| POST | /cobrand/login | Cobrand Login |
| PUT | /cobrand/config/notifications/events/{eventName} | Update Subscription |
| POST | /cobrand/config/notifications/events/{eventName} | Subscribe Event |
| DELETE | /cobrand/config/notifications/events/{eventName} | Delete Subscription |
| POST | /cobrand/logout | Cobrand Logout |
| GET | /cobrand/config/notifications/events | Get Subscribed Events |
| GET | /cobrand/publicKey | Get Public Key |

### dataExtracts
| Method | Path | Description |
|--------|------|-------------|
| GET | /dataExtracts/userData | Get userData |
| GET | /dataExtracts/events | Get Events |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers | Get Providers |
| GET | /providers/{providerId} | Get Provider Details |
| GET | /providers/count | Get Providers Count |

### configs
| Method | Path | Description |
|--------|------|-------------|
| GET | /configs/notifications/events | Get Subscribed Notification Events |
| GET | /configs/publicKey | Get Public Key |
| PUT | /configs/notifications/events/{eventName} | Update Notification Subscription |
| POST | /configs/notifications/events/{eventName} | Subscribe For Notification Event |
| DELETE | /configs/notifications/events/{eventName} | Delete Notification Subscription |

### derived
| Method | Path | Description |
|--------|------|-------------|
| GET | /derived/networth | Get Networth Summary |
| GET | /derived/transactionSummary | Get Transaction Summary |
| GET | /derived/holdingSummary | Get Holding Summary |

### user
| Method | Path | Description |
|--------|------|-------------|
| POST | /user/samlLogin | Saml Login |
| GET | /user/accessTokens | Get Access Tokens |
| GET | /user | Get User Details |
| PUT | /user | Update User Details |
| DELETE | /user/unregister | Delete User |
| POST | /user/register | Register User |
| POST | /user/logout | User Logout |

### documents
| Method | Path | Description |
|--------|------|-------------|
| GET | /documents/{documentId} | Download a Document |
| DELETE | /documents/{documentId} | Delete Document |
| GET | /documents | Get Documents |

### providerAccounts
| Method | Path | Description |
|--------|------|-------------|
| PUT | /providerAccounts/{providerAccountId}/preferences | Update Preferences |
| GET | /providerAccounts/{providerAccountId} | Get Provider Account Details |
| DELETE | /providerAccounts/{providerAccountId} | Delete Provider Account |
| GET | /providerAccounts | Get Provider Accounts |
| PUT | /providerAccounts | Update Account |
| GET | /providerAccounts/profile | Get User Profile Details |

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/token | Generate Access Token |
| DELETE | /auth/token | Delete Token |
| DELETE | /auth/apiKey/{key} | Delete API Key |
| GET | /auth/apiKey | Get API Keys |
| POST | /auth/apiKey | Generate API Key |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | Get Accounts |
| POST | /accounts | Add Manual Account |
| POST | /accounts/evaluateAddress | Evaluate Address |
| GET | /accounts/{accountId} | Get Account Details |
| PUT | /accounts/{accountId} | Update Account |
| DELETE | /accounts/{accountId} | Delete Account |
| GET | /accounts/historicalBalances | Get Historical Balances |

### holdings
| Method | Path | Description |
|--------|------|-------------|
| GET | /holdings/assetClassificationList | Get Asset Classification List |
| GET | /holdings/securities | Get Security Details |
| GET | /holdings | Get Holdings |
| GET | /holdings/holdingTypeList | Get Holding Type List |

### verifyAccount
| Method | Path | Description |
|--------|------|-------------|
| POST | /verifyAccount/{providerAccountId} | Verify Accounts Using Transactions |

### verification
| Method | Path | Description |
|--------|------|-------------|
| GET | /verification | Get Verification Status |
| PUT | /verification | Verify Challenge Deposit |
| POST | /verification | Initiaite Matching Service and Challenge Deposit |

### statements
| Method | Path | Description |
|--------|------|-------------|
| GET | /statements | Get Statements |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all transactions?" -> GET /transactions
- "Create a login?" -> POST /cobrand/login
- "List all userData?" -> GET /dataExtracts/userData
- "List all providers?" -> GET /providers
- "Get provider details?" -> GET /providers/{providerId}
- "Update a event?" -> PUT /cobrand/config/notifications/events/{eventName}
- "Delete a event?" -> DELETE /cobrand/config/notifications/events/{eventName}
- "List all events?" -> GET /configs/notifications/events
- "List all count?" -> GET /providers/count
- "List all networth?" -> GET /derived/networth
- "Create a samlLogin?" -> POST /user/samlLogin
- "Update a rule?" -> PUT /transactions/categories/rules/{ruleId}
- "Delete a rule?" -> DELETE /transactions/categories/rules/{ruleId}
- "Get document details?" -> GET /documents/{documentId}
- "Delete a document?" -> DELETE /documents/{documentId}
- "List all accessTokens?" -> GET /user/accessTokens
- "Create a logout?" -> POST /cobrand/logout
- "Create a token?" -> POST /auth/token
- "List all user?" -> GET /user
- "Get providerAccount details?" -> GET /providerAccounts/{providerAccountId}
- "Delete a providerAccount?" -> DELETE /providerAccounts/{providerAccountId}
- "List all accounts?" -> GET /accounts
- "Create a account?" -> POST /accounts
- "List all assetClassificationList?" -> GET /holdings/assetClassificationList
- "List all publicKey?" -> GET /configs/publicKey
- "Delete a apiKey?" -> DELETE /auth/apiKey/{key}
- "List all providerAccounts?" -> GET /providerAccounts
- "List all count?" -> GET /transactions/count
- "List all transactionSummary?" -> GET /derived/transactionSummary
- "List all txnRules?" -> GET /transactions/categories/txnRules
- "Delete a category?" -> DELETE /transactions/categories/{categoryId}
- "List all documents?" -> GET /documents
- "Create a evaluateAddress?" -> POST /accounts/evaluateAddress
- "Get account details?" -> GET /accounts/{accountId}
- "Update a account?" -> PUT /accounts/{accountId}
- "Delete a account?" -> DELETE /accounts/{accountId}
- "List all historicalBalances?" -> GET /accounts/historicalBalances
- "Create a register?" -> POST /user/register
- "List all profile?" -> GET /providerAccounts/profile
- "List all verification?" -> GET /verification
- "Create a verification?" -> POST /verification
- "List all securities?" -> GET /holdings/securities
- "Update a event?" -> PUT /configs/notifications/events/{eventName}
- "Delete a event?" -> DELETE /configs/notifications/events/{eventName}
- "List all holdings?" -> GET /holdings
- "List all events?" -> GET /cobrand/config/notifications/events
- "List all apiKey?" -> GET /auth/apiKey
- "Create a apiKey?" -> POST /auth/apiKey
- "List all publicKey?" -> GET /cobrand/publicKey
- "List all categories?" -> GET /transactions/categories
- "Create a category?" -> POST /transactions/categories
- "List all rules?" -> GET /transactions/categories/rules
- "Create a rule?" -> POST /transactions/categories/rules
- "List all statements?" -> GET /statements
- "List all holdingTypeList?" -> GET /holdings/holdingTypeList
- "Create a logout?" -> POST /user/logout
- "Update a transaction?" -> PUT /transactions/{transactionId}
- "List all events?" -> GET /dataExtracts/events
- "List all holdingSummary?" -> GET /derived/holdingSummary

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
