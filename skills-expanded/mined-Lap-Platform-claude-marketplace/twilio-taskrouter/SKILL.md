---
name: twilio-taskrouter
description: "Twilio - Taskrouter API skill. Use when working with Twilio - Taskrouter for Workspaces. Covers 61 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Taskrouter
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://taskrouter.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v1/Workspaces -- verify access
3. POST /v1/Workspaces/{WorkspaceSid}/Activities/{Sid} -- create first Activities

## Endpoints

61 endpoints across 1 groups. See references/api-spec.lap for full details.

### Workspaces
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/Workspaces/{WorkspaceSid}/Activities/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Activities/{Sid} |  |
| DELETE | /v1/Workspaces/{WorkspaceSid}/Activities/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Activities |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Activities |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Events/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Events |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Tasks/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Tasks/{Sid} |  |
| DELETE | /v1/Workspaces/{WorkspaceSid}/Tasks/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Tasks |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Tasks |  |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskChannels/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/TaskChannels/{Sid} |  |
| DELETE | /v1/Workspaces/{WorkspaceSid}/TaskChannels/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskChannels |  |
| POST | /v1/Workspaces/{WorkspaceSid}/TaskChannels |  |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskQueues/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/TaskQueues/{Sid} |  |
| DELETE | /v1/Workspaces/{WorkspaceSid}/TaskQueues/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskQueues |  |
| POST | /v1/Workspaces/{WorkspaceSid}/TaskQueues |  |
| POST | /v1/Workspaces/{WorkspaceSid}/TaskQueues/RealTimeStatistics | Fetch a Task Queue Real Time Statistics in bulk for the array of TaskQueue SIDs, support upto 50 in a request. |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskQueues/{TaskQueueSid}/CumulativeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskQueues/{TaskQueueSid}/RealTimeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskQueues/{TaskQueueSid}/Statistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/TaskQueues/Statistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Tasks/{TaskSid}/Reservations |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Tasks/{TaskSid}/Reservations/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Tasks/{TaskSid}/Reservations/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Workers |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Workers/{Sid} |  |
| DELETE | /v1/Workspaces/{WorkspaceSid}/Workers/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Channels |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Channels/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Channels/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Statistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Reservations |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Reservations/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Reservations/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/Statistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/CumulativeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workers/RealTimeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workflows/{Sid} |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Workflows/{Sid} |  |
| DELETE | /v1/Workspaces/{WorkspaceSid}/Workflows/{Sid} |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workflows |  |
| POST | /v1/Workspaces/{WorkspaceSid}/Workflows |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workflows/{WorkflowSid}/CumulativeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workflows/{WorkflowSid}/RealTimeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Workflows/{WorkflowSid}/Statistics |  |
| GET | /v1/Workspaces/{Sid} |  |
| POST | /v1/Workspaces/{Sid} |  |
| DELETE | /v1/Workspaces/{Sid} |  |
| GET | /v1/Workspaces |  |
| POST | /v1/Workspaces |  |
| GET | /v1/Workspaces/{WorkspaceSid}/CumulativeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/RealTimeStatistics |  |
| GET | /v1/Workspaces/{WorkspaceSid}/Statistics |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get Activity details?" -> GET /v1/Workspaces/{WorkspaceSid}/Activities/{Sid}
- "Delete a Activity?" -> DELETE /v1/Workspaces/{WorkspaceSid}/Activities/{Sid}
- "List all Activities?" -> GET /v1/Workspaces/{WorkspaceSid}/Activities
- "Create a Activity?" -> POST /v1/Workspaces/{WorkspaceSid}/Activities
- "Get Event details?" -> GET /v1/Workspaces/{WorkspaceSid}/Events/{Sid}
- "List all Events?" -> GET /v1/Workspaces/{WorkspaceSid}/Events
- "Get Task details?" -> GET /v1/Workspaces/{WorkspaceSid}/Tasks/{Sid}
- "Delete a Task?" -> DELETE /v1/Workspaces/{WorkspaceSid}/Tasks/{Sid}
- "List all Tasks?" -> GET /v1/Workspaces/{WorkspaceSid}/Tasks
- "Create a Task?" -> POST /v1/Workspaces/{WorkspaceSid}/Tasks
- "Get TaskChannel details?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskChannels/{Sid}
- "Delete a TaskChannel?" -> DELETE /v1/Workspaces/{WorkspaceSid}/TaskChannels/{Sid}
- "List all TaskChannels?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskChannels
- "Create a TaskChannel?" -> POST /v1/Workspaces/{WorkspaceSid}/TaskChannels
- "Get TaskQueue details?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskQueues/{Sid}
- "Delete a TaskQueue?" -> DELETE /v1/Workspaces/{WorkspaceSid}/TaskQueues/{Sid}
- "List all TaskQueues?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskQueues
- "Create a TaskQueue?" -> POST /v1/Workspaces/{WorkspaceSid}/TaskQueues
- "Create a RealTimeStatistic?" -> POST /v1/Workspaces/{WorkspaceSid}/TaskQueues/RealTimeStatistics
- "List all CumulativeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskQueues/{TaskQueueSid}/CumulativeStatistics
- "List all RealTimeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskQueues/{TaskQueueSid}/RealTimeStatistics
- "List all Statistics?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskQueues/{TaskQueueSid}/Statistics
- "List all Statistics?" -> GET /v1/Workspaces/{WorkspaceSid}/TaskQueues/Statistics
- "List all Reservations?" -> GET /v1/Workspaces/{WorkspaceSid}/Tasks/{TaskSid}/Reservations
- "Get Reservation details?" -> GET /v1/Workspaces/{WorkspaceSid}/Tasks/{TaskSid}/Reservations/{Sid}
- "List all Workers?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers
- "Create a Worker?" -> POST /v1/Workspaces/{WorkspaceSid}/Workers
- "Get Worker details?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/{Sid}
- "Delete a Worker?" -> DELETE /v1/Workspaces/{WorkspaceSid}/Workers/{Sid}
- "List all Channels?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Channels
- "Get Channel details?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Channels/{Sid}
- "List all Statistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Statistics
- "List all Reservations?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Reservations
- "Get Reservation details?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/{WorkerSid}/Reservations/{Sid}
- "List all Statistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/Statistics
- "List all CumulativeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/CumulativeStatistics
- "List all RealTimeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Workers/RealTimeStatistics
- "Get Workflow details?" -> GET /v1/Workspaces/{WorkspaceSid}/Workflows/{Sid}
- "Delete a Workflow?" -> DELETE /v1/Workspaces/{WorkspaceSid}/Workflows/{Sid}
- "List all Workflows?" -> GET /v1/Workspaces/{WorkspaceSid}/Workflows
- "Create a Workflow?" -> POST /v1/Workspaces/{WorkspaceSid}/Workflows
- "List all CumulativeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Workflows/{WorkflowSid}/CumulativeStatistics
- "List all RealTimeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Workflows/{WorkflowSid}/RealTimeStatistics
- "List all Statistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Workflows/{WorkflowSid}/Statistics
- "Get Workspace details?" -> GET /v1/Workspaces/{Sid}
- "Delete a Workspace?" -> DELETE /v1/Workspaces/{Sid}
- "List all Workspaces?" -> GET /v1/Workspaces
- "Create a Workspace?" -> POST /v1/Workspaces
- "List all CumulativeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/CumulativeStatistics
- "List all RealTimeStatistics?" -> GET /v1/Workspaces/{WorkspaceSid}/RealTimeStatistics
- "List all Statistics?" -> GET /v1/Workspaces/{WorkspaceSid}/Statistics
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
