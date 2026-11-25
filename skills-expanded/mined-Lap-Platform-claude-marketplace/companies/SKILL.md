---
name: companies
description: "Companies API skill. Use when working with Companies for crm. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Companies
API version: v3

## Auth
OAuth2 | ApiKey private-app-legacy in header | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/v3/objects/companies -- verify access
3. POST /crm/v3/objects/companies -- create first companies

## Endpoints

12 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/v3/objects/companies | Retrieve companies |
| POST | /crm/v3/objects/companies | Create a company |
| POST | /crm/v3/objects/companies/batch/archive | Archive a batch of companies |
| POST | /crm/v3/objects/companies/batch/create | Create a batch of companies |
| POST | /crm/v3/objects/companies/batch/read | Retrieve a batch of companies |
| POST | /crm/v3/objects/companies/batch/update | Update a batch of companies |
| POST | /crm/v3/objects/companies/batch/upsert | Create or update a batch of companies by unique property values |
| POST | /crm/v3/objects/companies/merge | Merge two companies |
| POST | /crm/v3/objects/companies/search | Search for companies |
| GET | /crm/v3/objects/companies/{companyId} | Retrieve a company |
| DELETE | /crm/v3/objects/companies/{companyId} | Archive a company |
| PATCH | /crm/v3/objects/companies/{companyId} | Update a company |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all companies?" -> GET /crm/v3/objects/companies
- "Create a company?" -> POST /crm/v3/objects/companies
- "Create a archive?" -> POST /crm/v3/objects/companies/batch/archive
- "Create a create?" -> POST /crm/v3/objects/companies/batch/create
- "Create a read?" -> POST /crm/v3/objects/companies/batch/read
- "Create a update?" -> POST /crm/v3/objects/companies/batch/update
- "Create a upsert?" -> POST /crm/v3/objects/companies/batch/upsert
- "Create a merge?" -> POST /crm/v3/objects/companies/merge
- "Create a search?" -> POST /crm/v3/objects/companies/search
- "Get company details?" -> GET /crm/v3/objects/companies/{companyId}
- "Delete a company?" -> DELETE /crm/v3/objects/companies/{companyId}
- "Partially update a company?" -> PATCH /crm/v3/objects/companies/{companyId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
