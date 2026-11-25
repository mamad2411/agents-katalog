---
name: the-mercure-protocol
description: "The Mercure protocol API skill. Use when working with The Mercure protocol for .well-known. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# The Mercure protocol
API version: 0.3.2

## Auth
Bearer bearer | ApiKey mercureAuthorization in cookie

## Base URL
Not specified.

## Setup
1. Set Authorization header with your Bearer token
2. GET /.well-known/mercure -- verify access
3. POST /.well-known/mercure -- create first mercure

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### .well-known
| Method | Path | Description |
|--------|------|-------------|
| GET | /.well-known/mercure | Subscribe to updates |
| POST | /.well-known/mercure | Publish an update |
| GET | /.well-known/mercure/subscriptions | Active subscriptions |
| GET | /.well-known/mercure/subscriptions/{topic} | Active subscriptions for the given topic |
| GET | /.well-known/mercure/subscriptions/{topic}/{subscriber} | Active subscription for the given topic and subscriber |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all mercure?" -> GET /.well-known/mercure
- "Create a mercure?" -> POST /.well-known/mercure
- "List all subscriptions?" -> GET /.well-known/mercure/subscriptions
- "Get subscription details?" -> GET /.well-known/mercure/subscriptions/{topic}
- "Get subscription details?" -> GET /.well-known/mercure/subscriptions/{topic}/{subscriber}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
