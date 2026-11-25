---
name: ats-api
description: "ATS API skill. Use when working with ATS for ats. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# ATS API
API version: 10.24.0

## Auth
ApiKey Authorization in header

## Base URL
https://unify.apideck.com

## Setup
1. Set your API key in the appropriate header
2. GET /ats/jobs -- verify access
3. POST /ats/applicants -- create first applicants

## Endpoints

12 endpoints across 1 groups. See references/api-spec.lap for full details.

### ats
| Method | Path | Description |
|--------|------|-------------|
| GET | /ats/jobs | List Jobs |
| GET | /ats/jobs/{id} | Get Job |
| GET | /ats/applicants | List Applicants |
| POST | /ats/applicants | Create Applicant |
| GET | /ats/applicants/{id} | Get Applicant |
| PATCH | /ats/applicants/{id} | Update Applicant |
| DELETE | /ats/applicants/{id} | Delete Applicant |
| GET | /ats/applications | List Applications |
| POST | /ats/applications | Create Application |
| GET | /ats/applications/{id} | Get Application |
| PATCH | /ats/applications/{id} | Update Application |
| DELETE | /ats/applications/{id} | Delete Application |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all jobs?" -> GET /ats/jobs
- "Get job details?" -> GET /ats/jobs/{id}
- "List all applicants?" -> GET /ats/applicants
- "Create a applicant?" -> POST /ats/applicants
- "Get applicant details?" -> GET /ats/applicants/{id}
- "Partially update a applicant?" -> PATCH /ats/applicants/{id}
- "Delete a applicant?" -> DELETE /ats/applicants/{id}
- "List all applications?" -> GET /ats/applications
- "Create a application?" -> POST /ats/applications
- "Get application details?" -> GET /ats/applications/{id}
- "Partially update a application?" -> PATCH /ats/applications/{id}
- "Delete a application?" -> DELETE /ats/applications/{id}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
