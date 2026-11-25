---
name: twilio-sendgrid-marketing-campaigns-contacts-api
description: "Twilio SendGrid Marketing Campaigns Contacts API skill. Use when working with Twilio SendGrid Marketing Campaigns Contacts for marketing. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio SendGrid Marketing Campaigns Contacts API
API version: 1.0.0

## Auth
Bearer bearer

## Base URL
https://api.sendgrid.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v3/marketing/contacts -- verify access
3. POST /v3/marketing/contacts/batch -- create first batch

## Endpoints

15 endpoints across 1 groups. See references/api-spec.lap for full details.

### marketing
| Method | Path | Description |
|--------|------|-------------|
| PUT | /v3/marketing/contacts | Add or Update a Contact |
| DELETE | /v3/marketing/contacts | Delete Contacts |
| GET | /v3/marketing/contacts | Get Sample Contacts |
| GET | /v3/marketing/contacts/{id} | Get a Contact by ID |
| POST | /v3/marketing/contacts/batch | Get Batched Contacts by IDs |
| DELETE | /v3/marketing/contacts/{contact_id}/identifiers | Delete a Contact Identifier |
| GET | /v3/marketing/contacts/count | Get Total Contact Count |
| POST | /v3/marketing/contacts/exports | Export Contacts |
| GET | /v3/marketing/contacts/exports | Get All Existing Exports |
| GET | /v3/marketing/contacts/exports/{id} | Export Contacts Status |
| PUT | /v3/marketing/contacts/imports | Import Contacts |
| GET | /v3/marketing/contacts/imports/{id} | Import Contacts Status |
| POST | /v3/marketing/contacts/search | Search Contacts |
| POST | /v3/marketing/contacts/search/emails | Get Contacts by Emails |
| POST | /v3/marketing/contacts/search/identifiers/{identifier_type} | Get Contacts by Identifiers |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all contacts?" -> GET /v3/marketing/contacts
- "Get contact details?" -> GET /v3/marketing/contacts/{id}
- "Create a batch?" -> POST /v3/marketing/contacts/batch
- "List all count?" -> GET /v3/marketing/contacts/count
- "Create a export?" -> POST /v3/marketing/contacts/exports
- "List all exports?" -> GET /v3/marketing/contacts/exports
- "Get export details?" -> GET /v3/marketing/contacts/exports/{id}
- "Get import details?" -> GET /v3/marketing/contacts/imports/{id}
- "Create a search?" -> POST /v3/marketing/contacts/search
- "Create a email?" -> POST /v3/marketing/contacts/search/emails
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
