---
name: warehouse-connectors-api
description: "Warehouse Connectors API skill. Use when working with Warehouse Connectors for projects. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Warehouse Connectors API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /projects/{projectId}/warehouse-sources/imports -- verify access
3. POST /projects/{projectId}/warehouse-sources/imports/event-stream -- create first event-stream

## Endpoints

10 endpoints across 1 groups. See references/api-spec.lap for full details.

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{projectId}/warehouse-sources/imports | List all warehouse imports |
| GET | /projects/{projectId}/warehouse-sources/imports/{importId} | Get a specific warehouse import |
| PATCH | /projects/{projectId}/warehouse-sources/imports/{importId} | Update a warehouse import |
| DELETE | /projects/{projectId}/warehouse-sources/imports/{importId} | Delete a warehouse import |
| POST | /projects/{projectId}/warehouse-sources/imports/event-stream | Create an event stream import |
| POST | /projects/{projectId}/warehouse-sources/imports/people | Create a people (user profiles) import |
| POST | /projects/{projectId}/warehouse-sources/imports/groups | Create a groups import |
| POST | /projects/{projectId}/warehouse-sources/imports/lookup-table | Create a lookup table import |
| PUT | /projects/{projectId}/warehouse-sources/imports/{importId}/manual-sync | Run an import |
| GET | /projects/{projectId}/warehouse-sources/imports/{importId}/history | Get import job history |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all imports?" -> GET /projects/{projectId}/warehouse-sources/imports
- "Get import details?" -> GET /projects/{projectId}/warehouse-sources/imports/{importId}
- "Partially update a import?" -> PATCH /projects/{projectId}/warehouse-sources/imports/{importId}
- "Delete a import?" -> DELETE /projects/{projectId}/warehouse-sources/imports/{importId}
- "Create a event-stream?" -> POST /projects/{projectId}/warehouse-sources/imports/event-stream
- "Create a people?" -> POST /projects/{projectId}/warehouse-sources/imports/people
- "Create a group?" -> POST /projects/{projectId}/warehouse-sources/imports/groups
- "Create a lookup-table?" -> POST /projects/{projectId}/warehouse-sources/imports/lookup-table
- "List all history?" -> GET /projects/{projectId}/warehouse-sources/imports/{importId}/history

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
