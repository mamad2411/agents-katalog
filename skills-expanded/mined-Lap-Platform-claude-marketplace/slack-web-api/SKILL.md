---
name: slack-web-api
description: "Slack Web API skill. Use when working with Slack Web for admin.apps.approve, admin.apps.approved.list, admin.apps.requests.list. Covers 174 endpoints."
version: 1.0.0
generator: lapsh
---

# Slack Web API
API version: 1.7.0

## Auth
OAuth2

## Base URL
https://slack.com/api

## Setup
1. Configure auth: OAuth2
2. GET /admin.apps.approved.list -- verify access
3. POST /admin.apps.approve -- create first admin.apps.approve

## Endpoints

174 endpoints across 174 groups. See references/api-spec.lap for full details.

### admin.apps.approve
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.apps.approve | Approve an app for installation on a workspace. |

### admin.apps.approved.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.apps.approved.list | List approved apps for an org or workspace. |

### admin.apps.requests.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.apps.requests.list | List app requests for a team/workspace. |

### admin.apps.restrict
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.apps.restrict | Restrict an app for installation on a workspace. |

### admin.apps.restricted.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.apps.restricted.list | List restricted apps for an org or workspace. |

### admin.conversations.archive
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.archive | Archive a public or private channel. |

### admin.conversations.convertToPrivate
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.convertToPrivate | Convert a public channel to a private channel. |

### admin.conversations.create
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.create | Create a public or private channel-based conversation. |

### admin.conversations.delete
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.delete | Delete a public or private channel. |

### admin.conversations.disconnectShared
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.disconnectShared | Disconnect a connected channel from one or more workspaces. |

### admin.conversations.ekm.listOriginalConnectedChannelInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.conversations.ekm.listOriginalConnectedChannelInfo | List all disconnected channels—i.e., channels that were once connected to other workspaces and then disconnected—and the corresponding original channel IDs for key revocation with EKM. |

### admin.conversations.getConversationPrefs
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.conversations.getConversationPrefs | Get conversation preferences for a public or private channel. |

### admin.conversations.getTeams
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.conversations.getTeams | Get all the workspaces a given public or private channel is connected to within this Enterprise org. |

### admin.conversations.invite
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.invite | Invite a user to a public or private channel. |

### admin.conversations.rename
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.rename | Rename a public or private channel. |

### admin.conversations.restrictAccess.addGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.restrictAccess.addGroup | Add an allowlist of IDP groups for accessing a channel |

### admin.conversations.restrictAccess.listGroups
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.conversations.restrictAccess.listGroups | List all IDP Groups linked to a channel |

### admin.conversations.restrictAccess.removeGroup
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.restrictAccess.removeGroup | Remove a linked IDP group linked from a private channel |

### admin.conversations.search
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.conversations.search | Search for public or private channels in an Enterprise organization. |

### admin.conversations.setConversationPrefs
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.setConversationPrefs | Set the posting permissions for a public or private channel. |

### admin.conversations.setTeams
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.setTeams | Set the workspaces in an Enterprise grid org that connect to a public or private channel. |

### admin.conversations.unarchive
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.conversations.unarchive | Unarchive a public or private channel. |

### admin.emoji.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.emoji.add | Add an emoji. |

### admin.emoji.addAlias
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.emoji.addAlias | Add an emoji alias. |

### admin.emoji.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.emoji.list | List emoji for an Enterprise Grid organization. |

### admin.emoji.remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.emoji.remove | Remove an emoji across an Enterprise Grid organization |

### admin.emoji.rename
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.emoji.rename | Rename an emoji. |

### admin.inviteRequests.approve
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.inviteRequests.approve | Approve a workspace invite request. |

### admin.inviteRequests.approved.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.inviteRequests.approved.list | List all approved workspace invite requests. |

### admin.inviteRequests.denied.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.inviteRequests.denied.list | List all denied workspace invite requests. |

