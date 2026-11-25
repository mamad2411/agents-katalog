---
name: discord-http-api-preview
description: "Discord HTTP API (Preview) API skill. Use when working with Discord HTTP API (Preview) for applications, channels, gateway. Covers 229 endpoints."
version: 1.0.0
generator: lapsh
---

# Discord HTTP API (Preview)
API version: 10

## Auth
ApiKey Authorization in header | OAuth2

## Base URL
https://discord.com/api/v10

## Setup
1. Set your API key in the appropriate header
2. GET /applications/@me -- verify access
3. POST /applications/{application_id}/attachment -- create first attachment

## Endpoints

229 endpoints across 16 groups. See references/api-spec.lap for full details.

### applications
| Method | Path | Description |
|--------|------|-------------|
| GET | /applications/@me |  |
| PATCH | /applications/@me |  |
| GET | /applications/{application_id} |  |
| PATCH | /applications/{application_id} |  |
| GET | /applications/{application_id}/activity-instances/{instance_id} |  |
| POST | /applications/{application_id}/attachment |  |
| GET | /applications/{application_id}/commands |  |
| PUT | /applications/{application_id}/commands |  |
| POST | /applications/{application_id}/commands |  |
| GET | /applications/{application_id}/commands/{command_id} |  |
| DELETE | /applications/{application_id}/commands/{command_id} |  |
| PATCH | /applications/{application_id}/commands/{command_id} |  |
| GET | /applications/{application_id}/emojis |  |
| POST | /applications/{application_id}/emojis |  |
| GET | /applications/{application_id}/emojis/{emoji_id} |  |
| DELETE | /applications/{application_id}/emojis/{emoji_id} |  |
| PATCH | /applications/{application_id}/emojis/{emoji_id} |  |
| GET | /applications/{application_id}/entitlements |  |
| POST | /applications/{application_id}/entitlements |  |
| GET | /applications/{application_id}/entitlements/{entitlement_id} |  |
| DELETE | /applications/{application_id}/entitlements/{entitlement_id} |  |
| POST | /applications/{application_id}/entitlements/{entitlement_id}/consume |  |
| GET | /applications/{application_id}/guilds/{guild_id}/commands |  |
| PUT | /applications/{application_id}/guilds/{guild_id}/commands |  |
| POST | /applications/{application_id}/guilds/{guild_id}/commands |  |
| GET | /applications/{application_id}/guilds/{guild_id}/commands/permissions |  |
| GET | /applications/{application_id}/guilds/{guild_id}/commands/{command_id} |  |
| DELETE | /applications/{application_id}/guilds/{guild_id}/commands/{command_id} |  |
| PATCH | /applications/{application_id}/guilds/{guild_id}/commands/{command_id} |  |
| GET | /applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions |  |
| PUT | /applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions |  |
| GET | /applications/{application_id}/role-connections/metadata |  |
| PUT | /applications/{application_id}/role-connections/metadata |  |

### channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /channels/{channel_id} |  |
| DELETE | /channels/{channel_id} |  |
| PATCH | /channels/{channel_id} |  |
| POST | /channels/{channel_id}/followers |  |
| GET | /channels/{channel_id}/invites |  |
| POST | /channels/{channel_id}/invites |  |
| GET | /channels/{channel_id}/messages |  |
| POST | /channels/{channel_id}/messages |  |
| POST | /channels/{channel_id}/messages/bulk-delete |  |
| GET | /channels/{channel_id}/messages/pins |  |
| PUT | /channels/{channel_id}/messages/pins/{message_id} |  |
| DELETE | /channels/{channel_id}/messages/pins/{message_id} |  |
| GET | /channels/{channel_id}/messages/{message_id} |  |
| DELETE | /channels/{channel_id}/messages/{message_id} |  |
| PATCH | /channels/{channel_id}/messages/{message_id} |  |
| POST | /channels/{channel_id}/messages/{message_id}/crosspost |  |
| DELETE | /channels/{channel_id}/messages/{message_id}/reactions |  |
| GET | /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name} |  |
| DELETE | /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name} |  |
| PUT | /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}/@me |  |
| DELETE | /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}/@me |  |
| DELETE | /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}/{user_id} |  |
| POST | /channels/{channel_id}/messages/{message_id}/threads |  |
| PUT | /channels/{channel_id}/permissions/{overwrite_id} |  |
| DELETE | /channels/{channel_id}/permissions/{overwrite_id} |  |
| GET | /channels/{channel_id}/pins |  |
| PUT | /channels/{channel_id}/pins/{message_id} |  |
| DELETE | /channels/{channel_id}/pins/{message_id} |  |
| GET | /channels/{channel_id}/polls/{message_id}/answers/{answer_id} |  |
| POST | /channels/{channel_id}/polls/{message_id}/expire |  |
| PUT | /channels/{channel_id}/recipients/{user_id} |  |
| DELETE | /channels/{channel_id}/recipients/{user_id} |  |
| POST | /channels/{channel_id}/send-soundboard-sound |  |
| GET | /channels/{channel_id}/thread-members |  |
| PUT | /channels/{channel_id}/thread-members/@me |  |
| DELETE | /channels/{channel_id}/thread-members/@me |  |
| GET | /channels/{channel_id}/thread-members/{user_id} |  |
| PUT | /channels/{channel_id}/thread-members/{user_id} |  |
| DELETE | /channels/{channel_id}/thread-members/{user_id} |  |
| POST | /channels/{channel_id}/threads |  |
| GET | /channels/{channel_id}/threads/archived/private |  |
| GET | /channels/{channel_id}/threads/archived/public |  |
| GET | /channels/{channel_id}/threads/search |  |
| POST | /channels/{channel_id}/typing |  |
| GET | /channels/{channel_id}/users/@me/threads/archived/private |  |
| GET | /channels/{channel_id}/webhooks |  |
| POST | /channels/{channel_id}/webhooks |  |

### gateway
| Method | Path | Description |
|--------|------|-------------|
| GET | /gateway |  |
| GET | /gateway/bot |  |

