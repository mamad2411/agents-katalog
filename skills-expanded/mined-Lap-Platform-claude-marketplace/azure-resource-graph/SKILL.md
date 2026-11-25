---
name: azure-resource-graph
description: "Azure Resource Graph API skill. Use when working with Azure Resource Graph for providers. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Resource Graph
API version: 2019-04-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ResourceGraph/operations -- verify access
3. POST /providers/Microsoft.ResourceGraph/resources -- create first resources

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| POST | /providers/Microsoft.ResourceGraph/resources | Queries the resources managed by Azure Resource Manager for all subscriptions specified in the request. |
| GET | /providers/Microsoft.ResourceGraph/operations | Lists all of the available REST API operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a resource?" -> POST /providers/Microsoft.ResourceGraph/resources
- "List all operations?" -> GET /providers/Microsoft.ResourceGraph/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
