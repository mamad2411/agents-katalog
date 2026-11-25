---
name: zeit-api
description: "ZEIT API skill. Use when working with ZEIT for integrations, domains. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# ZEIT API
API version: v2019-01-07

## Auth
Bearer bearer | OAuth2

## Base URL
https://api.zeit.co

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/integrations/webhooks -- verify access
3. POST /v1/integrations/webhooks -- create first webhooks

## Endpoints

5 endpoints across 2 groups. See references/api-spec.lap for full details.

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/integrations/webhooks | Get a list of existent webhooks |
| POST | /v1/integrations/webhooks | Create a new webhook |
| DELETE | /v1/integrations/webhooks/:id | Remove a webhook by id |

### domains
| Method | Path | Description |
|--------|------|-------------|
| GET | /v4/domains | Gets a list of domains registered for the authenticating user. |
| GET | /v4/domains/{name} | Get a domain for the authenticated user by name |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all webhooks?" -> GET /v1/integrations/webhooks
- "Create a webhook?" -> POST /v1/integrations/webhooks
- "List all domains?" -> GET /v4/domains
- "Get domain details?" -> GET /v4/domains/{name}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
