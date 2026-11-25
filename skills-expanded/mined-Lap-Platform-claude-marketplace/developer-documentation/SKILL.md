---
name: developer-documentation
description: "Developer documentation API skill. Use when working with Developer documentation for link, events, users. Covers 16 endpoints."
version: 1.0.0
generator: lapsh
---

# Developer documentation
API version: 1.0.0

## Auth
ApiKey (inferred from docs)

## Base URL
https://api.journy.io

## Setup
1. Set your API key in the appropriate header
2. GET /events -- verify access
3. POST /link -- create first link

## Endpoints

16 endpoints across 9 groups. See references/api-spec.lap for full details.

### link
| Method | Path | Description |
|--------|------|-------------|
| POST | /link | Link web activity to user |

### events
| Method | Path | Description |
|--------|------|-------------|
| POST | /events | Track event |
| GET | /events | Get events |

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/upsert | Create or update user |
| DELETE | /users | Delete user |

### accounts
| Method | Path | Description |
|--------|------|-------------|
| POST | /accounts/upsert | Create or update account |
| POST | /accounts/users/add | Add users to an account |
| POST | /accounts/users/remove | Remove user from account |
| DELETE | /accounts | Delete account |

### properties
| Method | Path | Description |
|--------|------|-------------|
| GET | /properties/users | Get user properties |
| GET | /properties/accounts | Get account properties |

### validate
| Method | Path | Description |
|--------|------|-------------|
| GET | /validate | Validate API key |

### tracking
| Method | Path | Description |
|--------|------|-------------|
| GET | /tracking/snippet | Get snippet for a website |

### track
| Method | Path | Description |
|--------|------|-------------|
| POST | /track | Track event |

### segments
| Method | Path | Description |
|--------|------|-------------|
| GET | /segments/users | Get user segments |
| GET | /segments/accounts | Get account segments |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a link?" -> POST /link
- "Create a event?" -> POST /events
- "List all events?" -> GET /events
- "Create a upsert?" -> POST /users/upsert
- "Create a upsert?" -> POST /accounts/upsert
- "Create a add?" -> POST /accounts/users/add
- "Create a remove?" -> POST /accounts/users/remove
- "List all users?" -> GET /properties/users
- "List all accounts?" -> GET /properties/accounts
- "List all validate?" -> GET /validate
- "List all snippet?" -> GET /tracking/snippet
- "Create a track?" -> POST /track
- "List all users?" -> GET /segments/users
- "List all accounts?" -> GET /segments/accounts
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