### guilds
| Method | Path | Description |
|--------|------|-------------|
| GET | /guilds/templates/{code} |  |
| GET | /guilds/{guild_id} |  |
| PATCH | /guilds/{guild_id} |  |
| GET | /guilds/{guild_id}/audit-logs |  |
| GET | /guilds/{guild_id}/auto-moderation/rules |  |
| POST | /guilds/{guild_id}/auto-moderation/rules |  |
| GET | /guilds/{guild_id}/auto-moderation/rules/{rule_id} |  |
| DELETE | /guilds/{guild_id}/auto-moderation/rules/{rule_id} |  |
| PATCH | /guilds/{guild_id}/auto-moderation/rules/{rule_id} |  |
| GET | /guilds/{guild_id}/bans |  |
| GET | /guilds/{guild_id}/bans/{user_id} |  |
| PUT | /guilds/{guild_id}/bans/{user_id} |  |
| DELETE | /guilds/{guild_id}/bans/{user_id} |  |
| POST | /guilds/{guild_id}/bulk-ban |  |
| GET | /guilds/{guild_id}/channels |  |
| POST | /guilds/{guild_id}/channels |  |
| PATCH | /guilds/{guild_id}/channels |  |
| GET | /guilds/{guild_id}/emojis |  |
| POST | /guilds/{guild_id}/emojis |  |
| GET | /guilds/{guild_id}/emojis/{emoji_id} |  |
| DELETE | /guilds/{guild_id}/emojis/{emoji_id} |  |
| PATCH | /guilds/{guild_id}/emojis/{emoji_id} |  |
| GET | /guilds/{guild_id}/integrations |  |
| DELETE | /guilds/{guild_id}/integrations/{integration_id} |  |
| GET | /guilds/{guild_id}/invites |  |
| GET | /guilds/{guild_id}/members |  |
| PATCH | /guilds/{guild_id}/members/@me |  |
| GET | /guilds/{guild_id}/members/search |  |
| GET | /guilds/{guild_id}/members/{user_id} |  |
| PUT | /guilds/{guild_id}/members/{user_id} |  |
| DELETE | /guilds/{guild_id}/members/{user_id} |  |
| PATCH | /guilds/{guild_id}/members/{user_id} |  |
| PUT | /guilds/{guild_id}/members/{user_id}/roles/{role_id} |  |
| DELETE | /guilds/{guild_id}/members/{user_id}/roles/{role_id} |  |
| GET | /guilds/{guild_id}/new-member-welcome |  |
| GET | /guilds/{guild_id}/onboarding |  |
| PUT | /guilds/{guild_id}/onboarding |  |
| GET | /guilds/{guild_id}/preview |  |
| GET | /guilds/{guild_id}/prune |  |
| POST | /guilds/{guild_id}/prune |  |
| GET | /guilds/{guild_id}/regions |  |
| GET | /guilds/{guild_id}/roles |  |
| POST | /guilds/{guild_id}/roles |  |
| PATCH | /guilds/{guild_id}/roles |  |
| GET | /guilds/{guild_id}/roles/member-counts |  |
| GET | /guilds/{guild_id}/roles/{role_id} |  |
| DELETE | /guilds/{guild_id}/roles/{role_id} |  |
| PATCH | /guilds/{guild_id}/roles/{role_id} |  |
| GET | /guilds/{guild_id}/scheduled-events |  |
| POST | /guilds/{guild_id}/scheduled-events |  |
| GET | /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id} |  |
| DELETE | /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id} |  |
| PATCH | /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id} |  |
| GET | /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users |  |
| GET | /guilds/{guild_id}/soundboard-sounds |  |
| POST | /guilds/{guild_id}/soundboard-sounds |  |
| GET | /guilds/{guild_id}/soundboard-sounds/{sound_id} |  |
| DELETE | /guilds/{guild_id}/soundboard-sounds/{sound_id} |  |
| PATCH | /guilds/{guild_id}/soundboard-sounds/{sound_id} |  |
| GET | /guilds/{guild_id}/stickers |  |
| POST | /guilds/{guild_id}/stickers |  |
| GET | /guilds/{guild_id}/stickers/{sticker_id} |  |
| DELETE | /guilds/{guild_id}/stickers/{sticker_id} |  |
| PATCH | /guilds/{guild_id}/stickers/{sticker_id} |  |
| GET | /guilds/{guild_id}/templates |  |
| POST | /guilds/{guild_id}/templates |  |
| PUT | /guilds/{guild_id}/templates/{code} |  |
| DELETE | /guilds/{guild_id}/templates/{code} |  |
| PATCH | /guilds/{guild_id}/templates/{code} |  |
| GET | /guilds/{guild_id}/threads/active |  |
| GET | /guilds/{guild_id}/vanity-url |  |
| GET | /guilds/{guild_id}/voice-states/@me |  |
| PATCH | /guilds/{guild_id}/voice-states/@me |  |
| GET | /guilds/{guild_id}/voice-states/{user_id} |  |
| PATCH | /guilds/{guild_id}/voice-states/{user_id} |  |
| GET | /guilds/{guild_id}/webhooks |  |
| GET | /guilds/{guild_id}/welcome-screen |  |
| PATCH | /guilds/{guild_id}/welcome-screen |  |
| GET | /guilds/{guild_id}/widget |  |
| PATCH | /guilds/{guild_id}/widget |  |
| GET | /guilds/{guild_id}/widget.json |  |
| GET | /guilds/{guild_id}/widget.png |  |

### interactions
| Method | Path | Description |
|--------|------|-------------|
| POST | /interactions/{interaction_id}/{interaction_token}/callback |  |

### invites
| Method | Path | Description |
|--------|------|-------------|
| GET | /invites/{code} |  |
| DELETE | /invites/{code} |  |
| GET | /invites/{code}/target-users | Get the target users for an invite. |
| PUT | /invites/{code}/target-users | Update the target users for an existing invite. |
| GET | /invites/{code}/target-users/job-status | Get the target users job status for an invite. |

