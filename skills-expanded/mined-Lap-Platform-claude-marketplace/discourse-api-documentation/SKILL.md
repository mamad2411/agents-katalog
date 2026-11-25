---
name: discourse-api-documentation
description: "Discourse API Documentation API skill. Use when working with Discourse API Documentation for discourse-post-event, admin, categories.json. Covers 93 endpoints."
version: 1.0.0
generator: lapsh
---

# Discourse API Documentation
API version: latest

## Auth
ApiKey token in query

## Base URL
https://{defaultHost}

## Setup
1. Set your API key in the appropriate header
2. GET /discourse-post-event/events.json -- verify access
3. POST /admin/backups.json -- create first backups.json

## Endpoints

93 endpoints across 35 groups. See references/api-spec.lap for full details.

### discourse-post-event
| Method | Path | Description |
|--------|------|-------------|
| GET | /discourse-post-event/events.json | List calendar events |
| GET | /discourse-post-event/events.ics | Export calendar events in iCalendar format |

### admin
| Method | Path | Description |
|--------|------|-------------|
| GET | /admin/backups.json | List backups |
| POST | /admin/backups.json | Create backup |
| PUT | /admin/backups/{filename} | Send download backup email |
| GET | /admin/backups/{filename} | Download backup |
| GET | /admin/badges.json | List badges |
| POST | /admin/badges.json | Create badge |
| PUT | /admin/badges/{id}.json | Update badge |
| DELETE | /admin/badges/{id}.json | Delete badge |
| POST | /admin/groups.json | Create a group |
| DELETE | /admin/groups/{id}.json | Delete a group |
| GET | /admin/users/{id}.json | Get a user by id |
| DELETE | /admin/users/{id}.json | Delete a user |
| PUT | /admin/users/{id}/activate.json | Activate a user |
| PUT | /admin/users/{id}/deactivate.json | Deactivate a user |
| PUT | /admin/users/{id}/suspend.json | Suspend a user |
| PUT | /admin/users/{id}/silence.json | Silence a user |
| PUT | /admin/users/{id}/anonymize.json | Anonymize a user |
| POST | /admin/users/{id}/log_out.json | Log a user out |
| GET | /admin/users.json | List users |
| GET | /admin/users/list/{flag}.json | List users by flag |

### categories.json
| Method | Path | Description |
|--------|------|-------------|
| POST | /categories.json | Creates a category |
| GET | /categories.json | Retrieves a list of categories |

### categories
| Method | Path | Description |
|--------|------|-------------|
| PUT | /categories/{id}.json | Updates a category |

### c
| Method | Path | Description |
|--------|------|-------------|
| GET | /c/{slug}/{id}.json | List topics |
| GET | /c/{id}/show.json | Show category |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups/{name}.json | Get a group |
| PUT | /groups/{id}.json | Update a group |
| GET | /groups/by-id/{id}.json | Get a group by id |
| GET | /groups/{name}/members.json | List group members |
| PUT | /groups/{id}/members.json | Add group members |
| DELETE | /groups/{id}/members.json | Remove group members |

### groups.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups.json | List groups |

### invites.json
| Method | Path | Description |
|--------|------|-------------|
| POST | /invites.json | Create an invite |

### invites
| Method | Path | Description |
|--------|------|-------------|
| POST | /invites/create-multiple.json | Create multiple invites |

### notifications.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /notifications.json | Get the notifications that belong to the current user |

### notifications
| Method | Path | Description |
|--------|------|-------------|
| PUT | /notifications/mark-read.json | Mark notifications as read |

### posts.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /posts.json | List latest posts across topics |
| POST | /posts.json | Creates a new topic, a new post, or a private message |

### posts
| Method | Path | Description |
|--------|------|-------------|
| GET | /posts/{id}.json | Retrieve a single post |
| PUT | /posts/{id}.json | Update a single post |
| DELETE | /posts/{id}.json | delete a single post |
| GET | /posts/{id}/replies.json | List replies to a post |
| PUT | /posts/{id}/locked.json | Lock a post from being edited |

### post_actions.json
| Method | Path | Description |
|--------|------|-------------|
| POST | /post_actions.json | Like a post and other actions |

### topics
| Method | Path | Description |
|--------|------|-------------|
| GET | /topics/private-messages/{username}.json | Get a list of private messages for a user |
| GET | /topics/private-messages-sent/{username}.json | Get a list of private messages sent for a user |

