---
name: gdpr-api
description: "GDPR API skill. Use when working with GDPR for data-retrievals, data-deletions. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# GDPR API
API version: 3.0.0

## Auth
Requires API key (token parameter)

## Base URL
Not specified.

## Setup
1. Include your API key via the token parameter
2. GET /data-retrievals/v3.0/{tracking_id} -- verify access
3. POST /data-retrievals/v3.0 -- create first v3.0

## Endpoints

5 endpoints across 2 groups. See references/api-spec.lap for full details.

### data-retrievals
| Method | Path | Description |
|--------|------|-------------|
| POST | /data-retrievals/v3.0 | Create a Retrieval |
| GET | /data-retrievals/v3.0/{tracking_id} | Check Status of Retrieval |

### data-deletions
| Method | Path | Description |
|--------|------|-------------|
| POST | /data-deletions/v3.0 | Create a Deletion |
| GET | /data-deletions/v3.0/{tracking_id} | Check Status of Deletion |
| DELETE | /data-deletions/v3.0/{tracking_id} | Cancel a Deletion |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a v3.0?" -> POST /data-retrievals/v3.0
- "Get v3.0 details?" -> GET /data-retrievals/v3.0/{tracking_id}
- "Create a v3.0?" -> POST /data-deletions/v3.0
- "Get v3.0 details?" -> GET /data-deletions/v3.0/{tracking_id}
- "Delete a v3.0?" -> DELETE /data-deletions/v3.0/{tracking_id}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
