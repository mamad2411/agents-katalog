---
name: managedservicesclient
description: "ManagedServicesClient API skill. Use when working with ManagedServicesClient for {scope}, providers. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# ManagedServicesClient
API version: 2019-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.ManagedServices/operations -- verify access

## Endpoints

9 endpoints across 2 groups. See references/api-spec.lap for full details.

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions/{registrationDefinitionId} | Gets the registration definition details. |
| DELETE | /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions/{registrationDefinitionId} | Deletes the registration definition. |
| PUT | /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions/{registrationDefinitionId} | Creates or updates a registration definition. |
| GET | /{scope}/providers/Microsoft.ManagedServices/registrationAssignments/{registrationAssignmentId} | Gets the details of specified registration assignment. |
| DELETE | /{scope}/providers/Microsoft.ManagedServices/registrationAssignments/{registrationAssignmentId} | Deletes the specified registration assignment. |
| PUT | /{scope}/providers/Microsoft.ManagedServices/registrationAssignments/{registrationAssignmentId} | Creates or updates a registration assignment. |
| GET | /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions | Gets a list of the registration definitions. |
| GET | /{scope}/providers/Microsoft.ManagedServices/registrationAssignments | Gets a list of the registration assignments. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.ManagedServices/operations | Gets a list of the operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get registrationDefinition details?" -> GET /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions/{registrationDefinitionId}
- "Delete a registrationDefinition?" -> DELETE /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions/{registrationDefinitionId}
- "Update a registrationDefinition?" -> PUT /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions/{registrationDefinitionId}
- "Get registrationAssignment details?" -> GET /{scope}/providers/Microsoft.ManagedServices/registrationAssignments/{registrationAssignmentId}
- "Delete a registrationAssignment?" -> DELETE /{scope}/providers/Microsoft.ManagedServices/registrationAssignments/{registrationAssignmentId}
- "Update a registrationAssignment?" -> PUT /{scope}/providers/Microsoft.ManagedServices/registrationAssignments/{registrationAssignmentId}
- "List all registrationDefinitions?" -> GET /{scope}/providers/Microsoft.ManagedServices/registrationDefinitions
- "List all registrationAssignments?" -> GET /{scope}/providers/Microsoft.ManagedServices/registrationAssignments
- "List all operations?" -> GET /providers/Microsoft.ManagedServices/operations
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
