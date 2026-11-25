---
name: eventgridmanagementclient
description: "EventGridManagementClient API skill. Use when working with EventGridManagementClient for subscriptions, {scope}, providers. Covers 40 endpoints."
version: 1.0.0
generator: lapsh
---

# EventGridManagementClient
API version: 2019-06-01

## Auth
OAuth2

## Base URL
https://management.azure.com

## Setup
1. Configure auth: OAuth2
2. GET /providers/Microsoft.EventGrid/operations -- verify access
3. POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/listKeys -- create first listKeys

## Endpoints

40 endpoints across 3 groups. See references/api-spec.lap for full details.

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName} | Get a domain. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName} | Create or update a domain. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName} | Delete a domain. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName} | Update a domain. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/domains | List domains under an Azure subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains | List domains under a resource group. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/listKeys | List keys for a domain. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/regenerateKey | Regenerate key for a domain. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{domainTopicName} | Get a domain topic. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{domainTopicName} | Create or update a domain topic. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{domainTopicName} | Delete a domain topic. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics | List domain topics. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/eventSubscriptions | Get an aggregated list of all global event subscriptions under an Azure subscription. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/topicTypes/{topicTypeName}/eventSubscriptions | List all global event subscriptions for a topic type. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/eventSubscriptions | List all global event subscriptions under an Azure subscription and resource group. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topicTypes/{topicTypeName}/eventSubscriptions | List all global event subscriptions under a resource group for a topic type. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/locations/{location}/eventSubscriptions | List all regional event subscriptions under an Azure subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/locations/{location}/eventSubscriptions | List all regional event subscriptions under an Azure subscription and resource group. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/locations/{location}/topicTypes/{topicTypeName}/eventSubscriptions | List all regional event subscriptions under an Azure subscription for a topic type. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/locations/{location}/topicTypes/{topicTypeName}/eventSubscriptions | List all regional event subscriptions under an Azure subscription and resource group for a topic type. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{providerNamespace}/{resourceTypeName}/{resourceName}/providers/Microsoft.EventGrid/eventSubscriptions | List all event subscriptions for a specific topic. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{topicName}/providers/Microsoft.EventGrid/eventSubscriptions | List all event subscriptions for a specific domain topic. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName} | Get a topic. |
| PUT | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName} | Create a topic. |
| DELETE | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName} | Delete a topic. |
| PATCH | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName} | Update a topic. |
| GET | /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/topics | List topics under an Azure subscription. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics | List topics under a resource group. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}/listKeys | List keys for a topic. |
| POST | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}/regenerateKey | Regenerate key for a topic. |
| GET | /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{providerNamespace}/{resourceTypeName}/{resourceName}/providers/Microsoft.EventGrid/eventTypes | List topic event types. |

### {scope}
| Method | Path | Description |
|--------|------|-------------|
| GET | /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName} | Get an event subscription. |
| PUT | /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName} | Create or update an event subscription. |
| DELETE | /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName} | Delete an event subscription. |
| PATCH | /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName} | Update an event subscription. |
| POST | /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName}/getFullUrl | Get full URL of an event subscription. |

### providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /providers/Microsoft.EventGrid/operations | List available operations. |
| GET | /providers/Microsoft.EventGrid/topicTypes | List topic types. |
| GET | /providers/Microsoft.EventGrid/topicTypes/{topicTypeName} | Get a topic type. |
| GET | /providers/Microsoft.EventGrid/topicTypes/{topicTypeName}/eventTypes | List event types. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get domain details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}
- "Update a domain?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}
- "Delete a domain?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}
- "Partially update a domain?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}
- "List all domains?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/domains
- "List all domains?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains
- "Create a listKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/listKeys
- "Create a regenerateKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/regenerateKey
- "Get topic details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{domainTopicName}
- "Update a topic?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{domainTopicName}
- "Delete a topic?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{domainTopicName}
- "List all topics?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics
- "Get eventSubscription details?" -> GET /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName}
- "Update a eventSubscription?" -> PUT /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName}
- "Delete a eventSubscription?" -> DELETE /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName}
- "Partially update a eventSubscription?" -> PATCH /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName}
- "Create a getFullUrl?" -> POST /{scope}/providers/Microsoft.EventGrid/eventSubscriptions/{eventSubscriptionName}/getFullUrl
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/topicTypes/{topicTypeName}/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topicTypes/{topicTypeName}/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/locations/{location}/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/locations/{location}/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/locations/{location}/topicTypes/{topicTypeName}/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/locations/{location}/topicTypes/{topicTypeName}/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{providerNamespace}/{resourceTypeName}/{resourceName}/providers/Microsoft.EventGrid/eventSubscriptions
- "List all eventSubscriptions?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/domains/{domainName}/topics/{topicName}/providers/Microsoft.EventGrid/eventSubscriptions
- "List all operations?" -> GET /providers/Microsoft.EventGrid/operations
- "Get topic details?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}
- "Update a topic?" -> PUT /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}
- "Delete a topic?" -> DELETE /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}
- "Partially update a topic?" -> PATCH /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}
- "List all topics?" -> GET /subscriptions/{subscriptionId}/providers/Microsoft.EventGrid/topics
- "List all topics?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics
- "Create a listKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}/listKeys
- "Create a regenerateKey?" -> POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.EventGrid/topics/{topicName}/regenerateKey
- "List all eventTypes?" -> GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{providerNamespace}/{resourceTypeName}/{resourceName}/providers/Microsoft.EventGrid/eventTypes
- "List all topicTypes?" -> GET /providers/Microsoft.EventGrid/topicTypes
- "Get topicType details?" -> GET /providers/Microsoft.EventGrid/topicTypes/{topicTypeName}
- "List all eventTypes?" -> GET /providers/Microsoft.EventGrid/topicTypes/{topicTypeName}/eventTypes
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