### admin.inviteRequests.deny
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.inviteRequests.deny | Deny a workspace invite request. |

### admin.inviteRequests.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.inviteRequests.list | List all pending workspace invite requests. |

### admin.teams.admins.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.teams.admins.list | List all of the admins on a given workspace. |

### admin.teams.create
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.teams.create | Create an Enterprise team. |

### admin.teams.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.teams.list | List all teams on an Enterprise organization |

### admin.teams.owners.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.teams.owners.list | List all of the owners on a given workspace. |

### admin.teams.settings.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.teams.settings.info | Fetch information about settings in a workspace |

### admin.teams.settings.setDefaultChannels
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.teams.settings.setDefaultChannels | Set the default channels of a workspace. |

### admin.teams.settings.setDescription
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.teams.settings.setDescription | Set the description of a given workspace. |

### admin.teams.settings.setDiscoverability
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.teams.settings.setDiscoverability | An API method that allows admins to set the discoverability of a given workspace |

### admin.teams.settings.setIcon
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.teams.settings.setIcon | Sets the icon of a workspace. |

### admin.teams.settings.setName
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.teams.settings.setName | Set the name of a given workspace. |

### admin.usergroups.addChannels
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.usergroups.addChannels | Add one or more default channels to an IDP group. |

### admin.usergroups.addTeams
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.usergroups.addTeams | Associate one or more default workspaces with an organization-wide IDP group. |

### admin.usergroups.listChannels
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.usergroups.listChannels | List the channels linked to an org-level IDP group (user group). |

### admin.usergroups.removeChannels
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.usergroups.removeChannels | Remove one or more default channels from an org-level IDP group (user group). |

### admin.users.assign
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.assign | Add an Enterprise user to a workspace. |

### admin.users.invite
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.invite | Invite a user to a workspace. |

### admin.users.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin.users.list | List users on a workspace |

### admin.users.remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.remove | Remove a user from a workspace. |

### admin.users.session.invalidate
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.session.invalidate | Invalidate a single session for a user by session_id |

### admin.users.session.reset
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.session.reset | Wipes all valid sessions on all devices for a given user |

### admin.users.setAdmin
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.setAdmin | Set an existing guest, regular user, or owner to be an admin user. |

### admin.users.setExpiration
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.setExpiration | Set an expiration for a guest user |

### admin.users.setOwner
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.setOwner | Set an existing guest, regular user, or admin user to be a workspace owner. |

### admin.users.setRegular
| Method | Path | Description |
|--------|------|-------------|
| POST | /admin.users.setRegular | Set an existing guest user, admin user, or owner to be a regular user. |

### api.test
| Method | Path | Description |
|--------|------|-------------|
| GET | /api.test | Checks API calling code. |

### apps.event.authorizations.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.event.authorizations.list | Get a list of authorizations for the given event context. Each authorization represents an app installation that the event is visible to. |

### apps.permissions.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.permissions.info | Returns list of permissions this app has on a team. |

### apps.permissions.request
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.permissions.request | Allows an app to request additional scopes |

### apps.permissions.resources.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.permissions.resources.list | Returns list of resource grants this app has on a team. |

### apps.permissions.scopes.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.permissions.scopes.list | Returns list of scopes this app has on a team. |

### apps.permissions.users.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.permissions.users.list | Returns list of user grants and corresponding scopes this app has on a team. |

### apps.permissions.users.request
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.permissions.users.request | Enables an app to trigger a permissions modal to grant an app access to a user access scope. |

### apps.uninstall
| Method | Path | Description |
|--------|------|-------------|
| GET | /apps.uninstall | Uninstalls your app from a workspace. |

### auth.revoke
| Method | Path | Description |
|--------|------|-------------|
| GET | /auth.revoke | Revokes a token. |

### auth.test
| Method | Path | Description |
|--------|------|-------------|
| GET | /auth.test | Checks authentication & identity. |

