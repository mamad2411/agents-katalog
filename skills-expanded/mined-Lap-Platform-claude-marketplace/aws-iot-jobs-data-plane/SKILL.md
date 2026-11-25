---
name: aws-iot-jobs-data-plane
description: "AWS IoT Jobs Data Plane API skill. Use when working with AWS IoT Jobs Data Plane for things. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Jobs Data Plane
API version: 2017-09-29

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /things/{thingName}/jobs -- verify access
3. POST /things/{thingName}/jobs/{jobId} -- create first jobs

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### things
| Method | Path | Description |
|--------|------|-------------|
| GET | /things/{thingName}/jobs/{jobId} | Gets details of a job execution. |
| GET | /things/{thingName}/jobs | Gets the list of all jobs for a thing that are not in a terminal status. |
| PUT | /things/{thingName}/jobs/$next | Gets and starts the next pending (status IN_PROGRESS or QUEUED) job execution for a thing. |
| POST | /things/{thingName}/jobs/{jobId} | Updates the status of a job execution. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get job details?" -> GET /things/{thingName}/jobs/{jobId}
- "List all jobs?" -> GET /things/{thingName}/jobs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
