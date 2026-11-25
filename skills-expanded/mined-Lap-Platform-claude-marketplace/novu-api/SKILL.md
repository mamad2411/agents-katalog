---
name: novu-api
description: "Novu API skill. Use when working with Novu for environments, events, notifications. Covers 95 endpoints."
version: 1.0.0
generator: lapsh
---

# Novu API
API version: 3.14.0

## Auth
ApiKey Authorization in header

## Base URL
https://api.novu.co

## Setup
1. Set your API key in the appropriate header
2. GET /v1/environments -- verify access
3. POST /v1/environments -- create first environments

## Endpoints

95 endpoints across 14 groups. See references/api-spec.lap for full details.

### environments
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/environments | Create an environment |
| GET | /v1/environments | List all environments |
| PUT | /v1/environments/{environmentId} | Update an environment |
| DELETE | /v1/environments/{environmentId} | Delete an environment |
| GET | /v2/environments/{environmentId}/tags | List environment tags |
| POST | /v2/environments/{targetEnvironmentId}/publish | Publish resources to target environment |
| POST | /v2/environments/{targetEnvironmentId}/diff | Compare resources between environments |

### events
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/events/trigger | Trigger event |
| POST | /v1/events/trigger/bulk | Bulk trigger event |
| POST | /v1/events/trigger/broadcast | Broadcast event to all |
| DELETE | /v1/events/trigger/{transactionId} | Cancel triggered event |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/notifications | List all events |
| GET | /v1/notifications/{notificationId} | Retrieve an event |

### integrations
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/integrations | List all integrations |
| POST | /v1/integrations | Create an integration |
| GET | /v1/integrations/active | List active integrations |
| PUT | /v1/integrations/{integrationId} | Update an integration |
| DELETE | /v1/integrations/{integrationId} | Delete an integration |
| POST | /v1/integrations/{integrationId}/auto-configure | Auto-configure an integration for inbound webhooks |
| POST | /v1/integrations/{integrationId}/set-primary | Update integration as primary |
| POST | /v1/integrations/chat/oauth | Generate chat OAuth URL |

### contexts
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/contexts | Create a context |
| GET | /v2/contexts | List all contexts |
| PATCH | /v2/contexts/{type}/{id} | Update a context |
| GET | /v2/contexts/{type}/{id} | Retrieve a context |
| DELETE | /v2/contexts/{type}/{id} | Delete a context |

### subscribers
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/subscribers/bulk | Bulk create subscribers |
| PUT | /v1/subscribers/{subscriberId}/credentials | Update provider credentials |
| PATCH | /v1/subscribers/{subscriberId}/credentials | Upsert provider credentials |
| DELETE | /v1/subscribers/{subscriberId}/credentials/{providerId} | Delete provider credentials |
| PATCH | /v1/subscribers/{subscriberId}/online-status | Update subscriber online status |
| GET | /v1/subscribers/{subscriberId}/notifications/feed | Retrieve subscriber notifications |
| GET | /v1/subscribers/{subscriberId}/notifications/unseen | Retrieve unseen notifications count |
| POST | /v1/subscribers/{subscriberId}/messages/mark-as | Update notifications state |
| POST | /v1/subscribers/{subscriberId}/messages/mark-all | Update all notifications state |
| POST | /v1/subscribers/{subscriberId}/messages/{messageId}/actions/{type} | Update notification action status |
| GET | /v2/subscribers | Search subscribers |
| POST | /v2/subscribers | Create a subscriber |
| GET | /v2/subscribers/{subscriberId} | Retrieve a subscriber |
| PATCH | /v2/subscribers/{subscriberId} | Update a subscriber |
| DELETE | /v2/subscribers/{subscriberId} | Delete a subscriber |
| GET | /v2/subscribers/{subscriberId}/preferences | Retrieve subscriber preferences |
| PATCH | /v2/subscribers/{subscriberId}/preferences | Update subscriber preferences |
| PATCH | /v2/subscribers/{subscriberId}/preferences/bulk | Bulk update subscriber preferences |
| GET | /v2/subscribers/{subscriberId}/subscriptions | Retrieve subscriber subscriptions |

### layouts
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/layouts | Create a layout |
| GET | /v2/layouts | List all layouts |
| PUT | /v2/layouts/{layoutId} | Update a layout |
| GET | /v2/layouts/{layoutId} | Retrieve a layout |
| DELETE | /v2/layouts/{layoutId} | Delete a layout |
| POST | /v2/layouts/{layoutId}/duplicate | Duplicate a layout |
| POST | /v2/layouts/{layoutId}/preview | Generate layout preview |
| GET | /v2/layouts/{layoutId}/usage | Get layout usage |

### messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/messages | List all messages |
| DELETE | /v1/messages/{messageId} | Delete a message |
| DELETE | /v1/messages/transaction/{transactionId} | Delete messages by transactionId |