### search.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /search.json | Search for a term |

### site.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /site.json | Get site info |

### site
| Method | Path | Description |
|--------|------|-------------|
| GET | /site/basic-info.json | Get site basic info |

### tag_groups.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /tag_groups.json | Get a list of tag groups |
| POST | /tag_groups.json | Creates a tag group |

### tag_groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /tag_groups/{id}.json | Get a single tag group |
| PUT | /tag_groups/{id}.json | Update tag group |

### tags.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags.json | Get a list of tags |

### tag
| Method | Path | Description |
|--------|------|-------------|
| GET | /tag/{name}.json | Get a specific tag |

### t
| Method | Path | Description |
|--------|------|-------------|
| GET | /t/{id}/posts.json | Get specific posts from a topic |
| GET | /t/{id}.json | Get a single topic |
| DELETE | /t/{id}.json | Remove a topic |
| PUT | /t/-/{id}.json | Update a topic |
| POST | /t/{id}/invite.json | Invite to topic |
| POST | /t/{id}/invite-group.json | Invite group to topic |
| PUT | /t/{id}/bookmark.json | Bookmark topic |
| PUT | /t/{id}/status.json | Update the status of a topic |
| POST | /t/{id}/notifications.json | Set notification level |
| PUT | /t/{id}/change-timestamp.json | Update topic timestamp |
| POST | /t/{id}/timer.json | Create topic timer |
| GET | /t/external_id/{external_id}.json | Get topic by external_id |

### latest.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /latest.json | Get the latest topics |

### top.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /top.json | Get the top topics filtered by period |

### uploads.json
| Method | Path | Description |
|--------|------|-------------|
| POST | /uploads.json | Creates an upload |

### uploads
| Method | Path | Description |
|--------|------|-------------|
| POST | /uploads/generate-presigned-put.json | Initiates a direct external upload |
| POST | /uploads/complete-external-upload.json | Completes a direct external upload |
| POST | /uploads/create-multipart.json | Creates a multipart external upload |
| POST | /uploads/batch-presign-multipart-parts.json | Generates batches of presigned URLs for multipart parts |
| POST | /uploads/abort-multipart.json | Abort multipart upload |
| POST | /uploads/complete-multipart.json | Complete multipart upload |

### user-badges
| Method | Path | Description |
|--------|------|-------------|
| GET | /user-badges/{username}.json | List badges for a user |

### users.json
| Method | Path | Description |
|--------|------|-------------|
| POST | /users.json | Creates a user |

### u
| Method | Path | Description |
|--------|------|-------------|
| GET | /u/{username}.json | Get a single user by username |
| PUT | /u/{username}.json | Update a user |
| GET | /u/by-external/{external_id}.json | Get a user by external_id |
| GET | /u/by-external/{provider}/{external_id}.json | Get a user by identity provider external ID |
| PUT | /u/{username}/preferences/avatar/pick.json | Update avatar |
| PUT | /u/{username}/preferences/email.json | Update email |
| PUT | /u/{username}/preferences/username.json | Update username |
| GET | /u/{username}/emails.json | Get email addresses belonging to a user |

### directory_items.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /directory_items.json | Get a public list of users |

### user_avatar
| Method | Path | Description |
|--------|------|-------------|
| POST | /user_avatar/{username}/refresh_gravatar.json | Refresh gravatar |

### user_actions.json
| Method | Path | Description |
|--------|------|-------------|
| GET | /user_actions.json | Get a list of user actions |

### session
| Method | Path | Description |
|--------|------|-------------|
| POST | /session/forgot_password.json | Send password reset email |

