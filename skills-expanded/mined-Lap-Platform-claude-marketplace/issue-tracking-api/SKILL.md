---
name: issue-tracking-api
description: "Issue Tracking API skill. Use when working with Issue Tracking for issue-tracking. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Issue Tracking API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /issue-tracking/collections -- verify access
3. POST /issue-tracking/collections/{collection_id}/tickets -- create first tickets

## Endpoints

15 endpoints across 1 groups. See references/api-spec.lap for full details.

### issue-tracking
| Method | Path | Description |
|--------|------|-------------|
| GET | /issue-tracking/collections | List Collections |
| GET | /issue-tracking/collections/{collection_id} | Get Collection |
| GET | /issue-tracking/collections/{collection_id}/tickets | List Tickets |
| POST | /issue-tracking/collections/{collection_id}/tickets | Create Ticket |
| GET | /issue-tracking/collections/{collection_id}/tickets/{ticket_id} | Get Ticket |
| PATCH | /issue-tracking/collections/{collection_id}/tickets/{ticket_id} | Update Ticket |
| DELETE | /issue-tracking/collections/{collection_id}/tickets/{ticket_id} | Delete Ticket |
| GET | /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments | List Comments |
| POST | /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments | Create Comment |
| GET | /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments/{id} | Get Comment |
| PATCH | /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments/{id} | Update Comment |
| DELETE | /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments/{id} | Delete Comment |
| GET | /issue-tracking/collections/{collection_id}/users | List Users |
| GET | /issue-tracking/collections/{collection_id}/users/{id} | Get user |
| GET | /issue-tracking/collections/{collection_id}/tags | List Tags |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all collections?" -> GET /issue-tracking/collections
- "Get collection details?" -> GET /issue-tracking/collections/{collection_id}
- "List all tickets?" -> GET /issue-tracking/collections/{collection_id}/tickets
- "Create a ticket?" -> POST /issue-tracking/collections/{collection_id}/tickets
- "Get ticket details?" -> GET /issue-tracking/collections/{collection_id}/tickets/{ticket_id}
- "Partially update a ticket?" -> PATCH /issue-tracking/collections/{collection_id}/tickets/{ticket_id}
- "Delete a ticket?" -> DELETE /issue-tracking/collections/{collection_id}/tickets/{ticket_id}
- "List all comments?" -> GET /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments
- "Create a comment?" -> POST /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments
- "Get comment details?" -> GET /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments/{id}
- "Partially update a comment?" -> PATCH /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments/{id}
- "Delete a comment?" -> DELETE /issue-tracking/collections/{collection_id}/tickets/{ticket_id}/comments/{id}
- "List all users?" -> GET /issue-tracking/collections/{collection_id}/users
- "Get user details?" -> GET /issue-tracking/collections/{collection_id}/users/{id}
- "List all tags?" -> GET /issue-tracking/collections/{collection_id}/tags
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
