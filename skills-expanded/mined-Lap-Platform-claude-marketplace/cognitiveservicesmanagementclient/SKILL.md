---
name: cognitiveservicesmanagementclient
description: "CognitiveServicesManagementClient API skill. Use when working with CognitiveServicesManagementClient for subscriptions, providers. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# CognitiveServicesManagementClient
API version: 2017-04-18

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.CognitiveServices/operations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/listKeys -- create first listKeys

## Endpoints

19 endpoints across 2 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName} | Create Cognitive Services Account. Accounts is a resource group wide resource type. It holds the keys for developer to access intelligent APIs. It's also the resource type for billing. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName} | Updates a Cognitive Services account |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName} | Deletes a Cognitive Services account from the resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName} | Returns a Cognitive Services account specified by the parameters. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts | Returns all the resources of a particular type belonging to a resource group |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/accounts | Returns all the resources of a particular type belonging to a subscription. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/listKeys | Lists the account keys for the specified Cognitive Services account. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/regenerateKey | Regenerates the specified account key for the specified Cognitive Services account. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/skus | Gets the list of Microsoft.CognitiveServices SKUs available for your Subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/skus | List available SKUs for the requested Cognitive Services account |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/usages | Get usages for the requested Cognitive Services account |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/checkSkuAvailability | Check available SKUs. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/checkDomainAvailability | Check whether a domain is available. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections | Gets the private endpoint connections associated with the Cognitive Services account. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName} | Gets the specified private endpoint connection associated with the Cognitive Services account. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName} | Update the state of specified private endpoint connection associated with the Cognitive Services account. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName} | Deletes the specified private endpoint connection associated with the Cognitive Services account. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateLinkResources | Gets the private link resources that need to be created for a Cognitive Services account. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.CognitiveServices/operations | Lists all the available Cognitive Services account operations. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Update a account?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}
- "Partially update a account?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}
- "Delete a account?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}
- "Get account details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}
- "List all accounts?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts
- "List all accounts?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/accounts
- "Create a listKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/listKeys
- "Create a regenerateKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/regenerateKey
- "List all skus?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/skus
- "List all skus?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/skus
- "List all usages?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/usages
- "List all operations?" -> GET /providers/Microsoft.CognitiveServices/operations
- "Create a checkSkuAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/locations/{location}/checkSkuAvailability
- "Create a checkDomainAvailability?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.CognitiveServices/checkDomainAvailability
- "List all privateEndpointConnections?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections
- "Get privateEndpointConnection details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}
- "Update a privateEndpointConnection?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}
- "Delete a privateEndpointConnection?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateEndpointConnections/{privateEndpointConnectionName}
- "List all privateLinkResources?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{accountName}/privateLinkResources
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
