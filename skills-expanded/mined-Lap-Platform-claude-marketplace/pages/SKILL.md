---
name: pages
description: "Pages API skill. Use when working with Pages for cms. Covers 72 endpoints."
version: 1.0.0
generator: lapsh
---

# Pages
API version: v3

## Auth
OAuth2 | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /cms/v3/pages/landing-pages -- verify access
3. POST /cms/v3/pages/landing-pages -- create first landing-pages

## Endpoints

72 endpoints across 1 groups. See references/api-spec.lap for full details.

### cms
| Method | Path | Description |
|--------|------|-------------|
| GET | /cms/v3/pages/landing-pages | Get all landing pages |
| POST | /cms/v3/pages/landing-pages | Create a landing page |
| POST | /cms/v3/pages/landing-pages/ab-test/create-variation | Create a new A/B test variation |
| POST | /cms/v3/pages/landing-pages/ab-test/end | End an active A/B test |
| POST | /cms/v3/pages/landing-pages/ab-test/rerun | Rerun a previous A/B test |
| POST | /cms/v3/pages/landing-pages/batch/archive | Delete landing pages |
| POST | /cms/v3/pages/landing-pages/batch/create | Create landing pages |
| POST | /cms/v3/pages/landing-pages/batch/read | Retrieve landing pages |
| POST | /cms/v3/pages/landing-pages/batch/update | Update landing pages |
| POST | /cms/v3/pages/landing-pages/clone | Clone a landing page |
| GET | /cms/v3/pages/landing-pages/cursor |  |
| GET | /cms/v3/pages/landing-pages/cursor/query |  |
| GET | /cms/v3/pages/landing-pages/folders | Get all landing page folders |
| POST | /cms/v3/pages/landing-pages/folders | Create a landing page folder |
| POST | /cms/v3/pages/landing-pages/folders/batch/archive | Delete folders |
| POST | /cms/v3/pages/landing-pages/folders/batch/create | Create folders |
| POST | /cms/v3/pages/landing-pages/folders/batch/read | Retrieve folders |
| POST | /cms/v3/pages/landing-pages/folders/batch/update | Update folders |
| GET | /cms/v3/pages/landing-pages/folders/cursor |  |
| GET | /cms/v3/pages/landing-pages/folders/cursor/query |  |
| GET | /cms/v3/pages/landing-pages/folders/{objectId} | Retrieve a landing page folder |
| DELETE | /cms/v3/pages/landing-pages/folders/{objectId} | Delete a landing page folder |
| PATCH | /cms/v3/pages/landing-pages/folders/{objectId} | Update a landing page folder |
| GET | /cms/v3/pages/landing-pages/folders/{objectId}/revisions | Retrieves previous versions of a folder |
| GET | /cms/v3/pages/landing-pages/folders/{objectId}/revisions/{revisionId} | Retrieve a previous version of a folder |
| POST | /cms/v3/pages/landing-pages/folders/{objectId}/revisions/{revisionId}/restore | Restore a previous version of a folder |
| POST | /cms/v3/pages/landing-pages/multi-language/attach-to-lang-group | Add a landing page to a multi-language group |
| POST | /cms/v3/pages/landing-pages/multi-language/create-language-variation | Create a new language variation |
| POST | /cms/v3/pages/landing-pages/multi-language/detach-from-lang-group | Remove a landing page from a multi-language group |
| PUT | /cms/v3/pages/landing-pages/multi-language/set-new-lang-primary | Set a new primary language |
| POST | /cms/v3/pages/landing-pages/multi-language/update-languages | Update languages of multi-language group |
| POST | /cms/v3/pages/landing-pages/schedule | Schedule landing page publishing |
| GET | /cms/v3/pages/landing-pages/{objectId} | Retrieve a landing page |
| DELETE | /cms/v3/pages/landing-pages/{objectId} | Delete a landing page |
| PATCH | /cms/v3/pages/landing-pages/{objectId} | Update a landing page |
| GET | /cms/v3/pages/landing-pages/{objectId}/draft | Retrieve a landing page draft |
| PATCH | /cms/v3/pages/landing-pages/{objectId}/draft | Update the draft of a landing page |
| POST | /cms/v3/pages/landing-pages/{objectId}/draft/push-live | Push Landing Page draft edits live |
| POST | /cms/v3/pages/landing-pages/{objectId}/draft/reset | Reset a landing page draft |
| GET | /cms/v3/pages/landing-pages/{objectId}/revisions | Retrieve all previous versions of a landing page |
| GET | /cms/v3/pages/landing-pages/{objectId}/revisions/{revisionId} | Retrieve a previous version of a landing page |
| POST | /cms/v3/pages/landing-pages/{objectId}/revisions/{revisionId}/restore | Restore a previous version of a landing page |
| POST | /cms/v3/pages/landing-pages/{objectId}/revisions/{revisionId}/restore-to-draft | Restore a previous version of a landing page |
| GET | /cms/v3/pages/site-pages | Retrieve all website pages |
| POST | /cms/v3/pages/site-pages | Create a website page |
| POST | /cms/v3/pages/site-pages/ab-test/create-variation | Create a new A/B test variation |
| POST | /cms/v3/pages/site-pages/ab-test/end | End an active A/B test |
| POST | /cms/v3/pages/site-pages/ab-test/rerun | Rerun a previous A/B test |
| POST | /cms/v3/pages/site-pages/batch/archive | Delete website pages |
| POST | /cms/v3/pages/site-pages/batch/create | Create website pages |
| POST | /cms/v3/pages/site-pages/batch/read | Retrieve website pages |
| POST | /cms/v3/pages/site-pages/batch/update | Update website pages |
| POST | /cms/v3/pages/site-pages/clone | Clone a website page |
| GET | /cms/v3/pages/site-pages/cursor |  |
| GET | /cms/v3/pages/site-pages/cursor/query |  |
| POST | /cms/v3/pages/site-pages/multi-language/attach-to-lang-group | Add a website page to a multi-language group |
| POST | /cms/v3/pages/site-pages/multi-language/create-language-variation | Create a new language variation |
| POST | /cms/v3/pages/site-pages/multi-language/detach-from-lang-group | Remove a website page from a multi-language group |
| PUT | /cms/v3/pages/site-pages/multi-language/set-new-lang-primary | Set a new primary language |
| POST | /cms/v3/pages/site-pages/multi-language/update-languages | Update languages of multi-language group |
| POST | /cms/v3/pages/site-pages/schedule | Schedule a website page to be published |
| GET | /cms/v3/pages/site-pages/{objectId} | Retrieve a website page |
| DELETE | /cms/v3/pages/site-pages/{objectId} | Delete a website page |
| PATCH | /cms/v3/pages/site-pages/{objectId} | Update a website page |
| GET | /cms/v3/pages/site-pages/{objectId}/draft | Retrieve a website page draft |
| PATCH | /cms/v3/pages/site-pages/{objectId}/draft | Update a website page draft |
| POST | /cms/v3/pages/site-pages/{objectId}/draft/push-live | Publish website page draft |
| POST | /cms/v3/pages/site-pages/{objectId}/draft/reset | Reset the draft of a website page |
| GET | /cms/v3/pages/site-pages/{objectId}/revisions | Retrieve all previous versions of a website page |
| GET | /cms/v3/pages/site-pages/{objectId}/revisions/{revisionId} | Retrieve a previous version of a website page |
| POST | /cms/v3/pages/site-pages/{objectId}/revisions/{revisionId}/restore | Restore a previous version of a website page |
| POST | /cms/v3/pages/site-pages/{objectId}/revisions/{revisionId}/restore-to-draft | Restore a previous draft of a website page |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all landing-pages?" -> GET /cms/v3/pages/landing-pages
- "Create a landing-page?" -> POST /cms/v3/pages/landing-pages
- "Create a create-variation?" -> POST /cms/v3/pages/landing-pages/ab-test/create-variation
- "Create a end?" -> POST /cms/v3/pages/landing-pages/ab-test/end
- "Create a rerun?" -> POST /cms/v3/pages/landing-pages/ab-test/rerun
- "Create a archive?" -> POST /cms/v3/pages/landing-pages/batch/archive
- "Create a create?" -> POST /cms/v3/pages/landing-pages/batch/create
- "Create a read?" -> POST /cms/v3/pages/landing-pages/batch/read
- "Create a update?" -> POST /cms/v3/pages/landing-pages/batch/update
- "Create a clone?" -> POST /cms/v3/pages/landing-pages/clone
- "List all cursor?" -> GET /cms/v3/pages/landing-pages/cursor
- "List all query?" -> GET /cms/v3/pages/landing-pages/cursor/query
- "List all folders?" -> GET /cms/v3/pages/landing-pages/folders
- "Create a folder?" -> POST /cms/v3/pages/landing-pages/folders
- "Create a archive?" -> POST /cms/v3/pages/landing-pages/folders/batch/archive
- "Create a create?" -> POST /cms/v3/pages/landing-pages/folders/batch/create
- "Create a read?" -> POST /cms/v3/pages/landing-pages/folders/batch/read
- "Create a update?" -> POST /cms/v3/pages/landing-pages/folders/batch/update
- "List all cursor?" -> GET /cms/v3/pages/landing-pages/folders/cursor
- "List all query?" -> GET /cms/v3/pages/landing-pages/folders/cursor/query
- "Get folder details?" -> GET /cms/v3/pages/landing-pages/folders/{objectId}
- "Delete a folder?" -> DELETE /cms/v3/pages/landing-pages/folders/{objectId}
- "Partially update a folder?" -> PATCH /cms/v3/pages/landing-pages/folders/{objectId}
- "List all revisions?" -> GET /cms/v3/pages/landing-pages/folders/{objectId}/revisions
- "Get revision details?" -> GET /cms/v3/pages/landing-pages/folders/{objectId}/revisions/{revisionId}
- "Create a restore?" -> POST /cms/v3/pages/landing-pages/folders/{objectId}/revisions/{revisionId}/restore
- "Create a attach-to-lang-group?" -> POST /cms/v3/pages/landing-pages/multi-language/attach-to-lang-group
- "Create a create-language-variation?" -> POST /cms/v3/pages/landing-pages/multi-language/create-language-variation
- "Create a detach-from-lang-group?" -> POST /cms/v3/pages/landing-pages/multi-language/detach-from-lang-group
- "Create a update-language?" -> POST /cms/v3/pages/landing-pages/multi-language/update-languages
- "Create a schedule?" -> POST /cms/v3/pages/landing-pages/schedule
- "Get landing-page details?" -> GET /cms/v3/pages/landing-pages/{objectId}
- "Delete a landing-page?" -> DELETE /cms/v3/pages/landing-pages/{objectId}
- "Partially update a landing-page?" -> PATCH /cms/v3/pages/landing-pages/{objectId}
- "List all draft?" -> GET /cms/v3/pages/landing-pages/{objectId}/draft
- "Create a push-live?" -> POST /cms/v3/pages/landing-pages/{objectId}/draft/push-live
- "Create a reset?" -> POST /cms/v3/pages/landing-pages/{objectId}/draft/reset
- "List all revisions?" -> GET /cms/v3/pages/landing-pages/{objectId}/revisions
- "Get revision details?" -> GET /cms/v3/pages/landing-pages/{objectId}/revisions/{revisionId}
- "Create a restore?" -> POST /cms/v3/pages/landing-pages/{objectId}/revisions/{revisionId}/restore
- "Create a restore-to-draft?" -> POST /cms/v3/pages/landing-pages/{objectId}/revisions/{revisionId}/restore-to-draft
- "List all site-pages?" -> GET /cms/v3/pages/site-pages
- "Create a site-page?" -> POST /cms/v3/pages/site-pages
- "Create a create-variation?" -> POST /cms/v3/pages/site-pages/ab-test/create-variation
- "Create a end?" -> POST /cms/v3/pages/site-pages/ab-test/end
- "Create a rerun?" -> POST /cms/v3/pages/site-pages/ab-test/rerun
- "Create a archive?" -> POST /cms/v3/pages/site-pages/batch/archive
- "Create a create?" -> POST /cms/v3/pages/site-pages/batch/create
- "Create a read?" -> POST /cms/v3/pages/site-pages/batch/read
- "Create a update?" -> POST /cms/v3/pages/site-pages/batch/update
- "Create a clone?" -> POST /cms/v3/pages/site-pages/clone
- "List all cursor?" -> GET /cms/v3/pages/site-pages/cursor
- "List all query?" -> GET /cms/v3/pages/site-pages/cursor/query
- "Create a attach-to-lang-group?" -> POST /cms/v3/pages/site-pages/multi-language/attach-to-lang-group
- "Create a create-language-variation?" -> POST /cms/v3/pages/site-pages/multi-language/create-language-variation
- "Create a detach-from-lang-group?" -> POST /cms/v3/pages/site-pages/multi-language/detach-from-lang-group
- "Create a update-language?" -> POST /cms/v3/pages/site-pages/multi-language/update-languages
- "Create a schedule?" -> POST /cms/v3/pages/site-pages/schedule
- "Get site-page details?" -> GET /cms/v3/pages/site-pages/{objectId}
- "Delete a site-page?" -> DELETE /cms/v3/pages/site-pages/{objectId}
- "Partially update a site-page?" -> PATCH /cms/v3/pages/site-pages/{objectId}
- "List all draft?" -> GET /cms/v3/pages/site-pages/{objectId}/draft
- "Create a push-live?" -> POST /cms/v3/pages/site-pages/{objectId}/draft/push-live
- "Create a reset?" -> POST /cms/v3/pages/site-pages/{objectId}/draft/reset
- "List all revisions?" -> GET /cms/v3/pages/site-pages/{objectId}/revisions
- "Get revision details?" -> GET /cms/v3/pages/site-pages/{objectId}/revisions/{revisionId}
- "Create a restore?" -> POST /cms/v3/pages/site-pages/{objectId}/revisions/{revisionId}/restore
- "Create a restore-to-draft?" -> POST /cms/v3/pages/site-pages/{objectId}/revisions/{revisionId}/restore-to-draft
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
