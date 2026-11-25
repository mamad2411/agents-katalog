---
name: victorops-api
description: "VictorOps API skill. Use when working with VictorOps for api-public, api-reporting. Covers 96 endpoints."
version: 1.0.0
generator: lapsh
---

# VictorOps API
API version: 0.0.3

## Auth
ApiKey X-VO-Api-Key in header

## Base URL
https://api.victorops.com/

## Setup
1. Set your API key in the appropriate header
2. GET /api-public/v1/user -- verify access
3. POST /api-public/v1/user -- create first user

## Endpoints

96 endpoints across 2 groups. See references/api-spec.lap for full details.

### api-public
| Method | Path | Description |
|--------|------|-------------|
| POST | /api-public/v1/user | Add a user |
| GET | /api-public/v1/user | List users |
| GET | /api-public/v2/user | List users |
| POST | /api-public/v1/user/batch | Add multiple users |
| GET | /api-public/v1/user/{user} | Retrieve information for a user |
| PUT | /api-public/v1/user/{user} | Update a user |
| DELETE | /api-public/v1/user/{user} | Remove a user |
| GET | /api-public/v1/user/{user}/teams | Retrieve the user's team membership |
| GET | /api-public/v1/policies/types/notifications | Get the available notification types |
| GET | /api-public/v1/policies/types/contacts | Get the available contact types |
| GET | /api-public/v1/policies/types/timeouts | Get the available timeout values |
| GET | /api-public/v1/profile/{username}/policies | Get the user's primary paging policy |
| POST | /api-public/v1/profile/{username}/policies | Create a paging policy step |
| GET | /api-public/v1/profile/{username}/policies/{step} | Get a paging policy step |
| PUT | /api-public/v1/profile/{username}/policies/{step} | Update a paging policy step |
| POST | /api-public/v1/profile/{username}/policies/{step} | Create a rule for a paging policy step |
| GET | /api-public/v1/profile/{username}/policies/{step}/{rule} | Get a rule from a paging policy step |
| PUT | /api-public/v1/profile/{username}/policies/{step}/{rule} | Update a rule for a paging policy step |
| DELETE | /api-public/v1/profile/{username}/policies/{step}/{rule} | Delete a rule from a paging policy step |
| GET | /api-public/v2/profile/{username}/policies | Get the user's paging policies |
| GET | /api-public/v1/user/{user}/contact-methods | Get a list of all contact methods for a user |
| GET | /api-public/v1/user/{user}/contact-methods/devices | Get a list of all contact devices for a user |
| GET | /api-public/v1/user/{user}/contact-methods/devices/{contactId} | Get the indicated contact device for a user |
| PUT | /api-public/v1/user/{user}/contact-methods/devices/{contactId} | Update a contact device for a user |
| DELETE | /api-public/v1/user/{user}/contact-methods/devices/{contactId} | Delete a contact device for a user |
| GET | /api-public/v1/user/{user}/contact-methods/emails | Get a list of all contact emails for a user |
| POST | /api-public/v1/user/{user}/contact-methods/emails | Create a contact emails for a user |
| GET | /api-public/v1/user/{user}/contact-methods/emails/{contactId} | Get the indicated contact email for a user |
| DELETE | /api-public/v1/user/{user}/contact-methods/emails/{contactId} | Delete a contact email for a user |
| GET | /api-public/v1/user/{user}/contact-methods/phones | Get a list of all contact phones for a user |
| POST | /api-public/v1/user/{user}/contact-methods/phones | Create a contact phones for a user |
| GET | /api-public/v1/user/{user}/contact-methods/phones/{contactId} | Get the indicated contact phone for a user |
| DELETE | /api-public/v1/user/{user}/contact-methods/phones/{contactId} | Delete a contact phone for a user |
| GET | /api-public/v1/user/{user}/policies | Get a list of paging policies for a user |
| GET | /api-public/v1/user/{user}/oncall/schedule | Get a user's on-call schedule |
| GET | /api-public/v2/user/{user}/oncall/schedule | Get a user's on-call schedule |
| GET | /api-public/v1/team/{team}/oncall/schedule | Get a team's on-call schedule |
| GET | /api-public/v2/team/{team}/oncall/schedule | Get a team's on-call schedule |
| GET | /api-public/v1/oncall/current | Get an organization's on-call users |
| PATCH | /api-public/v1/team/{team}/oncall/user | Create an on-call override (take on-call) |
| PATCH | /api-public/v1/policies/{policy}/oncall/user | Create an on-call override (take on-call) |
| GET | /api-public/v1/incidents/{incidentNumber} | Get a single incident |
| GET | /api-public/v1/incidents | Get current incident information |
| POST | /api-public/v1/incidents | Create a new incident |
| PATCH | /api-public/v1/incidents/ack | Acknowledge an incident or list of incidents |
| POST | /api-public/v1/incidents/reroute | Reroute one or more incidents to one or more new routable destinations. |
| PATCH | /api-public/v1/incidents/resolve | Resolve an incident or list of incidents |
| PATCH | /api-public/v1/incidents/byUser/ack | Acknowledge all incidents for which a user was paged. |
| PATCH | /api-public/v1/incidents/byUser/resolve | Resolve all incidents for which a user was paged. |
| GET | /api-public/v1/incidents/{incidentNumber}/notes | Get the notes associated with an incident |
| POST | /api-public/v1/incidents/{incidentNumber}/notes | Create a new Note |
| PUT | /api-public/v1/incidents/{incidentNumber}/notes/{noteName} | Update a Note |
| DELETE | /api-public/v1/incidents/{incidentNumber}/notes/{noteName} | Delete a Note |
| GET | /api-public/v1/alerts/{uuid} | Retrieve alert details. |
| GET | /api-public/v1/org/routing-keys | List routing keys with associated teams |
| POST | /api-public/v1/org/routing-keys | Create a new routing key |
| GET | /api-public/v1/overrides | List the scheduled overrides |
| POST | /api-public/v1/overrides | Creates a new scheduled override |
| GET | /api-public/v1/overrides/{publicId} | Get the specified scheduled override |
| DELETE | /api-public/v1/overrides/{publicId} | Deletes a scheduled override |
| GET | /api-public/v1/overrides/{publicId}/assignments | Get the specified scheduled override |
| GET | /api-public/v1/overrides/{publicId}/assignments/{policySlug} | Get the specified scheduled override assignment |
| PUT | /api-public/v1/overrides/{publicId}/assignments/{policySlug} | Update the scheduled override assignment |
| DELETE | /api-public/v1/overrides/{publicId}/assignments/{policySlug} | Delete the scheduled override assignment |
| GET | /api-public/v1/teams/{team}/rotations | Get all rotation groups for a team |
| POST | /api-public/v1/teams/{team}/rotations | Create a rotation group |
| DELETE | /api-public/v1/teams/{team}/rotations/{groupId} | Delete a rotation group |
| GET | /api-public/v1/teams/{team}/rotations/{groupId}/{shiftId}/scheduled | Get the scheduled user for a shift |
| PUT | /api-public/v1/teams/{team}/rotations/{groupId}/{shiftId}/scheduled | Set the scheduled user for a shift |
| GET | /api-public/v2/team/{team}/rotations | Get all rotations and some rotation details for a team |
| GET | /api-public/v1/webhooks | Get all of your organization's webhooks |
| GET | /api-public/v1/policies | Get a list of escalation policy info |
| POST | /api-public/v1/policies | Create an escalation policy |
| GET | /api-public/v1/policies/{policy} | Get a specific escalation policy |
| DELETE | /api-public/v1/policies/{policy} | Delete a specified escalation policy |
| POST | /api-public/v1/team | Add a team |
| GET | /api-public/v1/team | List teams |
| GET | /api-public/v1/team/{team} | Retrieve information for a team |
| PUT | /api-public/v1/team/{team} | Update a team |
| DELETE | /api-public/v1/team/{team} | Remove a team |
| GET | /api-public/v1/team/{team}/policies | Retrieve a list of escalation policies for a team |
| GET | /api-public/v1/team/{team}/admins | Retrieve a list of team admins for a team |
| GET | /api-public/v1/team/{team}/members | Retrieve a list of members for a team |
| POST | /api-public/v1/team/{team}/members | Add a team member |
| DELETE | /api-public/v1/team/{team}/members/{user} | Remove a team member |
| GET | /api-public/v1/maintenancemode | Get an organization's current maintenance mode state |
| POST | /api-public/v1/maintenancemode/start | Start maintenance mode for routing keys |
| PUT | /api-public/v1/maintenancemode/{maintenancemodeid}/end | End maintenance mode for routing keys |
| POST | /api-public/v1/chat | Send a chat message into VictorOps |
| POST | /api-public/v1/stakeholders/sendMessage | Sends a stakeholder message to the recipients. Recipients can either be User/team or both. |
| GET | /api-public/v1/alertRules | Get all alert rules |
| POST | /api-public/v1/alertRules | Create alert rule |
| PUT | /api-public/v1/alertRules/{ruleId} | Update alert rule |
| DELETE | /api-public/v1/alertRules/{ruleId} | Delete alert rule |

