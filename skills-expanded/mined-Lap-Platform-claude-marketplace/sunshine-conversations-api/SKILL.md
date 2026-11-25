---
name: sunshine-conversations-api
description: "Sunshine Conversations API skill. Use when working with Sunshine Conversations for apps, tokenInfo, oauth. Covers 68 endpoints."
version: 1.0.0
generator: lapsh
---

# Sunshine Conversations API
API version: 17.8.0

## Auth
Bearer bearer | Bearer basic

## Base URL
https://{subdomain}.zendesk.com/sc

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/apps -- verify access
3. POST /v2/apps -- create first apps

## Endpoints

68 endpoints across 3 groups. See references/api-spec.lap for full details.

### apps
| Method | Path | Description |
|--------|------|-------------|
| POST | /v2/apps | Create App |
| GET | /v2/apps | List Apps |
| GET | /v2/apps/{appId} | Get App |
| PATCH | /v2/apps/{appId} | Update App |
| DELETE | /v2/apps/{appId} | Delete App |
| POST | /v2/apps/{appId}/keys | Create App Key |
| GET | /v2/apps/{appId}/keys | List App Keys |
| GET | /v2/apps/{appId}/keys/{keyId} | Get App Key |
| DELETE | /v2/apps/{appId}/keys/{keyId} | Delete App Key |
| POST | /v2/apps/{appId}/attachments | Upload Attachment |
| POST | /v2/apps/{appId}/attachments/remove | Delete Attachment |
| POST | /v2/apps/{appId}/conversations | Create Conversation |
| GET | /v2/apps/{appId}/conversations | List Conversations |
| GET | /v2/apps/{appId}/conversations/{conversationId} | Get Conversation |
| PATCH | /v2/apps/{appId}/conversations/{conversationId} | Update Conversation |
| DELETE | /v2/apps/{appId}/conversations/{conversationId} | Delete Conversation |
| POST | /v2/apps/{appId}/conversations/{conversationId}/join | Join Conversation |
| GET | /v2/apps/{appId}/conversations/{conversationId}/participants | List Participants |
| POST | /v2/apps/{appId}/conversations/{conversationId}/leave | Leave Conversation |
| POST | /v2/apps/{appId}/conversations/{conversationId}/messages | Post Message |
| GET | /v2/apps/{appId}/conversations/{conversationId}/messages | List Messages |
| DELETE | /v2/apps/{appId}/conversations/{conversationId}/messages | Delete All Messages |
| DELETE | /v2/apps/{appId}/conversations/{conversationId}/messages/{messageId} | Delete Message |
| POST | /v2/apps/{appId}/conversations/{conversationId}/activity | Post Activity |
| POST | /v2/apps/{appId}/conversations/{conversationId}/acceptControl | Accept Control |
| POST | /v2/apps/{appId}/conversations/{conversationId}/offerControl | Offer Control |
| POST | /v2/apps/{appId}/conversations/{conversationId}/passControl | Pass Control |
| POST | /v2/apps/{appId}/conversations/{conversationId}/releaseControl | Release Control |
| POST | /v2/apps/{appId}/conversations/{conversationId}/download | Download Message Ref |
| POST | /v2/apps/{appId}/conversations/{conversationId}/conversionEvents | Post Conversion Events |
| POST | /v2/apps/{appId}/integrations | Create Integration |
| GET | /v2/apps/{appId}/integrations | List Integrations |
| GET | /v2/apps/{appId}/integrations/{integrationId} | Get Integration |
| PATCH | /v2/apps/{appId}/integrations/{integrationId} | Update Integration |
| DELETE | /v2/apps/{appId}/integrations/{integrationId} | Delete Integration |
| POST | /v2/apps/{appId}/integrations/{integrationId}/keys | Create Integration Key |
| GET | /v2/apps/{appId}/integrations/{integrationId}/keys | List Integration Keys |
| GET | /v2/apps/{appId}/integrations/{integrationId}/keys/{keyId} | Get Integration Key |
| DELETE | /v2/apps/{appId}/integrations/{integrationId}/keys/{keyId} | Delete Integration Key |
| POST | /v2/apps/{appId}/integrations/{integrationId}/webhooks | Create Webhook |
| GET | /v2/apps/{appId}/integrations/{integrationId}/webhooks | List Webhooks |
| GET | /v2/apps/{appId}/integrations/{integrationId}/webhooks/{webhookId} | Get Webhook |
| PATCH | /v2/apps/{appId}/integrations/{integrationId}/webhooks/{webhookId} | Update Webhook |
| DELETE | /v2/apps/{appId}/integrations/{integrationId}/webhooks/{webhookId} | Delete Webhook |
| POST | /v2/apps/{appId}/switchboards | Create Switchboard |
| GET | /v2/apps/{appId}/switchboards | List Switchboards |
| PATCH | /v2/apps/{appId}/switchboards/{switchboardId} | Update Switchboard |
| DELETE | /v2/apps/{appId}/switchboards/{switchboardId} | Delete Switchboard |
| POST | /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations | Create Switchboard Integration |
| GET | /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations | List Switchboard Integrations |
| PATCH | /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations/{switchboardIntegrationId} | Update Switchboard Integration |
| DELETE | /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations/{switchboardIntegrationId} | Delete Switchboard Integration |
| POST | /v2/apps/{appId}/users | Create User |
| GET | /v2/apps/{appId}/users | List Users |
| GET | /v2/apps/{appId}/users/{userIdOrExternalId} | Get User |
| PATCH | /v2/apps/{appId}/users/{userIdOrExternalId} | Update User |
| DELETE | /v2/apps/{appId}/users/{userIdOrExternalId} | Delete User |
| POST | /v2/apps/{appId}/users/{userIdOrExternalId}/clients | Create Client |
| GET | /v2/apps/{appId}/users/{userIdOrExternalId}/clients | List Clients |
| DELETE | /v2/apps/{appId}/users/{userIdOrExternalId}/clients/{clientId} | Remove Client |
| GET | /v2/apps/{appId}/users/{userIdOrExternalId}/devices | List Devices |
| GET | /v2/apps/{appId}/users/{userIdOrExternalId}/devices/{deviceId} | Get Device |
| DELETE | /v2/apps/{appId}/users/{userIdOrExternalId}/personalinformation | Delete User Personal Information |
| POST | /v2/apps/{appId}/users/{zendeskId}/sync | Synchronize User |

### tokenInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/tokenInfo | Get Token Info |

### oauth
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth/authorize | Authorize |
| POST | /oauth/token | Get Token |
| DELETE | /oauth/authorization | Revoke Access |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a app?" -> POST /v2/apps
- "List all apps?" -> GET /v2/apps
- "Get app details?" -> GET /v2/apps/{appId}
- "Partially update a app?" -> PATCH /v2/apps/{appId}
- "Delete a app?" -> DELETE /v2/apps/{appId}
- "Create a key?" -> POST /v2/apps/{appId}/keys
- "List all keys?" -> GET /v2/apps/{appId}/keys
- "Get key details?" -> GET /v2/apps/{appId}/keys/{keyId}
- "Delete a key?" -> DELETE /v2/apps/{appId}/keys/{keyId}
- "Create a attachment?" -> POST /v2/apps/{appId}/attachments
- "Create a remove?" -> POST /v2/apps/{appId}/attachments/remove
- "Create a conversation?" -> POST /v2/apps/{appId}/conversations
- "List all conversations?" -> GET /v2/apps/{appId}/conversations
- "Get conversation details?" -> GET /v2/apps/{appId}/conversations/{conversationId}
- "Partially update a conversation?" -> PATCH /v2/apps/{appId}/conversations/{conversationId}
- "Delete a conversation?" -> DELETE /v2/apps/{appId}/conversations/{conversationId}
- "Create a join?" -> POST /v2/apps/{appId}/conversations/{conversationId}/join
- "List all participants?" -> GET /v2/apps/{appId}/conversations/{conversationId}/participants
- "Create a leave?" -> POST /v2/apps/{appId}/conversations/{conversationId}/leave
- "Create a message?" -> POST /v2/apps/{appId}/conversations/{conversationId}/messages
- "List all messages?" -> GET /v2/apps/{appId}/conversations/{conversationId}/messages
- "Delete a message?" -> DELETE /v2/apps/{appId}/conversations/{conversationId}/messages/{messageId}
- "Create a activity?" -> POST /v2/apps/{appId}/conversations/{conversationId}/activity
- "Create a acceptControl?" -> POST /v2/apps/{appId}/conversations/{conversationId}/acceptControl
- "Create a offerControl?" -> POST /v2/apps/{appId}/conversations/{conversationId}/offerControl
- "Create a passControl?" -> POST /v2/apps/{appId}/conversations/{conversationId}/passControl
- "Create a releaseControl?" -> POST /v2/apps/{appId}/conversations/{conversationId}/releaseControl
- "Create a download?" -> POST /v2/apps/{appId}/conversations/{conversationId}/download
- "Create a conversionEvent?" -> POST /v2/apps/{appId}/conversations/{conversationId}/conversionEvents
- "Create a integration?" -> POST /v2/apps/{appId}/integrations
- "List all integrations?" -> GET /v2/apps/{appId}/integrations
- "Get integration details?" -> GET /v2/apps/{appId}/integrations/{integrationId}
- "Partially update a integration?" -> PATCH /v2/apps/{appId}/integrations/{integrationId}
- "Delete a integration?" -> DELETE /v2/apps/{appId}/integrations/{integrationId}
- "Create a key?" -> POST /v2/apps/{appId}/integrations/{integrationId}/keys
- "List all keys?" -> GET /v2/apps/{appId}/integrations/{integrationId}/keys
- "Get key details?" -> GET /v2/apps/{appId}/integrations/{integrationId}/keys/{keyId}
- "Delete a key?" -> DELETE /v2/apps/{appId}/integrations/{integrationId}/keys/{keyId}
- "Create a webhook?" -> POST /v2/apps/{appId}/integrations/{integrationId}/webhooks
- "List all webhooks?" -> GET /v2/apps/{appId}/integrations/{integrationId}/webhooks
- "Get webhook details?" -> GET /v2/apps/{appId}/integrations/{integrationId}/webhooks/{webhookId}
- "Partially update a webhook?" -> PATCH /v2/apps/{appId}/integrations/{integrationId}/webhooks/{webhookId}
- "Delete a webhook?" -> DELETE /v2/apps/{appId}/integrations/{integrationId}/webhooks/{webhookId}
- "Create a switchboard?" -> POST /v2/apps/{appId}/switchboards
- "List all switchboards?" -> GET /v2/apps/{appId}/switchboards
- "Partially update a switchboard?" -> PATCH /v2/apps/{appId}/switchboards/{switchboardId}
- "Delete a switchboard?" -> DELETE /v2/apps/{appId}/switchboards/{switchboardId}
- "Create a switchboardIntegration?" -> POST /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations
- "List all switchboardIntegrations?" -> GET /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations
- "Partially update a switchboardIntegration?" -> PATCH /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations/{switchboardIntegrationId}
- "Delete a switchboardIntegration?" -> DELETE /v2/apps/{appId}/switchboards/{switchboardId}/switchboardIntegrations/{switchboardIntegrationId}
- "Create a user?" -> POST /v2/apps/{appId}/users
- "List all users?" -> GET /v2/apps/{appId}/users
- "Get user details?" -> GET /v2/apps/{appId}/users/{userIdOrExternalId}
- "Partially update a user?" -> PATCH /v2/apps/{appId}/users/{userIdOrExternalId}
- "Delete a user?" -> DELETE /v2/apps/{appId}/users/{userIdOrExternalId}
- "Create a client?" -> POST /v2/apps/{appId}/users/{userIdOrExternalId}/clients
- "List all clients?" -> GET /v2/apps/{appId}/users/{userIdOrExternalId}/clients
- "Delete a client?" -> DELETE /v2/apps/{appId}/users/{userIdOrExternalId}/clients/{clientId}
- "List all devices?" -> GET /v2/apps/{appId}/users/{userIdOrExternalId}/devices
- "Get device details?" -> GET /v2/apps/{appId}/users/{userIdOrExternalId}/devices/{deviceId}
- "Create a sync?" -> POST /v2/apps/{appId}/users/{zendeskId}/sync
- "List all tokenInfo?" -> GET /v2/tokenInfo
- "List all authorize?" -> GET /oauth/authorize
- "Create a token?" -> POST /oauth/token
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
