---
name: advisormanagementclient
description: "AdvisorManagementClient API skill. Use when working with AdvisorManagementClient for providers, subscriptions, {resourceUri}. Covers 15 endpoints."
version: 1.0.0
generator: lapsh
---

# AdvisorManagementClient
API version: 2017-04-19

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Advisor/metadata -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/generateRecommendations -- create first generateRecommendations

## Endpoints

15 endpoints across 3 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Advisor/metadata/{name} | Gets the metadata entity. |
| GET | /providers/Microsoft.Advisor/metadata | Gets the list of metadata entities. |
| GET | /providers/Microsoft.Advisor/operations | Lists all the available Advisor REST API operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/configurations | Retrieve Azure Advisor configurations. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/configurations | Create/Overwrite Azure Advisor configuration. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Advisor/configurations | Retrieve Azure Advisor configurations. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Advisor/configurations | Create/Overwrite Azure Advisor configuration. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/generateRecommendations | Initiates the recommendation generation or computation process for a subscription. This operation is asynchronous. The generated recommendations are stored in a cache in the Advisor service. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/generateRecommendations/{operationId} | Retrieves the status of the recommendation computation or generation process. Invoke this API after calling the generation recommendation. The URI of this API is returned in the Location field of the response header. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/recommendations | Obtains cached recommendations for a subscription. The recommendations are generated or computed by invoking generateRecommendations. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/suppressions | Retrieves the list of snoozed or dismissed suppressions for a subscription. The snoozed or dismissed attribute of a recommendation is referred to as a suppression. |

### {resourceUri}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId} | Obtains details of a cached recommendation. |
| GET | /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId}/suppressions/{name} | Obtains the details of a suppression. |
| PUT | /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId}/suppressions/{name} | Enables the snoozed or dismissed attribute of a recommendation. The snoozed or dismissed attribute is referred to as a suppression. Use this API to create or update the snoozed or dismissed status of a recommendation. |
| DELETE | /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId}/suppressions/{name} | Enables the activation of a snoozed or dismissed recommendation. The snoozed or dismissed attribute of a recommendation is referred to as a suppression. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get metadata details?" -> GET /providers/Microsoft.Advisor/metadata/{name}
- "List all metadata?" -> GET /providers/Microsoft.Advisor/metadata
- "List all configurations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/configurations
- "List all configurations?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Advisor/configurations
- "Create a generateRecommendation?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/generateRecommendations
- "Get generateRecommendation details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/generateRecommendations/{operationId}
- "List all recommendations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/recommendations
- "List all operations?" -> GET /providers/Microsoft.Advisor/operations
- "Get recommendation details?" -> GET /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId}
- "Get suppression details?" -> GET /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId}/suppressions/{name}
- "Update a suppression?" -> PUT /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId}/suppressions/{name}
- "Delete a suppression?" -> DELETE /{resourceUri}/providers/Microsoft.Advisor/recommendations/{recommendationId}/suppressions/{name}
- "List all suppressions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Advisor/suppressions
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
