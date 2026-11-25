---
name: crm-api
description: "CRM API skill. Use when working with CRM for crm. Covers 50 endpoints."
version: 1.0.0
generator: lapsh
---

# CRM API
API version: 10.24.0

## Auth
ApiKey Authorization in header | ApiKey x-apideck-app-id in header | ApiKey x-apideck-consumer-id in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /crm/companies -- verify access
3. POST /crm/companies -- create first companies

## Endpoints

50 endpoints across 1 groups. See references/api-spec.lap for full details.

### crm
| Method | Path | Description |
|--------|------|-------------|
| GET | /crm/companies | List companies |
| POST | /crm/companies | Create company |
| GET | /crm/companies/{id} | Get company |
| PATCH | /crm/companies/{id} | Update company |
| DELETE | /crm/companies/{id} | Delete company |
| GET | /crm/contacts | List contacts |
| POST | /crm/contacts | Create contact |
| GET | /crm/contacts/{id} | Get contact |
| PATCH | /crm/contacts/{id} | Update contact |
| DELETE | /crm/contacts/{id} | Delete contact |
| GET | /crm/opportunities | List opportunities |
| POST | /crm/opportunities | Create opportunity |
| GET | /crm/opportunities/{id} | Get opportunity |
| PATCH | /crm/opportunities/{id} | Update opportunity |
| DELETE | /crm/opportunities/{id} | Delete opportunity |
| GET | /crm/leads | List leads |
| POST | /crm/leads | Create lead |
| GET | /crm/leads/{id} | Get lead |
| PATCH | /crm/leads/{id} | Update lead |
| DELETE | /crm/leads/{id} | Delete lead |
| GET | /crm/pipelines | List pipelines |
| POST | /crm/pipelines | Create pipeline |
| GET | /crm/pipelines/{id} | Get pipeline |
| PATCH | /crm/pipelines/{id} | Update pipeline |
| DELETE | /crm/pipelines/{id} | Delete pipeline |
| GET | /crm/notes | List notes |
| POST | /crm/notes | Create note |
| GET | /crm/notes/{id} | Get note |
| PATCH | /crm/notes/{id} | Update note |
| DELETE | /crm/notes/{id} | Delete note |
| GET | /crm/users | List users |
| POST | /crm/users | Create user |
| GET | /crm/users/{id} | Get user |
| PATCH | /crm/users/{id} | Update user |
| DELETE | /crm/users/{id} | Delete user |
| GET | /crm/activities | List activities |
| POST | /crm/activities | Create activity |
| GET | /crm/activities/{id} | Get activity |
| PATCH | /crm/activities/{id} | Update activity |
| DELETE | /crm/activities/{id} | Delete activity |
| GET | /crm/custom-object-schemas | List custom object schemas |
| POST | /crm/custom-object-schemas | Create custom object schema |
| GET | /crm/custom-object-schemas/{id} | Get custom object schema |
| PATCH | /crm/custom-object-schemas/{id} | Update custom object schema |
| DELETE | /crm/custom-object-schemas/{id} | Delete custom object schema |
| GET | /crm/custom-objects/{object_id} | List custom objects |
| POST | /crm/custom-objects/{object_id} | Create custom object |
| GET | /crm/custom-objects/{object_id}/{id} | Get custom object |
| PATCH | /crm/custom-objects/{object_id}/{id} | Update custom object |
| DELETE | /crm/custom-objects/{object_id}/{id} | Delete custom object |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all companies?" -> GET /crm/companies
- "Create a company?" -> POST /crm/companies
- "Get company details?" -> GET /crm/companies/{id}
- "Partially update a company?" -> PATCH /crm/companies/{id}
- "Delete a company?" -> DELETE /crm/companies/{id}
- "List all contacts?" -> GET /crm/contacts
- "Create a contact?" -> POST /crm/contacts
- "Get contact details?" -> GET /crm/contacts/{id}
- "Partially update a contact?" -> PATCH /crm/contacts/{id}
- "Delete a contact?" -> DELETE /crm/contacts/{id}
- "List all opportunities?" -> GET /crm/opportunities
- "Create a opportunity?" -> POST /crm/opportunities
- "Get opportunity details?" -> GET /crm/opportunities/{id}
- "Partially update a opportunity?" -> PATCH /crm/opportunities/{id}
- "Delete a opportunity?" -> DELETE /crm/opportunities/{id}
- "List all leads?" -> GET /crm/leads
- "Create a lead?" -> POST /crm/leads
- "Get lead details?" -> GET /crm/leads/{id}
- "Partially update a lead?" -> PATCH /crm/leads/{id}
- "Delete a lead?" -> DELETE /crm/leads/{id}
- "List all pipelines?" -> GET /crm/pipelines
- "Create a pipeline?" -> POST /crm/pipelines
- "Get pipeline details?" -> GET /crm/pipelines/{id}
- "Partially update a pipeline?" -> PATCH /crm/pipelines/{id}
- "Delete a pipeline?" -> DELETE /crm/pipelines/{id}
- "List all notes?" -> GET /crm/notes
- "Create a note?" -> POST /crm/notes
- "Get note details?" -> GET /crm/notes/{id}
- "Partially update a note?" -> PATCH /crm/notes/{id}
- "Delete a note?" -> DELETE /crm/notes/{id}
- "List all users?" -> GET /crm/users
- "Create a user?" -> POST /crm/users
- "Get user details?" -> GET /crm/users/{id}
- "Partially update a user?" -> PATCH /crm/users/{id}
- "Delete a user?" -> DELETE /crm/users/{id}
- "List all activities?" -> GET /crm/activities
- "Create a activity?" -> POST /crm/activities
- "Get activity details?" -> GET /crm/activities/{id}
- "Partially update a activity?" -> PATCH /crm/activities/{id}
- "Delete a activity?" -> DELETE /crm/activities/{id}
- "List all custom-object-schemas?" -> GET /crm/custom-object-schemas
- "Create a custom-object-schema?" -> POST /crm/custom-object-schemas
- "Get custom-object-schema details?" -> GET /crm/custom-object-schemas/{id}
- "Partially update a custom-object-schema?" -> PATCH /crm/custom-object-schemas/{id}
- "Delete a custom-object-schema?" -> DELETE /crm/custom-object-schemas/{id}
- "Get custom-object details?" -> GET /crm/custom-objects/{object_id}
- "Get custom-object details?" -> GET /crm/custom-objects/{object_id}/{id}
- "Partially update a custom-object?" -> PATCH /crm/custom-objects/{object_id}/{id}
- "Delete a custom-object?" -> DELETE /crm/custom-objects/{object_id}/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
