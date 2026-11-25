---
name: platform-api
description: "Platform API skill. Use when working with Platform for channels, push, keys. Covers 22 endpoints."
version: 1.0.0
generator: lapsh
---

# Platform API
API version: 1.1.1

## Auth
Bearer basic | Bearer bearer

## Base URL
https://rest.ably.io

## Setup
1. Set Authorization header with your Bearer token
2. GET /channels -- verify access
3. POST /channels/{channel_id}/messages -- create first messages

## Endpoints

22 endpoints across 5 groups. See references/api-spec.lap for full details.

### channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /channels/{channel_id}/messages | Get message history for a channel |
| POST | /channels/{channel_id}/messages | Publish a message to a channel |
| GET | /channels/{channel_id}/presence | Get presence of a channel |
| GET | /channels/{channel_id}/presence/history | Get presence history of a channel |
| GET | /channels/{channel_id} | Get metadata of a channel |
| GET | /channels | Enumerate all active channels of the application |

### push
| Method | Path | Description |
|--------|------|-------------|
| GET | /push/deviceRegistrations | List devices registered for receiving push notifications |
| POST | /push/deviceRegistrations | Register a device for receiving push notifications |
| DELETE | /push/deviceRegistrations | Unregister matching devices for push notifications |
| GET | /push/deviceRegistrations/{device_id} | Get a device registration |
| PUT | /push/deviceRegistrations/{device_id} | Update a device registration |
| PATCH | /push/deviceRegistrations/{device_id} | Update a device registration |
| DELETE | /push/deviceRegistrations/{device_id} | Unregister a single device for push notifications |
| GET | /push/deviceRegistrations/{device_id}/resetUpdateToken | Reset a registered device's update token |
| GET | /push/channelSubscriptions | List channel subscriptions |
| POST | /push/channelSubscriptions | Subscribe a device to a channel |
| DELETE | /push/channelSubscriptions | Delete a registered device's update token |
| GET | /push/channels | List all channels with at least one subscribed device |
| POST | /push/publish | Publish a push notification to device(s) |

### keys
| Method | Path | Description |
|--------|------|-------------|
| POST | /keys/{keyName}/requestToken | Request an access token |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats | Retrieve usage statistics for an application |

### time
| Method | Path | Description |
|--------|------|-------------|
| GET | /time | Get the service time |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all messages?" -> GET /channels/{channel_id}/messages
- "Create a message?" -> POST /channels/{channel_id}/messages
- "List all presence?" -> GET /channels/{channel_id}/presence
- "List all history?" -> GET /channels/{channel_id}/presence/history
- "Get channel details?" -> GET /channels/{channel_id}
- "List all channels?" -> GET /channels
- "List all deviceRegistrations?" -> GET /push/deviceRegistrations
- "Create a deviceRegistration?" -> POST /push/deviceRegistrations
- "Get deviceRegistration details?" -> GET /push/deviceRegistrations/{device_id}
- "Update a deviceRegistration?" -> PUT /push/deviceRegistrations/{device_id}
- "Partially update a deviceRegistration?" -> PATCH /push/deviceRegistrations/{device_id}
- "Delete a deviceRegistration?" -> DELETE /push/deviceRegistrations/{device_id}
- "List all resetUpdateToken?" -> GET /push/deviceRegistrations/{device_id}/resetUpdateToken
- "List all channelSubscriptions?" -> GET /push/channelSubscriptions
- "Create a channelSubscription?" -> POST /push/channelSubscriptions
- "List all channels?" -> GET /push/channels
- "Create a publish?" -> POST /push/publish
- "Create a requestToken?" -> POST /keys/{keyName}/requestToken
- "List all stats?" -> GET /stats
- "List all time?" -> GET /time
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
