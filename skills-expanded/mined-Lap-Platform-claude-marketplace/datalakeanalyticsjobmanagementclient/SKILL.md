---
name: datalakeanalyticsjobmanagementclient
description: "DataLakeAnalyticsJobManagementClient API skill. Use when working with DataLakeAnalyticsJobManagementClient for jobs, buildJob, pipelines. Covers 13 endpoints."
version: 1.0.0
generator: lapsh
---

# DataLakeAnalyticsJobManagementClient
API version: 2017-09-01-preview

## Auth
No authentication required.

## Base URL
Not specified.

## Setup
1. No auth setup needed
2. GET /jobs -- verify access
3. POST /jobs/{jobIdentity}/CancelJob -- create first CancelJob

## Endpoints

13 endpoints across 4 groups. See references/api-spec.lap for full details.

### jobs
| Method | Path | Description |
|--------|------|-------------|
| GET | /jobs | Lists the jobs, if any, associated with the specified Data Lake Analytics account. The response includes a link to the next page of results, if any. |
| PUT | /jobs/{jobIdentity} | Submits a job to the specified Data Lake Analytics account. |
| GET | /jobs/{jobIdentity} | Gets the job information for the specified job ID. |
| PATCH | /jobs/{jobIdentity} | Updates the job information for the specified job ID. (Only for use internally with Scope job type.) |
| GET | /jobs/{jobIdentity}/GetStatistics | Gets statistics of the specified job. |
| GET | /jobs/{jobIdentity}/GetDebugDataPath | Gets the job debug data information specified by the job ID. |
| POST | /jobs/{jobIdentity}/CancelJob | Cancels the running job specified by the job ID. |
| POST | /jobs/{jobIdentity}/YieldJob | Pauses the specified job and places it back in the job queue, behind other jobs of equal or higher importance, based on priority. (Only for use internally with Scope job type.) |

### buildJob
| Method | Path | Description |
|--------|------|-------------|
| POST | /buildJob | Builds (compiles) the specified job in the specified Data Lake Analytics account for job correctness and validation. |

### pipelines
| Method | Path | Description |
|--------|------|-------------|
| GET | /pipelines | Lists all pipelines. |
| GET | /pipelines/{pipelineIdentity} | Gets the Pipeline information for the specified pipeline ID. |

### recurrences
| Method | Path | Description |
|--------|------|-------------|
| GET | /recurrences | Lists all recurrences. |
| GET | /recurrences/{recurrenceIdentity} | Gets the recurrence information for the specified recurrence ID. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all jobs?" -> GET /jobs
- "Update a job?" -> PUT /jobs/{jobIdentity}
- "Get job details?" -> GET /jobs/{jobIdentity}
- "Partially update a job?" -> PATCH /jobs/{jobIdentity}
- "List all GetStatistics?" -> GET /jobs/{jobIdentity}/GetStatistics
- "List all GetDebugDataPath?" -> GET /jobs/{jobIdentity}/GetDebugDataPath
- "Create a CancelJob?" -> POST /jobs/{jobIdentity}/CancelJob
- "Create a YieldJob?" -> POST /jobs/{jobIdentity}/YieldJob
- "Create a buildJob?" -> POST /buildJob
- "List all pipelines?" -> GET /pipelines
- "Get pipeline details?" -> GET /pipelines/{pipelineIdentity}
- "List all recurrences?" -> GET /recurrences
- "Get recurrence details?" -> GET /recurrences/{recurrenceIdentity}

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
