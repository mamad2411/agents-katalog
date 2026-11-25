---
name: winsms
description: "WINSMS API skill. Use when working with WINSMS for credits, sms, shortcode. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# WINSMS
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://api.winsms.co.za/api/rest/v1

## Setup
1. No auth setup needed
2. GET /credits/balance -- verify access
3. POST /credits/transfer -- create first transfer

## Endpoints

11 endpoints across 4 groups. See references/api-spec.lap for full details.

### credits
| Method | Path | Description |
|--------|------|-------------|
| GET | /credits/balance | Get your current WinSMS credit balance |
| POST | /credits/transfer | Transfer credits between main and sub accounts. |

### sms
| Method | Path | Description |
|--------|------|-------------|
| POST | /sms/outgoing/send | Send SMS messages |
| POST | /sms/outgoing/sendmulti | Send multiple different SMS messages |
| POST | /sms/outgoing/status | Get SMS delivery statuses |
| GET | /sms/scheduled | Get a list of scheduled SMS messages |
| POST | /sms/scheduled/delete | Delete scheduled SMS messages and refund credits |
| GET | /sms/incoming | Get a list of incoming SMS messages |
| GET | /sms/incoming/optout | Get a list of incoming opt-out SMS messages |

### shortcode
| Method | Path | Description |
|--------|------|-------------|
| GET | /shortcode/incoming | Get a list of incoming short/long code messages |

### subaccounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /subaccounts | Get a list of all Sub Accounts. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all balance?" -> GET /credits/balance
- "Create a transfer?" -> POST /credits/transfer
- "Create a send?" -> POST /sms/outgoing/send
- "Create a sendmulti?" -> POST /sms/outgoing/sendmulti
- "Create a status?" -> POST /sms/outgoing/status
- "List all scheduled?" -> GET /sms/scheduled
- "Create a delete?" -> POST /sms/scheduled/delete
- "List all incoming?" -> GET /sms/incoming
- "List all optout?" -> GET /sms/incoming/optout
- "List all incoming?" -> GET /shortcode/incoming
- "List all subaccounts?" -> GET /subaccounts

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
