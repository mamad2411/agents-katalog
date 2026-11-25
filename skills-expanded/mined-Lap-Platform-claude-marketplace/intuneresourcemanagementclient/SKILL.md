---
name: intuneresourcemanagementclient
description: "IntuneResourceManagementClient API skill. Use when working with IntuneResourceManagementClient for providers. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# IntuneResourceManagementClient
API version: 2015-01-14-privatepreview

## Auth
No authentication required.

## Base URL
https://management.azure.com

## Setup
1. No auth setup needed
2. GET /providers/Microsoft.Intune/locations -- verify access
3. POST /providers/Microsoft.Intune/locations/{hostName}/users/{userName}/devices/{deviceName}/wipe -- create first wipe

## Endpoints

33 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Intune/locations | Returns location for user tenant. |
| GET | /providers/Microsoft.Intune/locations/hostName | Returns location for given tenant. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/apps | Returns Intune Manageable apps. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies | Returns Intune iOSPolicies. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies | Returns Intune Android policies. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName} | Returns Intune iOS policies. |
| PUT | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName} | Creates or updates iOSMAMPolicy. |
| PATCH | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName} | patch an iOSMAMPolicy. |
| DELETE | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName} | Delete Ios Policy |
| GET | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName} | Returns AndroidMAMPolicy with given name. |
| PUT | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName} | Creates or updates AndroidMAMPolicy. |
| PATCH | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName} | Patch AndroidMAMPolicy. |
| DELETE | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName} | Delete Android Policy |
| GET | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/apps | Get apps for an iOSMAMPolicy. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/AndroidPolicies/{policyName}/apps | Get apps for an AndroidMAMPolicy. |
| PUT | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/apps/{appName} | Add app to an iOSMAMPolicy. |
| DELETE | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/apps/{appName} | Delete App for Ios Policy |
| PUT | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/apps/{appName} | Add app to an AndroidMAMPolicy. |
| DELETE | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/apps/{appName} | Delete App for Android Policy |
| GET | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/groups | Returns groups for a given iOSMAMPolicy. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/groups | Returns groups for a given AndroidMAMPolicy. |
| PUT | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/groups/{groupId} | Add group to an iOSMAMPolicy. |
| DELETE | /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/groups/{groupId} | Delete Group for iOS Policy |
| PUT | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/groups/{groupId} | Add group to an AndroidMAMPolicy. |
| DELETE | /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/groups/{groupId} | Delete Group for Android Policy |
| GET | /providers/Microsoft.Intune/locations/{hostName}/users/{userName}/devices | Get devices for a user. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/users/{userName}/devices/{deviceName} | Get a unique device for a user. |
| POST | /providers/Microsoft.Intune/locations/{hostName}/users/{userName}/devices/{deviceName}/wipe | Wipe a device for a user. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/operationResults | Returns operationResults. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/statuses/default | Returns Intune Tenant level statuses. |
| GET | /providers/Microsoft.Intune/locations/{hostName}/flaggedUsers | Returns Intune flagged user collection |
| GET | /providers/Microsoft.Intune/locations/{hostName}/flaggedUsers/{userName} | Returns Intune flagged user details |
| GET | /providers/Microsoft.Intune/locations/{hostName}/flaggedUsers/{userName}/flaggedEnrolledApps | Returns Intune flagged enrolled app collection for the User |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all locations?" -> GET /providers/Microsoft.Intune/locations
- "List all hostName?" -> GET /providers/Microsoft.Intune/locations/hostName
- "List all apps?" -> GET /providers/Microsoft.Intune/locations/{hostName}/apps
- "List all iosPolicies?" -> GET /providers/Microsoft.Intune/locations/{hostName}/iosPolicies
- "List all androidPolicies?" -> GET /providers/Microsoft.Intune/locations/{hostName}/androidPolicies
- "Get iosPolicy details?" -> GET /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}
- "Update a iosPolicy?" -> PUT /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}
- "Partially update a iosPolicy?" -> PATCH /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}
- "Delete a iosPolicy?" -> DELETE /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}
- "Get androidPolicy details?" -> GET /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}
- "Update a androidPolicy?" -> PUT /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}
- "Partially update a androidPolicy?" -> PATCH /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}
- "Delete a androidPolicy?" -> DELETE /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}
- "List all apps?" -> GET /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/apps
- "List all apps?" -> GET /providers/Microsoft.Intune/locations/{hostName}/AndroidPolicies/{policyName}/apps
- "Update a app?" -> PUT /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/apps/{appName}
- "Delete a app?" -> DELETE /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/apps/{appName}
- "Update a app?" -> PUT /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/apps/{appName}
- "Delete a app?" -> DELETE /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/apps/{appName}
- "List all groups?" -> GET /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/groups
- "List all groups?" -> GET /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/groups
- "Update a group?" -> PUT /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/groups/{groupId}
- "Delete a group?" -> DELETE /providers/Microsoft.Intune/locations/{hostName}/iosPolicies/{policyName}/groups/{groupId}
- "Update a group?" -> PUT /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/groups/{groupId}
- "Delete a group?" -> DELETE /providers/Microsoft.Intune/locations/{hostName}/androidPolicies/{policyName}/groups/{groupId}
- "List all devices?" -> GET /providers/Microsoft.Intune/locations/{hostName}/users/{userName}/devices
- "Get device details?" -> GET /providers/Microsoft.Intune/locations/{hostName}/users/{userName}/devices/{deviceName}
- "Create a wipe?" -> POST /providers/Microsoft.Intune/locations/{hostName}/users/{userName}/devices/{deviceName}/wipe
- "List all operationResults?" -> GET /providers/Microsoft.Intune/locations/{hostName}/operationResults
- "List all default?" -> GET /providers/Microsoft.Intune/locations/{hostName}/statuses/default
- "List all flaggedUsers?" -> GET /providers/Microsoft.Intune/locations/{hostName}/flaggedUsers
- "Get flaggedUser details?" -> GET /providers/Microsoft.Intune/locations/{hostName}/flaggedUsers/{userName}
- "List all flaggedEnrolledApps?" -> GET /providers/Microsoft.Intune/locations/{hostName}/flaggedUsers/{userName}/flaggedEnrolledApps

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