### topics
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/topics/{topicKey}/subscribers/{externalSubscriberId} | Check topic subscriber |
| GET | /v2/topics | List all topics |
| POST | /v2/topics | Create a topic |
| GET | /v2/topics/{topicKey} | Retrieve a topic |
| PATCH | /v2/topics/{topicKey} | Update a topic |
| DELETE | /v2/topics/{topicKey} | Delete a topic |
| GET | /v2/topics/{topicKey}/subscriptions | List topic subscriptions |
| POST | /v2/topics/{topicKey}/subscriptions | Create topic subscriptions |
| DELETE | /v2/topics/{topicKey}/subscriptions | Delete topic subscriptions |
| GET | /v2/topics/{topicKey}/subscriptions/{identifier} | Retrieve a topic subscription |
| PATCH | /v2/topics/{topicKey}/subscriptions/{identifier} | Update a topic subscription |

### workflows
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/workflows | Create a workflow |
| GET | /v2/workflows | List all workflows |
| PUT | /v2/workflows/{workflowId}/sync | Sync a workflow |
| PUT | /v2/workflows/{workflowId} | Update a workflow |
| GET | /v2/workflows/{workflowId} | Retrieve a workflow |
| DELETE | /v2/workflows/{workflowId} | Delete a workflow |
| PATCH | /v2/workflows/{workflowId} | Update a workflow |
| GET | /v2/workflows/{workflowId}/steps/{stepId} | Retrieve workflow step |

### channel-connections
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/channel-connections | List all channel connections |
| POST | /v1/channel-connections | Create a channel connection |
| GET | /v1/channel-connections/{identifier} | Retrieve a channel connection |
| PATCH | /v1/channel-connections/{identifier} | Update a channel connection |
| DELETE | /v1/channel-connections/{identifier} | Delete a channel connection |

### channel-endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/channel-endpoints | List all channel endpoints |
| POST | /v1/channel-endpoints | Create a channel endpoint |
| GET | /v1/channel-endpoints/{identifier} | Retrieve a channel endpoint |
| PATCH | /v1/channel-endpoints/{identifier} | Update a channel endpoint |
| DELETE | /v1/channel-endpoints/{identifier} | Delete a channel endpoint |

### translations
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/translations/upload | Upload translation files |
| POST | /v2/translations | Create a translation |
| GET | /v2/translations/master-json | Retrieve master translations JSON |
| POST | /v2/translations/master-json | Import master translations JSON |
| POST | /v2/translations/master-json/upload | Upload master translations JSON file |
| GET | /v2/translations/group/{resourceType}/{resourceId} | Retrieve a translation group |
| GET | /v2/translations/{resourceType}/{resourceId}/{locale} | Retrieve a translation |
| DELETE | /v2/translations/{resourceType}/{resourceId}/{locale} | Delete a translation |
| DELETE | /v2/translations/{resourceType}/{resourceId} | Delete a translation group |

