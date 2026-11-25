---
name: azure-stack-azure-bridge-client
description: "Azure Stack Azure Bridge Client API skill. Use when working with Azure Stack Azure Bridge Client for subscriptions. Covers 8 endpoints."
version: 1.0.0
generator: lapsh
---

# Azure Stack Azure Bridge Client
API version: 2017-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}/getactivationkey -- create first getactivationkey

## Endpoints

8 endpoints across 1 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations | Returns a list of all registrations. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.AzureStack/registrations | Returns a list of all registrations under current subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName} | Returns the properties of an Azure Stack registration. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName} | Delete the requested Azure Stack registration. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName} | Create or update an Azure Stack registration. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName} | Patch an Azure Stack registration. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}/getactivationkey | Returns Azure Stack Activation Key. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}/enableRemoteManagement | Enables remote management for device under the Azure Stack registration. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all registrations?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations
- "List all registrations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.AzureStack/registrations
- "Get registration details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}
- "Delete a registration?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}
- "Update a registration?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}
- "Partially update a registration?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}
- "Create a getactivationkey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}/getactivationkey
- "Create a enableRemoteManagement?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.AzureStack/registrations/{registrationName}/enableRemoteManagement
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