### bots.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /bots.info | Gets information about a bot user. |

### calls.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /calls.add | Registers a new Call. |

### calls.end
| Method | Path | Description |
|--------|------|-------------|
| POST | /calls.end | Ends a Call. |

### calls.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /calls.info | Returns information about a Call. |

### calls.participants.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /calls.participants.add | Registers new participants added to a Call. |

### calls.participants.remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /calls.participants.remove | Registers participants removed from a Call. |

### calls.update
| Method | Path | Description |
|--------|------|-------------|
| POST | /calls.update | Updates information about a Call. |

### chat.delete
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.delete | Deletes a message. |

### chat.deleteScheduledMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.deleteScheduledMessage | Deletes a pending scheduled message from the queue. |

### chat.getPermalink
| Method | Path | Description |
|--------|------|-------------|
| GET | /chat.getPermalink | Retrieve a permalink URL for a specific extant message |

### chat.meMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.meMessage | Share a me message into a channel. |

### chat.postEphemeral
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.postEphemeral | Sends an ephemeral message to a user in a channel. |

### chat.postMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.postMessage | Sends a message to a channel. |

### chat.scheduleMessage
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.scheduleMessage | Schedules a message to be sent to a channel. |

### chat.scheduledMessages.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /chat.scheduledMessages.list | Returns a list of scheduled messages. |

### chat.unfurl
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.unfurl | Provide custom unfurl behavior for user-posted URLs |

### chat.update
| Method | Path | Description |
|--------|------|-------------|
| POST | /chat.update | Updates a message. |

### conversations.archive
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.archive | Archives a conversation. |

### conversations.close
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.close | Closes a direct message or multi-person direct message. |

### conversations.create
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.create | Initiates a public or private channel-based conversation |

### conversations.history
| Method | Path | Description |
|--------|------|-------------|
| GET | /conversations.history | Fetches a conversation's history of messages and events. |

### conversations.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /conversations.info | Retrieve information about a conversation. |

### conversations.invite
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.invite | Invites users to a channel. |

### conversations.join
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.join | Joins an existing conversation. |

### conversations.kick
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.kick | Removes a user from a conversation. |

### conversations.leave
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.leave | Leaves a conversation. |

### conversations.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /conversations.list | Lists all channels in a Slack team. |

### conversations.mark
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.mark | Sets the read cursor in a channel. |

### conversations.members
| Method | Path | Description |
|--------|------|-------------|
| GET | /conversations.members | Retrieve members of a conversation. |

### conversations.open
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.open | Opens or resumes a direct message or multi-person direct message. |

### conversations.rename
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.rename | Renames a conversation. |

### conversations.replies
| Method | Path | Description |
|--------|------|-------------|
| GET | /conversations.replies | Retrieve a thread of messages posted to a conversation |

### conversations.setPurpose
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.setPurpose | Sets the purpose for a conversation. |

### conversations.setTopic
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.setTopic | Sets the topic for a conversation. |

### conversations.unarchive
| Method | Path | Description |
|--------|------|-------------|
| POST | /conversations.unarchive | Reverses conversation archival. |

### dialog.open
| Method | Path | Description |
|--------|------|-------------|
| GET | /dialog.open | Open a dialog with a user |

### dnd.endDnd
| Method | Path | Description |
|--------|------|-------------|
| POST | /dnd.endDnd | Ends the current user's Do Not Disturb session immediately. |

### dnd.endSnooze
| Method | Path | Description |
|--------|------|-------------|
| POST | /dnd.endSnooze | Ends the current user's snooze mode immediately. |

### dnd.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /dnd.info | Retrieves a user's current Do Not Disturb status. |

### dnd.setSnooze
| Method | Path | Description |
|--------|------|-------------|
| POST | /dnd.setSnooze | Turns on Do Not Disturb mode for the current user, or changes its duration. |

### dnd.teamInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /dnd.teamInfo | Retrieves the Do Not Disturb status for up to 50 users on a team. |

