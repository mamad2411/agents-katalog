---
name: authentication
description: "Authentication API skill. Use when working with Authentication for auth. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# Authentication
API version: 1.0

## Auth
Requires API key (client_secret parameter)

## Base URL
https://api.personio.de/v1

## Setup
1. Include your API key via the client_secret parameter
3. POST /auth -- create first auth

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /auth | Request Authentication Token |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a auth?" -> POST /auth

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
