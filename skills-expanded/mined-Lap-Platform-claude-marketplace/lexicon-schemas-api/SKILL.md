---
name: lexicon-schemas-api
description: "Lexicon Schemas API skill. Use when working with Lexicon Schemas for projects. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Lexicon Schemas API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /projects/{projectId}/schemas -- verify access
3. POST /projects/{projectId}/schemas -- create first schemas

## Endpoints

8 endpoints across 1 groups. See references/api-spec.lap for full details.

### projects
| Method | Path | Description |
|--------|------|-------------|
| GET | /projects/{projectId}/schemas | List Schemas |
| POST | /projects/{projectId}/schemas | Create/Replace Multiple |
| DELETE | /projects/{projectId}/schemas | Delete all Schemas |
| GET | /projects/{projectId}/schemas/{entityType} | List for Entity |
| DELETE | /projects/{projectId}/schemas/{entityType} | Delete for Entity |
| GET | /projects/{projectId}/schemas/{entityType}/{name} | List for Entity and Name |
| DELETE | /projects/{projectId}/schemas/{entityType}/{name} | Delete for Entity and Name |
| POST | /projects/{projectId}/schemas/{entityType}/{name} | Create/Replace One |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all schemas?" -> GET /projects/{projectId}/schemas
- "Create a schema?" -> POST /projects/{projectId}/schemas
- "Get schema details?" -> GET /projects/{projectId}/schemas/{entityType}
- "Delete a schema?" -> DELETE /projects/{projectId}/schemas/{entityType}
- "Get schema details?" -> GET /projects/{projectId}/schemas/{entityType}/{name}
- "Delete a schema?" -> DELETE /projects/{projectId}/schemas/{entityType}/{name}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
