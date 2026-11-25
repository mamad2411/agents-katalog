---
name: marketing-emails
description: "Marketing Emails API skill. Use when working with Marketing Emails for marketing. Covers 19 endpoints."
version: 1.0.0
generator: lapsh
---

# Marketing Emails
API version: v3

## Auth
OAuth2 | ApiKey private-app in header

## Base URL
https://api.hubapi.com

## Setup
1. Set your API key in the appropriate header
2. GET /marketing/v3/emails/ -- verify access
3. POST /marketing/v3/emails/ -- create first emails

## Endpoints

19 endpoints across 1 groups. See references/api-spec.lap for full details.

### marketing
| Method | Path | Description |
|--------|------|-------------|
| GET | /marketing/v3/emails/ | Get all marketing emails |
| POST | /marketing/v3/emails/ | Create a new marketing email |
| POST | /marketing/v3/emails/ab-test/create-variation | Create an A/B test variation of a marketing email |
| POST | /marketing/v3/emails/clone | Clone a marketing email |
| GET | /marketing/v3/emails/statistics/histogram | Get aggregated statistic intervals |
| GET | /marketing/v3/emails/statistics/list | Get aggregated statistics |
| GET | /marketing/v3/emails/{emailId} | Get the details of a specified marketing email |
| DELETE | /marketing/v3/emails/{emailId} | Delete a marketing email |
| PATCH | /marketing/v3/emails/{emailId} | Update a marketing email |
| GET | /marketing/v3/emails/{emailId}/ab-test/get-variation | Get the variation of a an A/B marketing email |
| GET | /marketing/v3/emails/{emailId}/draft | Get draft version of a marketing email |
| PATCH | /marketing/v3/emails/{emailId}/draft | Create or update draft version |
| POST | /marketing/v3/emails/{emailId}/draft/reset | Reset the draft version |
| POST | /marketing/v3/emails/{emailId}/publish | Publish or send a marketing email |
| GET | /marketing/v3/emails/{emailId}/revisions | Get revisions of a marketing email |
| GET | /marketing/v3/emails/{emailId}/revisions/{revisionId} | Get a revision of a marketing email |
| POST | /marketing/v3/emails/{emailId}/revisions/{revisionId}/restore | Restore a revision of a marketing email |
| POST | /marketing/v3/emails/{emailId}/revisions/{revisionId}/restore-to-draft | Restore a revision of a marketing email to DRAFT state |
| POST | /marketing/v3/emails/{emailId}/unpublish | Unpublish or cancel a marketing email |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all emails?" -> GET /marketing/v3/emails/
- "Create a email?" -> POST /marketing/v3/emails/
- "Create a create-variation?" -> POST /marketing/v3/emails/ab-test/create-variation
- "Create a clone?" -> POST /marketing/v3/emails/clone
- "List all histogram?" -> GET /marketing/v3/emails/statistics/histogram
- "List all list?" -> GET /marketing/v3/emails/statistics/list
- "Get email details?" -> GET /marketing/v3/emails/{emailId}
- "Delete a email?" -> DELETE /marketing/v3/emails/{emailId}
- "Partially update a email?" -> PATCH /marketing/v3/emails/{emailId}
- "List all get-variation?" -> GET /marketing/v3/emails/{emailId}/ab-test/get-variation
- "List all draft?" -> GET /marketing/v3/emails/{emailId}/draft
- "Create a reset?" -> POST /marketing/v3/emails/{emailId}/draft/reset
- "Create a publish?" -> POST /marketing/v3/emails/{emailId}/publish
- "List all revisions?" -> GET /marketing/v3/emails/{emailId}/revisions
- "Get revision details?" -> GET /marketing/v3/emails/{emailId}/revisions/{revisionId}
- "Create a restore?" -> POST /marketing/v3/emails/{emailId}/revisions/{revisionId}/restore
- "Create a restore-to-draft?" -> POST /marketing/v3/emails/{emailId}/revisions/{revisionId}/restore-to-draft
- "Create a unpublish?" -> POST /marketing/v3/emails/{emailId}/unpublish
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
