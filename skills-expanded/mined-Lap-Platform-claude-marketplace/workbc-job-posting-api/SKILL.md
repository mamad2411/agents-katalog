---
name: workbc-job-posting-api
description: "WorkBC Job Posting API skill. Use when working with WorkBC Job Posting for majorProjects, jobTypes, regions. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# WorkBC Job Posting API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://workbcjobs.api.gov.bc.ca/v1

## Setup
1. No auth setup needed
2. GET /majorProjects -- verify access
3. POST /jobs -- create first jobs

## Endpoints

5 endpoints across 5 groups. See references/api-spec.lap for full details.

### majorProjects
| Method | Path | Description |
|--------|------|-------------|
| GET | /majorProjects | Major Projects |

### jobTypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /jobTypes | Job Types |

### regions
| Method | Path | Description |
|--------|------|-------------|
| GET | /regions | Regions |

### Industries
| Method | Path | Description |
|--------|------|-------------|
| GET | /Industries | Industries |

### jobs
| Method | Path | Description |
|--------|------|-------------|
| POST | /jobs | Job Feed |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all majorProjects?" -> GET /majorProjects
- "List all jobTypes?" -> GET /jobTypes
- "List all regions?" -> GET /regions
- "List all Industries?" -> GET /Industries
- "Create a job?" -> POST /jobs

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
