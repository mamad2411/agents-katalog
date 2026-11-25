---
name: faretrotter-travel-api
description: "Faretrotter Travel API skill. Use when working with Faretrotter Travel for places, routes. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Faretrotter Travel API
API version: 2.0

## Auth
ApiKey ApiKeyAuth in header

## Base URL
https://api.faretrotter.com/v2.0/{apikey}

## Setup
1. Set your API key in the appropriate header
2. GET /places -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### places
| Method | Path | Description |
|--------|------|-------------|
| GET | /places | Returns possible modes of transportation between two cities. |

### routes
| Method | Path | Description |
|--------|------|-------------|
| GET | /routes |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all places?" -> GET /places
- "List all routes?" -> GET /routes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
