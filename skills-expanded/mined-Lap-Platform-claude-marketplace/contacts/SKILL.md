---
name: contacts
description: "Contacts API skill. Use when working with Contacts for crm. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# Contacts
API version: v3

## Auth
OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/objects/contacts -- verify access
3. POST /crm/v3/objects/contacts -- create first contacts

## Endpoints

13 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/objects/contacts | Retrieve contacts |
| POST | /crm/v3/objects/contacts | Create a contact |
| POST | /crm/v3/objects/contacts/batch/archive | Archive a batch of contacts |
| POST | /crm/v3/objects/contacts/batch/create | Create a batch of contacts |
| POST | /crm/v3/objects/contacts/batch/read | Retrieve a batch of contacts |
| POST | /crm/v3/objects/contacts/batch/update | Update a batch of contacts |
| POST | /crm/v3/objects/contacts/batch/upsert | Create or update a batch of contacts |
| POST | /crm/v3/objects/contacts/gdpr-delete | Permanently delete a contact (GDPR-compliant) |
| POST | /crm/v3/objects/contacts/merge | Merge two contacts |
| POST | /crm/v3/objects/contacts/search | Search for contacts |
| GET | /crm/v3/objects/contacts/{contactId} | Retrieve a contact |
| DELETE | /crm/v3/objects/contacts/{contactId} | Archive a contact |
| PATCH | /crm/v3/objects/contacts/{contactId} | Update a contact |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all contacts?" -> GET /crm/v3/objects/contacts
- "Create a contact?" -> POST /crm/v3/objects/contacts
- "Create a archive?" -> POST /crm/v3/objects/contacts/batch/archive
- "Create a create?" -> POST /crm/v3/objects/contacts/batch/create
- "Create a read?" -> POST /crm/v3/objects/contacts/batch/read
- "Create a update?" -> POST /crm/v3/objects/contacts/batch/update
- "Create a upsert?" -> POST /crm/v3/objects/contacts/batch/upsert
- "Create a gdpr-delete?" -> POST /crm/v3/objects/contacts/gdpr-delete
- "Create a merge?" -> POST /crm/v3/objects/contacts/merge
- "Create a search?" -> POST /crm/v3/objects/contacts/search
- "Get contact details?" -> GET /crm/v3/objects/contacts/{contactId}
- "Delete a contact?" -> DELETE /crm/v3/objects/contacts/{contactId}
- "Partially update a contact?" -> PATCH /crm/v3/objects/contacts/{contactId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
