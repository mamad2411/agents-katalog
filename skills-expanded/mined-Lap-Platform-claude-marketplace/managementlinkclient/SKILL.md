---
name: managementlinkclient
description: "ManagementLinkClient API skill. Use when working with ManagementLinkClient for providers, {linkId}, subscriptions. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# ManagementLinkClient
API version: 2016-09-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Resources/operations -- verify access

## Endpoints

6 endpoints across 4 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Resources/operations | Lists all of the available Microsoft.Resources REST API operations. |

### {linkId}
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /{linkId} | Deletes a resource link with the specified ID. |
| PUT | /{linkId} | Creates or updates a resource link between the specified resources. |
| GET | /{linkId} | Gets a resource link with the specified ID. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/links | Gets all the linked resources for the subscription. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.Resources/links | Gets a list of resource links at and below the specified source scope. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.Resources/operations
- "List all links?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Resources/links
- "List all links?" -> GET /{scope}/providers/Microsoft.Resources/links
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
