---
name: microsoftresourcehealth
description: "Microsoft.ResourceHealth API skill. Use when working with Microsoft.ResourceHealth for subscriptions, {resourceUri}, providers. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Microsoft.ResourceHealth
API version: 2017-07-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ResourceHealth/operations -- verify access

## Endpoints

10 endpoints across 3 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.ResourceHealth/availabilityStatuses | Lists the current availability status for all the resources in the subscription. Use the nextLink property in the response to get the next page of availability statuses. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ResourceHealth/availabilityStatuses | Lists the current availability status for all the resources in the resource group. Use the nextLink property in the response to get the next page of availability statuses. |

### {resourceUri}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{resourceUri}/providers/Microsoft.ResourceHealth/availabilityStatuses/current | Gets current availability status for a single resource |
| GET | /{resourceUri}/providers/Microsoft.ResourceHealth/availabilityStatuses | Lists all historical availability transitions and impacting events for a single resource. Use the nextLink property in the response to get the next page of availability status |
| GET | /{resourceUri}/providers/Microsoft.ResourceHealth/childAvailabilityStatuses/current | Gets current availability status for a single resource |
| GET | /{resourceUri}/providers/Microsoft.ResourceHealth/childAvailabilityStatuses | Lists the historical availability statuses for a single child resource. Use the nextLink property in the response to get the next page of availability status |
| GET | /{resourceUri}/providers/Microsoft.ResourceHealth/childResources | Lists the all the children and its current health status for a parent resource. Use the nextLink property in the response to get the next page of children current health |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ResourceHealth/operations | Lists available operations for the resourcehealth resource provider |
| GET | /providers/Microsoft.ResourceHealth/emergingIssues/{issueName} | Gets Azure services' emerging issues. |
| GET | /providers/Microsoft.ResourceHealth/emergingIssues | Lists Azure services' emerging issues. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all availabilityStatuses?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.ResourceHealth/availabilityStatuses
- "List all availabilityStatuses?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ResourceHealth/availabilityStatuses
- "List all current?" -> GET /{resourceUri}/providers/Microsoft.ResourceHealth/availabilityStatuses/current
- "List all availabilityStatuses?" -> GET /{resourceUri}/providers/Microsoft.ResourceHealth/availabilityStatuses
- "List all current?" -> GET /{resourceUri}/providers/Microsoft.ResourceHealth/childAvailabilityStatuses/current
- "List all childAvailabilityStatuses?" -> GET /{resourceUri}/providers/Microsoft.ResourceHealth/childAvailabilityStatuses
- "List all childResources?" -> GET /{resourceUri}/providers/Microsoft.ResourceHealth/childResources
- "List all operations?" -> GET /providers/Microsoft.ResourceHealth/operations
- "Get emergingIssue details?" -> GET /providers/Microsoft.ResourceHealth/emergingIssues/{issueName}
- "List all emergingIssues?" -> GET /providers/Microsoft.ResourceHealth/emergingIssues
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
