---
name: trash-nothing
description: "Trash Nothing API skill. Use when working with Trash Nothing for users, groups, posts. Covers 12 endpoints."
version: 1.0.0
generator: lapsh
---

# Trash Nothing
API version: 1.4

## Auth
ApiKey api_key in query

## Base URL
https://trashnothing.com/api/v1.4

## Setup
1. Set your API key in the appropriate header
2. GET /groups -- verify access

## Endpoints

12 endpoints across 3 groups. See references/api-spec.lap for full details.

### users
| Method | Path | Description |
|--------|------|-------------|
| GET | /users/{user_id}/posts | List posts by a user |
| GET | /users/{user_id}/posts/search | Search posts by a user |

### groups
| Method | Path | Description |
|--------|------|-------------|
| GET | /groups | Search groups |
| GET | /groups/{group_id} | Retrieve a group |
| GET | /groups/multiple | Retrieve multiple groups |

### posts
| Method | Path | Description |
|--------|------|-------------|
| GET | /posts | List posts |
| GET | /posts/search | Search posts |
| GET | /posts/all | List all posts |
| GET | /posts/all/changes | List all post changes |
| GET | /posts/{post_id}/display | Retrieve post display data |
| GET | /posts/{post_id} | Retrieve a post |
| GET | /posts/multiple | Retrieve multiple posts |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all posts?" -> GET /users/{user_id}/posts
- "Search search?" -> GET /users/{user_id}/posts/search
- "List all groups?" -> GET /groups
- "Get group details?" -> GET /groups/{group_id}
- "List all multiple?" -> GET /groups/multiple
- "List all posts?" -> GET /posts
- "Search search?" -> GET /posts/search
- "List all all?" -> GET /posts/all
- "List all changes?" -> GET /posts/all/changes
- "List all display?" -> GET /posts/{post_id}/display
- "Get post details?" -> GET /posts/{post_id}
- "List all multiple?" -> GET /posts/multiple
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
