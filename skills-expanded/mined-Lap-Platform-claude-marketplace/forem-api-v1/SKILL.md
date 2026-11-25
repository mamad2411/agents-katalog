---
name: forem-api-v1
description: "Forem API V1 API skill. Use when working with Forem API V1 for api. Covers 58 endpoints."
version: 1.0.0
generator: lapsh
---

# Forem API V1
API version: 1.0.0

## Auth
ApiKey api-key in header

## Base URL
https://dev.to/api

## Setup
1. Set your API key in the appropriate header
2. GET /api/articles -- verify access
3. POST /api/articles -- create first articles

## Endpoints

58 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| POST | /api/articles | Publish article |
| GET | /api/articles | Published articles |
| GET | /api/articles/latest | Published articles sorted by published date |
| GET | /api/articles/{id} | Published article by id |
| PUT | /api/articles/{id} | Update an article by id |
| GET | /api/articles/{username}/{slug} | Published article by path |
| GET | /api/articles/me | User's articles |
| GET | /api/articles/me/published | User's published articles |
| GET | /api/articles/me/unpublished | User's unpublished articles |
| GET | /api/articles/me/all | User's all articles |
| PUT | /api/articles/{id}/unpublish | Unpublish an article |
| GET | /api/segments | Manually managed audience segments |
| POST | /api/segments | Create a manually managed audience segment |
| GET | /api/segments/{id} | A manually managed audience segment |
| DELETE | /api/segments/{id} | Delete a manually managed audience segment |
| GET | /api/segments/{id}/users | Users in a manually managed audience segment |
| PUT | /api/segments/{id}/add_users | Add users to a manually managed audience segment |
| PUT | /api/segments/{id}/remove_users | Remove users from a manually managed audience segment |
| GET | /api/billboards | Billboards |
| POST | /api/billboards | Create a billboard |
| GET | /api/billboards/{id} | A billboard (by id) |
| PUT | /api/billboards/{id} | Update a billboard by ID |
| PUT | /api/billboards/{id}/unpublish | Unpublish a billboard |
| GET | /api/comments | Comments |
| GET | /api/comments/{id} | Comment by id |
| GET | /api/follows/tags | Followed Tags |
| GET | /api/followers/users | Followers |
| GET | /api/organizations/{username} | An organization (by username) |
| GET | /api/organizations/{organization_id_or_username}/users | Organization's users |
| GET | /api/organizations/{organization_id_or_username}/articles | Organization's Articles |
| GET | /api/organizations | Organizations |
| POST | /api/organizations | Create an Organization |
| GET | /api/organizations/{id} | An organization (by id) |
| PUT | /api/organizations/{id} | Update an organization by id |
| DELETE | /api/organizations/{id} | Delete an Organization by id |
| GET | /api/pages | show details for all pages |
| POST | /api/pages | pages |
| GET | /api/pages/{id} | show details for a page |
| PUT | /api/pages/{id} | update details for a page |
| DELETE | /api/pages/{id} | remove a page |
| GET | /api/podcast_episodes | Podcast Episodes |
| GET | /api/profile_images/{username} | A Users or organizations profile image |
| POST | /api/reactions/toggle | toggle reaction |
| POST | /api/reactions | create reaction |
| GET | /api/readinglist | Readinglist |
| GET | /api/tags | Tags |
| PUT | /api/users/{id}/suspend | Suspend a User |
| PUT | /api/users/{id}/limited | Add limited role for a User |
| DELETE | /api/users/{id}/limited | Remove limited for a User |
| PUT | /api/users/{id}/spam | Add spam role for a User |
| DELETE | /api/users/{id}/spam | Remove spam role from a User |
| PUT | /api/users/{id}/trusted | Add trusted role for a User |
| DELETE | /api/users/{id}/trusted | Remove trusted role from a User |
| GET | /api/users/me | The authenticated user |
| GET | /api/users/{id} | A User |
| PUT | /api/users/{id}/unpublish | Unpublish a User's Articles and Comments |
| POST | /api/admin/users | Invite a User |
| GET | /api/videos | Articles with a video |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Create a article?" -> POST /api/articles
- "List all articles?" -> GET /api/articles
- "List all latest?" -> GET /api/articles/latest
- "Get article details?" -> GET /api/articles/{id}
- "Update a article?" -> PUT /api/articles/{id}
- "Get article details?" -> GET /api/articles/{username}/{slug}
- "List all me?" -> GET /api/articles/me
- "List all published?" -> GET /api/articles/me/published
- "List all unpublished?" -> GET /api/articles/me/unpublished
- "List all all?" -> GET /api/articles/me/all
- "List all segments?" -> GET /api/segments
- "Create a segment?" -> POST /api/segments
- "Get segment details?" -> GET /api/segments/{id}
- "Delete a segment?" -> DELETE /api/segments/{id}
- "List all users?" -> GET /api/segments/{id}/users
- "List all billboards?" -> GET /api/billboards
- "Create a billboard?" -> POST /api/billboards
- "Get billboard details?" -> GET /api/billboards/{id}
- "Update a billboard?" -> PUT /api/billboards/{id}
- "List all comments?" -> GET /api/comments
- "Get comment details?" -> GET /api/comments/{id}
- "List all tags?" -> GET /api/follows/tags
- "List all users?" -> GET /api/followers/users
- "Get organization details?" -> GET /api/organizations/{username}
- "List all users?" -> GET /api/organizations/{organization_id_or_username}/users
- "List all articles?" -> GET /api/organizations/{organization_id_or_username}/articles
- "List all organizations?" -> GET /api/organizations
- "Create a organization?" -> POST /api/organizations
- "Get organization details?" -> GET /api/organizations/{id}
- "Update a organization?" -> PUT /api/organizations/{id}
- "Delete a organization?" -> DELETE /api/organizations/{id}
- "List all pages?" -> GET /api/pages
- "Create a page?" -> POST /api/pages
- "Get page details?" -> GET /api/pages/{id}
- "Update a page?" -> PUT /api/pages/{id}
- "Delete a page?" -> DELETE /api/pages/{id}
- "List all podcast_episodes?" -> GET /api/podcast_episodes
- "Get profile_image details?" -> GET /api/profile_images/{username}
- "Create a toggle?" -> POST /api/reactions/toggle
- "Create a reaction?" -> POST /api/reactions
- "List all readinglist?" -> GET /api/readinglist
- "List all tags?" -> GET /api/tags
- "List all me?" -> GET /api/users/me
- "Get user details?" -> GET /api/users/{id}
- "Create a user?" -> POST /api/admin/users
- "List all videos?" -> GET /api/videos
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
