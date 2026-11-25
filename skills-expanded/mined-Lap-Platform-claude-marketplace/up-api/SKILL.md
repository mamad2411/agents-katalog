---
name: up-api
description: "Up API skill. Use when working with Up for accounts, attachments, categories. Covers 20 endpoints."
version: 1.0.0
generator: lapsh
---

# Up API
API version: v1

## Auth
Bearer bearer

## Base URL
https://api.up.com.au/api/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /accounts -- verify access
3. POST /transactions/{transactionId}/relationships/tags -- create first tags

## Endpoints

20 endpoints across 7 groups. See references/api-spec.lap for full details.

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts | List accounts |
| GET | /accounts/{id} | Retrieve account |
| GET | /accounts/{accountId}/transactions | List transactions by account |

### attachments
| Method | Path | Description |
|--------|------|-------------|
| GET | /attachments | List attachments |
| GET | /attachments/{id} | Retrieve attachment |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories | List categories |
| GET | /categories/{id} | Retrieve category |

### transactions
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /transactions/{transactionId}/relationships/category | Categorize transaction |
| POST | /transactions/{transactionId}/relationships/tags | Add tags to transaction |
| DELETE | /transactions/{transactionId}/relationships/tags | Remove tags from transaction |
| GET | /transactions | List transactions |
| GET | /transactions/{id} | Retrieve transaction |

### util
| Method | Path | Description |
|--------|------|-------------|
| GET | /util/ping | Ping |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags | List tags |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks | List webhooks |
| POST | /webhooks | Create webhook |
| GET | /webhooks/{id} | Retrieve webhook |
| DELETE | /webhooks/{id} | Delete webhook |
| POST | /webhooks/{webhookId}/ping | Ping webhook |
| GET | /webhooks/{webhookId}/logs | List webhook logs |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all accounts?" -> GET /accounts
- "Get account details?" -> GET /accounts/{id}
- "List all attachments?" -> GET /attachments
- "Get attachment details?" -> GET /attachments/{id}
- "List all categories?" -> GET /categories
- "Get category details?" -> GET /categories/{id}
- "List all ping?" -> GET /util/ping
- "List all tags?" -> GET /tags
- "Create a tag?" -> POST /transactions/{transactionId}/relationships/tags
- "List all transactions?" -> GET /transactions
- "Get transaction details?" -> GET /transactions/{id}
- "List all transactions?" -> GET /accounts/{accountId}/transactions
- "List all webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "Get webhook details?" -> GET /webhooks/{id}
- "Delete a webhook?" -> DELETE /webhooks/{id}
- "Create a ping?" -> POST /webhooks/{webhookId}/ping
- "List all logs?" -> GET /webhooks/{webhookId}/logs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
