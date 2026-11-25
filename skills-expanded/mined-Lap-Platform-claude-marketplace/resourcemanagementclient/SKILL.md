---
name: resourcemanagementclient
description: "ResourceManagementClient API skill. Use when working with ResourceManagementClient for providers, subscriptions, {resourceId}. Covers 62 endpoints."
version: 1.0.0
generator: lapsh
---

# ResourceManagementClient
API version: 2019-05-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.Resources/operations -- verify access
3. POST /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/cancel -- create first cancel

## Endpoints

62 endpoints across 3 groups. See references/api-spec.lap for full details.

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/ | Get all the deployments for a management group. |
| DELETE | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName} | Deletes a deployment from the deployment history. |
| GET | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName} | Gets a deployment. |
| HEAD | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName} | Checks whether the deployment exists. |
| PUT | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName} | Deploys resources at management group scope. |
| POST | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/cancel | Cancels a currently running template deployment. |
| POST | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/exportTemplate | Exports the template used for specified deployment. |
| GET | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations | Gets all deployments operations for a deployment. |
| GET | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations/{operationId} | Gets a deployments operation. |
| POST | /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/validate | Validates whether the specified template is syntactically correct and will be accepted by Azure Resource Manager.. |
| POST | /providers/Microsoft.Resources/calculateTemplateHash | Calculate the hash of the given template. |
| GET | /providers/Microsoft.Resources/operations | Lists all of the available Microsoft.Resources REST API operations. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/providers | Gets all resource providers for a subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/ | Get all the deployments for a subscription. |
| DELETE | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName} | Deletes a deployment from the deployment history. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName} | Gets a deployment. |
| HEAD | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName} | Checks whether the deployment exists. |
| PUT | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName} | Deploys resources at subscription scope. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/cancel | Cancels a currently running template deployment. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/exportTemplate | Exports the template used for specified deployment. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations | Gets all deployments operations for a deployment. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations/{operationId} | Gets a deployments operation. |
| POST | /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/validate | Validates whether the specified template is syntactically correct and will be accepted by Azure Resource Manager.. |
| GET | /subscriptions/{subscriptionId}/providers/{resourceProviderNamespace} | Gets the specified resource provider. |
| POST | /subscriptions/{subscriptionId}/providers/{resourceProviderNamespace}/register | Registers a subscription with a resource provider. |
| POST | /subscriptions/{subscriptionId}/providers/{resourceProviderNamespace}/unregister | Unregisters a subscription from a resource provider. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/resources | Get all the resources for a resource group. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{sourceResourceGroupName}/moveResources | Moves resources from one resource group to another resource group. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{sourceResourceGroupName}/validateMoveResources | Validates whether resources can be moved from one resource group to another resource group. |
| GET | /subscriptions/{subscriptionId}/resourcegroups | Gets all the resource groups for a subscription. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName} | Deletes a resource group. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName} | Gets a resource group. |
| HEAD | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName} | Checks whether a resource group exists. |
| PATCH | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName} | Updates a resource group. |
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName} | Creates or updates a resource group. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/deployments/{deploymentName}/operations | Gets all deployments operations for a deployment. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/deployments/{deploymentName}/operations/{operationId} | Gets a deployments operation. |
| POST | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/exportTemplate | Captures the specified resource group as a template. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/ | Get all the deployments for a resource group. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName} | Deletes a deployment from the deployment history. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName} | Gets a deployment. |
| HEAD | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName} | Checks whether the deployment exists. |
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName} | Deploys resources to a resource group. |
| POST | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}/cancel | Cancels a currently running template deployment. |
| POST | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}/exportTemplate | Exports the template used for specified deployment. |
| POST | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}/validate | Validates whether the specified template is syntactically correct and will be accepted by Azure Resource Manager.. |
| DELETE | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName} | Deletes a resource. |
| GET | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName} | Gets a resource. |
| HEAD | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName} | Checks whether a resource exists. |
| PATCH | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName} | Updates a resource. |
| PUT | /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName} | Creates a resource. |
| GET | /subscriptions/{subscriptionId}/resources | Get all the resources in a subscription. |
| GET | /subscriptions/{subscriptionId}/tagNames | Gets the names and values of all resource tags that are defined in a subscription. |
| DELETE | /subscriptions/{subscriptionId}/tagNames/{tagName} | Deletes a tag from the subscription. |
| PUT | /subscriptions/{subscriptionId}/tagNames/{tagName} | Creates a tag in the subscription. |
| DELETE | /subscriptions/{subscriptionId}/tagNames/{tagName}/tagValues/{tagValue} | Deletes a tag value. |
| PUT | /subscriptions/{subscriptionId}/tagNames/{tagName}/tagValues/{tagValue} | Creates a tag value. The name of the tag must already exist. |

