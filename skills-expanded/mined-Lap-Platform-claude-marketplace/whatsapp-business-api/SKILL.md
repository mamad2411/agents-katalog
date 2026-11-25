---
name: whatsapp-business-api
description: "WhatsApp Business API skill. Use when working with WhatsApp Business for users, settings, account. Covers 55 endpoints."
version: 1.0.0
generator: lapsh
---

# WhatsApp Business API
API version: 1.0

## Auth
Bearer basic | Bearer bearer

## Base URL
http://example.com/v1

## Setup
1. Set Authorization header with your Bearer token
2. GET /settings/application -- verify access
3. POST /users/login -- create first login

## Endpoints

55 endpoints across 12 groups. See references/api-spec.lap for full details.

### users
| Method | Path | Description |
|--------|------|-------------|
| POST | /users/login | Login-User |
| POST | /users | Create-User |
| GET | /users/{UserUsername} | Get-User |
| PUT | /users/{UserUsername} | Update-User |
| DELETE | /users/{UserUsername} | Delete-User |
| POST | /users/logout | Logout-User |

### settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /settings/application | Get-Application-Settings |
| DELETE | /settings/application | Reset-Application-Settings |
| PATCH | /settings/application | Update-Application-Settings |
| GET | /settings/application/media/providers | Get-Media-Providers |
| POST | /settings/application/media/providers | Update-Media-Providers |
| DELETE | /settings/application/media/providers/{ProviderName} | Delete-Media-Providers |
| POST | /settings/backup | Backup-Settings |
| POST | /settings/restore | Restore-Settings |
| GET | /settings/business/profile | Get-Business-Profile |
| POST | /settings/business/profile | Update-Business-Profile |
| GET | /settings/profile/about | Get-Profile-About |
| PATCH | /settings/profile/about | Update-Profile-About |
| POST | /settings/account/two-step | Enable-Two-Step |
| DELETE | /settings/account/two-step | Disable-Two-Step |
| GET | /settings/profile/photo | Get-Profile-Photo |
| POST | /settings/profile/photo | Update-Profile-Photo |
| DELETE | /settings/profile/photo | Delete-Profile-Photo |

### account
| Method | Path | Description |
|--------|------|-------------|
| POST | /account/shards | Set-Shards |
| POST | /account/verify | Register-Account |
| POST | /account | Request-Code |

### contacts
| Method | Path | Description |
|--------|------|-------------|
| POST | /contacts | Check-Contact |

### messages
| Method | Path | Description |
|--------|------|-------------|
| POST | /messages | Send-Message |
| PUT | /messages/{MessageID} | Mark-Message-As-Read |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | Get-All-Groups |
| POST | /groups | Create-Group |
| GET | /groups/{GroupId} | Get-Group-Info |
| PUT | /groups/{GroupId} | Update-Group-Info |
| GET | /groups/{GroupId}/invite | Get-Group-Invite |
| DELETE | /groups/{GroupId}/invite | Delete-Group-Invite |
| DELETE | /groups/{GroupId}/participants | Remove-Group-Participant |
| POST | /groups/{GroupId}/leave | Leave-Group |
| GET | /groups/{GroupId}/icon | Get-Group-Icon-Binary |
| POST | /groups/{GroupId}/icon | Set-Group-Icon |
| DELETE | /groups/{GroupId}/icon | Delete-Group-Icon |
| DELETE | /groups/{GroupId}/admins | Demote-Group-Admin |
| PATCH | /groups/{GroupId}/admins | Promote-To-Group-Admin |

### health
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Check-Health |

### media
| Method | Path | Description |
|--------|------|-------------|
| POST | /media | Upload-Media |
| GET | /media/{MediaId} | Download-Media |
| DELETE | /media/{MediaId} | Delete-Media |

### stats
| Method | Path | Description |
|--------|------|-------------|
| GET | /stats/app | Get-App-Stats |
| GET | /stats/db | Get-DB-Stats |

### metrics
| Method | Path | Description |
|--------|------|-------------|
| GET | /metrics | Get-Metrics (since v2.21.3) |

### support
| Method | Path | Description |
|--------|------|-------------|
| GET | /support | Get-Support-Info |

### certificates
| Method | Path | Description |
|--------|------|-------------|
| GET | /certificates/external/ca | Download-CA-Certificate |
| POST | /certificates/external | Upload-Certificate |
| GET | /certificates/webhooks/ca | Download Webhook CA Certificate |
| POST | /certificates/webhooks/ca | Upload Webhook CA Certificate |
| DELETE | /certificates/webhooks/ca | Delete Webhook CA Certificate |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a login?" -> POST /users/login
- "Create a user?" -> POST /users
- "Get user details?" -> GET /users/{UserUsername}
- "Update a user?" -> PUT /users/{UserUsername}
- "Delete a user?" -> DELETE /users/{UserUsername}
- "Create a logout?" -> POST /users/logout
- "List all application?" -> GET /settings/application
- "Create a shard?" -> POST /account/shards
- "List all providers?" -> GET /settings/application/media/providers
- "Create a provider?" -> POST /settings/application/media/providers
- "Delete a provider?" -> DELETE /settings/application/media/providers/{ProviderName}
- "Create a backup?" -> POST /settings/backup
- "Create a restore?" -> POST /settings/restore
- "List all profile?" -> GET /settings/business/profile
- "Create a profile?" -> POST /settings/business/profile
- "List all about?" -> GET /settings/profile/about
- "Create a two-step?" -> POST /settings/account/two-step
- "Create a verify?" -> POST /account/verify
- "Create a contact?" -> POST /contacts
- "Create a message?" -> POST /messages
- "Update a message?" -> PUT /messages/{MessageID}
- "List all groups?" -> GET /groups
- "Create a group?" -> POST /groups
- "Get group details?" -> GET /groups/{GroupId}
- "Update a group?" -> PUT /groups/{GroupId}
- "List all invite?" -> GET /groups/{GroupId}/invite
- "Create a leave?" -> POST /groups/{GroupId}/leave
- "List all icon?" -> GET /groups/{GroupId}/icon
- "Create a icon?" -> POST /groups/{GroupId}/icon
- "List all health?" -> GET /health
- "List all photo?" -> GET /settings/profile/photo
- "Create a photo?" -> POST /settings/profile/photo
- "Create a account?" -> POST /account
- "Create a media?" -> POST /media
- "Get media details?" -> GET /media/{MediaId}
- "Delete a media?" -> DELETE /media/{MediaId}
- "List all app?" -> GET /stats/app
- "List all db?" -> GET /stats/db
- "List all metrics?" -> GET /metrics
- "List all support?" -> GET /support
- "List all ca?" -> GET /certificates/external/ca
- "Create a external?" -> POST /certificates/external
- "List all ca?" -> GET /certificates/webhooks/ca
- "Create a ca?" -> POST /certificates/webhooks/ca
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
