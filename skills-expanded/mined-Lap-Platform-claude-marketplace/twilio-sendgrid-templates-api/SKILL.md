---
name: twilio-sendgrid-templates-api
description: "Twilio SendGrid Templates API skill. Use when working with Twilio SendGrid Templates for templates. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio SendGrid Templates API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.sendgrid.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v3/templates -- verify access
3. POST /v3/templates -- create first templates

## Endpoints

11 endpoints across 1 groups. See references/api-spec.lap for full details.

### templates
| Method | Path | Description |
|--------|------|-------------|
| POST | /v3/templates | Create a transactional template. |
| GET | /v3/templates | Retrieve paged transactional templates. |
| POST | /v3/templates/{template_id} | Duplicate a transactional template. |
| GET | /v3/templates/{template_id} | Retrieve a single transactional template. |
| PATCH | /v3/templates/{template_id} | Edit a transactional template. |
| DELETE | /v3/templates/{template_id} | Delete a template. |
| POST | /v3/templates/{template_id}/versions | Create a new transactional template version. |
| GET | /v3/templates/{template_id}/versions/{version_id} | Retrieve a specific transactional template version. |
| PATCH | /v3/templates/{template_id}/versions/{version_id} | Edit a transactional template version. |
| DELETE | /v3/templates/{template_id}/versions/{version_id} | Delete a transactional template version. |
| POST | /v3/templates/{template_id}/versions/{version_id}/activate | Activate a transactional template version. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a template?" -> POST /v3/templates
- "List all templates?" -> GET /v3/templates
- "Get template details?" -> GET /v3/templates/{template_id}
- "Partially update a template?" -> PATCH /v3/templates/{template_id}
- "Delete a template?" -> DELETE /v3/templates/{template_id}
- "Create a version?" -> POST /v3/templates/{template_id}/versions
- "Get version details?" -> GET /v3/templates/{template_id}/versions/{version_id}
- "Partially update a version?" -> PATCH /v3/templates/{template_id}/versions/{version_id}
- "Delete a version?" -> DELETE /v3/templates/{template_id}/versions/{version_id}
- "Create a activate?" -> POST /v3/templates/{template_id}/versions/{version_id}/activate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
