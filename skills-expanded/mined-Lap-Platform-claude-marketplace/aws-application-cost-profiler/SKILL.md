---
name: aws-application-cost-profiler
description: "AWS Application Cost Profiler API skill. Use when working with AWS Application Cost Profiler for reportDefinition, importApplicationUsage. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Application Cost Profiler
API version: 2020-09-10

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /reportDefinition -- verify access
3. POST /importApplicationUsage -- create first importApplicationUsage

## Endpoints

6 endpoints across 2 groups. See references/api-spec.lap for full details.

### reportDefinition
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /reportDefinition/{reportId} | Deletes the specified report definition in AWS Application Cost Profiler. This stops the report from being generated. |
| GET | /reportDefinition/{reportId} | Retrieves the definition of a report already configured in AWS Application Cost Profiler. |
| GET | /reportDefinition | Retrieves a list of all reports and their configurations for your AWS account. The maximum number of reports is one. |
| POST | /reportDefinition | Creates the report definition for a report in Application Cost Profiler. |
| PUT | /reportDefinition/{reportId} | Updates existing report in AWS Application Cost Profiler. |

### importApplicationUsage
| Method | Path | Description |
|--------|------|-------------|
| POST | /importApplicationUsage | Ingests application usage data from Amazon Simple Storage Service (Amazon S3). The data must already exist in the S3 location. As part of the action, AWS Application Cost Profiler copies the object from your S3 bucket to an S3 bucket owned by Amazon for processing asynchronously. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Delete a reportDefinition?" -> DELETE /reportDefinition/{reportId}
- "Get reportDefinition details?" -> GET /reportDefinition/{reportId}
- "Create a importApplicationUsage?" -> POST /importApplicationUsage
- "List all reportDefinition?" -> GET /reportDefinition
- "Create a reportDefinition?" -> POST /reportDefinition
- "Update a reportDefinition?" -> PUT /reportDefinition/{reportId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
