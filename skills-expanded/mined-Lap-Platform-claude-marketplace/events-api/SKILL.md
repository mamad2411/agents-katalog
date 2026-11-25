---
name: events-api
description: "Events API skill. Use when working with Events for api. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Events API
API version: 1.2.0

## Auth
Bearer bearer

## Base URL
https://events.1password.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /api/auth/introspect -- verify access
3. POST /api/v1/signinattempts -- create first signinattempts

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/auth/introspect | Performs introspection of the provided Bearer JWT token |
| GET | /api/v2/auth/introspect | Performs introspection of the provided Bearer JWT token |
| POST | /api/v1/signinattempts | Retrieves events for both successful and failed attempts to sign into a 1Password account |
| POST | /api/v1/itemusages | Retrieves events for each usage of an item stored in a shared vault within a 1Password account |
| POST | /api/v1/auditevents | Retrieves audit events for actions performed by team members within a 1Password account |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all introspect?" -> GET /api/auth/introspect
- "List all introspect?" -> GET /api/v2/auth/introspect
- "Create a signinattempt?" -> POST /api/v1/signinattempts
- "Create a itemusage?" -> POST /api/v1/itemusages
- "Create a auditevent?" -> POST /api/v1/auditevents
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
