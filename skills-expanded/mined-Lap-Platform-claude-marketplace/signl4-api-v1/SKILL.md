---
name: signl4-api-v1
description: "SIGNL4 API V1 API skill. Use when working with SIGNL4 API V1 for alerts, categories, events. Covers 109 endpoints."
version: 1.0.0
generator: lapsh
---

# SIGNL4 API V1
API version: 1

## Auth
ApiKey x-s4-api-key in header | ApiKey x-s4-api-key in query | OAuth2

## Base URL
https://connect.signl4.com/api

## Setup
1. Set your API key in the appropriate header
2. GET /alerts/report -- verify access
3. POST /alerts -- create first alerts

## Endpoints

109 endpoints across 9 groups. See references/api-spec.lap for full details.

### alerts
| Method | Path | Description |
|--------|------|-------------|
| POST | /alerts | Trigger Alert |
| GET | /alerts/{alertId} | Get Alert |
| POST | /alerts/{alertId}/acknowledge | Acknowledge an alert |
| POST | /alerts/{alertId}/annotate | Annotate Alert |
| GET | /alerts/{alertId}/annotations | Get annotations of an alert |
| GET | /alerts/{alertId}/attachments | Get attachments of an alert |
| GET | /alerts/{alertId}/attachments/{attachmentId} | Gets a specified attachment of a specified alert. |
| POST | /alerts/{alertId}/close | Close an alert |
| GET | /alerts/{alertId}/notifications | Get alert notifications |
| GET | /alerts/{alertId}/overview | Get an overview alert. |
| POST | /alerts/{alertId}/undoAcknowledge | Undo the acknowledgement of an alert. |
| POST | /alerts/{alertId}/undoClose | Undo the closure of an alert. |
| POST | /alerts/acknowledgeAll | Confirms all visible alerts |
| POST | /alerts/acknowledgeMultiple | Acknowlegde multiple alerts |
| POST | /alerts/closeAll | Close all acknowledged alerts. |
| POST | /alerts/closeMultiple | Close multiple alerts |
| POST | /alerts/paged | Gets alerts paged |
| GET | /alerts/report | Get Alert Report |
| POST | /alerts/undoAcknowledgeMultiple | Queue undo of multiple acknowledgments. |
| POST | /alerts/undoCloseMultiple | Withdraw closure of multiple alerts |

### categories
| Method | Path | Description |
|--------|------|-------------|
| GET | /categories/{teamId} | Get all categories |
| POST | /categories/{teamId} | Create a new category |
| GET | /categories/{teamId}/{categoryId} | Get a specific category |
| PUT | /categories/{teamId}/{categoryId} | Update an existing category |
| DELETE | /categories/{teamId}/{categoryId} | Delete an existing category |
| GET | /categories/{teamId}/{categoryId}/metrics | Get metrics for a specific category |
| GET | /categories/{teamId}/{categoryId}/subscriptions | Get category subscriptions |
| POST | /categories/{teamId}/{categoryId}/subscriptions | Set category subscriptions |
| GET | /categories/{teamId}/metrics | Get metrics for all categories |
| GET | /categories/images | Gets the names of all alert category images. |

### events
| Method | Path | Description |
|--------|------|-------------|
| GET | /events/{eventId}/overview | Get overview event |
| GET | /events/{eventId}/parameters | Get event parameters |
| POST | /events/{webhookIdOrTeamId} | Create new event |
| POST | /events/paged | Get overview event paged. |

### prepaid
| Method | Path | Description |
|--------|------|-------------|
| PUT | /prepaid/{subscriptionId}/prepaidSettings | Update a subscription's current prepaid settings. |
| GET | /prepaid/balance | Get your subscription's current prepaid balance. |
| GET | /prepaid/settings | Get your subscription's current prepaid settings. |
| PUT | /prepaid/settings | Update your subscription's current prepaid settings. |
| GET | /prepaid/transactions | Get your subscription's prepaid transactions. |

