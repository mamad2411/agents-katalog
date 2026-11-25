---
name: hdinsightjobclient
description: "HDInsightJobClient API skill. Use when working with HDInsightJobClient for templeton, ws. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# HDInsightJobClient
API version: 2018-11-01-preview

## Auth
OAuth2

## Base URL
Not specified.

## Setup
1. Configure auth: OAuth2
2. GET /templeton/v1/jobs -- verify access
3. POST /templeton/v1/hive -- create first hive

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### templeton
| Method | Path | Description |
|--------|------|-------------|
| GET | /templeton/v1/jobs/{jobId} | Gets job details from the specified HDInsight cluster. |
| DELETE | /templeton/v1/jobs/{jobId} | Initiates cancel on given running job in the specified HDInsight. |
| GET | /templeton/v1/jobs | Gets the list of jobs from the specified HDInsight cluster. |
| GET | /templeton/v1/jobs?op=LISTAFTERID | Gets numrecords Of Jobs after jobid from the specified HDInsight cluster. |
| POST | /templeton/v1/hive | Submits a Hive job to an HDInsight cluster. |
| POST | /templeton/v1/mapreduce/jar | Submits a MapReduce job to an HDInsight cluster. |
| POST | /templeton/v1/mapreduce/streaming | Submits a MapReduce streaming job to an HDInsight cluster. |
| POST | /templeton/v1/pig | Submits a Pig job to an HDInsight cluster. |
| POST | /templeton/v1/sqoop | Submits a Sqoop job to an HDInsight cluster. |

### ws
| Method | Path | Description |
|--------|------|-------------|
| GET | /ws/v1/cluster/apps/{appId}/state | Gets application state from the specified HDInsight cluster. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get job details?" -> GET /templeton/v1/jobs/{jobId}
- "Delete a job?" -> DELETE /templeton/v1/jobs/{jobId}
- "List all jobs?" -> GET /templeton/v1/jobs
- "List all jobs?op=LISTAFTERID?" -> GET /templeton/v1/jobs?op=LISTAFTERID
- "Create a hive?" -> POST /templeton/v1/hive
- "Create a jar?" -> POST /templeton/v1/mapreduce/jar
- "Create a streaming?" -> POST /templeton/v1/mapreduce/streaming
- "Create a pig?" -> POST /templeton/v1/pig
- "Create a sqoop?" -> POST /templeton/v1/sqoop
- "List all state?" -> GET /ws/v1/cluster/apps/{appId}/state
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
