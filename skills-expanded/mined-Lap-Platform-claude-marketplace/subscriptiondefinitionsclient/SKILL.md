---
name: subscriptiondefinitionsclient
description: "SubscriptionDefinitionsClient API skill. Use when working with SubscriptionDefinitionsClient for providers. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# SubscriptionDefinitionsClient
API version: 2017-11-01-preview

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Subscription/operations -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Subscription/operations | Lists all of the available Microsoft.Subscription API operations. |
| PUT | /providers/Microsoft.Subscription/subscriptionDefinitions/{subscriptionDefinitionName} | Create an Azure subscription definition. |
| GET | /providers/Microsoft.Subscription/subscriptionDefinitions/{subscriptionDefinitionName} | Get an Azure subscription definition. |
| GET | /providers/Microsoft.Subscription/subscriptionDefinitions | List an Azure subscription definition by subscriptionId. |
| GET | /providers/Microsoft.Subscription/subscriptionOperations/{operationId} | Retrieves the status of the subscription definition PUT operation. The URI of this API is returned in the Location field of the response header. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all operations?" -> GET /providers/Microsoft.Subscription/operations
- "Update a subscriptionDefinition?" -> PUT /providers/Microsoft.Subscription/subscriptionDefinitions/{subscriptionDefinitionName}
- "Get subscriptionDefinition details?" -> GET /providers/Microsoft.Subscription/subscriptionDefinitions/{subscriptionDefinitionName}
- "List all subscriptionDefinitions?" -> GET /providers/Microsoft.Subscription/subscriptionDefinitions
- "Get subscriptionOperation details?" -> GET /providers/Microsoft.Subscription/subscriptionOperations/{operationId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