### scripts
| Method | Path | Description |
|--------|------|-------------|
| GET | /scripts/instances | Returns all script instances of the SIGNL4 team |
| POST | /scripts/instances | Creates a new script instance in the in the SIGNL4 team. |
| GET | /scripts/instances/{instanceId} | Returns all information about a given script instance which includes its runtime status. |
| PUT | /scripts/instances/{instanceId} | Updates a given script instance, typically used for updating the configuration of a script. |
| DELETE | /scripts/instances/{instanceId} | Deletes a script instance. |
| PUT | /scripts/instances/{instanceId}/data | Updates custom data of a given script instance which includes its display name. |
| POST | /scripts/instances/{instanceId}/disable | Disables a given script instance. |
| POST | /scripts/instances/{instanceId}/enable | Enables a script instance. |
| GET | /scripts/inventory | Returns all available inventory scripts which can be added to a SIGNL4 subscription. |
| GET | /scripts/inventory/parsed | Returns all inventory scripts. |
| GET | /scripts/inventory/parsed/{scriptId} | Returns an inventory script by its id. |

### subscriptions
| Method | Path | Description |
|--------|------|-------------|
| GET | /subscriptions | Get infos of all available/managed subscriptions. |
| GET | /subscriptions/{subscriptionId} | Get infos of a specific subscription. |
| GET | /subscriptions/{subscriptionId}/channelPrices | Returns the subscription's channel price information. |
| GET | /subscriptions/{subscriptionId}/features | Returns the features of a specified subscription. |
| GET | /subscriptions/{subscriptionId}/inboundVoiceNumberLicenses | Gets a subscription's voice number licenses. |
| GET | /subscriptions/{subscriptionId}/prepaidBalance | Get a subscription's current prepaid balance. |
| GET | /subscriptions/{subscriptionId}/prepaidSettings | Get a subscription's current prepaid settings. |
| GET | /subscriptions/{subscriptionId}/prepaidTransactions | Get a subscription's prepaid transactions. |
| PUT | /subscriptions/{subscriptionId}/profile | Updates a subscriptions profile. |
| GET | /subscriptions/{subscriptionId}/settings | Gets a subscription's global settings. |
| PUT | /subscriptions/{subscriptionId}/settings | Updates a subscriptions global settings. |
| GET | /subscriptions/{subscriptionId}/teams | Get infos for all teams of the subscription. |
| GET | /subscriptions/{subscriptionId}/userLicenses | Gets a subscription's user licenses. |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams | Get infos of all teams. |
| POST | /teams | Adds another team to the subscription of the user |
| GET | /teams/{teamId} | Gets infos of a specific team. |
| DELETE | /teams/{teamId} | Deletes a team from the subscription. |
| GET | /teams/{teamId}/alertReports | Get information about downloadable alert reports |
| GET | /teams/{teamId}/alertReports/{fileName} | Returns Alert Report |
| GET | /teams/{teamId}/alertSettings | Gets alert settings of a specific team. |
| POST | /teams/{teamId}/alertSettings | Sets alert settings of a specific team. |
| GET | /teams/{teamId}/dutyReports | Get Information about downloadable reports |
| GET | /teams/{teamId}/dutyReports/{fileName} | Download duty report with a specific fileName |
| GET | /teams/{teamId}/dutysummary | Get duty assistant info for a team |
| GET | /teams/{teamId}/eventSources | Gets event sources of a specific team. |
| GET | /teams/{teamId}/memberships | Get all invites of a team. |
| POST | /teams/{teamId}/memberships | Invite users to a team |
| PUT | /teams/{teamId}/memberships/{userId} | Update user's team membership. |
| DELETE | /teams/{teamId}/memberships/{userId} | Removes a user or invitation from a team |
| POST | /teams/{teamId}/memberships/resendInviteMail | Sends invite email again if an invite exists |
| PUT | /teams/{teamId}/profile | Updates team profile of a team |
| GET | /teams/{teamId}/schedules | Returns information about all duties that belong to the team. |
| POST | /teams/{teamId}/schedules | Create/Update given duty schedule. |
| DELETE | /teams/{teamId}/schedules/{dutyId} | Delete a specific duty. |
| GET | /teams/{teamId}/schedules/{scheduleId} | Returns information of the duty schedule with the specified Id. |
| POST | /teams/{teamId}/schedules/deleteRange | Delete duty schedules in range |
| POST | /teams/{teamId}/schedules/multiple | Save multiple schedules. It is possible to override existing schedules if you wish |
| GET | /teams/{teamId}/setupProgress | Gets setup progress of a specific team. |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Get all Users |
| GET | /users/{userId} | Get User by Id |
| DELETE | /users/{userId} | Deletes user account. |
| PUT | /users/{userId}/changePassword | Updates the password of a user |
| POST | /users/{userId}/checkPermissions | Checks if a user has the provided permission. |
| GET | /users/{userId}/dutyStatus | Get duty status by user Id |
| GET | /users/{userId}/image |  |
| POST | /users/{userId}/image | Uploaded a profile image for a specified user. |
| POST | /users/{userId}/location | Set location of an user |
| PUT | /users/{userId}/profile | Updates user profile of an user |
| POST | /users/{userId}/punchIn | Punch User in |
| POST | /users/{userId}/punchInAsManager | Punch User in as Manager |
| POST | /users/{userId}/punchOut |  |
| GET | /users/{userId}/setupProgress | Gets setup progress of a specific user. |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks | Get Webhooks |
| POST | /webhooks | Create Webhook |
| GET | /webhooks/{webhookId} | Get Webhook by Id |
| PUT | /webhooks/{webhookId} | Update Webhook by Id |
| DELETE | /webhooks/{webhookId} | Delete Webhook by Id |
| POST | /webhooks/{webhookId}/disable | Ability to enable a webHook. |
| POST | /webhooks/{webhookId}/enable | Ability to disable a webHook. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a alert?" -> POST /alerts
- "Get alert details?" -> GET /alerts/{alertId}
- "Create a acknowledge?" -> POST /alerts/{alertId}/acknowledge
- "Create a annotate?" -> POST /alerts/{alertId}/annotate
- "List all annotations?" -> GET /alerts/{alertId}/annotations
- "List all attachments?" -> GET /alerts/{alertId}/attachments
- "Get attachment details?" -> GET /alerts/{alertId}/attachments/{attachmentId}
- "Create a close?" -> POST /alerts/{alertId}/close
- "List all notifications?" -> GET /alerts/{alertId}/notifications
- "List all overview?" -> GET /alerts/{alertId}/overview
- "Create a undoAcknowledge?" -> POST /alerts/{alertId}/undoAcknowledge
- "Create a undoClose?" -> POST /alerts/{alertId}/undoClose
- "Create a acknowledgeAll?" -> POST /alerts/acknowledgeAll
- "Create a acknowledgeMultiple?" -> POST /alerts/acknowledgeMultiple
- "Create a closeAll?" -> POST /alerts/closeAll
- "Create a closeMultiple?" -> POST /alerts/closeMultiple
- "Create a paged?" -> POST /alerts/paged
- "List all report?" -> GET /alerts/report
- "Create a undoAcknowledgeMultiple?" -> POST /alerts/undoAcknowledgeMultiple
- "Create a undoCloseMultiple?" -> POST /alerts/undoCloseMultiple
- "Get category details?" -> GET /categories/{teamId}
- "Get category details?" -> GET /categories/{teamId}/{categoryId}
- "Update a category?" -> PUT /categories/{teamId}/{categoryId}
- "Delete a category?" -> DELETE /categories/{teamId}/{categoryId}
- "List all metrics?" -> GET /categories/{teamId}/{categoryId}/metrics
- "List all subscriptions?" -> GET /categories/{teamId}/{categoryId}/subscriptions
- "Create a subscription?" -> POST /categories/{teamId}/{categoryId}/subscriptions
- "List all metrics?" -> GET /categories/{teamId}/metrics
- "List all images?" -> GET /categories/images
- "List all overview?" -> GET /events/{eventId}/overview
- "List all parameters?" -> GET /events/{eventId}/parameters
- "Create a paged?" -> POST /events/paged
- "List all balance?" -> GET /prepaid/balance
- "List all settings?" -> GET /prepaid/settings
- "List all transactions?" -> GET /prepaid/transactions
- "List all instances?" -> GET /scripts/instances
- "Create a instance?" -> POST /scripts/instances
- "Get instance details?" -> GET /scripts/instances/{instanceId}
- "Update a instance?" -> PUT /scripts/instances/{instanceId}
- "Delete a instance?" -> DELETE /scripts/instances/{instanceId}
- "Create a disable?" -> POST /scripts/instances/{instanceId}/disable
- "Create a enable?" -> POST /scripts/instances/{instanceId}/enable
- "List all inventory?" -> GET /scripts/inventory
- "List all parsed?" -> GET /scripts/inventory/parsed
- "Get parsed details?" -> GET /scripts/inventory/parsed/{scriptId}
- "List all subscriptions?" -> GET /subscriptions
- "Get subscription details?" -> GET /subscriptions/{subscriptionId}
- "List all channelPrices?" -> GET /subscriptions/{subscriptionId}/channelPrices
- "List all features?" -> GET /subscriptions/{subscriptionId}/features
- "List all inboundVoiceNumberLicenses?" -> GET /subscriptions/{subscriptionId}/inboundVoiceNumberLicenses
- "List all prepaidBalance?" -> GET /subscriptions/{subscriptionId}/prepaidBalance
- "List all prepaidSettings?" -> GET /subscriptions/{subscriptionId}/prepaidSettings
- "List all prepaidTransactions?" -> GET /subscriptions/{subscriptionId}/prepaidTransactions
- "List all settings?" -> GET /subscriptions/{subscriptionId}/settings
- "List all teams?" -> GET /subscriptions/{subscriptionId}/teams
- "List all userLicenses?" -> GET /subscriptions/{subscriptionId}/userLicenses
- "List all teams?" -> GET /teams
- "Create a team?" -> POST /teams
- "Get team details?" -> GET /teams/{teamId}
- "Delete a team?" -> DELETE /teams/{teamId}
- "List all alertReports?" -> GET /teams/{teamId}/alertReports
- "Get alertReport details?" -> GET /teams/{teamId}/alertReports/{fileName}
- "List all alertSettings?" -> GET /teams/{teamId}/alertSettings
- "Create a alertSetting?" -> POST /teams/{teamId}/alertSettings
- "List all dutyReports?" -> GET /teams/{teamId}/dutyReports
- "Get dutyReport details?" -> GET /teams/{teamId}/dutyReports/{fileName}
- "List all dutysummary?" -> GET /teams/{teamId}/dutysummary
- "List all eventSources?" -> GET /teams/{teamId}/eventSources
- "List all memberships?" -> GET /teams/{teamId}/memberships
- "Create a membership?" -> POST /teams/{teamId}/memberships
- "Update a membership?" -> PUT /teams/{teamId}/memberships/{userId}
- "Delete a membership?" -> DELETE /teams/{teamId}/memberships/{userId}
- "Create a resendInviteMail?" -> POST /teams/{teamId}/memberships/resendInviteMail
- "List all schedules?" -> GET /teams/{teamId}/schedules
- "Create a schedule?" -> POST /teams/{teamId}/schedules
- "Delete a schedule?" -> DELETE /teams/{teamId}/schedules/{dutyId}
- "Get schedule details?" -> GET /teams/{teamId}/schedules/{scheduleId}
- "Create a deleteRange?" -> POST /teams/{teamId}/schedules/deleteRange
- "Create a multiple?" -> POST /teams/{teamId}/schedules/multiple
- "List all setupProgress?" -> GET /teams/{teamId}/setupProgress
- "List all users?" -> GET /users
- "Get user details?" -> GET /users/{userId}
- "Delete a user?" -> DELETE /users/{userId}
- "Create a checkPermission?" -> POST /users/{userId}/checkPermissions
- "List all dutyStatus?" -> GET /users/{userId}/dutyStatus
- "List all image?" -> GET /users/{userId}/image
- "Create a image?" -> POST /users/{userId}/image
- "Create a location?" -> POST /users/{userId}/location
- "Create a punchIn?" -> POST /users/{userId}/punchIn
- "Create a punchInAsManager?" -> POST /users/{userId}/punchInAsManager
- "Create a punchOut?" -> POST /users/{userId}/punchOut
- "List all setupProgress?" -> GET /users/{userId}/setupProgress
- "List all webhooks?" -> GET /webhooks
- "Create a webhook?" -> POST /webhooks
- "Get webhook details?" -> GET /webhooks/{webhookId}
- "Update a webhook?" -> PUT /webhooks/{webhookId}
- "Delete a webhook?" -> DELETE /webhooks/{webhookId}
- "Create a disable?" -> POST /webhooks/{webhookId}/disable
- "Create a enable?" -> POST /webhooks/{webhookId}/enable
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
