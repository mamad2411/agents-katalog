---
name: instagram-api
description: "Instagram API skill. Use when working with Instagram for geographies, locations, media. Covers 27 endpoints."
version: 1.0.0
generator: lapsh
---

# Instagram API
API version: 1.0.0

## Auth
ApiKey access_token in query | OAuth2

## Base URL
https://api.instagram.com/v1

## Setup
1. Set your API key in the appropriate header
2. GET /locations/search -- verify access
3. POST /media/{media-id}/comments -- create first comments

## Endpoints

27 endpoints across 5 groups. See references/api-spec.lap for full details.

### geographies
| Method | Path | Description |
|--------|------|-------------|
| GET | /geographies/{geo-id}/media/recent | Get recent media from a custom geo-id. |

### locations
| Method | Path | Description |
|--------|------|-------------|
| GET | /locations/search | Search for a location by geographic coordinate. |
| GET | /locations/{location-id} | Get information about a location. |
| GET | /locations/{location-id}/media/recent | Get a list of recent media objects from a given location. |

### media
| Method | Path | Description |
|--------|------|-------------|
| GET | /media/popular | Get a list of currently popular media. |
| GET | /media/search | Search for media in a given area. |
| GET | /media/shortcode/{shortcode} | Get information about a media object. |
| GET | /media/{media-id} | Get information about a media object. |
| GET | /media/{media-id}/comments | Get a list of recent comments on a media object. |
| POST | /media/{media-id}/comments | Create a comment on a media object. |
| DELETE | /media/{media-id}/comments/{comment-id} | Remove a comment. |
| DELETE | /media/{media-id}/likes | Remove a like on this media by the current user. |
| GET | /media/{media-id}/likes | Get a list of users who have liked this media. |
| POST | /media/{media-id}/likes | Set a like on this media by the current user. |

### tags
| Method | Path | Description |
|--------|------|-------------|
| GET | /tags/search | Search for tags by name. |
| GET | /tags/{tag-name} | Get information about a tag object. |
| GET | /tags/{tag-name}/media/recent | Get a list of recently tagged media. |

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/search | Search for a user by name. |
| GET | /users/self/feed | See the authenticated user's feed. |
| GET | /users/self/media/liked | See the list of media liked by the authenticated user. |
| GET | /users/self/requested-by | List the users who have requested this user's permission to follow. |
| GET | /users/{user-id} | Get basic information about a user. |
| GET | /users/{user-id}/followed-by | Get the list of users this user is followed by. |
| GET | /users/{user-id}/follows | Get the list of users this user follows. |
| GET | /users/{user-id}/media/recent | Get the most recent media published by a user. |
| GET | /users/{user-id}/relationship | Get information about a relationship to another user. |
| POST | /users/{user-id}/relationship | Modify the relationship between the current user and the target user. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all recent?" -> GET /geographies/{geo-id}/media/recent
- "List all search?" -> GET /locations/search
- "Get location details?" -> GET /locations/{location-id}
- "List all recent?" -> GET /locations/{location-id}/media/recent
- "List all popular?" -> GET /media/popular
- "List all search?" -> GET /media/search
- "Get shortcode details?" -> GET /media/shortcode/{shortcode}
- "Get media details?" -> GET /media/{media-id}
- "List all comments?" -> GET /media/{media-id}/comments
- "Create a comment?" -> POST /media/{media-id}/comments
- "Delete a comment?" -> DELETE /media/{media-id}/comments/{comment-id}
- "List all likes?" -> GET /media/{media-id}/likes
- "Create a like?" -> POST /media/{media-id}/likes
- "Search search?" -> GET /tags/search
- "Get tag details?" -> GET /tags/{tag-name}
- "List all recent?" -> GET /tags/{tag-name}/media/recent
- "Search search?" -> GET /users/search
- "List all feed?" -> GET /users/self/feed
- "List all liked?" -> GET /users/self/media/liked
- "List all requested-by?" -> GET /users/self/requested-by
- "Get user details?" -> GET /users/{user-id}
- "List all followed-by?" -> GET /users/{user-id}/followed-by
- "List all follows?" -> GET /users/{user-id}/follows
- "List all recent?" -> GET /users/{user-id}/media/recent
- "List all relationship?" -> GET /users/{user-id}/relationship
- "Create a relationship?" -> POST /users/{user-id}/relationship
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
