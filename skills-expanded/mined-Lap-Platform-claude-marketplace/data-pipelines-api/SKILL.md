---
name: data-pipelines-api
description: "Data Pipelines API skill. Use when working with Data Pipelines for nessie. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Data Pipelines API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /nessie/pipeline/jobs -- verify access
3. POST /nessie/pipeline/create -- create first create

## Endpoints

8 endpoints across 1 groups. See references/api-spec.lap for full details.

### nessie
| Method | Path | Description |
|--------|------|-------------|
| GET | /nessie/pipeline/jobs | List Pipelines |
| POST | /nessie/pipeline/create | Create Pipeline |
| POST | /nessie/pipeline/edit | Edit Pipeline |
| POST | /nessie/pipeline/cancel | Delete Pipeline |
| POST | /nessie/pipeline/pause | Pause Pipeline |
| POST | /nessie/pipeline/resume | Resume Pipeline |
| GET | /nessie/pipeline/status | Get Pipeline |
| GET | /nessie/pipeline/timeline | List Pipeline Logs |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all jobs?" -> GET /nessie/pipeline/jobs
- "Create a create?" -> POST /nessie/pipeline/create
- "Create a edit?" -> POST /nessie/pipeline/edit
- "Create a cancel?" -> POST /nessie/pipeline/cancel
- "Create a pause?" -> POST /nessie/pipeline/pause
- "Create a resume?" -> POST /nessie/pipeline/resume
- "List all status?" -> GET /nessie/pipeline/status
- "List all timeline?" -> GET /nessie/pipeline/timeline

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
