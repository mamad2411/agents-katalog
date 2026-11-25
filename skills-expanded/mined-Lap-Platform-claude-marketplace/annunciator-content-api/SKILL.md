---
name: annunciator-content-api
description: "Annunciator content API skill. Use when working with Annunciator content for api. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Annunciator content API
API version: v1

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /api/Message/message/{annunciator}/current -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/Message/message/{annunciator}/current | Return the current message by annunciator type |
| GET | /api/Message/message/{annunciator}/{date} | Return the most recent message by annunciator after date time specified |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all current?" -> GET /api/Message/message/{annunciator}/current
- "Get message details?" -> GET /api/Message/message/{annunciator}/{date}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
