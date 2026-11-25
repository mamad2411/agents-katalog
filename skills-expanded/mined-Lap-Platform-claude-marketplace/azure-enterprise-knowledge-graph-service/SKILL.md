---
name: azure-enterprise-knowledge-graph-service
description: "Azure Enterprise Knowledge Graph Service API skill. Use when working with Azure Enterprise Knowledge Graph Service for subscriptions, providers. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Enterprise Knowledge Graph Service
API version: 2018-12-03

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.EnterpriseKnowledgeGraph/operations -- verify access

## Endpoints

7 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName} | Creates a EnterpriseKnowledgeGraph Service. EnterpriseKnowledgeGraph Service is a resource group wide resource type. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName} | Updates a EnterpriseKnowledgeGraph Service |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName} | Deletes a EnterpriseKnowledgeGraph Service from the resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName} | Returns a EnterpriseKnowledgeGraph service specified by the parameters. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services | Returns all the resources of a particular type belonging to a resource group |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EnterpriseKnowledgeGraph/services | Returns all the resources of a particular type belonging to a subscription. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.EnterpriseKnowledgeGraph/operations | Lists all the available EnterpriseKnowledgeGraph services operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a service?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName}
- "Partially update a service?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName}
- "Delete a service?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName}
- "Get service details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services/{resourceName}
- "List all services?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EnterpriseKnowledgeGraph/services
- "List all services?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EnterpriseKnowledgeGraph/services
- "List all operations?" -> GET /providers/Microsoft.EnterpriseKnowledgeGraph/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
