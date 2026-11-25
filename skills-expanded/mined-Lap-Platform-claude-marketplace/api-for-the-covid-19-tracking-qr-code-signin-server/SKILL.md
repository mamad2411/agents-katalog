---
name: api-for-the-covid-19-tracking-qr-code-signin-server
description: "API for the COVID-19 Tracking QR Code Signin Server. API skill. Use when working with API for the COVID-19 Tracking QR Code Signin Server. for login, logout, signins. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# API for the COVID-19 Tracking QR Code Signin Server.
API version: 1.1

## Auth
ApiKey token in header

## Base URL
https://virtserver.swaggerhub.com/aijaz/QRCodeSigninServer/1.1

## Setup
1. Set your API key in the appropriate header
2. GET /signins -- verify access
3. POST /login -- create first login

## Endpoints

14 endpoints across 9 groups. See references/api-spec.lap for full details.

### login
| Method | Path | Description |
|--------|------|-------------|
| POST | /login | Log in to get an API token |

### logout
| Method | Path | Description |
|--------|------|-------------|
| POST | /logout | Log out |

### signins
| Method | Path | Description |
|--------|------|-------------|
| GET | /signins | Get signin info |

### signin
| Method | Path | Description |
|--------|------|-------------|
| POST | /signin | Create a new signin record |
| GET | /signin/{signinId} | Retrieve the information associated with a signin record |
| PUT | /signin/{signinId} | Update a signin record |
| DELETE | /signin/{signinId} | Delete a signin record |

### verifyPasswordChange
| Method | Path | Description |
|--------|------|-------------|
| POST | /verifyPasswordChange | Used for resetting your password when you forgot it |

### changePassword
| Method | Path | Description |
|--------|------|-------------|
| POST | /changePassword | Used for changing your password |

### requestPasswordReset
| Method | Path | Description |
|--------|------|-------------|
| POST | /requestPasswordReset | Used for requesting a password reset code |

### user
| Method | Path | Description |
|--------|------|-------------|
| POST | /user | Create a user |
| DELETE | /user/{userId} | Delete a team member's user record |
| GET | /user/{userId} | Retrieve the information associated with a team member's user record |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Retrieve the information associated with all team members' user records |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a login?" -> POST /login
- "Create a logout?" -> POST /logout
- "List all signins?" -> GET /signins
- "Create a signin?" -> POST /signin
- "Get signin details?" -> GET /signin/{signinId}
- "Update a signin?" -> PUT /signin/{signinId}
- "Delete a signin?" -> DELETE /signin/{signinId}
- "Create a verifyPasswordChange?" -> POST /verifyPasswordChange
- "Create a changePassword?" -> POST /changePassword
- "Create a requestPasswordReset?" -> POST /requestPasswordReset
- "Create a user?" -> POST /user
- "Delete a user?" -> DELETE /user/{userId}
- "Get user details?" -> GET /user/{userId}
- "List all users?" -> GET /users
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
