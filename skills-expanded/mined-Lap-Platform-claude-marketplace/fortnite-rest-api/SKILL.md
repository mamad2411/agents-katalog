---
name: fortnite-rest-api
description: "FORTNITE REST API skill. Use when working with FORTNITE REST for oauth, check, news. Covers 9 endpoints."
version: 1.0.0
generator: lapsh
---

# FORTNITE REST API
API version: 3.1.5

## Auth
ApiKey Authorization in header

## Base URL
https://skynewz-api-fortnite.herokuapp.com/api

## Setup
1. Set your API key in the appropriate header
2. GET /check -- verify access
3. POST /oauth/token -- create first token

## Endpoints

9 endpoints across 7 groups. See references/api-spec.lap for full details.

### oauth
| Method | Path | Description |
|--------|------|-------------|
| POST | /oauth/token | Get a Bearer token |

### check
| Method | Path | Description |
|--------|------|-------------|
| GET | /check | Get Fortnite game status |

### news
| Method | Path | Description |
|--------|------|-------------|
| GET | /news | Get Fortnite News |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /user/{plateform}/{username} | Get a user by username |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats/{plateform}/{username} | Get user's stats by username |
| GET | /stats/id/{plateform}/{id} | Get user's stats by user id |

### pve
| Method | Path | Description |
|--------|------|-------------|
| GET | /pve/user/{username} | Get PVE Stat by given username |
| GET | /pve/info | Get Fortnite PVE Info (storm, etc) |

### store
| Method | Path | Description |
|--------|------|-------------|
| GET | /store | Get Fortnite Store |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a token?" -> POST /oauth/token
- "List all check?" -> GET /check
- "List all news?" -> GET /news
- "Get user details?" -> GET /user/{plateform}/{username}
- "Get stat details?" -> GET /stats/{plateform}/{username}
- "Get id details?" -> GET /stats/id/{plateform}/{id}
- "Get user details?" -> GET /pve/user/{username}
- "List all info?" -> GET /pve/info
- "List all store?" -> GET /store
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
