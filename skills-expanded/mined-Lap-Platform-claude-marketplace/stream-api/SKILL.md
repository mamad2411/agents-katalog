---
name: stream-api
description: "Stream API skill. Use when working with Stream for app, blocklists, campaigns. Covers 167 endpoints."
version: 1.0.0
generator: lapsh
---

# Stream API
API version: v223.6.0

## Auth
ApiKey Authorization in header | ApiKey api_key in query | ApiKey Stream-Auth-Type in header

## Base URL
https://chat.stream-io-api.com

## Setup
1. Set your API key in the appropriate header
2. GET /app -- verify access
3. POST /blocklists -- create first blocklists

## Endpoints

167 endpoints across 41 groups. See references/api-spec.lap for full details.

### app
| Method | Path | Description |
|--------|------|-------------|
| GET | /app | Get App Settings |
| PATCH | /app | Update App Settings |

### blocklists
| Method | Path | Description |
|--------|------|-------------|
| GET | /blocklists | List block lists |
| POST | /blocklists | Create block list |
| DELETE | /blocklists/{name} | Delete block list |
| GET | /blocklists/{name} | Get block list |
| PUT | /blocklists/{name} | Update block list |

### campaigns
| Method | Path | Description |
|--------|------|-------------|
| GET | /campaigns/{id} | Get campaign |
| POST | /campaigns/{id}/start | Start/schedule campaign |
| POST | /campaigns/{id}/stop | Stop campaign |
| POST | /campaigns/query | Query campaigns |

### channels
| Method | Path | Description |
|--------|------|-------------|
| POST | /channels | Query channels |
| DELETE | /channels/{type}/{id} | Delete channel |
| PATCH | /channels/{type}/{id} | Partially update channel |
| POST | /channels/{type}/{id} | Update channel |
| DELETE | /channels/{type}/{id}/draft | Delete draft |
| GET | /channels/{type}/{id}/draft | Get draft |
| POST | /channels/{type}/{id}/event | Send event |
| DELETE | /channels/{type}/{id}/file | Delete file |
| POST | /channels/{type}/{id}/file | Upload file |
| POST | /channels/{type}/{id}/hide | Hide channel |
| DELETE | /channels/{type}/{id}/image | Delete image |
| POST | /channels/{type}/{id}/image | Upload image |
| PATCH | /channels/{type}/{id}/member | Partially channel member update |
| POST | /channels/{type}/{id}/message | Send new message |
| GET | /channels/{type}/{id}/messages | Get many messages |
| POST | /channels/{type}/{id}/query | Get or create channel |
| POST | /channels/{type}/{id}/read | Mark read |
| POST | /channels/{type}/{id}/show | Show channel |
| POST | /channels/{type}/{id}/truncate | Truncate channel |
| POST | /channels/{type}/{id}/unread | Mark unread |
| POST | /channels/{type}/query | Get or create channel |
| PUT | /channels/batch | Update channels in batch |
| POST | /channels/delete | Deletes channels asynchronously |
| POST | /channels/delivered | Mark channel message delivery status |
| POST | /channels/read | Mark channels as read |

### channeltypes
| Method | Path | Description |
|--------|------|-------------|
| GET | /channeltypes | List channel types |
| POST | /channeltypes | Create channel type |
| DELETE | /channeltypes/{name} | Delete channel type |
| GET | /channeltypes/{name} | Get channel type |
| PUT | /channeltypes/{name} | Update channel type |

### check_push
| Method | Path | Description |
|--------|------|-------------|
| POST | /check_push | Check push |

### check_sns
| Method | Path | Description |
|--------|------|-------------|
| POST | /check_sns | Check SNS |

### check_sqs
| Method | Path | Description |
|--------|------|-------------|
| POST | /check_sqs | Check SQS |

### commands
| Method | Path | Description |
|--------|------|-------------|
| GET | /commands | List commands |
| POST | /commands | Create command |
| DELETE | /commands/{name} | Delete command |
| GET | /commands/{name} | Get command |
| PUT | /commands/{name} | Update command |