### {resourceId}
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /{resourceId} | Deletes a resource by ID. |
| GET | /{resourceId} | Gets a resource by ID. |
| HEAD | /{resourceId} | Checks by ID whether a resource exists. |
| PATCH | /{resourceId} | Updates a resource by ID. |
| PUT | /{resourceId} | Create a resource by ID. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all deployments?" -> GET /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/
- "Delete a deployment?" -> DELETE /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Get deployment details?" -> GET /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Update a deployment?" -> PUT /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Create a cancel?" -> POST /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/cancel
- "Create a exportTemplate?" -> POST /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/exportTemplate
- "List all operations?" -> GET /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations
- "Get operation details?" -> GET /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations/{operationId}
- "Create a validate?" -> POST /providers/Microsoft.Management/managementGroups/{groupId}/providers/Microsoft.Resources/deployments/{deploymentName}/validate
- "Create a calculateTemplateHash?" -> POST /providers/Microsoft.Resources/calculateTemplateHash
- "List all operations?" -> GET /providers/Microsoft.Resources/operations
- "List all providers?" -> GET /subscriptions/{subscriptionId}/providers
- "List all deployments?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/
- "Delete a deployment?" -> DELETE /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Get deployment details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Update a deployment?" -> PUT /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Create a cancel?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/cancel
- "Create a exportTemplate?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/exportTemplate
- "List all operations?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations
- "Get operation details?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/operations/{operationId}
- "Create a validate?" -> POST /subscriptions/{subscriptionId}/providers/Microsoft.Resources/deployments/{deploymentName}/validate
- "Get provider details?" -> GET /subscriptions/{subscriptionId}/providers/{resourceProviderNamespace}
- "Create a register?" -> POST /subscriptions/{subscriptionId}/providers/{resourceProviderNamespace}/register
- "Create a unregister?" -> POST /subscriptions/{subscriptionId}/providers/{resourceProviderNamespace}/unregister
- "List all resources?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/resources
- "Create a moveResource?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{sourceResourceGroupName}/moveResources
- "Create a validateMoveResource?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{sourceResourceGroupName}/validateMoveResources
- "List all resourcegroups?" -> GET /subscriptions/{subscriptionId}/resourcegroups
- "Delete a resourcegroup?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}
- "Get resourcegroup details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}
- "Partially update a resourcegroup?" -> PATCH /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}
- "Update a resourcegroup?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}
- "List all operations?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/deployments/{deploymentName}/operations
- "Get operation details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/deployments/{deploymentName}/operations/{operationId}
- "Create a exportTemplate?" -> POST /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/exportTemplate
- "List all deployments?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/
- "Delete a deployment?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Get deployment details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Update a deployment?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}
- "Create a cancel?" -> POST /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}/cancel
- "Create a exportTemplate?" -> POST /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}/exportTemplate
- "Create a validate?" -> POST /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.Resources/deployments/{deploymentName}/validate
- "Delete a provider?" -> DELETE /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}
- "Get provider details?" -> GET /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}
- "Partially update a provider?" -> PATCH /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}
- "Update a provider?" -> PUT /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{parentResourcePath}/{resourceType}/{resourceName}
- "List all resources?" -> GET /subscriptions/{subscriptionId}/resources
- "List all tagNames?" -> GET /subscriptions/{subscriptionId}/tagNames
- "Delete a tagName?" -> DELETE /subscriptions/{subscriptionId}/tagNames/{tagName}
- "Update a tagName?" -> PUT /subscriptions/{subscriptionId}/tagNames/{tagName}
- "Delete a tagValue?" -> DELETE /subscriptions/{subscriptionId}/tagNames/{tagName}/tagValues/{tagValue}
- "Update a tagValue?" -> PUT /subscriptions/{subscriptionId}/tagNames/{tagName}/tagValues/{tagValue}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
