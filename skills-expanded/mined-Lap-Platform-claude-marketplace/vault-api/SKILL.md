---
name: vault-api
description: "Vault API skill. Use when working with Vault for vault. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# Vault API
API version: 10.24.0

## Auth
ApiKey Authorization in header | ApiKey x-apideck-app-id in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /vault/consumers -- verify access
3. POST /vault/consumers -- create first consumers

## Endpoints

33 endpoints across 1 groups. See references/api-spec.lap for full details.

### vault
| Method | Path | Description |
|--------|------|-------------|
| POST | /vault/consumers | Create consumer |
| GET | /vault/consumers | Get all consumers |
| GET | /vault/consumers/{consumer_id} | Get consumer |
| PATCH | /vault/consumers/{consumer_id} | Update consumer |
| DELETE | /vault/consumers/{consumer_id} | Delete consumer |
| GET | /vault/consumers/{consumer_id}/stats | Consumer request counts |
| GET | /vault/connections | Get all connections |
| GET | /vault/connections/{unified_api}/{service_id} | Get connection |
| POST | /vault/connections/{unified_api}/{service_id} | Create connection |
| PATCH | /vault/connections/{unified_api}/{service_id} | Update connection |
| DELETE | /vault/connections/{unified_api}/{service_id} | Deletes a connection |
| POST | /vault/connections/{unified_api}/{service_id}/import | Import connection |
| POST | /vault/connections/{unified_api}/{service_id}/token | Authorize Access Token |
| POST | /vault/connections/{unified_api}/{service_id}/validate | Validate Connection State |
| GET | /vault/connections/{unified_api}/{service_id}/consent | Get consent records |
| PATCH | /vault/connections/{unified_api}/{service_id}/consent | Update consent state |
| POST | /vault/connections/{unified_api}/{service_id}/callback-state | Create Callback State |
| GET | /vault/connections/{unified_api}/{service_id}/{resource}/config | Get resource settings |
| PATCH | /vault/connections/{unified_api}/{service_id}/{resource}/config | Update settings |
| GET | /vault/connections/{unified_api}/{service_id}/{resource}/schema | Get resource schema |
| GET | /vault/connections/{unified_api}/{service_id}/{resource}/example | Get resource example |
| GET | /vault/connections/{unified_api}/{service_id}/{resource}/custom-fields | Get resource custom fields |
| GET | /vault/connections/{unified_api}/{service_id}/{resource}/custom-mappings | List connection custom mappings |
| GET | /vault/authorize/{service_id}/{application_id} | Authorize |
| GET | /vault/revoke/{service_id}/{application_id} | Revoke connection |
| GET | /vault/custom-mappings/{unified_api}/{service_id}/{target_field_id} | Get custom mapping |
| POST | /vault/custom-mappings/{unified_api}/{service_id}/{target_field_id} | Create custom mapping |
| PATCH | /vault/custom-mappings/{unified_api}/{service_id}/{target_field_id} | Update custom mapping |
| DELETE | /vault/custom-mappings/{unified_api}/{service_id}/{target_field_id} | Deletes a custom mapping |
| GET | /vault/custom-mappings/{unified_api}/{service_id} | List custom mappings |
| GET | /vault/callback | Callback |
| POST | /vault/sessions | Create Session |
| GET | /vault/logs | Get all consumer request logs |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a consumer?" -> POST /vault/consumers
- "List all consumers?" -> GET /vault/consumers
- "Get consumer details?" -> GET /vault/consumers/{consumer_id}
- "Partially update a consumer?" -> PATCH /vault/consumers/{consumer_id}
- "Delete a consumer?" -> DELETE /vault/consumers/{consumer_id}
- "List all stats?" -> GET /vault/consumers/{consumer_id}/stats
- "List all connections?" -> GET /vault/connections
- "Get connection details?" -> GET /vault/connections/{unified_api}/{service_id}
- "Partially update a connection?" -> PATCH /vault/connections/{unified_api}/{service_id}
- "Delete a connection?" -> DELETE /vault/connections/{unified_api}/{service_id}
- "Create a import?" -> POST /vault/connections/{unified_api}/{service_id}/import
- "Create a token?" -> POST /vault/connections/{unified_api}/{service_id}/token
- "Create a validate?" -> POST /vault/connections/{unified_api}/{service_id}/validate
- "List all consent?" -> GET /vault/connections/{unified_api}/{service_id}/consent
- "Create a callback-state?" -> POST /vault/connections/{unified_api}/{service_id}/callback-state
- "List all config?" -> GET /vault/connections/{unified_api}/{service_id}/{resource}/config
- "List all schema?" -> GET /vault/connections/{unified_api}/{service_id}/{resource}/schema
- "List all example?" -> GET /vault/connections/{unified_api}/{service_id}/{resource}/example
- "List all custom-fields?" -> GET /vault/connections/{unified_api}/{service_id}/{resource}/custom-fields
- "List all custom-mappings?" -> GET /vault/connections/{unified_api}/{service_id}/{resource}/custom-mappings
- "Get authorize details?" -> GET /vault/authorize/{service_id}/{application_id}
- "Get revoke details?" -> GET /vault/revoke/{service_id}/{application_id}
- "Get custom-mapping details?" -> GET /vault/custom-mappings/{unified_api}/{service_id}/{target_field_id}
- "Partially update a custom-mapping?" -> PATCH /vault/custom-mappings/{unified_api}/{service_id}/{target_field_id}
- "Delete a custom-mapping?" -> DELETE /vault/custom-mappings/{unified_api}/{service_id}/{target_field_id}
- "Get custom-mapping details?" -> GET /vault/custom-mappings/{unified_api}/{service_id}
- "List all callback?" -> GET /vault/callback
- "Create a session?" -> POST /vault/sessions
- "List all logs?" -> GET /vault/logs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