### devices
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /devices | Delete device |
| GET | /devices | List devices |
| POST | /devices | Create device |

### drafts
| Method | Path | Description |
|--------|------|-------------|
| POST | /drafts/query | Query draft messages |

### export
| Method | Path | Description |
|--------|------|-------------|
| POST | /export/users | Export users |

### export_channels
| Method | Path | Description |
|--------|------|-------------|
| POST | /export_channels | Export channels |

### external_storage
| Method | Path | Description |
|--------|------|-------------|
| GET | /external_storage | List external storage |
| POST | /external_storage | Create external storage |
| DELETE | /external_storage/{name} | Delete external storage |
| PUT | /external_storage/{name} | Update External Storage |
| GET | /external_storage/{name}/check | Check External Storage |

### guest
| Method | Path | Description |
|--------|------|-------------|
| POST | /guest | Create Guest |

### import_urls
| Method | Path | Description |
|--------|------|-------------|
| POST | /import_urls | Create import URL |

### imports
| Method | Path | Description |
|--------|------|-------------|
| GET | /imports | Get import |
| POST | /imports | Create import |
| GET | /imports/{id} | Get import |
| GET | /imports/v2 | List import v2 tasks |
| POST | /imports/v2 | Create import v2 task |
| DELETE | /imports/v2/{id} | Delete import v2 task |
| GET | /imports/v2/{id} | Get import v2 task |

### members
| Method | Path | Description |
|--------|------|-------------|
| GET | /members | Query members |

### messages
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /messages/{id} | Delete message |
| GET | /messages/{id} | Get message |
| POST | /messages/{id} | Update message |
| PUT | /messages/{id} | Partially message update |
| POST | /messages/{id}/action | Run message command action |
| POST | /messages/{id}/commit | Commit message |
| PATCH | /messages/{id}/ephemeral | Ephemeral message update |
| POST | /messages/{id}/reaction | Send reaction |
| DELETE | /messages/{id}/reaction/{type} | Delete reaction |
| GET | /messages/{id}/reactions | Get reactions |
| POST | /messages/{id}/reactions | Get reactions on a message |
| POST | /messages/{id}/translate | Translate message |
| POST | /messages/{id}/undelete | Undelete message |
| POST | /messages/{message_id}/polls/{poll_id}/vote | Cast vote |
| DELETE | /messages/{message_id}/polls/{poll_id}/vote/{vote_id} | Delete vote |
| DELETE | /messages/{message_id}/reminders | Delete reminder |
| PATCH | /messages/{message_id}/reminders | Updates Reminder |
| POST | /messages/{message_id}/reminders | Create reminder |
| GET | /messages/{parent_id}/replies | Get replies |
| POST | /messages/history | Query message history |

### moderation
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /moderation/ban | Unban user |
| POST | /moderation/ban | Ban user |
| POST | /moderation/flag | Flag |
| GET | /moderation/flags/message | Query Message Flags |
| POST | /moderation/mute | Mute user |
| POST | /moderation/mute/channel | Mute channel |
| POST | /moderation/unmute | Unmute user |
| POST | /moderation/unmute/channel | Unmute channel |

### og
| Method | Path | Description |
|--------|------|-------------|
| GET | /og | Get OG |

### permissions
| Method | Path | Description |
|--------|------|-------------|
| GET | /permissions | List permissions |
| GET | /permissions/{id} | Get permission |

### polls
| Method | Path | Description |
|--------|------|-------------|
| POST | /polls | Create poll |
| PUT | /polls | Update poll |
| DELETE | /polls/{poll_id} | Delete poll |
| GET | /polls/{poll_id} | Get poll |
| PATCH | /polls/{poll_id} | Partial update poll |
| POST | /polls/{poll_id}/options | Create poll option |
| PUT | /polls/{poll_id}/options | Update poll option |
| DELETE | /polls/{poll_id}/options/{option_id} | Delete poll option |
| GET | /polls/{poll_id}/options/{option_id} | Get poll option |
| POST | /polls/{poll_id}/votes | Query votes |
| POST | /polls/query | Query polls |

