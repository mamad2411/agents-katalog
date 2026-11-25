---
name: developer-api-upstash
description: "Developer API - Upstash API skill. Use when working with Developer API - Upstash for redis, teams, auditlogs. Covers 52 endpoints."
version: 1.0.0
generator: lapsh
---

# Developer API - Upstash
API version: 1.0.0

## Auth
Bearer basic

## Base URL
https://api.upstash.com/v2

## Setup
1. Set Authorization header with your Bearer token
2. GET /redis/databases -- verify access
3. POST /redis/database -- create first database

## Endpoints

52 endpoints across 8 groups. See references/api-spec.lap for full details.

### redis
| Method | Path | Description |
|--------|------|-------------|
| GET | /redis/databases | List Databases |
| GET | /redis/database/{id} | Get Database |
| DELETE | /redis/database/{id} | Delete Database |
| POST | /redis/database | Create Redis Database |
| POST | /redis/rename/{id} | Rename Database |
| POST | /redis/reset-password/{id} | Reset Password |
| POST | /redis/enable-tls/{id} | Enable TLS |
| POST | /redis/enable-eviction/{id} | Enable Eviction |
| POST | /redis/disable-eviction/{id} | Disable Eviction |
| POST | /redis/enable-autoupgrade/{id} | Enable Auto Upgrade |
| POST | /redis/disable-autoupgrade/{id} | Disable Auto Upgrade |
| POST | /redis/change-plan/{id} | Change Database Plan |
| PATCH | /redis/update-budget/{id} | Update Database Budget |
| POST | /redis/update-regions/{id} | Update Regions |
| POST | /redis/move-to-team | Move To Team |
| GET | /redis/stats/{id} | Get Database Stats |
| GET | /redis/list-backup/{id} | List Backup |
| POST | /redis/create-backup/{id} | Create Backup |
| DELETE | /redis/delete-backup/{id}/{backup_id} | Delete Backup |
| POST | /redis/restore-backup/{id} | Restore Backup |
| PATCH | /redis/enable-dailybackup/{id} | Enable Daily Backup |
| PATCH | /redis/disable-dailybackup/{id} | Disable Daily Backup |

### teams
| Method | Path | Description |
|--------|------|-------------|
| GET | /teams | List Teams |
| GET | /teams/{team_id} | Get Team Members |
| POST | /teams/member | Add Team Member |
| DELETE | /teams/member | Delete Team Member |

### auditlogs
| Method | Path | Description |
|--------|------|-------------|
| GET | /auditlogs | List Audit Logs |

### team
| Method | Path | Description |
|--------|------|-------------|
| POST | /team | Create Team |
| DELETE | /team/{id} | Delete Team |

### vector
| Method | Path | Description |
|--------|------|-------------|
| GET | /vector/index | List Indices |
| POST | /vector/index | Create Index |
| GET | /vector/index/{id} | Get Index |
| DELETE | /vector/index/{id} | Delete Index |
| POST | /vector/index/{id}/rename | Rename Index |
| POST | /vector/index/{id}/reset-password | Reset Index Passwords |
| POST | /vector/index/{id}/setplan | Set Index Plan |
| POST | /vector/index/{id}/transfer | Transfer Index |
| GET | /vector/index/stats | Get Vector Stats |
| GET | /vector/index/{id}/stats | Get Index Stats |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | List Search Indexes |
| POST | /search | Create Search Index |
| GET | /search/{id} | Get Search Index |
| DELETE | /search/{id} | Delete Search Index |
| GET | /search/stats | Get Search Stats |
| GET | /search/{id}/stats | Get Index Stats |
| POST | /search/{id}/reset-password | Reset Password |
| POST | /search/{id}/transfer | Transfer Search Index |
| POST | /search/{id}/rename | Rename Search Index |

### qstash
| Method | Path | Description |
|--------|------|-------------|
| GET | /qstash/user | Get QStash |
| POST | /qstash/user/rotatetoken | Reset QStash Token |
| GET | /qstash/stats | Get QStash Stats |

### qstash-upgrade
| Method | Path | Description |
|--------|------|-------------|
| POST | /qstash-upgrade | Set QStash Plan |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all databases?" -> GET /redis/databases
- "Get database details?" -> GET /redis/database/{id}
- "Delete a database?" -> DELETE /redis/database/{id}
- "Create a database?" -> POST /redis/database
- "Partially update a update-budget?" -> PATCH /redis/update-budget/{id}
- "Create a move-to-team?" -> POST /redis/move-to-team
- "Get stat details?" -> GET /redis/stats/{id}
- "Get list-backup details?" -> GET /redis/list-backup/{id}
- "Delete a delete-backup?" -> DELETE /redis/delete-backup/{id}/{backup_id}
- "Partially update a enable-dailybackup?" -> PATCH /redis/enable-dailybackup/{id}
- "Partially update a disable-dailybackup?" -> PATCH /redis/disable-dailybackup/{id}
- "List all teams?" -> GET /teams
- "List all auditlogs?" -> GET /auditlogs
- "Create a team?" -> POST /team
- "Delete a team?" -> DELETE /team/{id}
- "Get team details?" -> GET /teams/{team_id}
- "Create a member?" -> POST /teams/member
- "List all index?" -> GET /vector/index
- "Create a index?" -> POST /vector/index
- "Get index details?" -> GET /vector/index/{id}
- "Delete a index?" -> DELETE /vector/index/{id}
- "Create a rename?" -> POST /vector/index/{id}/rename
- "Create a reset-password?" -> POST /vector/index/{id}/reset-password
- "Create a setplan?" -> POST /vector/index/{id}/setplan
- "Create a transfer?" -> POST /vector/index/{id}/transfer
- "List all stats?" -> GET /vector/index/stats
- "List all stats?" -> GET /vector/index/{id}/stats
- "List all search?" -> GET /search
- "Create a search?" -> POST /search
- "Get search details?" -> GET /search/{id}
- "Delete a search?" -> DELETE /search/{id}
- "List all stats?" -> GET /search/stats
- "List all stats?" -> GET /search/{id}/stats
- "Create a reset-password?" -> POST /search/{id}/reset-password
- "Create a transfer?" -> POST /search/{id}/transfer
- "Create a rename?" -> POST /search/{id}/rename
- "List all user?" -> GET /qstash/user
- "Create a rotatetoken?" -> POST /qstash/user/rotatetoken
- "Create a qstash-upgrade?" -> POST /qstash-upgrade
- "List all stats?" -> GET /qstash/stats
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
