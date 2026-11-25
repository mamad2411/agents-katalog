---
name: compute-admin-client
description: "Compute Admin Client API skill. Use when working with Compute Admin Client for subscriptions. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Compute Admin Client
API version: 2015-12-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension -- verify access

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension/publishers/{publisher}/types/{type}/versions/{version} | Returns requested Virtual Machine Extension Image. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension/publishers/{publisher}/types/{type}/versions/{version} | Create a Virtual Machine Extension Image. |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension/publishers/{publisher}/types/{type}/versions/{version} | Deletes a Virtual Machine Extension Image. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension | Returns a list of all Virtual Machine Extension Images. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get version details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension/publishers/{publisher}/types/{type}/versions/{version}
- "Update a version?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension/publishers/{publisher}/types/{type}/versions/{version}
- "Delete a version?" -> DELETE /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension/publishers/{publisher}/types/{type}/versions/{version}
- "List all VMExtension?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Compute.Admin/locations/{location}/artifactTypes/VMExtension
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
