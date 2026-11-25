---
name: background-removal-api
description: "Background Removal API skill. Use when working with Background Removal for removebg, improve, account. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Background Removal API
API version: 1.0.0

## Auth
ApiKey X-API-Key in header

## Base URL
https://api.remove.bg/v1.0

## Setup
1. Set your API key in the appropriate header
2. GET /account -- verify access
3. POST /removebg -- create first removebg

## Endpoints

3 endpoints across 3 groups. See references/api-spec.lap for full details.

### removebg
| Method | Path | Description |
|--------|------|-------------|
| POST | /removebg | Remove the background of an image |

### improve
| Method | Path | Description |
|--------|------|-------------|
| POST | /improve | Submit an image to the remove.bg Improvement program |

### account
| Method | Path | Description |
|--------|------|-------------|
| GET | /account | Fetch credit balance and free API calls. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a removebg?" -> POST /removebg
- "Create a improve?" -> POST /improve
- "List all account?" -> GET /account
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object
- Error responses use types: Error

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