### lobbies
| Method | Path | Description |
|--------|------|-------------|
| PUT | /lobbies |  |
| POST | /lobbies |  |
| GET | /lobbies/{lobby_id} |  |
| PATCH | /lobbies/{lobby_id} |  |
| PATCH | /lobbies/{lobby_id}/channel-linking |  |
| DELETE | /lobbies/{lobby_id}/members/@me |  |
| POST | /lobbies/{lobby_id}/members/@me/invites |  |
| POST | /lobbies/{lobby_id}/members/bulk |  |
| PUT | /lobbies/{lobby_id}/members/{user_id} |  |
| DELETE | /lobbies/{lobby_id}/members/{user_id} |  |
| POST | /lobbies/{lobby_id}/members/{user_id}/invites |  |
| GET | /lobbies/{lobby_id}/messages |  |
| POST | /lobbies/{lobby_id}/messages |  |
| PUT | /lobbies/{lobby_id}/messages/{message_id}/moderation-metadata | Update the external moderation metadata for a lobby message. |

### oauth2
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth2/@me |  |
| GET | /oauth2/applications/@me |  |
| GET | /oauth2/keys |  |
| GET | /oauth2/userinfo |  |

### partner-sdk
| Method | Path | Description |
|--------|------|-------------|
| PUT | /partner-sdk/dms/{user_id_1}/{user_id_2}/messages/{message_id}/moderation-metadata | Update the external moderation metadata for a user message (DM). |
| POST | /partner-sdk/provisional-accounts/unmerge |  |
| POST | /partner-sdk/provisional-accounts/unmerge/bot |  |
| POST | /partner-sdk/token |  |
| POST | /partner-sdk/token/bot |  |

### soundboard-default-sounds
| Method | Path | Description |
|--------|------|-------------|
| GET | /soundboard-default-sounds |  |

### stage-instances
| Method | Path | Description |
|--------|------|-------------|
| POST | /stage-instances |  |
| GET | /stage-instances/{channel_id} |  |
| DELETE | /stage-instances/{channel_id} |  |
| PATCH | /stage-instances/{channel_id} |  |

### sticker-packs
| Method | Path | Description |
|--------|------|-------------|
| GET | /sticker-packs |  |
| GET | /sticker-packs/{pack_id} |  |

### stickers
| Method | Path | Description |
|--------|------|-------------|
| GET | /stickers/{sticker_id} |  |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/@me |  |
| PATCH | /users/@me |  |
| GET | /users/@me/applications/{application_id}/entitlements |  |
| GET | /users/@me/applications/{application_id}/role-connection |  |
| PUT | /users/@me/applications/{application_id}/role-connection |  |
| DELETE | /users/@me/applications/{application_id}/role-connection |  |
| POST | /users/@me/channels |  |
| GET | /users/@me/connections |  |
| GET | /users/@me/guilds |  |
| DELETE | /users/@me/guilds/{guild_id} |  |
| GET | /users/@me/guilds/{guild_id}/member |  |
| GET | /users/{user_id} |  |

### voice
| Method | Path | Description |
|--------|------|-------------|
| GET | /voice/regions |  |

