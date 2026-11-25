---
name: koomalooma-partner-api
description: "koomalooma Partner API skill. Use when working with koomalooma Partner for users. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# koomalooma Partner API
API version: 1.0

## Auth
ApiKey X-KoomaLooma-JWT in header

## Base URL
https://api.koomalooma.com/api

## Setup
1. Set your API key in the appropriate header
3. POST /users -- create first users

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users | Create a User |
| POST | /users/{user_id}/commitments | Assign points to a User |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a user?" -> POST /users
- "Create a commitment?" -> POST /users/{user_id}/commitments
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