### api-reporting
| Method | Path | Description |
|--------|------|-------------|
| GET | /api-reporting/v1/team/{team}/oncall/log | A list of shift changes for a team |
| GET | /api-reporting/v2/incidents | Get/search incident history |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a user?" -> POST /api-public/v1/user
- "List all user?" -> GET /api-public/v1/user
- "List all user?" -> GET /api-public/v2/user
- "Create a batch?" -> POST /api-public/v1/user/batch
- "Get user details?" -> GET /api-public/v1/user/{user}
- "Update a user?" -> PUT /api-public/v1/user/{user}
- "Delete a user?" -> DELETE /api-public/v1/user/{user}
- "List all teams?" -> GET /api-public/v1/user/{user}/teams
- "List all notifications?" -> GET /api-public/v1/policies/types/notifications
- "List all contacts?" -> GET /api-public/v1/policies/types/contacts
- "List all timeouts?" -> GET /api-public/v1/policies/types/timeouts
- "List all policies?" -> GET /api-public/v1/profile/{username}/policies
- "Create a policy?" -> POST /api-public/v1/profile/{username}/policies
- "Get policy details?" -> GET /api-public/v1/profile/{username}/policies/{step}
- "Update a policy?" -> PUT /api-public/v1/profile/{username}/policies/{step}
- "Get policy details?" -> GET /api-public/v1/profile/{username}/policies/{step}/{rule}
- "Update a policy?" -> PUT /api-public/v1/profile/{username}/policies/{step}/{rule}
- "Delete a policy?" -> DELETE /api-public/v1/profile/{username}/policies/{step}/{rule}
- "List all policies?" -> GET /api-public/v2/profile/{username}/policies
- "List all contact-methods?" -> GET /api-public/v1/user/{user}/contact-methods
- "List all devices?" -> GET /api-public/v1/user/{user}/contact-methods/devices
- "Get device details?" -> GET /api-public/v1/user/{user}/contact-methods/devices/{contactId}
- "Update a device?" -> PUT /api-public/v1/user/{user}/contact-methods/devices/{contactId}
- "Delete a device?" -> DELETE /api-public/v1/user/{user}/contact-methods/devices/{contactId}
- "List all emails?" -> GET /api-public/v1/user/{user}/contact-methods/emails
- "Create a email?" -> POST /api-public/v1/user/{user}/contact-methods/emails
- "Get email details?" -> GET /api-public/v1/user/{user}/contact-methods/emails/{contactId}
- "Delete a email?" -> DELETE /api-public/v1/user/{user}/contact-methods/emails/{contactId}
- "List all phones?" -> GET /api-public/v1/user/{user}/contact-methods/phones
- "Create a phone?" -> POST /api-public/v1/user/{user}/contact-methods/phones
- "Get phone details?" -> GET /api-public/v1/user/{user}/contact-methods/phones/{contactId}
- "Delete a phone?" -> DELETE /api-public/v1/user/{user}/contact-methods/phones/{contactId}
- "List all policies?" -> GET /api-public/v1/user/{user}/policies
- "List all schedule?" -> GET /api-public/v1/user/{user}/oncall/schedule
- "List all schedule?" -> GET /api-public/v2/user/{user}/oncall/schedule
- "List all schedule?" -> GET /api-public/v1/team/{team}/oncall/schedule
- "List all schedule?" -> GET /api-public/v2/team/{team}/oncall/schedule
- "List all current?" -> GET /api-public/v1/oncall/current
- "List all log?" -> GET /api-reporting/v1/team/{team}/oncall/log
- "Get incident details?" -> GET /api-public/v1/incidents/{incidentNumber}
- "List all incidents?" -> GET /api-public/v1/incidents
- "Create a incident?" -> POST /api-public/v1/incidents
- "Create a reroute?" -> POST /api-public/v1/incidents/reroute
- "List all notes?" -> GET /api-public/v1/incidents/{incidentNumber}/notes
- "Create a note?" -> POST /api-public/v1/incidents/{incidentNumber}/notes
- "Update a note?" -> PUT /api-public/v1/incidents/{incidentNumber}/notes/{noteName}
- "Delete a note?" -> DELETE /api-public/v1/incidents/{incidentNumber}/notes/{noteName}
- "Get alert details?" -> GET /api-public/v1/alerts/{uuid}
- "List all routing-keys?" -> GET /api-public/v1/org/routing-keys
- "Create a routing-key?" -> POST /api-public/v1/org/routing-keys
- "List all overrides?" -> GET /api-public/v1/overrides
- "Create a override?" -> POST /api-public/v1/overrides
- "Get override details?" -> GET /api-public/v1/overrides/{publicId}
- "Delete a override?" -> DELETE /api-public/v1/overrides/{publicId}
- "List all assignments?" -> GET /api-public/v1/overrides/{publicId}/assignments
- "Get assignment details?" -> GET /api-public/v1/overrides/{publicId}/assignments/{policySlug}
- "Update a assignment?" -> PUT /api-public/v1/overrides/{publicId}/assignments/{policySlug}
- "Delete a assignment?" -> DELETE /api-public/v1/overrides/{publicId}/assignments/{policySlug}
- "List all rotations?" -> GET /api-public/v1/teams/{team}/rotations
- "Create a rotation?" -> POST /api-public/v1/teams/{team}/rotations
- "Delete a rotation?" -> DELETE /api-public/v1/teams/{team}/rotations/{groupId}
- "List all scheduled?" -> GET /api-public/v1/teams/{team}/rotations/{groupId}/{shiftId}/scheduled
- "List all rotations?" -> GET /api-public/v2/team/{team}/rotations
- "List all webhooks?" -> GET /api-public/v1/webhooks
- "List all policies?" -> GET /api-public/v1/policies
- "Create a policy?" -> POST /api-public/v1/policies
- "Get policy details?" -> GET /api-public/v1/policies/{policy}
- "Delete a policy?" -> DELETE /api-public/v1/policies/{policy}
- "List all incidents?" -> GET /api-reporting/v2/incidents
- "Create a team?" -> POST /api-public/v1/team
- "List all team?" -> GET /api-public/v1/team
- "Get team details?" -> GET /api-public/v1/team/{team}
- "Update a team?" -> PUT /api-public/v1/team/{team}
- "Delete a team?" -> DELETE /api-public/v1/team/{team}
- "List all policies?" -> GET /api-public/v1/team/{team}/policies
- "List all admins?" -> GET /api-public/v1/team/{team}/admins
- "List all members?" -> GET /api-public/v1/team/{team}/members
- "Create a member?" -> POST /api-public/v1/team/{team}/members
- "Delete a member?" -> DELETE /api-public/v1/team/{team}/members/{user}
- "List all maintenancemode?" -> GET /api-public/v1/maintenancemode
- "Create a start?" -> POST /api-public/v1/maintenancemode/start
- "Create a chat?" -> POST /api-public/v1/chat
- "Create a sendMessage?" -> POST /api-public/v1/stakeholders/sendMessage
- "List all alertRules?" -> GET /api-public/v1/alertRules
- "Create a alertRule?" -> POST /api-public/v1/alertRules
- "Update a alertRule?" -> PUT /api-public/v1/alertRules/{ruleId}
- "Delete a alertRule?" -> DELETE /api-public/v1/alertRules/{ruleId}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
