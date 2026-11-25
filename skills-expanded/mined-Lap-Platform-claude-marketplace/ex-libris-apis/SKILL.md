---
name: ex-libris-apis
description: "Ex Libris APIs API skill. Use when working with Ex Libris APIs for almaws. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# Ex Libris APIs
API version: 1.0

## Auth
ApiKey apikey in query

## Base URL
https://api-eu.hosted.exlibrisgroup.com

## Setup
1. Set your API key in the appropriate header
2. GET /almaws/v1/task-lists/printouts -- verify access
3. POST /almaws/v1/task-lists/printouts -- create first printouts

## Endpoints

11 endpoints across 1 groups. See references/api-spec.lap for full details.

### almaws
| Method | Path | Description |
|--------|------|-------------|
| GET | /almaws/v1/task-lists/printouts | Retrieve Printouts |
| POST | /almaws/v1/task-lists/printouts | Act on Printouts |
| POST | /almaws/v1/task-lists/printouts/create | Create a Printout |
| GET | /almaws/v1/task-lists/printouts/{printout_id} | Retrieve a Printout |
| POST | /almaws/v1/task-lists/printouts/{printout_id} | Printout Service |
| GET | /almaws/v1/task-lists/requested-resources | Get Requested Resources |
| POST | /almaws/v1/task-lists/requested-resources | Act on Requested Resources |
| GET | /almaws/v1/task-lists/rs/lending-requests | Get Lending Requests |
| POST | /almaws/v1/task-lists/rs/lending-requests | Act on Lending Requests |
| GET | /almaws/v1/task-lists/test | GET Task-lists Test API |
| POST | /almaws/v1/task-lists/test | POST Task-lists Test API |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all printouts?" -> GET /almaws/v1/task-lists/printouts
- "Create a printout?" -> POST /almaws/v1/task-lists/printouts
- "Create a create?" -> POST /almaws/v1/task-lists/printouts/create
- "Get printout details?" -> GET /almaws/v1/task-lists/printouts/{printout_id}
- "List all requested-resources?" -> GET /almaws/v1/task-lists/requested-resources
- "Create a requested-resource?" -> POST /almaws/v1/task-lists/requested-resources
- "List all lending-requests?" -> GET /almaws/v1/task-lists/rs/lending-requests
- "Create a lending-request?" -> POST /almaws/v1/task-lists/rs/lending-requests
- "List all test?" -> GET /almaws/v1/task-lists/test
- "Create a test?" -> POST /almaws/v1/task-lists/test
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
