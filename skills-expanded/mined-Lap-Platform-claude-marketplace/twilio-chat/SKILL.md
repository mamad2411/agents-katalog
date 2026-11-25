---
name: twilio-chat
description: "Twilio - Chat API skill. Use when working with Twilio - Chat for Services, Credentials. Covers 54 endpoints."
version: 1.0.0
generator: lapsh
---

# Twilio - Chat
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://chat.twilio.com

## Setup
1. Set Authorization header with your Bearer token
2. GET /v2/Credentials -- verify access
3. POST /v2/Services/{ServiceSid}/Channels/{Sid} -- create first Channels

## Endpoints

54 endpoints across 2 groups. See references/api-spec.lap for full details.

### Services
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/Services/{ServiceSid}/Bindings |  |
| GET | /v2/Services/{ServiceSid}/Bindings/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Bindings/{Sid} |  |
| GET | /v2/Services/{ServiceSid}/Channels/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Channels/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels |  |
| GET | /v2/Services/{ServiceSid}/Channels |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks |  |
| POST | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks/{Sid} |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages |  |
| GET | /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages |  |
| GET | /v2/Services/{ServiceSid}/Roles/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Roles/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Roles/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Roles |  |
| GET | /v2/Services/{ServiceSid}/Roles |  |
| GET | /v2/Services/{Sid} |  |
| DELETE | /v2/Services/{Sid} |  |
| POST | /v2/Services/{Sid} |  |
| POST | /v2/Services |  |
| GET | /v2/Services |  |
| GET | /v2/Services/{ServiceSid}/Users/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Users/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Users/{Sid} |  |
| POST | /v2/Services/{ServiceSid}/Users |  |
| GET | /v2/Services/{ServiceSid}/Users |  |
| GET | /v2/Services/{ServiceSid}/Users/{UserSid}/Bindings |  |
| GET | /v2/Services/{ServiceSid}/Users/{UserSid}/Bindings/{Sid} |  |
| DELETE | /v2/Services/{ServiceSid}/Users/{UserSid}/Bindings/{Sid} |  |
| GET | /v2/Services/{ServiceSid}/Users/{UserSid}/Channels | List all Channels for a given User. |
| GET | /v2/Services/{ServiceSid}/Users/{UserSid}/Channels/{ChannelSid} |  |
| DELETE | /v2/Services/{ServiceSid}/Users/{UserSid}/Channels/{ChannelSid} | Removes User from selected Channel. |
| POST | /v2/Services/{ServiceSid}/Users/{UserSid}/Channels/{ChannelSid} |  |

### Credentials
| Method | Path | Description |
|--------|------|-------------|
| GET | /v2/Credentials |  |
| POST | /v2/Credentials |  |
| GET | /v2/Credentials/{Sid} |  |
| POST | /v2/Credentials/{Sid} |  |
| DELETE | /v2/Credentials/{Sid} |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all Bindings?" -> GET /v2/Services/{ServiceSid}/Bindings
- "Get Binding details?" -> GET /v2/Services/{ServiceSid}/Bindings/{Sid}
- "Delete a Binding?" -> DELETE /v2/Services/{ServiceSid}/Bindings/{Sid}
- "Get Channel details?" -> GET /v2/Services/{ServiceSid}/Channels/{Sid}
- "Delete a Channel?" -> DELETE /v2/Services/{ServiceSid}/Channels/{Sid}
- "Create a Channel?" -> POST /v2/Services/{ServiceSid}/Channels
- "List all Channels?" -> GET /v2/Services/{ServiceSid}/Channels
- "List all Webhooks?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks
- "Create a Webhook?" -> POST /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks
- "Get Webhook details?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks/{Sid}
- "Delete a Webhook?" -> DELETE /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Webhooks/{Sid}
- "List all Credentials?" -> GET /v2/Credentials
- "Create a Credential?" -> POST /v2/Credentials
- "Get Credential details?" -> GET /v2/Credentials/{Sid}
- "Delete a Credential?" -> DELETE /v2/Credentials/{Sid}
- "Get Invite details?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites/{Sid}
- "Delete a Invite?" -> DELETE /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites/{Sid}
- "Create a Invite?" -> POST /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites
- "List all Invites?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Invites
- "Get Member details?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members/{Sid}
- "Delete a Member?" -> DELETE /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members/{Sid}
- "Create a Member?" -> POST /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members
- "List all Members?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Members
- "Get Message details?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages/{Sid}
- "Delete a Message?" -> DELETE /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages/{Sid}
- "Create a Message?" -> POST /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages
- "List all Messages?" -> GET /v2/Services/{ServiceSid}/Channels/{ChannelSid}/Messages
- "Get Role details?" -> GET /v2/Services/{ServiceSid}/Roles/{Sid}
- "Delete a Role?" -> DELETE /v2/Services/{ServiceSid}/Roles/{Sid}
- "Create a Role?" -> POST /v2/Services/{ServiceSid}/Roles
- "List all Roles?" -> GET /v2/Services/{ServiceSid}/Roles
- "Get Service details?" -> GET /v2/Services/{Sid}
- "Delete a Service?" -> DELETE /v2/Services/{Sid}
- "Create a Service?" -> POST /v2/Services
- "List all Services?" -> GET /v2/Services
- "Get User details?" -> GET /v2/Services/{ServiceSid}/Users/{Sid}
- "Delete a User?" -> DELETE /v2/Services/{ServiceSid}/Users/{Sid}
- "Create a User?" -> POST /v2/Services/{ServiceSid}/Users
- "List all Users?" -> GET /v2/Services/{ServiceSid}/Users
- "List all Bindings?" -> GET /v2/Services/{ServiceSid}/Users/{UserSid}/Bindings
- "Get Binding details?" -> GET /v2/Services/{ServiceSid}/Users/{UserSid}/Bindings/{Sid}
- "Delete a Binding?" -> DELETE /v2/Services/{ServiceSid}/Users/{UserSid}/Bindings/{Sid}
- "List all Channels?" -> GET /v2/Services/{ServiceSid}/Users/{UserSid}/Channels
- "Get Channel details?" -> GET /v2/Services/{ServiceSid}/Users/{UserSid}/Channels/{ChannelSid}
- "Delete a Channel?" -> DELETE /v2/Services/{ServiceSid}/Users/{UserSid}/Channels/{ChannelSid}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
