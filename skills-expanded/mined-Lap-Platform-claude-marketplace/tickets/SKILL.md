---
name: tickets
description: "Tickets API skill. Use when working with Tickets for crm. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Tickets
API version: v3

## Auth
OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/objects/tickets -- verify access
3. POST /crm/v3/objects/tickets -- create first tickets

## Endpoints

12 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/objects/tickets | List |
| POST | /crm/v3/objects/tickets | Create |
| POST | /crm/v3/objects/tickets/batch/archive | Archive a batch of tickets by ID |
| POST | /crm/v3/objects/tickets/batch/create | Create a batch of tickets |
| POST | /crm/v3/objects/tickets/batch/read | Read a batch of tickets by internal ID, or unique property values |
| POST | /crm/v3/objects/tickets/batch/update | Update a batch of tickets by internal ID, or unique property values |
| POST | /crm/v3/objects/tickets/batch/upsert | Create or update a batch of tickets by unique property values |
| POST | /crm/v3/objects/tickets/merge | Merge two tickets |
| POST | /crm/v3/objects/tickets/search | Search for tickets |
| GET | /crm/v3/objects/tickets/{ticketId} | Read |
| DELETE | /crm/v3/objects/tickets/{ticketId} | Archive |
| PATCH | /crm/v3/objects/tickets/{ticketId} | Update |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all tickets?" -> GET /crm/v3/objects/tickets
- "Create a ticket?" -> POST /crm/v3/objects/tickets
- "Create a archive?" -> POST /crm/v3/objects/tickets/batch/archive
- "Create a create?" -> POST /crm/v3/objects/tickets/batch/create
- "Create a read?" -> POST /crm/v3/objects/tickets/batch/read
- "Create a update?" -> POST /crm/v3/objects/tickets/batch/update
- "Create a upsert?" -> POST /crm/v3/objects/tickets/batch/upsert
- "Create a merge?" -> POST /crm/v3/objects/tickets/merge
- "Create a search?" -> POST /crm/v3/objects/tickets/search
- "Get ticket details?" -> GET /crm/v3/objects/tickets/{ticketId}
- "Delete a ticket?" -> DELETE /crm/v3/objects/tickets/{ticketId}
- "Partially update a ticket?" -> PATCH /crm/v3/objects/tickets/{ticketId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
