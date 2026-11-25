---
name: azure-devops
description: "Azure DevOps API skill. Use when working with Azure DevOps for providers, subscriptions. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure DevOps
API version: 2019-07-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.DevOps/operations -- verify access

## Endpoints

8 endpoints across 2 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.DevOps/operations | Lists all the operations supported by Microsoft.DevOps resource provider. |
| GET | /providers/Microsoft.DevOps/pipelineTemplateDefinitions | Lists all pipeline templates which can be used to configure an Azure Pipeline. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName} | Creates or updates an Azure Pipeline. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName} | Gets an existing Azure Pipeline. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName} | Updates the properties of an Azure Pipeline. Currently, only tags can be updated. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName} | Deletes an Azure Pipeline. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines | Lists all Azure Pipelines under the specified resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.DevOps/pipelines | Lists all Azure Pipelines under the specified subscription. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.DevOps/operations
- "List all pipelineTemplateDefinitions?" -> GET /providers/Microsoft.DevOps/pipelineTemplateDefinitions
- "Update a pipeline?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName}
- "Get pipeline details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName}
- "Partially update a pipeline?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName}
- "Delete a pipeline?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines/{pipelineName}
- "List all pipelines?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.DevOps/pipelines
- "List all pipelines?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.DevOps/pipelines
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
