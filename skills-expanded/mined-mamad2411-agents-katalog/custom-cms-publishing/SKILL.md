---
name: custom-cms-publishing
description: "Publish and update markdown content through custom CMS/admin APIs: store secrets safely, build payloads, handle create-vs-update, and verify public URLs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [cms, publishing, admin-api, markdown, content, verification, secrets]
    related_skills: [google-workspace, notion]
    created_by: agent
---

# Custom CMS Publishing

Use this skill when the user asks to publish, update, or republish an article/page/post through a custom website admin API, CMS endpoint, or lightweight backend rather than a known product integration.

The goal is a live, verified public artifact — not just a local draft or a claimed API call.

## Workflow

0. **Check the intake channel when the CMS has one.**
   - If the user asks to create or use a dedicated Telegram topic for publishing intake, create the forum topic via the Telegram Bot API, record the `message_thread_id`, update the gateway channel directory if needed, send a test message into the topic, and store only the stable routing fact in memory.
   - For `cerita.basim.id`, see `references/cerita-basim-admin-api.md` for the current Telegram topic mapping and admin API notes.
1. **Collect API contract and scope.**
   - Endpoint URL and method for create/update.
   - Required headers, especially auth header names.
   - Required body fields and status values (`draft`, `published`, etc.).
   - Public route shape(s) for verification.
   - Whether duplicate slugs create conflicts, revisions, or overwrites.
2. **Store secrets safely before use.**
   - Secrets belong in `~/.hermes/.env` or another user-approved private env file, never in the published article, prompt-visible summaries, logs sent to the user, or reusable references.
   - Use permission `600` for env files when writing credentials.
   - In final replies and support files, represent tokens as `[REDACTED]`.
3. **Create a local markdown source of truth.**
   - Write/keep a local `.md` file for the article body.
   - Build the JSON payload from that file so retries and updates are deterministic.
   - Save the payload locally only if it does not expose secrets.
4. **Publish with exact API semantics.**
   - Send `Content-Type: application/json` and the documented auth header.
   - Set `status: "published"` when the user asks for a live post.
   - Capture HTTP status and response body, redacting secrets before surfacing output.
5. **Handle create-vs-update explicitly.**
   - `201` or `200` with `success: true` usually means success.
   - `409 Slug already exists` means do not keep POSTing the same slug. Discover or use the documented update endpoint, commonly `PATCH /posts/<slug>`.
   - If the API has no update endpoint, ask whether to create a new slug or stop.
6. **Verify both admin and public views.**
   - Admin GET verifies persisted fields and body length/content markers.
   - Public GET verifies the route users can open.
   - If docs say one route but public verification succeeds on another, report the verified route and the mismatch.

## Payload pattern

```json
{
  "slug": "stable-slug",
  "title": "Human Title",
  "description": "Short summary for cards/SEO",
  "body_md": "# Markdown body...",
  "tags": ["tag-a", "tag-b"],
  "status": "published",
  "featured": false,
  "author": "Author Name",
  "source": "admin-api"
}
```

## Verification pattern

- Verify admin persistence with a GET endpoint if available: check `id`, `slug`, `status`, body character count, and a phrase unique to the new version.
- Verify the public URL with cache-busting when necessary (`?nocache=<timestamp>`) and check for unique content markers.
- Report exact status codes and the final verified URL.

## Pitfalls

- Do not print or quote API tokens back to the user after receiving them.
- Do not assume `POST` overwrites. Treat duplicate slugs as update-required unless docs prove otherwise.
- Do not trust the response `url` blindly if public verification returns 404; test alternate documented routes and report the one that actually returns 200.
- Do not call a local draft “published” until the API response and public route have been verified.
- Do not save transient 401/403 failures as durable conclusions. Save the fix pattern: verify the actual auth header/secret, check whether Cloudflare/WAF is intercepting, and retry only with corrected inputs.

## References

- `references/cerita-basim-admin-api.md` — session-derived admin API notes for `cerita.basim.id`, including token storage, POST create, PATCH update by slug, 409 handling, and verified public route shape.
