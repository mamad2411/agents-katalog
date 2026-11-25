---
name: aws-iot-core-device-advisor
description: "AWS IoT Core Device Advisor API skill. Use when working with AWS IoT Core Device Advisor for suiteDefinitions, endpoint, suiteRuns. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS IoT Core Device Advisor
API version: 2020-09-18

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
2. GET /endpoint -- verify access
3. POST /suiteDefinitions -- create first suiteDefinitions

## Endpoints

14 endpoints across 4 groups. See references/api-spec.lap for full details.

### suiteDefinitions
| Method | Path | Description |
|--------|------|-------------|
| POST | /suiteDefinitions | Creates a Device Advisor test suite. Requires permission to access the CreateSuiteDefinition action. |
| DELETE | /suiteDefinitions/{suiteDefinitionId} | Deletes a Device Advisor test suite. Requires permission to access the DeleteSuiteDefinition action. |
| GET | /suiteDefinitions/{suiteDefinitionId} | Gets information about a Device Advisor test suite. Requires permission to access the GetSuiteDefinition action. |
| GET | /suiteDefinitions/{suiteDefinitionId}/suiteRuns/{suiteRunId} | Gets information about a Device Advisor test suite run. Requires permission to access the GetSuiteRun action. |
| GET | /suiteDefinitions/{suiteDefinitionId}/suiteRuns/{suiteRunId}/report | Gets a report download link for a successful Device Advisor qualifying test suite run. Requires permission to access the GetSuiteRunReport action. |
| GET | /suiteDefinitions | Lists the Device Advisor test suites you have created. Requires permission to access the ListSuiteDefinitions action. |
| POST | /suiteDefinitions/{suiteDefinitionId}/suiteRuns | Starts a Device Advisor test suite run. Requires permission to access the StartSuiteRun action. |
| POST | /suiteDefinitions/{suiteDefinitionId}/suiteRuns/{suiteRunId}/stop | Stops a Device Advisor test suite run that is currently running. Requires permission to access the StopSuiteRun action. |
| PATCH | /suiteDefinitions/{suiteDefinitionId} | Updates a Device Advisor test suite. Requires permission to access the UpdateSuiteDefinition action. |

### endpoint
| Method | Path | Description |
|--------|------|-------------|
| GET | /endpoint | Gets information about an Device Advisor endpoint. |

### suiteRuns
| Method | Path | Description |
|--------|------|-------------|
| GET | /suiteRuns | Lists runs of the specified Device Advisor test suite. You can list all runs of the test suite, or the runs of a specific version of the test suite. Requires permission to access the ListSuiteRuns action. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/{resourceArn} | Lists the tags attached to an IoT Device Advisor resource. Requires permission to access the ListTagsForResource action. |
| POST | /tags/{resourceArn} | Adds to and modifies existing tags of an IoT Device Advisor resource. Requires permission to access the TagResource action. |
| DELETE | /tags/{resourceArn} | Removes tags from an IoT Device Advisor resource. Requires permission to access the UntagResource action. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a suiteDefinition?" -> POST /suiteDefinitions
- "Delete a suiteDefinition?" -> DELETE /suiteDefinitions/{suiteDefinitionId}
- "List all endpoint?" -> GET /endpoint
- "Get suiteDefinition details?" -> GET /suiteDefinitions/{suiteDefinitionId}
- "Get suiteRun details?" -> GET /suiteDefinitions/{suiteDefinitionId}/suiteRuns/{suiteRunId}
- "List all report?" -> GET /suiteDefinitions/{suiteDefinitionId}/suiteRuns/{suiteRunId}/report
- "List all suiteDefinitions?" -> GET /suiteDefinitions
- "List all suiteRuns?" -> GET /suiteRuns
- "Get tag details?" -> GET /tags/{resourceArn}
- "Create a suiteRun?" -> POST /suiteDefinitions/{suiteDefinitionId}/suiteRuns
- "Create a stop?" -> POST /suiteDefinitions/{suiteDefinitionId}/suiteRuns/{suiteRunId}/stop
- "Delete a tag?" -> DELETE /tags/{resourceArn}
- "Partially update a suiteDefinition?" -> PATCH /suiteDefinitions/{suiteDefinitionId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