### inbound-webhooks
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/inbound-webhooks/delivery-providers/{environmentId}/{integrationId} | Track activity and engagement events |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a environment?" -> POST /v1/environments
- "List all environments?" -> GET /v1/environments
- "Update a environment?" -> PUT /v1/environments/{environmentId}
- "Delete a environment?" -> DELETE /v1/environments/{environmentId}
- "Create a trigger?" -> POST /v1/events/trigger
- "Create a bulk?" -> POST /v1/events/trigger/bulk
- "Create a broadcast?" -> POST /v1/events/trigger/broadcast
- "Delete a trigger?" -> DELETE /v1/events/trigger/{transactionId}
- "Search notifications?" -> GET /v1/notifications
- "Get notification details?" -> GET /v1/notifications/{notificationId}
- "List all integrations?" -> GET /v1/integrations
- "Create a integration?" -> POST /v1/integrations
- "List all active?" -> GET /v1/integrations/active
- "Update a integration?" -> PUT /v1/integrations/{integrationId}
- "Delete a integration?" -> DELETE /v1/integrations/{integrationId}
- "Create a auto-configure?" -> POST /v1/integrations/{integrationId}/auto-configure
- "Create a set-primary?" -> POST /v1/integrations/{integrationId}/set-primary
- "Create a oauth?" -> POST /v1/integrations/chat/oauth
- "Create a context?" -> POST /v2/contexts
- "Search contexts?" -> GET /v2/contexts
- "Partially update a context?" -> PATCH /v2/contexts/{type}/{id}
- "Get context details?" -> GET /v2/contexts/{type}/{id}
- "Delete a context?" -> DELETE /v2/contexts/{type}/{id}
- "Create a bulk?" -> POST /v1/subscribers/bulk
- "Delete a credential?" -> DELETE /v1/subscribers/{subscriberId}/credentials/{providerId}
- "List all feed?" -> GET /v1/subscribers/{subscriberId}/notifications/feed
- "List all unseen?" -> GET /v1/subscribers/{subscriberId}/notifications/unseen
- "Create a mark-a?" -> POST /v1/subscribers/{subscriberId}/messages/mark-as
- "Create a mark-all?" -> POST /v1/subscribers/{subscriberId}/messages/mark-all
- "List all subscribers?" -> GET /v2/subscribers
- "Create a subscriber?" -> POST /v2/subscribers
- "Get subscriber details?" -> GET /v2/subscribers/{subscriberId}
- "Partially update a subscriber?" -> PATCH /v2/subscribers/{subscriberId}
- "Delete a subscriber?" -> DELETE /v2/subscribers/{subscriberId}
- "List all preferences?" -> GET /v2/subscribers/{subscriberId}/preferences
- "List all subscriptions?" -> GET /v2/subscribers/{subscriberId}/subscriptions
- "Create a layout?" -> POST /v2/layouts
- "Search layouts?" -> GET /v2/layouts
- "Update a layout?" -> PUT /v2/layouts/{layoutId}
- "Get layout details?" -> GET /v2/layouts/{layoutId}
- "Delete a layout?" -> DELETE /v2/layouts/{layoutId}
- "Create a duplicate?" -> POST /v2/layouts/{layoutId}/duplicate
- "Create a preview?" -> POST /v2/layouts/{layoutId}/preview
- "List all usage?" -> GET /v2/layouts/{layoutId}/usage
- "List all messages?" -> GET /v1/messages
- "Delete a message?" -> DELETE /v1/messages/{messageId}
- "Delete a transaction?" -> DELETE /v1/messages/transaction/{transactionId}
- "Get subscriber details?" -> GET /v1/topics/{topicKey}/subscribers/{externalSubscriberId}
- "List all topics?" -> GET /v2/topics
- "Create a topic?" -> POST /v2/topics
- "Get topic details?" -> GET /v2/topics/{topicKey}
- "Partially update a topic?" -> PATCH /v2/topics/{topicKey}
- "Delete a topic?" -> DELETE /v2/topics/{topicKey}
- "List all subscriptions?" -> GET /v2/topics/{topicKey}/subscriptions
- "Create a subscription?" -> POST /v2/topics/{topicKey}/subscriptions
- "Get subscription details?" -> GET /v2/topics/{topicKey}/subscriptions/{identifier}
- "Partially update a subscription?" -> PATCH /v2/topics/{topicKey}/subscriptions/{identifier}
- "Create a workflow?" -> POST /v2/workflows
- "Search workflows?" -> GET /v2/workflows
- "Update a workflow?" -> PUT /v2/workflows/{workflowId}
- "Get workflow details?" -> GET /v2/workflows/{workflowId}
- "Delete a workflow?" -> DELETE /v2/workflows/{workflowId}
- "Partially update a workflow?" -> PATCH /v2/workflows/{workflowId}
- "Get step details?" -> GET /v2/workflows/{workflowId}/steps/{stepId}
- "List all tags?" -> GET /v2/environments/{environmentId}/tags
- "Create a publish?" -> POST /v2/environments/{targetEnvironmentId}/publish
- "Create a diff?" -> POST /v2/environments/{targetEnvironmentId}/diff
- "List all channel-connections?" -> GET /v1/channel-connections
- "Create a channel-connection?" -> POST /v1/channel-connections
- "Get channel-connection details?" -> GET /v1/channel-connections/{identifier}
- "Partially update a channel-connection?" -> PATCH /v1/channel-connections/{identifier}
- "Delete a channel-connection?" -> DELETE /v1/channel-connections/{identifier}
- "List all channel-endpoints?" -> GET /v1/channel-endpoints
- "Create a channel-endpoint?" -> POST /v1/channel-endpoints
- "Get channel-endpoint details?" -> GET /v1/channel-endpoints/{identifier}
- "Partially update a channel-endpoint?" -> PATCH /v1/channel-endpoints/{identifier}
- "Delete a channel-endpoint?" -> DELETE /v1/channel-endpoints/{identifier}
- "Create a upload?" -> POST /v2/translations/upload
- "Create a translation?" -> POST /v2/translations
- "List all master-json?" -> GET /v2/translations/master-json
- "Create a master-json?" -> POST /v2/translations/master-json
- "Create a upload?" -> POST /v2/translations/master-json/upload
- "Get group details?" -> GET /v2/translations/group/{resourceType}/{resourceId}
- "Get translation details?" -> GET /v2/translations/{resourceType}/{resourceId}/{locale}
- "Delete a translation?" -> DELETE /v2/translations/{resourceType}/{resourceId}/{locale}
- "Delete a translation?" -> DELETE /v2/translations/{resourceType}/{resourceId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
