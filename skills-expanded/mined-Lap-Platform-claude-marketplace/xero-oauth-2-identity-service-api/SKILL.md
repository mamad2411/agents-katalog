---
name: xero-oauth-2-identity-service-api
description: "Xero OAuth 2 Identity Service API skill. Use when working with Xero OAuth 2 Identity Service for Connections. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Xero OAuth 2 Identity Service API
API version: 11.1.0

## Auth
Bearer basic | OAuth2

## Base URL
https://api.xero.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /Connections -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### Connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /Connections | Retrieves the connections for this user |
| DELETE | /Connections/{id} | Deletes a connection for this user (i.e. disconnect a tenant) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Connections?" -> GET /Connections
- "Delete a Connection?" -> DELETE /Connections/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
