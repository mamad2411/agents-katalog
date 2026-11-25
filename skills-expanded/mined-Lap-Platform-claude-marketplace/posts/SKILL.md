---
name: posts
description: "Posts API skill. Use when working with Posts for cms. Covers 30 endpoints."
version: 1.0.0
generator: lapsh
---

# Posts
API version: v3

## Auth
OAuth2 | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /cms/v3/blogs/authors/cursor -- verify access
3. POST /cms/v3/blogs/posts -- create first posts

## Endpoints

30 endpoints across 1 groups. See references/api-spec.lap for full details.

### cms
| Method | Path | Description |
|--------|------|-------------|
| GET | /cms/v3/blogs/authors/cursor |  |
| GET | /cms/v3/blogs/authors/cursor/query |  |
| GET | /cms/v3/blogs/posts | Get all posts |
| POST | /cms/v3/blogs/posts | Create a new post |
| POST | /cms/v3/blogs/posts/batch/archive | Delete a batch of blog posts |
| POST | /cms/v3/blogs/posts/batch/create | Create a batch of blog posts |
| POST | /cms/v3/blogs/posts/batch/read | Retrieve a batch of Blog Posts |
| POST | /cms/v3/blogs/posts/batch/update | Update a batch of Blog Posts |
| POST | /cms/v3/blogs/posts/clone | Clone a blog post |
| GET | /cms/v3/blogs/posts/cursor |  |
| GET | /cms/v3/blogs/posts/cursor/query |  |
| POST | /cms/v3/blogs/posts/multi-language/attach-to-lang-group | Attach post to a multi-language group |
| POST | /cms/v3/blogs/posts/multi-language/create-language-variation | Create a language variation |
| POST | /cms/v3/blogs/posts/multi-language/detach-from-lang-group | Detach post from a multi-language group |
| PUT | /cms/v3/blogs/posts/multi-language/set-new-lang-primary | Set a new primary language |
| POST | /cms/v3/blogs/posts/multi-language/update-languages | Update languages of multi-language group |
| POST | /cms/v3/blogs/posts/schedule | Schedule a post to be published |
| GET | /cms/v3/blogs/posts/{objectId} | Retrieve a blog post |
| DELETE | /cms/v3/blogs/posts/{objectId} | Delete a blog post |
| PATCH | /cms/v3/blogs/posts/{objectId} | Update a post |
| GET | /cms/v3/blogs/posts/{objectId}/draft | Retrieve the full draft version of the Blog Post |
| PATCH | /cms/v3/blogs/posts/{objectId}/draft | Update the draft of a post |
| POST | /cms/v3/blogs/posts/{objectId}/draft/push-live | Publish blog post draft |
| POST | /cms/v3/blogs/posts/{objectId}/draft/reset | Reset post draft to the live version |
| GET | /cms/v3/blogs/posts/{objectId}/revisions | Retrieves all previous versions of a post |
| GET | /cms/v3/blogs/posts/{objectId}/revisions/{revisionId} | Retrieve a previous version of a blog post |
| POST | /cms/v3/blogs/posts/{objectId}/revisions/{revisionId}/restore | Restore a previous version |
| POST | /cms/v3/blogs/posts/{objectId}/revisions/{revisionId}/restore-to-draft | Restore a draft to a previous version |
| GET | /cms/v3/blogs/tags/cursor |  |
| GET | /cms/v3/blogs/tags/cursor/query |  |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all cursor?" -> GET /cms/v3/blogs/authors/cursor
- "List all query?" -> GET /cms/v3/blogs/authors/cursor/query
- "List all posts?" -> GET /cms/v3/blogs/posts
- "Create a post?" -> POST /cms/v3/blogs/posts
- "Create a archive?" -> POST /cms/v3/blogs/posts/batch/archive
- "Create a create?" -> POST /cms/v3/blogs/posts/batch/create
- "Create a read?" -> POST /cms/v3/blogs/posts/batch/read
- "Create a update?" -> POST /cms/v3/blogs/posts/batch/update
- "Create a clone?" -> POST /cms/v3/blogs/posts/clone
- "List all cursor?" -> GET /cms/v3/blogs/posts/cursor
- "List all query?" -> GET /cms/v3/blogs/posts/cursor/query
- "Create a attach-to-lang-group?" -> POST /cms/v3/blogs/posts/multi-language/attach-to-lang-group
- "Create a create-language-variation?" -> POST /cms/v3/blogs/posts/multi-language/create-language-variation
- "Create a detach-from-lang-group?" -> POST /cms/v3/blogs/posts/multi-language/detach-from-lang-group
- "Create a update-language?" -> POST /cms/v3/blogs/posts/multi-language/update-languages
- "Create a schedule?" -> POST /cms/v3/blogs/posts/schedule
- "Get post details?" -> GET /cms/v3/blogs/posts/{objectId}
- "Delete a post?" -> DELETE /cms/v3/blogs/posts/{objectId}
- "Partially update a post?" -> PATCH /cms/v3/blogs/posts/{objectId}
- "List all draft?" -> GET /cms/v3/blogs/posts/{objectId}/draft
- "Create a push-live?" -> POST /cms/v3/blogs/posts/{objectId}/draft/push-live
- "Create a reset?" -> POST /cms/v3/blogs/posts/{objectId}/draft/reset
- "List all revisions?" -> GET /cms/v3/blogs/posts/{objectId}/revisions
- "Get revision details?" -> GET /cms/v3/blogs/posts/{objectId}/revisions/{revisionId}
- "Create a restore?" -> POST /cms/v3/blogs/posts/{objectId}/revisions/{revisionId}/restore
- "Create a restore-to-draft?" -> POST /cms/v3/blogs/posts/{objectId}/revisions/{revisionId}/restore-to-draft
- "List all cursor?" -> GET /cms/v3/blogs/tags/cursor
- "List all query?" -> GET /cms/v3/blogs/tags/cursor/query
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
