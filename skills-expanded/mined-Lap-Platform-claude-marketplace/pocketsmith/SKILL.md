---
name: pocketsmith
description: "PocketSmith API skill. Use when working with PocketSmith for me, users, institutions. Covers 56 endpoints."
version: 1.0.0
generator: lapsh
---

# PocketSmith
API version: 2.0

## Auth
ApiKey X-Developer-Key in header | OAuth2

## Base URL
https://api.pocketsmith.com/v2

## Setup
1. Set your API key in the appropriate header
2. GET /me -- verify access
3. POST /users/{id}/institutions -- create first institutions

## Endpoints

56 endpoints across 12 groups. See references/api-spec.lap for full details.

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | Get the authorised user |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{id} | Get user |
| PUT | /users/{id} | Update user |
| GET | /users/{id}/institutions | List institutions in user |
| POST | /users/{id}/institutions | Create institution in user |
| GET | /users/{id}/accounts | List accounts in user |
| PUT | /users/{id}/accounts | Update the display order of accounts in user |
| POST | /users/{id}/accounts | Create an account in user |
| GET | /users/{id}/transaction_accounts | List transaction accounts in user |
| GET | /users/{id}/transactions | List transactions in user |
| GET | /users/{id}/categories | List categories in user |
| POST | /users/{id}/categories | Create category in user |
| GET | /users/{id}/category_rules | List category rules in user |
| GET | /users/{id}/budget | List budget for user |
| GET | /users/{id}/budget_summary | Get budget summary for user |
| GET | /users/{id}/trend_analysis | Get trend analysis for user |
| DELETE | /users/{id}/forecast_cache | Delete forecast cache for user |
| GET | /users/{id}/events | List events in user. |
| GET | /users/{id}/attachments | Lists attachments in user |
| POST | /users/{id}/attachments | Create attachment in user |
| GET | /users/{id}/labels | List labels in user |
| GET | /users/{id}/saved_searches | List saved searches in user |

### institutions
| Method | Path | Description |
|--------|------|-------------|
| GET | /institutions/{id} | Get institution |
| PUT | /institutions/{id} | Update institution |
| DELETE | /institutions/{id} | Delete institution |
| GET | /institutions/{id}/accounts | List accounts in institution |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts/{id} | Get account |
| PUT | /accounts/{id} | Update account |
| DELETE | /accounts/{id} | Delete account |
| GET | /accounts/{id}/transactions | List transactions in account |

### transaction_accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /transaction_accounts/{id} | Get transaction account |
| PUT | /transaction_accounts/{id} | Update transaction account |
| GET | /transaction_accounts/{id}/transactions | List transactions in transaction account |
| POST | /transaction_accounts/{id}/transactions | Create a transaction in transaction account |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| GET | /transactions/{id} | Get a transaction |
| PUT | /transactions/{id} | Update a transaction |
| DELETE | /transactions/{id} | Delete transaction |
| GET | /transactions/{id}/attachments | List attachments in transaction |
| POST | /transactions/{id}/attachments | Assigns attachment to transaction |
| DELETE | /transactions/{transaction_id}/attachments/{attachment_id} | Unassigns attachment in transaction |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories/{id}/transactions | List transactions in categories |
| GET | /categories/{id} | Get category |
| PUT | /categories/{id} | Update category |
| DELETE | /categories/{id} | Delete category |
| POST | /categories/{id}/category_rules | Create category rule in category |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events/{id} | Get event |
| PUT | /events/{id} | Update event |
| DELETE | /events/{id} | Delete event |

### scenarios
| Method | Path | Description |
|--------|------|-------------|
| GET | /scenarios/{id}/events | List events in scenario. |
| POST | /scenarios/{id}/events | Create event in scenario |

### attachments
| Method | Path | Description |
|--------|------|-------------|
| GET | /attachments/{id} | Get attachment |
| PUT | /attachments/{id} | Update attachment |
| DELETE | /attachments/{id} | Delete attachment |

### currencies
| Method | Path | Description |
|--------|------|-------------|
| GET | /currencies | List currencies |
| GET | /currencies/{id} | Get currency |

### time_zones
| Method | Path | Description |
|--------|------|-------------|
| GET | /time_zones | List time zones |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all me?" -> GET /me
- "Get user details?" -> GET /users/{id}
- "Update a user?" -> PUT /users/{id}
- "Get institution details?" -> GET /institutions/{id}
- "Update a institution?" -> PUT /institutions/{id}
- "Delete a institution?" -> DELETE /institutions/{id}
- "List all institutions?" -> GET /users/{id}/institutions
- "Create a institution?" -> POST /users/{id}/institutions
- "Get account details?" -> GET /accounts/{id}
- "Update a account?" -> PUT /accounts/{id}
- "Delete a account?" -> DELETE /accounts/{id}
- "List all accounts?" -> GET /users/{id}/accounts
- "Create a account?" -> POST /users/{id}/accounts
- "List all accounts?" -> GET /institutions/{id}/accounts
- "Get transaction_account details?" -> GET /transaction_accounts/{id}
- "Update a transaction_account?" -> PUT /transaction_accounts/{id}
- "List all transaction_accounts?" -> GET /users/{id}/transaction_accounts
- "Get transaction details?" -> GET /transactions/{id}
- "Update a transaction?" -> PUT /transactions/{id}
- "Delete a transaction?" -> DELETE /transactions/{id}
- "Search transactions?" -> GET /users/{id}/transactions
- "Search transactions?" -> GET /accounts/{id}/transactions
- "Search transactions?" -> GET /categories/{id}/transactions
- "Search transactions?" -> GET /transaction_accounts/{id}/transactions
- "Create a transaction?" -> POST /transaction_accounts/{id}/transactions
- "Get category details?" -> GET /categories/{id}
- "Update a category?" -> PUT /categories/{id}
- "Delete a category?" -> DELETE /categories/{id}
- "List all categories?" -> GET /users/{id}/categories
- "Create a category?" -> POST /users/{id}/categories
- "List all category_rules?" -> GET /users/{id}/category_rules
- "Create a category_rule?" -> POST /categories/{id}/category_rules
- "List all budget?" -> GET /users/{id}/budget
- "List all budget_summary?" -> GET /users/{id}/budget_summary
- "List all trend_analysis?" -> GET /users/{id}/trend_analysis
- "Get event details?" -> GET /events/{id}
- "Update a event?" -> PUT /events/{id}
- "Delete a event?" -> DELETE /events/{id}
- "List all events?" -> GET /users/{id}/events
- "List all events?" -> GET /scenarios/{id}/events
- "Create a event?" -> POST /scenarios/{id}/events
- "Get attachment details?" -> GET /attachments/{id}
- "Update a attachment?" -> PUT /attachments/{id}
- "Delete a attachment?" -> DELETE /attachments/{id}
- "List all attachments?" -> GET /users/{id}/attachments
- "Create a attachment?" -> POST /users/{id}/attachments
- "List all attachments?" -> GET /transactions/{id}/attachments
- "Create a attachment?" -> POST /transactions/{id}/attachments
- "Delete a attachment?" -> DELETE /transactions/{transaction_id}/attachments/{attachment_id}
- "List all labels?" -> GET /users/{id}/labels
- "List all saved_searches?" -> GET /users/{id}/saved_searches
- "List all currencies?" -> GET /currencies
- "Get currency details?" -> GET /currencies/{id}
- "List all time_zones?" -> GET /time_zones
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
