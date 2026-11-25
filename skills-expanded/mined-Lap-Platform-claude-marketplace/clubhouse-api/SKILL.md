---
name: clubhouse-api
description: "Clubhouse API skill. Use when working with Clubhouse for start_phone_number_auth, call_phone_number_auth, resend_phone_number_auth. Covers 41 endpoints."
version: 1.0.0
generator: lapsh
---

# Clubhouse API
API version: 1

## Auth
No authentication required.

## Base URL
https://www.clubhouseapi.com/api/

## Setup
1. No auth setup needed
2. GET /get_all_topics -- verify access
3. POST /start_phone_number_auth -- create first start_phone_number_auth

## Endpoints

41 endpoints across 41 groups. See references/api-spec.lap for full details.

### start_phone_number_auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /start_phone_number_auth | Starts phone number auth. |

### call_phone_number_auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /call_phone_number_auth | Call phone number auth. |

### resend_phone_number_auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /resend_phone_number_auth | Resend phone number auth. |

### complete_phone_number_auth
| Method | Path | Description |
|--------|------|-------------|
| POST | /complete_phone_number_auth | Call phone number auth. |

### check_waitlist_status
| Method | Path | Description |
|--------|------|-------------|
| POST | /check_waitlist_status | checks waitlist status. |

### me
| Method | Path | Description |
|--------|------|-------------|
| POST | /me | gets user |

### get_release_notes
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_release_notes | gets release notes. |

### get_all_topics
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_all_topics | gets all topics. |

### get_topic
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_topic | looks up topic by ID. |

### get_clubs_for_topic
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_clubs_for_topic | looks up clubs by topic. |

### get_profile
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_profile | looks up user profile by ID. |

### get_users_for_topic
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_users_for_topic | looks up users by topic. |

### get_channels
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_channels | get all channels |

### join_channel
| Method | Path | Description |
|--------|------|-------------|
| POST | /join_channel | join a channel. |

### leave_channel
| Method | Path | Description |
|--------|------|-------------|
| POST | /leave_channel | leave a channel. |

### update_username
| Method | Path | Description |
|--------|------|-------------|
| POST | /update_username | edits username. |

### follow
| Method | Path | Description |
|--------|------|-------------|
| POST | /follow | follows a user |

### refresh_token
| Method | Path | Description |
|--------|------|-------------|
| POST | /refresh_token | gets an access_token from a refresh_token. |

### get_suggested_invites
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_suggested_invites | find users to invite based on phone number. |

### get_suggested_club_invites
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_suggested_club_invites | find users to invite to clubs based on phone number |

### get_club
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_club | gets club by id |

### check_for_update
| Method | Path | Description |
|--------|------|-------------|
| GET | /check_for_update | Clubhouse uses this to check for updates when app is not installed from App Store (eg TestFlight) |

### invite_to_app
| Method | Path | Description |
|--------|------|-------------|
| POST | /invite_to_app | invite a user to the app, using one of your invites |

### invite_from_waitlist
| Method | Path | Description |
|--------|------|-------------|
| POST | /invite_from_waitlist | wave to another user on the waitlist to give them access |

### get_following
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_following | get a list of the users and clubs that this user is following. Returned users have bios truncated to ~80 characters. |

### get_suggested_follows_friends_only
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_suggested_follows_friends_only | find people to follow by uploading contacts during signup |

### get_suggested_follows_all
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_suggested_follows_all | gets suggested follows during signup |

### update_notifications
| Method | Path | Description |
|--------|------|-------------|
| POST | /update_notifications | updates notification during signup. |

### get_online_friends
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_online_friends | gets online friends on the app homepage. |

### get_events
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_events | the Upcoming for You page |

### get_settings
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_settings | get notification settings |

### get_welcome_channel
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_welcome_channel | called during signup |

### record_action_trails
| Method | Path | Description |
|--------|------|-------------|
| POST | /record_action_trails | analytics |

### get_notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_notifications | get notifications (the bell icon) |

### get_actionable_notifications
| Method | Path | Description |
|--------|------|-------------|
| GET | /get_actionable_notifications | get actionable notifications (the bell again) |

### get_create_channel_targets
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_create_channel_targets | is fetched when you tap Create Room |

### create_channel
| Method | Path | Description |
|--------|------|-------------|
| POST | /create_channel | creates a channel |

### get_suggested_speakers
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_suggested_speakers | gets suggested users when you start a private room |

### search_users
| Method | Path | Description |
|--------|------|-------------|
| POST | /search_users | search for users |

### get_suggested_follows_similar
| Method | Path | Description |
|--------|------|-------------|
| POST | /get_suggested_follows_similar | find similar users. (The Sparkles button on Clubhouse's profile page) |

### search_clubs
| Method | Path | Description |
|--------|------|-------------|
| POST | /search_clubs | search clubs. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a start_phone_number_auth?" -> POST /start_phone_number_auth
- "Create a call_phone_number_auth?" -> POST /call_phone_number_auth
- "Create a resend_phone_number_auth?" -> POST /resend_phone_number_auth
- "Create a complete_phone_number_auth?" -> POST /complete_phone_number_auth
- "Create a check_waitlist_status?" -> POST /check_waitlist_status
- "Create a me?" -> POST /me
- "Create a get_release_note?" -> POST /get_release_notes
- "List all get_all_topics?" -> GET /get_all_topics
- "Create a get_topic?" -> POST /get_topic
- "Create a get_clubs_for_topic?" -> POST /get_clubs_for_topic
- "Create a get_profile?" -> POST /get_profile
- "List all get_users_for_topic?" -> GET /get_users_for_topic
- "List all get_channels?" -> GET /get_channels
- "Create a join_channel?" -> POST /join_channel
- "Create a leave_channel?" -> POST /leave_channel
- "Create a update_username?" -> POST /update_username
- "Create a follow?" -> POST /follow
- "Create a refresh_token?" -> POST /refresh_token
- "Create a get_suggested_invite?" -> POST /get_suggested_invites
- "Create a get_suggested_club_invite?" -> POST /get_suggested_club_invites
- "Create a get_club?" -> POST /get_club
- "List all check_for_update?" -> GET /check_for_update
- "Create a invite_to_app?" -> POST /invite_to_app
- "Create a invite_from_waitlist?" -> POST /invite_from_waitlist
- "Create a get_following?" -> POST /get_following
- "Create a get_suggested_follows_friends_only?" -> POST /get_suggested_follows_friends_only
- "List all get_suggested_follows_all?" -> GET /get_suggested_follows_all
- "Create a update_notification?" -> POST /update_notifications
- "Create a get_online_friend?" -> POST /get_online_friends
- "List all get_events?" -> GET /get_events
- "List all get_settings?" -> GET /get_settings
- "List all get_welcome_channel?" -> GET /get_welcome_channel
- "Create a record_action_trail?" -> POST /record_action_trails
- "List all get_notifications?" -> GET /get_notifications
- "List all get_actionable_notifications?" -> GET /get_actionable_notifications
- "Create a get_create_channel_target?" -> POST /get_create_channel_targets
- "Create a create_channel?" -> POST /create_channel
- "Create a get_suggested_speaker?" -> POST /get_suggested_speakers
- "Create a search_user?" -> POST /search_users
- "Create a get_suggested_follows_similar?" -> POST /get_suggested_follows_similar
- "Create a search_club?" -> POST /search_clubs

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
