---
name: d7sms
description: "D7SMS API skill. Use when working with D7SMS for balance, send, sendbatch. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# D7SMS
API version: 1.0.2

## Auth
basic

## Base URL
https://rest-api.d7networks.com/secure

## Setup
1. Configure auth: basic
2. GET /balance -- verify access
3. POST /send -- create first send

## Endpoints

3 endpoints across 3 groups. See references/api-spec.lap for full details.

### balance
| Method | Path | Description |
|--------|------|-------------|
| GET | /balance | Balance |

### send
| Method | Path | Description |
|--------|------|-------------|
| POST | /send | SendSMS |

### sendbatch
| Method | Path | Description |
|--------|------|-------------|
| POST | /sendbatch | Bulk SMS |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all balance?" -> GET /balance
- "Create a send?" -> POST /send
- "Create a sendbatch?" -> POST /sendbatch
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
