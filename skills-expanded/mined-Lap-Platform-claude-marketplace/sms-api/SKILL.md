---
name: sms-api
description: "SMS API skill. Use when working with SMS for sms. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# SMS API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /sms/messages -- verify access
3. POST /sms/messages -- create first messages

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### sms
| Method | Path | Description |
|--------|------|-------------|
| GET | /sms/messages | List Messages |
| POST | /sms/messages | Create Message |
| GET | /sms/messages/{id} | Get Message |
| PATCH | /sms/messages/{id} | Update Message |
| DELETE | /sms/messages/{id} | Delete Message |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all messages?" -> GET /sms/messages
- "Create a message?" -> POST /sms/messages
- "Get message details?" -> GET /sms/messages/{id}
- "Partially update a message?" -> PATCH /sms/messages/{id}
- "Delete a message?" -> DELETE /sms/messages/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
