---
name: twilio-studio
description: "Twilio - Studio API skill. Use when working with Twilio - Studio for Flows. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Studio
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://studio.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/Flows -- verify access
3. POST /v2/Flows/{FlowSid}/Executions -- create first Executions

## Endpoints

19 endpoints across 1 groups. See references/api-spec.lap for full details.

### Flows
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/Flows/{FlowSid}/Executions | Retrieve a list of all Executions for the Flow. |
| POST | /v2/Flows/{FlowSid}/Executions | Triggers a new Execution for the Flow |
| GET | /v2/Flows/{FlowSid}/Executions/{Sid} | Retrieve an Execution |
| DELETE | /v2/Flows/{FlowSid}/Executions/{Sid} | Delete the Execution and all Steps relating to it. |
| POST | /v2/Flows/{FlowSid}/Executions/{Sid} | Update the status of an Execution to `ended`. |
| GET | /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Context | Retrieve the most recent context for an Execution. |
| GET | /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Steps | Retrieve a list of all Steps for an Execution. |
| GET | /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Steps/{Sid} | Retrieve a Step. |
| GET | /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Steps/{StepSid}/Context | Retrieve the context for an Execution Step. |
| POST | /v2/Flows | Create a Flow. |
| GET | /v2/Flows | Retrieve a list of all Flows. |
| POST | /v2/Flows/{Sid} | Update a Flow. |
| GET | /v2/Flows/{Sid} | Retrieve a specific Flow. |
| DELETE | /v2/Flows/{Sid} | Delete a specific Flow. |
| GET | /v2/Flows/{Sid}/Revisions | Retrieve a list of all Flows revisions. |
| GET | /v2/Flows/{Sid}/Revisions/{Revision} | Retrieve a specific Flow revision. |
| POST | /v2/Flows/Validate | Validate flow JSON definition |
| GET | /v2/Flows/{Sid}/TestUsers | Fetch flow test users |
| POST | /v2/Flows/{Sid}/TestUsers | Update flow test users |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Executions?" -> GET /v2/Flows/{FlowSid}/Executions
- "Create a Execution?" -> POST /v2/Flows/{FlowSid}/Executions
- "Get Execution details?" -> GET /v2/Flows/{FlowSid}/Executions/{Sid}
- "Delete a Execution?" -> DELETE /v2/Flows/{FlowSid}/Executions/{Sid}
- "List all Context?" -> GET /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Context
- "List all Steps?" -> GET /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Steps
- "Get Step details?" -> GET /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Steps/{Sid}
- "List all Context?" -> GET /v2/Flows/{FlowSid}/Executions/{ExecutionSid}/Steps/{StepSid}/Context
- "Create a Flow?" -> POST /v2/Flows
- "List all Flows?" -> GET /v2/Flows
- "Get Flow details?" -> GET /v2/Flows/{Sid}
- "Delete a Flow?" -> DELETE /v2/Flows/{Sid}
- "List all Revisions?" -> GET /v2/Flows/{Sid}/Revisions
- "Get Revision details?" -> GET /v2/Flows/{Sid}/Revisions/{Revision}
- "Create a Validate?" -> POST /v2/Flows/Validate
- "List all TestUsers?" -> GET /v2/Flows/{Sid}/TestUsers
- "Create a TestUser?" -> POST /v2/Flows/{Sid}/TestUsers
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