### emoji.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /emoji.list | Lists custom emoji for a team. |

### files.comments.delete
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.comments.delete | Deletes an existing comment on a file. |

### files.delete
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.delete | Deletes a file. |

### files.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /files.info | Gets information about a file. |

### files.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /files.list | List for a team, in a channel, or from a user with applied filters. |

### files.remote.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.remote.add | Adds a file from a remote service |

### files.remote.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /files.remote.info | Retrieve information about a remote file added to Slack |

### files.remote.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /files.remote.list | Retrieve information about a remote file added to Slack |

### files.remote.remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.remote.remove | Remove a remote file. |

### files.remote.share
| Method | Path | Description |
|--------|------|-------------|
| GET | /files.remote.share | Share a remote file into a channel. |

### files.remote.update
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.remote.update | Updates an existing remote file. |

### files.revokePublicURL
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.revokePublicURL | Revokes public/external sharing access for a file |

### files.sharedPublicURL
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.sharedPublicURL | Enables a file for public/external sharing. |

### files.upload
| Method | Path | Description |
|--------|------|-------------|
| POST | /files.upload | Uploads or creates a file. |

### migration.exchange
| Method | Path | Description |
|--------|------|-------------|
| GET | /migration.exchange | For Enterprise Grid workspaces, map local user IDs to global user IDs |

### oauth.access
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth.access | Exchanges a temporary OAuth verifier code for an access token. |

### oauth.token
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth.token | Exchanges a temporary OAuth verifier code for a workspace token. |

### oauth.v2.access
| Method | Path | Description |
|--------|------|-------------|
| GET | /oauth.v2.access | Exchanges a temporary OAuth verifier code for an access token. |

### pins.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /pins.add | Pins an item to a channel. |

### pins.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /pins.list | Lists items pinned to a channel. |

### pins.remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /pins.remove | Un-pins an item from a channel. |

### reactions.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /reactions.add | Adds a reaction to an item. |

### reactions.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /reactions.get | Gets reactions for an item. |

### reactions.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /reactions.list | Lists reactions made by a user. |

### reactions.remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /reactions.remove | Removes a reaction from an item. |

### reminders.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /reminders.add | Creates a reminder. |

### reminders.complete
| Method | Path | Description |
|--------|------|-------------|
| POST | /reminders.complete | Marks a reminder as complete. |

### reminders.delete
| Method | Path | Description |
|--------|------|-------------|
| POST | /reminders.delete | Deletes a reminder. |

### reminders.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /reminders.info | Gets information about a reminder. |

### reminders.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /reminders.list | Lists all reminders created by or for a given user. |

### rtm.connect
| Method | Path | Description |
|--------|------|-------------|
| GET | /rtm.connect | Starts a Real Time Messaging session. |

### search.messages
| Method | Path | Description |
|--------|------|-------------|
| GET | /search.messages | Searches for messages matching a query. |

### stars.add
| Method | Path | Description |
|--------|------|-------------|
| POST | /stars.add | Adds a star to an item. |

### stars.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /stars.list | Lists stars for a user. |

### stars.remove
| Method | Path | Description |
|--------|------|-------------|
| POST | /stars.remove | Removes a star from an item. |

### team.accessLogs
| Method | Path | Description |
|--------|------|-------------|
| GET | /team.accessLogs | Gets the access logs for the current team. |

### team.billableInfo
| Method | Path | Description |
|--------|------|-------------|
| GET | /team.billableInfo | Gets billable users information for the current team. |

### team.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /team.info | Gets information about the current team. |

### team.integrationLogs
| Method | Path | Description |
|--------|------|-------------|
| GET | /team.integrationLogs | Gets the integration logs for the current team. |

### team.profile.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /team.profile.get | Retrieve a team's profile. |

### usergroups.create
| Method | Path | Description |
|--------|------|-------------|
| POST | /usergroups.create | Create a User Group |