### push_preferences
| Method | Path | Description |
|--------|------|-------------|
| POST | /push_preferences | Push notification preferences |

### push_providers
| Method | Path | Description |
|--------|------|-------------|
| GET | /push_providers | List push providers |
| POST | /push_providers | Upsert a push provider |
| DELETE | /push_providers/{type}/{name} | Delete a push provider |

### push_templates
| Method | Path | Description |
|--------|------|-------------|
| GET | /push_templates | Get push notification templates |
| POST | /push_templates | Upsert a push notification template |

### query_banned_users
| Method | Path | Description |
|--------|------|-------------|
| GET | /query_banned_users | Query Banned Users |

### query_future_channel_bans
| Method | Path | Description |
|--------|------|-------------|
| GET | /query_future_channel_bans | Query Future Channel Bans |

### rate_limits
| Method | Path | Description |
|--------|------|-------------|
| GET | /rate_limits | Get rate limits |

### reminders
| Method | Path | Description |
|--------|------|-------------|
| POST | /reminders/query | Query reminders |

### roles
| Method | Path | Description |
|--------|------|-------------|
| GET | /roles | List roles |
| POST | /roles | Create role |
| DELETE | /roles/{name} | Delete role |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Search messages |

### segments
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /segments/{id} | Delete segment |
| GET | /segments/{id} | Get segment |
| POST | /segments/{id}/deletetargets | Delete targets from a segment |
| GET | /segments/{id}/target/{target_id} | Check whether a target exists in a segment |
| POST | /segments/{id}/targets/query | Query segment targets |
| POST | /segments/query | Query segments |

### stats
| Method | Path | Description |
|--------|------|-------------|
| POST | /stats/team_usage | Query Team Usage Statistics |

### tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | /tasks/{id} | Get status of a task |

### threads
| Method | Path | Description |
|--------|------|-------------|
| POST | /threads | Query Threads |
| GET | /threads/{message_id} | Get Thread |
| PATCH | /threads/{message_id} | Partially update thread |

### unread
| Method | Path | Description |
|--------|------|-------------|
| GET | /unread | Unread counts |

### unread_batch
| Method | Path | Description |
|--------|------|-------------|
| POST | /unread_batch | Batch unread counts |

### uploads
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /uploads/file | Delete file |
| POST | /uploads/file | Upload file |
| DELETE | /uploads/image | Delete image |
| POST | /uploads/image | Upload image |