### webhooks
| Method | Path | Description |
|--------|------|-------------|
| GET | /webhooks/{webhook_id} |  |
| DELETE | /webhooks/{webhook_id} |  |
| PATCH | /webhooks/{webhook_id} |  |
| GET | /webhooks/{webhook_id}/{webhook_token} |  |
| POST | /webhooks/{webhook_id}/{webhook_token} |  |
| DELETE | /webhooks/{webhook_id}/{webhook_token} |  |
| PATCH | /webhooks/{webhook_id}/{webhook_token} |  |
| POST | /webhooks/{webhook_id}/{webhook_token}/github |  |
| GET | /webhooks/{webhook_id}/{webhook_token}/messages/@original |  |
| DELETE | /webhooks/{webhook_id}/{webhook_token}/messages/@original |  |
| PATCH | /webhooks/{webhook_id}/{webhook_token}/messages/@original |  |
| GET | /webhooks/{webhook_id}/{webhook_token}/messages/{message_id} |  |
| DELETE | /webhooks/{webhook_id}/{webhook_token}/messages/{message_id} |  |
| PATCH | /webhooks/{webhook_id}/{webhook_token}/messages/{message_id} |  |
| POST | /webhooks/{webhook_id}/{webhook_token}/slack |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all @me?" -> GET /applications/@me
- "Get application details?" -> GET /applications/{application_id}
- "Partially update a application?" -> PATCH /applications/{application_id}
- "Get activity-instance details?" -> GET /applications/{application_id}/activity-instances/{instance_id}
- "Create a attachment?" -> POST /applications/{application_id}/attachment
- "List all commands?" -> GET /applications/{application_id}/commands
- "Create a command?" -> POST /applications/{application_id}/commands
- "Get command details?" -> GET /applications/{application_id}/commands/{command_id}
- "Delete a command?" -> DELETE /applications/{application_id}/commands/{command_id}
- "Partially update a command?" -> PATCH /applications/{application_id}/commands/{command_id}
- "List all emojis?" -> GET /applications/{application_id}/emojis
- "Create a emojis?" -> POST /applications/{application_id}/emojis
- "Get emojis details?" -> GET /applications/{application_id}/emojis/{emoji_id}
- "Delete a emojis?" -> DELETE /applications/{application_id}/emojis/{emoji_id}
- "Partially update a emojis?" -> PATCH /applications/{application_id}/emojis/{emoji_id}
- "List all entitlements?" -> GET /applications/{application_id}/entitlements
- "Create a entitlement?" -> POST /applications/{application_id}/entitlements
- "Get entitlement details?" -> GET /applications/{application_id}/entitlements/{entitlement_id}
- "Delete a entitlement?" -> DELETE /applications/{application_id}/entitlements/{entitlement_id}
- "Create a consume?" -> POST /applications/{application_id}/entitlements/{entitlement_id}/consume
- "List all commands?" -> GET /applications/{application_id}/guilds/{guild_id}/commands
- "Create a command?" -> POST /applications/{application_id}/guilds/{guild_id}/commands
- "List all permissions?" -> GET /applications/{application_id}/guilds/{guild_id}/commands/permissions
- "Get command details?" -> GET /applications/{application_id}/guilds/{guild_id}/commands/{command_id}
- "Delete a command?" -> DELETE /applications/{application_id}/guilds/{guild_id}/commands/{command_id}
- "Partially update a command?" -> PATCH /applications/{application_id}/guilds/{guild_id}/commands/{command_id}
- "List all permissions?" -> GET /applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions
- "List all metadata?" -> GET /applications/{application_id}/role-connections/metadata
- "Get channel details?" -> GET /channels/{channel_id}
- "Delete a channel?" -> DELETE /channels/{channel_id}
- "Partially update a channel?" -> PATCH /channels/{channel_id}
- "Create a follower?" -> POST /channels/{channel_id}/followers
- "List all invites?" -> GET /channels/{channel_id}/invites
- "Create a invite?" -> POST /channels/{channel_id}/invites
- "List all messages?" -> GET /channels/{channel_id}/messages
- "Create a message?" -> POST /channels/{channel_id}/messages
- "Create a bulk-delete?" -> POST /channels/{channel_id}/messages/bulk-delete
- "List all pins?" -> GET /channels/{channel_id}/messages/pins
- "Update a pin?" -> PUT /channels/{channel_id}/messages/pins/{message_id}
- "Delete a pin?" -> DELETE /channels/{channel_id}/messages/pins/{message_id}
- "Get message details?" -> GET /channels/{channel_id}/messages/{message_id}
- "Delete a message?" -> DELETE /channels/{channel_id}/messages/{message_id}
- "Partially update a message?" -> PATCH /channels/{channel_id}/messages/{message_id}
- "Create a crosspost?" -> POST /channels/{channel_id}/messages/{message_id}/crosspost
- "Get reaction details?" -> GET /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}
- "Delete a reaction?" -> DELETE /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}
- "Delete a reaction?" -> DELETE /channels/{channel_id}/messages/{message_id}/reactions/{emoji_name}/{user_id}
- "Create a thread?" -> POST /channels/{channel_id}/messages/{message_id}/threads
- "Update a permission?" -> PUT /channels/{channel_id}/permissions/{overwrite_id}
- "Delete a permission?" -> DELETE /channels/{channel_id}/permissions/{overwrite_id}
- "List all pins?" -> GET /channels/{channel_id}/pins
- "Update a pin?" -> PUT /channels/{channel_id}/pins/{message_id}
- "Delete a pin?" -> DELETE /channels/{channel_id}/pins/{message_id}
- "Get answer details?" -> GET /channels/{channel_id}/polls/{message_id}/answers/{answer_id}
- "Create a expire?" -> POST /channels/{channel_id}/polls/{message_id}/expire
- "Update a recipient?" -> PUT /channels/{channel_id}/recipients/{user_id}
- "Delete a recipient?" -> DELETE /channels/{channel_id}/recipients/{user_id}
- "Create a send-soundboard-sound?" -> POST /channels/{channel_id}/send-soundboard-sound
- "List all thread-members?" -> GET /channels/{channel_id}/thread-members
- "Get thread-member details?" -> GET /channels/{channel_id}/thread-members/{user_id}
- "Update a thread-member?" -> PUT /channels/{channel_id}/thread-members/{user_id}
- "Delete a thread-member?" -> DELETE /channels/{channel_id}/thread-members/{user_id}
- "Create a thread?" -> POST /channels/{channel_id}/threads
- "List all private?" -> GET /channels/{channel_id}/threads/archived/private
- "List all public?" -> GET /channels/{channel_id}/threads/archived/public
- "List all search?" -> GET /channels/{channel_id}/threads/search
- "Create a typing?" -> POST /channels/{channel_id}/typing
- "List all private?" -> GET /channels/{channel_id}/users/@me/threads/archived/private
- "List all webhooks?" -> GET /channels/{channel_id}/webhooks
- "Create a webhook?" -> POST /channels/{channel_id}/webhooks
- "List all gateway?" -> GET /gateway
- "List all bot?" -> GET /gateway/bot
- "Get template details?" -> GET /guilds/templates/{code}
- "Get guild details?" -> GET /guilds/{guild_id}
- "Partially update a guild?" -> PATCH /guilds/{guild_id}
- "List all audit-logs?" -> GET /guilds/{guild_id}/audit-logs
- "List all rules?" -> GET /guilds/{guild_id}/auto-moderation/rules
- "Create a rule?" -> POST /guilds/{guild_id}/auto-moderation/rules
- "Get rule details?" -> GET /guilds/{guild_id}/auto-moderation/rules/{rule_id}
- "Delete a rule?" -> DELETE /guilds/{guild_id}/auto-moderation/rules/{rule_id}
- "Partially update a rule?" -> PATCH /guilds/{guild_id}/auto-moderation/rules/{rule_id}
- "List all bans?" -> GET /guilds/{guild_id}/bans
- "Get ban details?" -> GET /guilds/{guild_id}/bans/{user_id}
- "Update a ban?" -> PUT /guilds/{guild_id}/bans/{user_id}
- "Delete a ban?" -> DELETE /guilds/{guild_id}/bans/{user_id}
- "Create a bulk-ban?" -> POST /guilds/{guild_id}/bulk-ban
- "List all channels?" -> GET /guilds/{guild_id}/channels
- "Create a channel?" -> POST /guilds/{guild_id}/channels
- "List all emojis?" -> GET /guilds/{guild_id}/emojis
- "Create a emojis?" -> POST /guilds/{guild_id}/emojis
- "Get emojis details?" -> GET /guilds/{guild_id}/emojis/{emoji_id}
- "Delete a emojis?" -> DELETE /guilds/{guild_id}/emojis/{emoji_id}
- "Partially update a emojis?" -> PATCH /guilds/{guild_id}/emojis/{emoji_id}
- "List all integrations?" -> GET /guilds/{guild_id}/integrations
- "Delete a integration?" -> DELETE /guilds/{guild_id}/integrations/{integration_id}
- "List all invites?" -> GET /guilds/{guild_id}/invites
- "List all members?" -> GET /guilds/{guild_id}/members
- "Search search?" -> GET /guilds/{guild_id}/members/search
- "Get member details?" -> GET /guilds/{guild_id}/members/{user_id}
- "Update a member?" -> PUT /guilds/{guild_id}/members/{user_id}
- "Delete a member?" -> DELETE /guilds/{guild_id}/members/{user_id}
- "Partially update a member?" -> PATCH /guilds/{guild_id}/members/{user_id}
- "Update a role?" -> PUT /guilds/{guild_id}/members/{user_id}/roles/{role_id}
- "Delete a role?" -> DELETE /guilds/{guild_id}/members/{user_id}/roles/{role_id}
- "List all new-member-welcome?" -> GET /guilds/{guild_id}/new-member-welcome
- "List all onboarding?" -> GET /guilds/{guild_id}/onboarding
- "List all preview?" -> GET /guilds/{guild_id}/preview
- "List all prune?" -> GET /guilds/{guild_id}/prune
- "Create a prune?" -> POST /guilds/{guild_id}/prune
- "List all regions?" -> GET /guilds/{guild_id}/regions
- "List all roles?" -> GET /guilds/{guild_id}/roles
- "Create a role?" -> POST /guilds/{guild_id}/roles
- "List all member-counts?" -> GET /guilds/{guild_id}/roles/member-counts
- "Get role details?" -> GET /guilds/{guild_id}/roles/{role_id}
- "Delete a role?" -> DELETE /guilds/{guild_id}/roles/{role_id}
- "Partially update a role?" -> PATCH /guilds/{guild_id}/roles/{role_id}
- "List all scheduled-events?" -> GET /guilds/{guild_id}/scheduled-events
- "Create a scheduled-event?" -> POST /guilds/{guild_id}/scheduled-events
- "Get scheduled-event details?" -> GET /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}
- "Delete a scheduled-event?" -> DELETE /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}
- "Partially update a scheduled-event?" -> PATCH /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}
- "List all users?" -> GET /guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}/users
- "List all soundboard-sounds?" -> GET /guilds/{guild_id}/soundboard-sounds
- "Create a soundboard-sound?" -> POST /guilds/{guild_id}/soundboard-sounds
- "Get soundboard-sound details?" -> GET /guilds/{guild_id}/soundboard-sounds/{sound_id}
- "Delete a soundboard-sound?" -> DELETE /guilds/{guild_id}/soundboard-sounds/{sound_id}
- "Partially update a soundboard-sound?" -> PATCH /guilds/{guild_id}/soundboard-sounds/{sound_id}
- "List all stickers?" -> GET /guilds/{guild_id}/stickers
- "Create a sticker?" -> POST /guilds/{guild_id}/stickers
- "Get sticker details?" -> GET /guilds/{guild_id}/stickers/{sticker_id}
- "Delete a sticker?" -> DELETE /guilds/{guild_id}/stickers/{sticker_id}
- "Partially update a sticker?" -> PATCH /guilds/{guild_id}/stickers/{sticker_id}
- "List all templates?" -> GET /guilds/{guild_id}/templates
- "Create a template?" -> POST /guilds/{guild_id}/templates
- "Update a template?" -> PUT /guilds/{guild_id}/templates/{code}
- "Delete a template?" -> DELETE /guilds/{guild_id}/templates/{code}
- "Partially update a template?" -> PATCH /guilds/{guild_id}/templates/{code}
- "List all active?" -> GET /guilds/{guild_id}/threads/active
- "List all vanity-url?" -> GET /guilds/{guild_id}/vanity-url
- "List all @me?" -> GET /guilds/{guild_id}/voice-states/@me
- "Get voice-state details?" -> GET /guilds/{guild_id}/voice-states/{user_id}
- "Partially update a voice-state?" -> PATCH /guilds/{guild_id}/voice-states/{user_id}
- "List all webhooks?" -> GET /guilds/{guild_id}/webhooks
- "List all welcome-screen?" -> GET /guilds/{guild_id}/welcome-screen
- "List all widget?" -> GET /guilds/{guild_id}/widget
- "List all widget.json?" -> GET /guilds/{guild_id}/widget.json
- "List all widget.png?" -> GET /guilds/{guild_id}/widget.png
- "Create a callback?" -> POST /interactions/{interaction_id}/{interaction_token}/callback
- "Get invite details?" -> GET /invites/{code}
- "Delete a invite?" -> DELETE /invites/{code}
- "List all target-users?" -> GET /invites/{code}/target-users
- "List all job-status?" -> GET /invites/{code}/target-users/job-status
- "Create a lobby?" -> POST /lobbies
- "Get lobby details?" -> GET /lobbies/{lobby_id}
- "Partially update a lobby?" -> PATCH /lobbies/{lobby_id}
- "Create a invite?" -> POST /lobbies/{lobby_id}/members/@me/invites
- "Create a bulk?" -> POST /lobbies/{lobby_id}/members/bulk
- "Update a member?" -> PUT /lobbies/{lobby_id}/members/{user_id}
- "Delete a member?" -> DELETE /lobbies/{lobby_id}/members/{user_id}
- "Create a invite?" -> POST /lobbies/{lobby_id}/members/{user_id}/invites
- "List all messages?" -> GET /lobbies/{lobby_id}/messages
- "Create a message?" -> POST /lobbies/{lobby_id}/messages
- "List all @me?" -> GET /oauth2/@me
- "List all @me?" -> GET /oauth2/applications/@me
- "List all keys?" -> GET /oauth2/keys
- "List all userinfo?" -> GET /oauth2/userinfo
- "Create a unmerge?" -> POST /partner-sdk/provisional-accounts/unmerge
- "Create a bot?" -> POST /partner-sdk/provisional-accounts/unmerge/bot
- "Create a token?" -> POST /partner-sdk/token
- "Create a bot?" -> POST /partner-sdk/token/bot
- "List all soundboard-default-sounds?" -> GET /soundboard-default-sounds
- "Create a stage-instance?" -> POST /stage-instances
- "Get stage-instance details?" -> GET /stage-instances/{channel_id}
- "Delete a stage-instance?" -> DELETE /stage-instances/{channel_id}
- "Partially update a stage-instance?" -> PATCH /stage-instances/{channel_id}
- "List all sticker-packs?" -> GET /sticker-packs
- "Get sticker-pack details?" -> GET /sticker-packs/{pack_id}
- "Get sticker details?" -> GET /stickers/{sticker_id}
- "List all @me?" -> GET /users/@me
- "List all entitlements?" -> GET /users/@me/applications/{application_id}/entitlements
- "List all role-connection?" -> GET /users/@me/applications/{application_id}/role-connection
- "Create a channel?" -> POST /users/@me/channels
- "List all connections?" -> GET /users/@me/connections
- "List all guilds?" -> GET /users/@me/guilds
- "Delete a guild?" -> DELETE /users/@me/guilds/{guild_id}
- "List all member?" -> GET /users/@me/guilds/{guild_id}/member
- "Get user details?" -> GET /users/{user_id}
- "List all regions?" -> GET /voice/regions
- "Get webhook details?" -> GET /webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /webhooks/{webhook_id}
- "Partially update a webhook?" -> PATCH /webhooks/{webhook_id}
- "Get webhook details?" -> GET /webhooks/{webhook_id}/{webhook_token}
- "Delete a webhook?" -> DELETE /webhooks/{webhook_id}/{webhook_token}
- "Partially update a webhook?" -> PATCH /webhooks/{webhook_id}/{webhook_token}
- "Create a github?" -> POST /webhooks/{webhook_id}/{webhook_token}/github
- "List all @original?" -> GET /webhooks/{webhook_id}/{webhook_token}/messages/@original
- "Get message details?" -> GET /webhooks/{webhook_id}/{webhook_token}/messages/{message_id}
- "Delete a message?" -> DELETE /webhooks/{webhook_id}/{webhook_token}/messages/{message_id}
- "Partially update a message?" -> PATCH /webhooks/{webhook_id}/{webhook_token}/messages/{message_id}
- "Create a slack?" -> POST /webhooks/{webhook_id}/{webhook_token}/slack
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
