---
name: deploymentadminclient
description: "DeploymentAdminClient API skill. Use when working with DeploymentAdminClient for subscriptions. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# DeploymentAdminClient
API version: 2019-01-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets -- verify access
3. POST /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets/{secretName}/import -- create first import

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets | Returns an array of product secrets. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets/{secretName} | Returns the specific product secret. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets/{secretName}/import | Imports a product secret. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets/{secretName}/validate | Validates a product secret. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all secrets?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets
- "Get secret details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets/{secretName}
- "Create a import?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets/{secretName}/import
- "Create a validate?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Deployment.Admin/locations/global/productPackages/{packageId}/secrets/{secretName}/validate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
