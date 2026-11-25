---
name: kumpeapps-api
description: "KumpeApps API skill. Use when working with KumpeApps for appkey, authkey, authentication. Covers 33 endpoints."
version: 1.0.0
generator: lapsh
---

# KumpeApps API
API version: 5.0.0

## Auth
ApiKey X-Auth in header | ApiKey X-Auth in header

## Base URL
https://restapi.kumpeapps.com/v5

## Setup
1. Set your API key in the appropriate header
2. GET /authkey -- verify access
3. POST /appkey -- create first appkey

## Endpoints

33 endpoints across 4 groups. See references/api-spec.lap for full details.

### appkey
| Method | Path | Description |
|--------|------|-------------|
| PUT | /appkey | Deactivate app key |
| POST | /appkey | Request app key |
| PATCH | /appkey | Compromise app key |

### authkey
| Method | Path | Description |
|--------|------|-------------|
| GET | /authkey | Request auth key for user (login user) |
| PUT | /authkey | Deactivate auth key (logout) |
| POST | /authkey | Request auth key for user (login user) |
| PATCH | /authkey | Compromise auth key |

### authentication
| Method | Path | Description |
|--------|------|-------------|
| PUT | /authentication/appkey | Deactivate app key |
| POST | /authentication/appkey | Request app key |
| PATCH | /authentication/appkey | Compromise app key |
| GET | /authentication/verifyotp | Verifies YubiKey OTP for authenticated user |
| GET | /authentication/authkey | Request auth key for user (login user) |
| PUT | /authentication/authkey | Deactivate auth key (logout) |
| POST | /authentication/authkey | Request auth key for user (login user) |
| PATCH | /authentication/authkey | Compromise auth key |

### kkid
| Method | Path | Description |
|--------|------|-------------|
| POST | /kkid/masteruser | adds new master user account |
| GET | /kkid/user | Gets user info |
| GET | /kkid/userlist | returns list of users |
| PUT | /kkid/userlist | updates user |
| POST | /kkid/userlist | adds new child user |
| DELETE | /kkid/userlist | deletes user |
| GET | /kkid/chorelist | returns list of chores for given user |
| PUT | /kkid/chorelist | updates chore for given chore id |
| POST | /kkid/chorelist | adds chore for given user |
| DELETE | /kkid/chorelist | deletes chore for given chore id |
| GET | /kkid/allowance | returns allowance balance and allowance transactions |
| POST | /kkid/allowance | adds new allowance transaction to kidUserID |
| POST | /kkid/apns | subscribes/unsubscribes/registers for apns push notifications |
| GET | /kkid/wishlist | Get list of wishlist items |
| PUT | /kkid/wishlist | Update item on kid's wishlist |
| POST | /kkid/wishlist | Add item to kid's wishlist |
| DELETE | /kkid/wishlist | Delete item from wishlist |
| GET | /kkid/share | Create Share Link |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a appkey?" -> POST /appkey
- "List all authkey?" -> GET /authkey
- "Create a authkey?" -> POST /authkey
- "Create a appkey?" -> POST /authentication/appkey
- "List all verifyotp?" -> GET /authentication/verifyotp
- "List all authkey?" -> GET /authentication/authkey
- "Create a authkey?" -> POST /authentication/authkey
- "Create a masteruser?" -> POST /kkid/masteruser
- "List all user?" -> GET /kkid/user
- "List all userlist?" -> GET /kkid/userlist
- "Create a userlist?" -> POST /kkid/userlist
- "List all chorelist?" -> GET /kkid/chorelist
- "Create a chorelist?" -> POST /kkid/chorelist
- "List all allowance?" -> GET /kkid/allowance
- "Create a allowance?" -> POST /kkid/allowance
- "Create a apn?" -> POST /kkid/apns
- "List all wishlist?" -> GET /kkid/wishlist
- "Create a wishlist?" -> POST /kkid/wishlist
- "List all share?" -> GET /kkid/share
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
