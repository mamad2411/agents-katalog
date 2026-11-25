---
name: docs-api
description: >-
  Writes and maintains docs/api-reference.md — the HTTP API reference for
  InterlinedList. Use when the user asks to generate, update, or review API
  documentation, add a new endpoint to the reference, or explain how to call
  a specific route.
---

# docs-api skill (InterlinedList)

## When this applies

Use this skill whenever the task involves **API documentation** for InterlinedList:

- Generating `docs/api-reference.md` from scratch
- Updating it when a new route is added or an existing one changes
- Answering "what does this endpoint accept?" or "how do I authenticate?"
- Reviewing or extending an existing draft

## Two modes of operation

### Mode 1 — Automated (recommended for initial generation or full refresh)

```bash
node scripts/generate-docs.js --perspective api
```

Requires `ANTHROPIC_API_KEY`. Reads all ~117 route files and writes `docs/api-reference.md` autonomously.

### Mode 2 — Interactive (this Claude Code session)

Follow the reading order below, then write or update the reference.

## Reading order for interactive mode

Work through route groups in this order (highest value first):

### Auth & session (highest priority)
- `app/api/auth/login/route.ts`
- `app/api/auth/register/route.ts`
- `app/api/auth/logout/route.ts`
- `app/api/auth/sync-token/route.ts`
- `app/api/auth/forgot-password/route.ts`
- `app/api/auth/reset-password/route.ts`
- `app/api/auth/verify-email/route.ts`
- `lib/auth/session.ts`

### Messages (core resource)
- `app/api/messages/route.ts` — read in full; complex POST with cross-posting
- `app/api/messages/[id]/route.ts`
- `app/api/messages/[id]/replies/route.ts`
- `app/api/messages/scheduled/route.ts`
- `app/api/messages/images/upload/route.ts`
- `app/api/messages/videos/upload/route.ts`

### Lists
- `app/api/lists/route.ts`
- `app/api/lists/[id]/route.ts`
- `app/api/lists/[id]/data/route.ts`
- `app/api/lists/[id]/data/[rowId]/route.ts`
- `app/api/lists/[id]/schema/route.ts`
- `app/api/lists/[id]/watchers/route.ts`
- `app/api/lists/connections/route.ts`

### Users & following
- `app/api/user/route.ts`
- `app/api/user/update/route.ts`
- `app/api/user/[username]/messages/route.ts`
- `app/api/follow/[userId]/route.ts`
- `app/api/follow/[userId]/status/route.ts`
- `app/api/follow/requests/route.ts`

### Documents, Organizations, Notifications, Push, Exports
- Read each resource's `route.ts` and `[id]/route.ts`

### Cron, Webhooks, Admin
- Document as **internal/secured** — not publicly callable

## Per-endpoint template

```markdown
### METHOD /api/path/with/:param

**Auth required:** yes | no  
**Description:** One sentence.

**Path parameters** _(if any)_
| Param | Type | Description |
|-------|------|-------------|
| `id` | string | UUID of the resource |

**Query parameters** _(if any)_
| Param | Type | Required | Description |
|-------|------|----------|-------------|

**Request body** _(for POST / PUT / PATCH)_
\`\`\`json
{
  "field": "type and description"
}
\`\`\`

**Response** `200 OK`
\`\`\`json
{
  "field": "..."
}
\`\`\`

**Error responses**
| Status | Condition |
|--------|-----------|
| 400 | Missing required field |
| 401 | Not authenticated |
```

## Document structure for docs/api-reference.md

```markdown
# InterlinedList API Reference

## Table of Contents

## Overview
- Base URL
- Authentication
- Error format
- Common response fields

## Quick Start
Three-step example: authenticate → post a message → cross-post

## Authentication
### POST /api/auth/register
### POST /api/auth/login
### POST /api/auth/logout
### GET  /api/auth/sync-token
... (all auth routes)

## Messages
### POST /api/messages
... (full cross-posting options documented here)

## Lists
...

## Documents
...

## Organizations
...

## Users & Profile
...

## Following
...

## Notifications
...

## Push Notifications
...

## Exports
...

## OAuth Provider Flows
(LinkedIn, Mastodon, Bluesky, GitHub — describe the authorize → callback pattern)

## Admin Endpoints
(internal, document minimally)

## Cron Endpoints
(internal, secured by CRON_SECRET, not for public use)

## Webhook Endpoints
(Stripe, Resend — signature-verified, not for direct calls)
```

## Constraints

- Derive every field name from the actual route handler source — do not invent.
- Mark auth requirement accurately; read `getCurrentUser()` or session checks in each handler.
- Do not describe UI flows or infrastructure — those belong in the other two docs.
- Cron and webhook endpoints must be clearly marked as internal/secured.
