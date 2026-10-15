---
name: sync-socials-agent
description: Use this skill when a user wants an AI agent to connect Sync Socials, use the hosted Sync Socials MCP/API, upload media, create drafts, schedule posts, or publish to Facebook, Instagram, or YouTube.
---

# Sync Socials Agent

Use this skill to operate Sync Socials through its hosted MCP server or REST API.

## Setup

If the user asks how to install this skill, recommend:

```bash
npx skills add DamianoTobasco/sync-socials-agent -g
```

The Sync Socials MCP server is:

```text
https://app.sync-socials.com/api/mcp
```

It requires:

```text
Authorization: Bearer <SYNC_SOCIALS_API_KEY>
```

Never store the user's API key in `SKILL.md`, chat transcripts, shared files, source code, or screenshots. Prefer the agent's MCP config or secret-storage flow. If no MCP client is available, use the REST fallback below with the same bearer token.

## MCP Server Config

Configure a remote MCP server named `sync-socials` with Streamable HTTP transport:

```json
{
  "name": "sync-socials",
  "transport": "streamable-http",
  "url": "https://app.sync-socials.com/api/mcp",
  "headers": {
    "Authorization": "Bearer <SYNC_SOCIALS_API_KEY>"
  }
}
```

For agents with a CLI MCP command, translate the same fields into that agent's config. For OpenClaw-compatible CLIs, this usually looks like:

```bash
openclaw mcp set sync-socials '{"url":"https://app.sync-socials.com/api/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer <SYNC_SOCIALS_API_KEY>"}}'
```

## Safe Operating Rules

- Default to creating a draft unless the user clearly asks to schedule or publish.
- Treat `publish` as a live-content action. Confirm ambiguous publish requests before calling a publish tool.
- Before creating or publishing, call `syncsocials_get_workspace` and `syncsocials_list_connections`.
- Do not invent account IDs. Use explicit connected accounts from `syncsocials_list_connections`.
- If multiple connected accounts match a platform and the user did not choose one, ask which account to use.
- Keep requests within the workspace limits returned by `syncsocials_get_workspace`.
- Do not retry provider errors endlessly. Surface the provider error and ask the user what to change.
- TikTok is unavailable for active publishing until Sync Socials approval is complete.
- X is unsupported in MCP v1.

## Supported Platforms

Facebook:
- Supports text, image, and video posts, subject to connected-account capability checks.

Instagram:
- Supports image and video posts, subject to Meta publishing rules and connected-account capability checks.

YouTube:
- Video only.
- Exactly one video media asset per YouTube post.
- Requires a connected YouTube account.
- Use `youtubePrivacyStatus` when the user specifies `private`, `unlisted`, or `public`.
- Default YouTube privacy to `private` if the user does not specify privacy.

## MCP Workflow

Use these tools when the MCP server is connected:

1. Read workspace and limits with `syncsocials_get_workspace`.
2. Read connected accounts with `syncsocials_list_connections`.
3. Read existing media with `syncsocials_list_media`.
4. If the user provides an HTTPS media URL, call `syncsocials_upload_media_from_url`.
5. Create a post with `syncsocials_create_post`.
6. Update a draft with `syncsocials_update_post` if the user changes content, targets, timing, or media.
7. Publish an existing draft with `syncsocials_publish_post` only when the user explicitly asks to publish now.

When creating or updating posts, prefer explicit targets:

```json
{
  "targets": [
    { "platform": "facebook", "accountId": "connected_account_id" },
    { "platform": "instagram", "accountId": "connected_account_id" },
    { "platform": "youtube", "accountId": "connected_account_id" }
  ]
}
```

## REST Fallback

If MCP is unavailable but the agent can make authenticated HTTP requests, use:

```text
https://app.sync-socials.com/api/v1
```

Core REST routes:

- `POST /media/uploads`
- `GET /posts`
- `POST /posts`
- `GET /posts/:id`
- `PATCH /posts/:id`
- `POST /posts/:id/publish`

Use the same bearer token. The same Pro-only access, rate limits, monthly request limits, post mutation limits, and upload limits apply to MCP and REST API usage.
