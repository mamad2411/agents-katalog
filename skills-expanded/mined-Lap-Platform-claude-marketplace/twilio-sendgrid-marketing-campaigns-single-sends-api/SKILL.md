---
name: twilio-sendgrid-marketing-campaigns-single-sends-api
description: "Twilio SendGrid Marketing Campaigns Single Sends API skill. Use when working with Twilio SendGrid Marketing Campaigns Single Sends for marketing. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio SendGrid Marketing Campaigns Single Sends API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.sendgrid.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v3/marketing/singlesends -- verify access
3. POST /v3/marketing/singlesends -- create first singlesends

## Endpoints

11 endpoints across 1 groups. See references/api-spec.lap for full details.

### marketing
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/marketing/singlesends | Create Single Send |
| GET | /v3/marketing/singlesends | Get All Single Sends |
| DELETE | /v3/marketing/singlesends | Bulk Delete Single Sends |
| POST | /v3/marketing/singlesends/{id} | Duplicate Single Send |
| PATCH | /v3/marketing/singlesends/{id} | Update Single Send |
| GET | /v3/marketing/singlesends/{id} | Get Single Send by ID |
| DELETE | /v3/marketing/singlesends/{id} | Delete Single Send by ID |
| PUT | /v3/marketing/singlesends/{id}/schedule | Schedule Single Send |
| DELETE | /v3/marketing/singlesends/{id}/schedule | Delete Single Send Schedule |
| GET | /v3/marketing/singlesends/categories | Get All Categories |
| POST | /v3/marketing/singlesends/search | Get Single Sends Search |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a singlesend?" -> POST /v3/marketing/singlesends
- "List all singlesends?" -> GET /v3/marketing/singlesends
- "Partially update a singlesend?" -> PATCH /v3/marketing/singlesends/{id}
- "Get singlesend details?" -> GET /v3/marketing/singlesends/{id}
- "Delete a singlesend?" -> DELETE /v3/marketing/singlesends/{id}
- "List all categories?" -> GET /v3/marketing/singlesends/categories
- "Create a search?" -> POST /v3/marketing/singlesends/search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
