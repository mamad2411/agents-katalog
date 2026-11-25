---
name: computemanagementconvenienceclient
description: "ComputeManagementConvenienceClient API skill. Use when working with ComputeManagementConvenienceClient for subscriptions. Covers 1 endpoint."
version: 1.0.0
generator: lapsh
---

# ComputeManagementConvenienceClient
API version: 2015-11-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2

## Endpoints

1 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName} | Create a named template deployment using a template. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a deployment?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