### usergroups.disable
| Method | Path | Description |
|--------|------|-------------|
| POST | /usergroups.disable | Disable an existing User Group |

### usergroups.enable
| Method | Path | Description |
|--------|------|-------------|
| POST | /usergroups.enable | Enable a User Group |

### usergroups.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /usergroups.list | List all User Groups for a team |

### usergroups.update
| Method | Path | Description |
|--------|------|-------------|
| POST | /usergroups.update | Update an existing User Group |

### usergroups.users.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /usergroups.users.list | List all users in a User Group |

### usergroups.users.update
| Method | Path | Description |
|--------|------|-------------|
| POST | /usergroups.users.update | Update the list of users for a User Group |

### users.conversations
| Method | Path | Description |
|--------|------|-------------|
| GET | /users.conversations | List conversations the calling user may access. |

### users.deletePhoto
| Method | Path | Description |
|--------|------|-------------|
| POST | /users.deletePhoto | Delete the user profile photo |

### users.getPresence
| Method | Path | Description |
|--------|------|-------------|
| GET | /users.getPresence | Gets user presence information. |

### users.identity
| Method | Path | Description |
|--------|------|-------------|
| GET | /users.identity | Get a user's identity. |

### users.info
| Method | Path | Description |
|--------|------|-------------|
| GET | /users.info | Gets information about a user. |

### users.list
| Method | Path | Description |
|--------|------|-------------|
| GET | /users.list | Lists all users in a Slack team. |

### users.lookupByEmail
| Method | Path | Description |
|--------|------|-------------|
| GET | /users.lookupByEmail | Find a user with an email address. |

### users.profile.get
| Method | Path | Description |
|--------|------|-------------|
| GET | /users.profile.get | Retrieves a user's profile information. |

### users.profile.set
| Method | Path | Description |
|--------|------|-------------|
| POST | /users.profile.set | Set the profile information for a user. |

### users.setActive
| Method | Path | Description |
|--------|------|-------------|
| POST | /users.setActive | Marked a user as active. Deprecated and non-functional. |

### users.setPhoto
| Method | Path | Description |
|--------|------|-------------|
| POST | /users.setPhoto | Set the user profile photo |

### users.setPresence
| Method | Path | Description |
|--------|------|-------------|
| POST | /users.setPresence | Manually sets user presence. |

### views.open
| Method | Path | Description |
|--------|------|-------------|
| GET | /views.open | Open a view for a user. |

### views.publish
| Method | Path | Description |
|--------|------|-------------|
| GET | /views.publish | Publish a static view for a User. |

### views.push
| Method | Path | Description |
|--------|------|-------------|
| GET | /views.push | Push a view onto the stack of a root view. |

### views.update
| Method | Path | Description |
|--------|------|-------------|
| GET | /views.update | Update an existing view. |

### workflows.stepCompleted
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflows.stepCompleted | Indicate that an app's step in a workflow completed execution. |

### workflows.stepFailed
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflows.stepFailed | Indicate that an app's step in a workflow failed to execute. |

