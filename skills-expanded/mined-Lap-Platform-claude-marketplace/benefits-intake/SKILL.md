---
name: benefits-intake
description: "Benefits Intake API skill. Use when working with Benefits Intake for uploads, path. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Benefits Intake
API version: 1.0.0

## Auth
ApiKey apikey in header

## Base URL
https://sandbox-api.va.gov/services/vba_documents/v1

## Setup
1. Set your API key in the appropriate header
2. GET /uploads/{id}/download -- verify access
3. POST /uploads -- create first uploads

## Endpoints

6 endpoints across 2 groups. See references/api-spec.lap for full details.

### uploads
| Method | Path | Description |
|--------|------|-------------|
| POST | /uploads | Get a location for subsequent document upload PUT request |
| GET | /uploads/{id} | Get status for a previous benefits document upload |
| GET | /uploads/{id}/download | Download zip of "what the server sees" |
| POST | /uploads/report | Get a bulk status report for a list of previous uploads |
| POST | /uploads/validate_document | Validate an individual document against system file requirements |

### path
| Method | Path | Description |
|--------|------|-------------|
| PUT | /path | Accepts document upload. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a upload?" -> POST /uploads
- "Get upload details?" -> GET /uploads/{id}
- "List all download?" -> GET /uploads/{id}/download
- "Create a report?" -> POST /uploads/report
- "Create a validate_document?" -> POST /uploads/validate_document
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
