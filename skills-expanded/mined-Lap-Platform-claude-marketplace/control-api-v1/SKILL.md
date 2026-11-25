---
name: control-api-v1
description: "Control API v1 API skill. Use when working with Control API v1 for accounts, apps, me. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# Control API v1
API version: 1.0.32

## Auth
Bearer bearer

## Base URL
https://control.ably.net/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /me -- verify access
3. POST /accounts/{account_id}/apps -- create first apps

## Endpoints

22 endpoints across 3 groups. See references/api-spec.lap for full details.

### accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /accounts/{account_id}/apps | Lists account apps |
| POST | /accounts/{account_id}/apps | Creates an app |

### apps
| Method | Path | Description |
|--------|------|-------------|
| PATCH | /apps/{id} | Updates an app |
| DELETE | /apps/{id} | Deletes an app |
| POST | /apps/{id}/pkcs12 | Updates app's APNs info from a `.p12` file |
| GET | /apps/{app_id}/keys | Lists app keys |
| POST | /apps/{app_id}/keys | Creates a key |
| PATCH | /apps/{app_id}/keys/{key_id} | Updates a key |
| POST | /apps/{app_id}/keys/{key_id}/revoke | Revokes a key |
| GET | /apps/{app_id}/namespaces | Lists namespaces |
| POST | /apps/{app_id}/namespaces | Creates a namespace |
| PATCH | /apps/{app_id}/namespaces/{namespace_id} | Updates a namespace |
| DELETE | /apps/{app_id}/namespaces/{namespace_id} | Deletes a namespace |
| GET | /apps/{app_id}/queues | Lists queues |
| POST | /apps/{app_id}/queues | Creates a queue |
| DELETE | /apps/{app_id}/queues/{queue_id} | Deletes a queue |
| GET | /apps/{app_id}/rules | Lists rules |
| POST | /apps/{app_id}/rules | Creates a rule |
| GET | /apps/{app_id}/rules/{rule_id} | Gets a rule using a rule ID |
| PATCH | /apps/{app_id}/rules/{rule_id} | Updates a Rule |
| DELETE | /apps/{app_id}/rules/{rule_id} | Deletes a rule |

### me
| Method | Path | Description |
|--------|------|-------------|
| GET | /me | Get token details |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all apps?" -> GET /accounts/{account_id}/apps
- "Create a app?" -> POST /accounts/{account_id}/apps
- "Partially update a app?" -> PATCH /apps/{id}
- "Delete a app?" -> DELETE /apps/{id}
- "Create a pkcs12?" -> POST /apps/{id}/pkcs12
- "List all keys?" -> GET /apps/{app_id}/keys
- "Create a key?" -> POST /apps/{app_id}/keys
- "Partially update a key?" -> PATCH /apps/{app_id}/keys/{key_id}
- "Create a revoke?" -> POST /apps/{app_id}/keys/{key_id}/revoke
- "List all namespaces?" -> GET /apps/{app_id}/namespaces
- "Create a namespace?" -> POST /apps/{app_id}/namespaces
- "Partially update a namespace?" -> PATCH /apps/{app_id}/namespaces/{namespace_id}
- "Delete a namespace?" -> DELETE /apps/{app_id}/namespaces/{namespace_id}
- "List all queues?" -> GET /apps/{app_id}/queues
- "Create a queue?" -> POST /apps/{app_id}/queues
- "Delete a queue?" -> DELETE /apps/{app_id}/queues/{queue_id}
- "List all rules?" -> GET /apps/{app_id}/rules
- "Create a rule?" -> POST /apps/{app_id}/rules
- "Get rule details?" -> GET /apps/{app_id}/rules/{rule_id}
- "Partially update a rule?" -> PATCH /apps/{app_id}/rules/{rule_id}
- "Delete a rule?" -> DELETE /apps/{app_id}/rules/{rule_id}
- "List all me?" -> GET /me
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
