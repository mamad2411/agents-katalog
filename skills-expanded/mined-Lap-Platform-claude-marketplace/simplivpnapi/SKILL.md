---
name: simplivpnapi
description: "SimpliVPNAPI API skill. Use when working with SimpliVPNAPI for servers, server-summaries, register. Covers 7 endpoints."
version: 1.0.0
generator: lapsh
---

# SimpliVPNAPI
API version: 1.0

## Auth
ApiKey Authorization in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /servers -- verify access
3. POST /register -- create first register

## Endpoints

7 endpoints across 7 groups. See references/api-spec.lap for full details.

### servers
| Method | Path | Description |
|--------|------|-------------|
| GET | /servers |  |

### server-summaries
| Method | Path | Description |
|--------|------|-------------|
| GET | /server-summaries |  |

### register
| Method | Path | Description |
|--------|------|-------------|
| POST | /register | Register |

### login
| Method | Path | Description |
|--------|------|-------------|
| POST | /login | Login |

### enable-user
| Method | Path | Description |
|--------|------|-------------|
| POST | /enable-user | EnableUser |

### disable-user
| Method | Path | Description |
|--------|------|-------------|
| POST | /disable-user | DisableUser |

### username-available
| Method | Path | Description |
|--------|------|-------------|
| POST | /username-available | UsernameAvailable |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all servers?" -> GET /servers
- "List all server-summaries?" -> GET /server-summaries
- "Create a register?" -> POST /register
- "Create a login?" -> POST /login
- "Create a enable-user?" -> POST /enable-user
- "Create a disable-user?" -> POST /disable-user
- "Create a username-available?" -> POST /username-available
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