### usergroups
| Method | Path | Description |
|--------|------|-------------|
| GET | /usergroups | List user groups |
| POST | /usergroups | Create user group |
| DELETE | /usergroups/{id} | Delete user group |
| GET | /usergroups/{id} | Get user group |
| PUT | /usergroups/{id} | Update user group |
| DELETE | /usergroups/{id}/members | Remove user group members |
| POST | /usergroups/{id}/members | Add user group members |
| GET | /usergroups/search | Search user groups |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users | Query users |
| PATCH | /users | Partially update user |
| POST | /users | Upsert users |
| POST | /users/{user_id}/deactivate | Deactivate user |
| POST | /users/{user_id}/event | Send user event |
| GET | /users/{user_id}/export | Export user |
| POST | /users/{user_id}/reactivate | Reactivate user |
| GET | /users/block | Get list of blocked Users |
| POST | /users/block | Block user |
| POST | /users/deactivate | Deactivate users |
| POST | /users/delete | Delete Users |
| GET | /users/live_locations | Get user live locations |
| PUT | /users/live_locations | Update live location |
| POST | /users/reactivate | Reactivate users |
| POST | /users/restore | Restore users |
| POST | /users/unblock | Unblock user |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all app?" -> GET /app
- "List all blocklists?" -> GET /blocklists
- "Create a blocklist?" -> POST /blocklists
- "Delete a blocklist?" -> DELETE /blocklists/{name}
- "Get blocklist details?" -> GET /blocklists/{name}
- "Update a blocklist?" -> PUT /blocklists/{name}
- "Get campaign details?" -> GET /campaigns/{id}
- "Create a start?" -> POST /campaigns/{id}/start
- "Create a stop?" -> POST /campaigns/{id}/stop
- "Create a query?" -> POST /campaigns/query
- "Create a channel?" -> POST /channels
- "Delete a channel?" -> DELETE /channels/{type}/{id}
- "Partially update a channel?" -> PATCH /channels/{type}/{id}
- "List all draft?" -> GET /channels/{type}/{id}/draft
- "Create a event?" -> POST /channels/{type}/{id}/event
- "Create a file?" -> POST /channels/{type}/{id}/file
- "Create a hide?" -> POST /channels/{type}/{id}/hide
- "Create a image?" -> POST /channels/{type}/{id}/image
- "Create a message?" -> POST /channels/{type}/{id}/message
- "List all messages?" -> GET /channels/{type}/{id}/messages
- "Create a query?" -> POST /channels/{type}/{id}/query
- "Create a read?" -> POST /channels/{type}/{id}/read
- "Create a show?" -> POST /channels/{type}/{id}/show
- "Create a truncate?" -> POST /channels/{type}/{id}/truncate
- "Create a unread?" -> POST /channels/{type}/{id}/unread
- "Create a query?" -> POST /channels/{type}/query
- "Create a delete?" -> POST /channels/delete
- "Create a delivered?" -> POST /channels/delivered
- "Create a read?" -> POST /channels/read
- "List all channeltypes?" -> GET /channeltypes
- "Create a channeltype?" -> POST /channeltypes
- "Delete a channeltype?" -> DELETE /channeltypes/{name}
- "Get channeltype details?" -> GET /channeltypes/{name}
- "Update a channeltype?" -> PUT /channeltypes/{name}
- "Create a check_push?" -> POST /check_push
- "Create a check_sn?" -> POST /check_sns
- "Create a check_sq?" -> POST /check_sqs
- "List all commands?" -> GET /commands
- "Create a command?" -> POST /commands
- "Delete a command?" -> DELETE /commands/{name}
- "Get command details?" -> GET /commands/{name}
- "Update a command?" -> PUT /commands/{name}
- "List all devices?" -> GET /devices
- "Create a device?" -> POST /devices
- "Create a query?" -> POST /drafts/query
- "Create a user?" -> POST /export/users
- "Create a export_channel?" -> POST /export_channels
- "List all external_storage?" -> GET /external_storage
- "Create a external_storage?" -> POST /external_storage
- "Delete a external_storage?" -> DELETE /external_storage/{name}
- "Update a external_storage?" -> PUT /external_storage/{name}
- "List all check?" -> GET /external_storage/{name}/check
- "Create a guest?" -> POST /guest
- "Create a import_url?" -> POST /import_urls
- "List all imports?" -> GET /imports
- "Create a import?" -> POST /imports
- "Get import details?" -> GET /imports/{id}
- "List all imports?" -> GET /imports/v2
- "Create a import?" -> POST /imports/v2
- "Delete a import?" -> DELETE /imports/v2/{id}
- "Get import details?" -> GET /imports/v2/{id}
- "List all members?" -> GET /members
- "Delete a message?" -> DELETE /messages/{id}
- "Get message details?" -> GET /messages/{id}
- "Update a message?" -> PUT /messages/{id}
- "Create a action?" -> POST /messages/{id}/action
- "Create a commit?" -> POST /messages/{id}/commit
- "Create a reaction?" -> POST /messages/{id}/reaction
- "Delete a reaction?" -> DELETE /messages/{id}/reaction/{type}
- "List all reactions?" -> GET /messages/{id}/reactions
- "Create a reaction?" -> POST /messages/{id}/reactions
- "Create a translate?" -> POST /messages/{id}/translate
- "Create a undelete?" -> POST /messages/{id}/undelete
- "Create a vote?" -> POST /messages/{message_id}/polls/{poll_id}/vote
- "Delete a vote?" -> DELETE /messages/{message_id}/polls/{poll_id}/vote/{vote_id}
- "Create a reminder?" -> POST /messages/{message_id}/reminders
- "List all replies?" -> GET /messages/{parent_id}/replies
- "Create a history?" -> POST /messages/history
- "Create a ban?" -> POST /moderation/ban
- "Create a flag?" -> POST /moderation/flag
- "List all message?" -> GET /moderation/flags/message
- "Create a mute?" -> POST /moderation/mute
- "Create a channel?" -> POST /moderation/mute/channel
- "Create a unmute?" -> POST /moderation/unmute
- "Create a channel?" -> POST /moderation/unmute/channel
- "List all og?" -> GET /og
- "List all permissions?" -> GET /permissions
- "Get permission details?" -> GET /permissions/{id}
- "Create a poll?" -> POST /polls
- "Delete a poll?" -> DELETE /polls/{poll_id}
- "Get poll details?" -> GET /polls/{poll_id}
- "Partially update a poll?" -> PATCH /polls/{poll_id}
- "Create a option?" -> POST /polls/{poll_id}/options
- "Delete a option?" -> DELETE /polls/{poll_id}/options/{option_id}
- "Get option details?" -> GET /polls/{poll_id}/options/{option_id}
- "Create a vote?" -> POST /polls/{poll_id}/votes
- "Create a query?" -> POST /polls/query
- "Create a push_preference?" -> POST /push_preferences
- "List all push_providers?" -> GET /push_providers
- "Create a push_provider?" -> POST /push_providers
- "Delete a push_provider?" -> DELETE /push_providers/{type}/{name}
- "List all push_templates?" -> GET /push_templates
- "Create a push_template?" -> POST /push_templates
- "List all query_banned_users?" -> GET /query_banned_users
- "List all query_future_channel_bans?" -> GET /query_future_channel_bans
- "List all rate_limits?" -> GET /rate_limits
- "Create a query?" -> POST /reminders/query
- "List all roles?" -> GET /roles
- "Create a role?" -> POST /roles
- "Delete a role?" -> DELETE /roles/{name}
- "List all search?" -> GET /search
- "Delete a segment?" -> DELETE /segments/{id}
- "Get segment details?" -> GET /segments/{id}
- "Create a deletetarget?" -> POST /segments/{id}/deletetargets
- "Get target details?" -> GET /segments/{id}/target/{target_id}
- "Create a query?" -> POST /segments/{id}/targets/query
- "Create a query?" -> POST /segments/query
- "Create a team_usage?" -> POST /stats/team_usage
- "Get task details?" -> GET /tasks/{id}
- "Create a thread?" -> POST /threads
- "Get thread details?" -> GET /threads/{message_id}
- "Partially update a thread?" -> PATCH /threads/{message_id}
- "List all unread?" -> GET /unread
- "Create a unread_batch?" -> POST /unread_batch
- "Create a file?" -> POST /uploads/file
- "Create a image?" -> POST /uploads/image
- "List all usergroups?" -> GET /usergroups
- "Create a usergroup?" -> POST /usergroups
- "Delete a usergroup?" -> DELETE /usergroups/{id}
- "Get usergroup details?" -> GET /usergroups/{id}
- "Update a usergroup?" -> PUT /usergroups/{id}
- "Create a member?" -> POST /usergroups/{id}/members
- "Search search?" -> GET /usergroups/search
- "List all users?" -> GET /users
- "Create a user?" -> POST /users
- "Create a deactivate?" -> POST /users/{user_id}/deactivate
- "Create a event?" -> POST /users/{user_id}/event
- "List all export?" -> GET /users/{user_id}/export
- "Create a reactivate?" -> POST /users/{user_id}/reactivate
- "List all block?" -> GET /users/block
- "Create a block?" -> POST /users/block
- "Create a deactivate?" -> POST /users/deactivate
- "Create a delete?" -> POST /users/delete
- "List all live_locations?" -> GET /users/live_locations
- "Create a reactivate?" -> POST /users/reactivate
- "Create a restore?" -> POST /users/restore
- "Create a unblock?" -> POST /users/unblock
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
