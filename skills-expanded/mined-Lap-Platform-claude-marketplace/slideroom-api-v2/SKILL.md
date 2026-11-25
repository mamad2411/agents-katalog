---
name: slideroom-api-v2
description: "SlideRoom API V2 API skill. Use when working with SlideRoom API V2 for api. Covers 11 endpoints."
version: 1.0.0
generator: lapsh
---

# SlideRoom API V2
API version: v2

## Auth
ApiKey token in path

## Base URL
https://api.slideroom.com

## Setup
1. Set your API key in the appropriate header
2. GET /api/v2/applicant/attributes/names -- verify access
3. POST /api/v2/application/{applicationId}/attributes -- create first attributes

## Endpoints

11 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/v2/applicant/attributes/names | Gets the custom applicant attributes used by the organization. |
| GET | /api/v2/application/{applicationId}/attributes | Gets the custom attributes for an application. |
| POST | /api/v2/application/{applicationId}/attributes | Updates the custom attributes for an application. API Import is available in the Advanced Plan. |
| DELETE | /api/v2/application/{applicationId}/attributes | Deletes a custom attribute for an application. |
| GET | /api/v2/application/attributes/names | Gets the custom application attributes used by the organization. |
| POST | /api/v2/application/{applicationId}/request-export | Requests the generation of a single application export file (tabular, pdf, zip). |
| POST | /api/v2/application/request-export | Requests the generation of application export files (tabular, pdf, zip). |
| GET | /api/v2/export/{token} | Gets the status/result of a requested export. |
| GET | /api/v2/applicant/attributes | Gets the custom attributes for an applicant. |
| POST | /api/v2/applicant/attributes | Updates the custom attributes for an applicant. |
| DELETE | /api/v2/applicant/attributes | Deletes a custom attribute for an applicant. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all names?" -> GET /api/v2/applicant/attributes/names
- "List all attributes?" -> GET /api/v2/application/{applicationId}/attributes
- "Create a attribute?" -> POST /api/v2/application/{applicationId}/attributes
- "List all names?" -> GET /api/v2/application/attributes/names
- "Create a request-export?" -> POST /api/v2/application/{applicationId}/request-export
- "Create a request-export?" -> POST /api/v2/application/request-export
- "Get export details?" -> GET /api/v2/export/{token}
- "List all attributes?" -> GET /api/v2/applicant/attributes
- "Create a attribute?" -> POST /api/v2/applicant/attributes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