### workflows.updateStep
| Method | Path | Description |
|--------|------|-------------|
| GET | /workflows.updateStep | Update the configuration for a workflow extension step. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a admin.apps.approve?" -> POST /admin.apps.approve
- "List all admin.apps.approved.list?" -> GET /admin.apps.approved.list
- "List all admin.apps.requests.list?" -> GET /admin.apps.requests.list
- "Create a admin.apps.restrict?" -> POST /admin.apps.restrict
- "List all admin.apps.restricted.list?" -> GET /admin.apps.restricted.list
- "Create a admin.conversations.archive?" -> POST /admin.conversations.archive
- "Create a admin.conversations.convertToPrivate?" -> POST /admin.conversations.convertToPrivate
- "Create a admin.conversations.create?" -> POST /admin.conversations.create
- "Create a admin.conversations.delete?" -> POST /admin.conversations.delete
- "Create a admin.conversations.disconnectShared?" -> POST /admin.conversations.disconnectShared
- "List all admin.conversations.ekm.listOriginalConnectedChannelInfo?" -> GET /admin.conversations.ekm.listOriginalConnectedChannelInfo
- "List all admin.conversations.getConversationPrefs?" -> GET /admin.conversations.getConversationPrefs
- "List all admin.conversations.getTeams?" -> GET /admin.conversations.getTeams
- "Create a admin.conversations.invite?" -> POST /admin.conversations.invite
- "Create a admin.conversations.rename?" -> POST /admin.conversations.rename
- "Create a admin.conversations.restrictAccess.addGroup?" -> POST /admin.conversations.restrictAccess.addGroup
- "List all admin.conversations.restrictAccess.listGroups?" -> GET /admin.conversations.restrictAccess.listGroups
- "Create a admin.conversations.restrictAccess.removeGroup?" -> POST /admin.conversations.restrictAccess.removeGroup
- "Search admin.conversations.search?" -> GET /admin.conversations.search
- "Create a admin.conversations.setConversationPref?" -> POST /admin.conversations.setConversationPrefs
- "Create a admin.conversations.setTeam?" -> POST /admin.conversations.setTeams
- "Create a admin.conversations.unarchive?" -> POST /admin.conversations.unarchive
- "Create a admin.emoji.add?" -> POST /admin.emoji.add
- "Create a admin.emoji.addAlia?" -> POST /admin.emoji.addAlias
- "List all admin.emoji.list?" -> GET /admin.emoji.list
- "Create a admin.emoji.remove?" -> POST /admin.emoji.remove
- "Create a admin.emoji.rename?" -> POST /admin.emoji.rename
- "Create a admin.inviteRequests.approve?" -> POST /admin.inviteRequests.approve
- "List all admin.inviteRequests.approved.list?" -> GET /admin.inviteRequests.approved.list
- "List all admin.inviteRequests.denied.list?" -> GET /admin.inviteRequests.denied.list
- "Create a admin.inviteRequests.deny?" -> POST /admin.inviteRequests.deny
- "List all admin.inviteRequests.list?" -> GET /admin.inviteRequests.list
- "List all admin.teams.admins.list?" -> GET /admin.teams.admins.list
- "Create a admin.teams.create?" -> POST /admin.teams.create
- "List all admin.teams.list?" -> GET /admin.teams.list
- "List all admin.teams.owners.list?" -> GET /admin.teams.owners.list
- "List all admin.teams.settings.info?" -> GET /admin.teams.settings.info
- "Create a admin.teams.settings.setDefaultChannel?" -> POST /admin.teams.settings.setDefaultChannels
- "Create a admin.teams.settings.setDescription?" -> POST /admin.teams.settings.setDescription
- "Create a admin.teams.settings.setDiscoverability?" -> POST /admin.teams.settings.setDiscoverability
- "Create a admin.teams.settings.setIcon?" -> POST /admin.teams.settings.setIcon
- "Create a admin.teams.settings.setName?" -> POST /admin.teams.settings.setName
- "Create a admin.usergroups.addChannel?" -> POST /admin.usergroups.addChannels
- "Create a admin.usergroups.addTeam?" -> POST /admin.usergroups.addTeams
- "List all admin.usergroups.listChannels?" -> GET /admin.usergroups.listChannels
- "Create a admin.usergroups.removeChannel?" -> POST /admin.usergroups.removeChannels
- "Create a admin.users.assign?" -> POST /admin.users.assign
- "Create a admin.users.invite?" -> POST /admin.users.invite
- "List all admin.users.list?" -> GET /admin.users.list
- "Create a admin.users.remove?" -> POST /admin.users.remove
- "Create a admin.users.session.invalidate?" -> POST /admin.users.session.invalidate
- "Create a admin.users.session.reset?" -> POST /admin.users.session.reset
- "Create a admin.users.setAdmin?" -> POST /admin.users.setAdmin
- "Create a admin.users.setExpiration?" -> POST /admin.users.setExpiration
- "Create a admin.users.setOwner?" -> POST /admin.users.setOwner
- "Create a admin.users.setRegular?" -> POST /admin.users.setRegular
- "List all api.test?" -> GET /api.test
- "List all apps.event.authorizations.list?" -> GET /apps.event.authorizations.list
- "List all apps.permissions.info?" -> GET /apps.permissions.info
- "List all apps.permissions.request?" -> GET /apps.permissions.request
- "List all apps.permissions.resources.list?" -> GET /apps.permissions.resources.list
- "List all apps.permissions.scopes.list?" -> GET /apps.permissions.scopes.list
- "List all apps.permissions.users.list?" -> GET /apps.permissions.users.list
- "List all apps.permissions.users.request?" -> GET /apps.permissions.users.request
- "List all apps.uninstall?" -> GET /apps.uninstall
- "List all auth.revoke?" -> GET /auth.revoke
- "List all auth.test?" -> GET /auth.test
- "List all bots.info?" -> GET /bots.info
- "Create a calls.add?" -> POST /calls.add
- "Create a calls.end?" -> POST /calls.end
- "List all calls.info?" -> GET /calls.info
- "Create a calls.participants.add?" -> POST /calls.participants.add
- "Create a calls.participants.remove?" -> POST /calls.participants.remove
- "Create a calls.update?" -> POST /calls.update
- "Create a chat.delete?" -> POST /chat.delete
- "Create a chat.deleteScheduledMessage?" -> POST /chat.deleteScheduledMessage
- "List all chat.getPermalink?" -> GET /chat.getPermalink
- "Create a chat.meMessage?" -> POST /chat.meMessage
- "Create a chat.postEphemeral?" -> POST /chat.postEphemeral
- "Create a chat.postMessage?" -> POST /chat.postMessage
- "Create a chat.scheduleMessage?" -> POST /chat.scheduleMessage
- "List all chat.scheduledMessages.list?" -> GET /chat.scheduledMessages.list
- "Create a chat.unfurl?" -> POST /chat.unfurl
- "Create a chat.update?" -> POST /chat.update
- "Create a conversations.archive?" -> POST /conversations.archive
- "Create a conversations.close?" -> POST /conversations.close
- "Create a conversations.create?" -> POST /conversations.create
- "List all conversations.history?" -> GET /conversations.history
- "List all conversations.info?" -> GET /conversations.info
- "Create a conversations.invite?" -> POST /conversations.invite
- "Create a conversations.join?" -> POST /conversations.join
- "Create a conversations.kick?" -> POST /conversations.kick
- "Create a conversations.leave?" -> POST /conversations.leave
- "List all conversations.list?" -> GET /conversations.list
- "Create a conversations.mark?" -> POST /conversations.mark
- "List all conversations.members?" -> GET /conversations.members
- "Create a conversations.open?" -> POST /conversations.open
- "Create a conversations.rename?" -> POST /conversations.rename
- "List all conversations.replies?" -> GET /conversations.replies
- "Create a conversations.setPurpose?" -> POST /conversations.setPurpose
- "Create a conversations.setTopic?" -> POST /conversations.setTopic
- "Create a conversations.unarchive?" -> POST /conversations.unarchive
- "List all dialog.open?" -> GET /dialog.open
- "Create a dnd.endDnd?" -> POST /dnd.endDnd
- "Create a dnd.endSnooze?" -> POST /dnd.endSnooze
- "List all dnd.info?" -> GET /dnd.info
- "Create a dnd.setSnooze?" -> POST /dnd.setSnooze
- "List all dnd.teamInfo?" -> GET /dnd.teamInfo
- "List all emoji.list?" -> GET /emoji.list
- "Create a files.comments.delete?" -> POST /files.comments.delete
- "Create a files.delete?" -> POST /files.delete
- "List all files.info?" -> GET /files.info
- "List all files.list?" -> GET /files.list
- "Create a files.remote.add?" -> POST /files.remote.add
- "List all files.remote.info?" -> GET /files.remote.info
- "List all files.remote.list?" -> GET /files.remote.list
- "Create a files.remote.remove?" -> POST /files.remote.remove
- "List all files.remote.share?" -> GET /files.remote.share
- "Create a files.remote.update?" -> POST /files.remote.update
- "Create a files.revokePublicURL?" -> POST /files.revokePublicURL
- "Create a files.sharedPublicURL?" -> POST /files.sharedPublicURL
- "Create a files.upload?" -> POST /files.upload
- "List all migration.exchange?" -> GET /migration.exchange
- "List all oauth.access?" -> GET /oauth.access
- "List all oauth.token?" -> GET /oauth.token
- "List all oauth.v2.access?" -> GET /oauth.v2.access
- "Create a pins.add?" -> POST /pins.add
- "List all pins.list?" -> GET /pins.list
- "Create a pins.remove?" -> POST /pins.remove
- "Create a reactions.add?" -> POST /reactions.add
- "List all reactions.get?" -> GET /reactions.get
- "List all reactions.list?" -> GET /reactions.list
- "Create a reactions.remove?" -> POST /reactions.remove
- "Create a reminders.add?" -> POST /reminders.add
- "Create a reminders.complete?" -> POST /reminders.complete
- "Create a reminders.delete?" -> POST /reminders.delete
- "List all reminders.info?" -> GET /reminders.info
- "List all reminders.list?" -> GET /reminders.list
- "List all rtm.connect?" -> GET /rtm.connect
- "Search search.messages?" -> GET /search.messages
- "Create a stars.add?" -> POST /stars.add
- "List all stars.list?" -> GET /stars.list
- "Create a stars.remove?" -> POST /stars.remove
- "List all team.accessLogs?" -> GET /team.accessLogs
- "List all team.billableInfo?" -> GET /team.billableInfo
- "List all team.info?" -> GET /team.info
- "List all team.integrationLogs?" -> GET /team.integrationLogs
- "List all team.profile.get?" -> GET /team.profile.get
- "Create a usergroups.create?" -> POST /usergroups.create
- "Create a usergroups.disable?" -> POST /usergroups.disable
- "Create a usergroups.enable?" -> POST /usergroups.enable
- "List all usergroups.list?" -> GET /usergroups.list
- "Create a usergroups.update?" -> POST /usergroups.update
- "List all usergroups.users.list?" -> GET /usergroups.users.list
- "Create a usergroups.users.update?" -> POST /usergroups.users.update
- "List all users.conversations?" -> GET /users.conversations
- "Create a users.deletePhoto?" -> POST /users.deletePhoto
- "List all users.getPresence?" -> GET /users.getPresence
- "List all users.identity?" -> GET /users.identity
- "List all users.info?" -> GET /users.info
- "List all users.list?" -> GET /users.list
- "List all users.lookupByEmail?" -> GET /users.lookupByEmail
- "List all users.profile.get?" -> GET /users.profile.get
- "Create a users.profile.set?" -> POST /users.profile.set
- "Create a users.setActive?" -> POST /users.setActive
- "Create a users.setPhoto?" -> POST /users.setPhoto
- "Create a users.setPresence?" -> POST /users.setPresence
- "List all views.open?" -> GET /views.open
- "List all views.publish?" -> GET /views.publish
- "List all views.push?" -> GET /views.push
- "List all views.update?" -> GET /views.update
- "List all workflows.stepCompleted?" -> GET /workflows.stepCompleted
- "List all workflows.stepFailed?" -> GET /workflows.stepFailed
- "List all workflows.updateStep?" -> GET /workflows.updateStep
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
