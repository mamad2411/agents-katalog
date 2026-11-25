---
name: bulksms-json-rest-api
description: "BulkSMS JSON REST API skill. Use when working with BulkSMS JSON REST for webhooks, profile, messages. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# BulkSMS JSON REST API
API version: 1.1.0

## Auth
basic

## Base URL
https://api.bulksms.com/v1

## Setup
1. Configure auth: basic
2. GET /webhooks -- verify access
3. POST /webhooks -- create first webhooks

## Endpoints

15 endpoints across 6 groups. See references/api-spec.lap for full details.

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /webhooks | Create a webhook |
| GET | /webhooks | List webhooks |
| GET | /webhooks/{id} | Read a webhook |
| POST | /webhooks/{id} | Update a webhook |
| DELETE | /webhooks/{id} | Delete a webhook |

### profile
| Method | Path | Description |
|--------|------|-------------|
| GET | /profile | Get profile |

### messages
| Method | Path | Description |
|--------|------|-------------|
| POST | /messages | Send Messages |
| GET | /messages | Retrieve Messages |
| GET | /messages/send | Send message by simple GET or POST |
| GET | /messages/{id}/relatedReceivedMessages | List Related Messages |
| GET | /messages/{id} | Show Message |

### blocked-numbers
| Method | Path | Description |
|--------|------|-------------|
| POST | /blocked-numbers | Create a blocked number |
| GET | /blocked-numbers | List blocked numbers |

### credit
| Method | Path | Description |
|--------|------|-------------|
| POST | /credit/transfer | Transfer credits to another account |

### rmm
| Method | Path | Description |
|--------|------|-------------|
| POST | /rmm/pre-sign-attachment | Upload an attachment via a signed URL |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a webhook?" -> POST /webhooks
- "List all webhooks?" -> GET /webhooks
- "Get webhook details?" -> GET /webhooks/{id}
- "Delete a webhook?" -> DELETE /webhooks/{id}
- "List all profile?" -> GET /profile
- "Create a message?" -> POST /messages
- "List all messages?" -> GET /messages
- "List all send?" -> GET /messages/send
- "List all relatedReceivedMessages?" -> GET /messages/{id}/relatedReceivedMessages
- "Get message details?" -> GET /messages/{id}
- "Create a blocked-number?" -> POST /blocked-numbers
- "List all blocked-numbers?" -> GET /blocked-numbers
- "Create a transfer?" -> POST /credit/transfer
- "Create a pre-sign-attachment?" -> POST /rmm/pre-sign-attachment
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