### users
| Method | Path | Description |
|--------|------|-------------|
| PUT | /users/password-reset/{token}.json | Change password |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all events.json?" -> GET /discourse-post-event/events.json
- "List all events.ics?" -> GET /discourse-post-event/events.ics
- "List all backups.json?" -> GET /admin/backups.json
- "Create a backups.json?" -> POST /admin/backups.json
- "Update a backup?" -> PUT /admin/backups/{filename}
- "Get backup details?" -> GET /admin/backups/{filename}
- "List all badges.json?" -> GET /admin/badges.json
- "Create a badges.json?" -> POST /admin/badges.json
- "Update a badge?" -> PUT /admin/badges/{id}.json
- "Delete a badge?" -> DELETE /admin/badges/{id}.json
- "Create a categories.json?" -> POST /categories.json
- "List all categories.json?" -> GET /categories.json
- "Update a category?" -> PUT /categories/{id}.json
- "Get c details?" -> GET /c/{slug}/{id}.json
- "List all show.json?" -> GET /c/{id}/show.json
- "Create a groups.json?" -> POST /admin/groups.json
- "Delete a group?" -> DELETE /admin/groups/{id}.json
- "Get group details?" -> GET /groups/{name}.json
- "Update a group?" -> PUT /groups/{id}.json
- "Get by-id details?" -> GET /groups/by-id/{id}.json
- "List all members.json?" -> GET /groups/{name}/members.json
- "List all groups.json?" -> GET /groups.json
- "Create a invites.json?" -> POST /invites.json
- "Create a create-multiple.json?" -> POST /invites/create-multiple.json
- "List all notifications.json?" -> GET /notifications.json
- "List all posts.json?" -> GET /posts.json
- "Create a posts.json?" -> POST /posts.json
- "Get post details?" -> GET /posts/{id}.json
- "Update a post?" -> PUT /posts/{id}.json
- "Delete a post?" -> DELETE /posts/{id}.json
- "List all replies.json?" -> GET /posts/{id}/replies.json
- "Create a post_actions.json?" -> POST /post_actions.json
- "Get private-message details?" -> GET /topics/private-messages/{username}.json
- "Get private-messages-sent details?" -> GET /topics/private-messages-sent/{username}.json
- "Search search.json?" -> GET /search.json
- "List all site.json?" -> GET /site.json
- "List all basic-info.json?" -> GET /site/basic-info.json
- "List all tag_groups.json?" -> GET /tag_groups.json
- "Create a tag_groups.json?" -> POST /tag_groups.json
- "Get tag_group details?" -> GET /tag_groups/{id}.json
- "Update a tag_group?" -> PUT /tag_groups/{id}.json
- "List all tags.json?" -> GET /tags.json
- "Get tag details?" -> GET /tag/{name}.json
- "List all posts.json?" -> GET /t/{id}/posts.json
- "Get t details?" -> GET /t/{id}.json
- "Delete a t?" -> DELETE /t/{id}.json
- "Update a -?" -> PUT /t/-/{id}.json
- "Create a invite.json?" -> POST /t/{id}/invite.json
- "Create a invite-group.json?" -> POST /t/{id}/invite-group.json
- "List all latest.json?" -> GET /latest.json
- "List all top.json?" -> GET /top.json
- "Create a notifications.json?" -> POST /t/{id}/notifications.json
- "Create a timer.json?" -> POST /t/{id}/timer.json
- "Get external_id details?" -> GET /t/external_id/{external_id}.json
- "Create a uploads.json?" -> POST /uploads.json
- "Create a generate-presigned-put.json?" -> POST /uploads/generate-presigned-put.json
- "Create a complete-external-upload.json?" -> POST /uploads/complete-external-upload.json
- "Create a create-multipart.json?" -> POST /uploads/create-multipart.json
- "Create a batch-presign-multipart-parts.json?" -> POST /uploads/batch-presign-multipart-parts.json
- "Create a abort-multipart.json?" -> POST /uploads/abort-multipart.json
- "Create a complete-multipart.json?" -> POST /uploads/complete-multipart.json
- "Get user-badge details?" -> GET /user-badges/{username}.json
- "Create a users.json?" -> POST /users.json
- "Get u details?" -> GET /u/{username}.json
- "Update a u?" -> PUT /u/{username}.json
- "Get by-external details?" -> GET /u/by-external/{external_id}.json
- "Get by-external details?" -> GET /u/by-external/{provider}/{external_id}.json
- "List all directory_items.json?" -> GET /directory_items.json
- "Get user details?" -> GET /admin/users/{id}.json
- "Delete a user?" -> DELETE /admin/users/{id}.json
- "Create a log_out.json?" -> POST /admin/users/{id}/log_out.json
- "Create a refresh_gravatar.json?" -> POST /user_avatar/{username}/refresh_gravatar.json
- "List all users.json?" -> GET /admin/users.json
- "Get list details?" -> GET /admin/users/list/{flag}.json
- "List all user_actions.json?" -> GET /user_actions.json
- "Create a forgot_password.json?" -> POST /session/forgot_password.json
- "Update a password-reset?" -> PUT /users/password-reset/{token}.json
- "List all emails.json?" -> GET /u/{username}/emails.json
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
