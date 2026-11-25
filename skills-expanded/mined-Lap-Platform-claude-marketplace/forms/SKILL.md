---
name: forms
description: "Forms API skill. Use when working with Forms for marketing. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Forms
API version: v3

## Auth
OAuth2 | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /marketing/v3/forms/ -- verify access
3. POST /marketing/v3/forms/ -- create first forms

## Endpoints

6 endpoints across 1 groups. See references/api-spec.lap for full details.

### marketing
| Method | Path | Description |
|--------|------|-------------|
| GET | /marketing/v3/forms/ | Get a list of forms |
| POST | /marketing/v3/forms/ | Create a form |
| GET | /marketing/v3/forms/{formId} | Get a form definition |
| PUT | /marketing/v3/forms/{formId} | Update a form definition |
| DELETE | /marketing/v3/forms/{formId} | Archive a form definition |
| PATCH | /marketing/v3/forms/{formId} | Partially update a form definition |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all forms?" -> GET /marketing/v3/forms/
- "Create a form?" -> POST /marketing/v3/forms/
- "Get form details?" -> GET /marketing/v3/forms/{formId}
- "Update a form?" -> PUT /marketing/v3/forms/{formId}
- "Delete a form?" -> DELETE /marketing/v3/forms/{formId}
- "Partially update a form?" -> PATCH /marketing/v3/forms/{formId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
