---
name: smartphone-test-farm
description: "Smartphone Test Farm API skill. Use when working with Smartphone Test Farm for user, devices. Covers 10 endpoints."
version: 1.0.0
generator: lapsh
---

# Smartphone Test Farm
API version: 2.3.0

## Auth
ApiKey authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /user -- verify access
3. POST /user/devices -- create first devices

## Endpoints

10 endpoints across 2 groups. See references/api-spec.lap for full details.

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user | User Profile |
| GET | /user/devices | User Devices |
| POST | /user/devices | Add a device to a user |
| GET | /user/devices/{serial} | User Device |
| DELETE | /user/devices/{serial} | Delete User Device |
| POST | /user/devices/{serial}/remoteConnect | Remote Connect |
| DELETE | /user/devices/{serial}/remoteConnect | Remote Disconnect |
| GET | /user/accessTokens | Access Tokens |

### devices
| Method | Path | Description |
|--------|------|-------------|
| GET | /devices | Device List |
| GET | /devices/{serial} | Device Information |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all user?" -> GET /user
- "List all devices?" -> GET /user/devices
- "Create a device?" -> POST /user/devices
- "Get device details?" -> GET /user/devices/{serial}
- "Delete a device?" -> DELETE /user/devices/{serial}
- "Create a remoteConnect?" -> POST /user/devices/{serial}/remoteConnect
- "List all accessTokens?" -> GET /user/accessTokens
- "List all devices?" -> GET /devices
- "Get device details?" -> GET /devices/{serial}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
