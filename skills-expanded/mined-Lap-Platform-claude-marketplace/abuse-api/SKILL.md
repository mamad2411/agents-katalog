---
name: abuse-api
description: "Abuse API skill. Use when working with Abuse for abuse. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Abuse API
API version: 2.0.0

## Auth
No authentication required.

## Base URL
https://api.ote-godaddy.com

## Setup
1. No auth setup needed
2. GET /v1/abuse/tickets -- verify access
3. POST /v1/abuse/tickets -- create first tickets

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### abuse
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/abuse/tickets | List all abuse tickets ids that match user provided filters |
| POST | /v1/abuse/tickets | Create a new abuse ticket |
| GET | /v1/abuse/tickets/{ticketId} | Return the abuse ticket data for a given ticket id |
| GET | /v2/abuse/tickets | List all abuse tickets ids that match user provided filters |
| POST | /v2/abuse/tickets | Create a new abuse ticket |
| GET | /v2/abuse/tickets/{ticketId} | Return the abuse ticket data for a given ticket id |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all tickets?" -> GET /v1/abuse/tickets
- "Create a ticket?" -> POST /v1/abuse/tickets
- "Get ticket details?" -> GET /v1/abuse/tickets/{ticketId}
- "List all tickets?" -> GET /v2/abuse/tickets
- "Create a ticket?" -> POST /v2/abuse/tickets
- "Get ticket details?" -> GET /v2/abuse/tickets/{ticketId}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
