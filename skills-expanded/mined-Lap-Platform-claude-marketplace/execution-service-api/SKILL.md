---
name: execution-service-api
description: "Execution Service API skill. Use when working with Execution Service for execution. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Execution Service API
API version: 2019-09-30

## Auth
OAuth2

## Base URL
Not specified.

## Setup
1. Configure auth: OAuth2
3. POST /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/startlocalrun -- create first startlocalrun

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### execution
| Method | Path | Description |
|--------|------|-------------|
| POST | /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/startlocalrun | Start a run on a local machine. |
| POST | /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/startrun | Start a run on a remote compute target. |
| POST | /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/snapshotrun | Start a run from a snapshot on a remote compute target. |
| POST | /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runId/{runId}/cancel | Cancel a run. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a startlocalrun?" -> POST /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/startlocalrun
- "Create a startrun?" -> POST /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/startrun
- "Create a snapshotrun?" -> POST /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/snapshotrun
- "Create a cancel?" -> POST /execution/v1.0/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.MachineLearningServices/workspaces/{workspaceName}/experiments/{experimentName}/runId/{runId}/cancel
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
