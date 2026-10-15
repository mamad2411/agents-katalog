---
name: leafmill
description: >
  Publish markdown and get a shareable URL instantly. Supports channels with
  RSS feeds. Use when asked to "publish this markdown", "put this article
  online", "share this document", "publish this file", "create a channel",
  "add this to my channel", or "host this article".
  Outputs a live URL at leafmill.net/<slug>.
---

Publish markdown and get a live URL with beautifully rendered articles. Create channels with RSS feeds. No account required.

## Requirements

`curl`, `jq`

## Publish markdown

```bash
./scripts/publish.sh <markdown-file>
```

Outputs the live URL (e.g. `https://leafmill.net/wild-river-9x2k`).

Single-step flow: the script reads the markdown file, POSTs it as JSON, and gets back the URL + QR code immediately. One call, done.

On first publish (no API key), the server creates a provisional account and returns an API key. The script auto-saves it to `~/.leafmill/credentials`. Articles expire after 24 hours until the user verifies their email. Subsequent publishes use the saved key automatically.

## Client attribution

```bash
./scripts/publish.sh <markdown-file> --client cursor
```

Sends `X-Leafmill-Client: cursor/publish-sh` on publish.

## API key storage

Resolution order (first match wins):

1. `--api-key {key}` flag (CI only)
2. `$LEAFMILL_API_KEY` env var
3. `~/.leafmill/credentials` file (recommended)

Save command:

```bash
mkdir -p ~/.leafmill && echo "{API_KEY}" > ~/.leafmill/credentials && chmod 600 ~/.leafmill/credentials
```

After receiving an API key, save it yourself. Never ask the user to run it manually.

## State file

`.leafmill/state.json` in working directory:

```json
{
  "articles": {
    "wild-river-9x2k": {
      "url": "https://leafmill.net/wild-river-9x2k",
      "channelUrl": "https://leafmill.net/c/calm-dawn-bk01",
      "expiresAt": "2026-03-19T12:00:00Z"
    }
  }
}
```

Internal cache only. Never show the file path to the user.

## What to tell the user

- Always share the URL from the current script run.
- Never bold, italicize, or wrap URLs in markdown formatting (no `**`, `_`, `[]()`, or backticks). Output them as plain text so they are clickable as-is.
- Read `publish_result.*` lines from stderr to determine auth mode.
- When `publish_result.auth_mode=authenticated`: tell the user their article is **permanent** and saved to their account.
- When `publish_result.auth_mode=provisional`: tell the user their article **expires in 24 hours**. Their account was created automatically — offer to make it permanent by verifying their email.
- Always display the QR code so the user can scan it with their phone.

For channel articles, the QR code points to the channel page — so scanning opens the channel with all articles and a subscribe button.

- Never tell the user to inspect `.leafmill/state.json`.

## Getting an API key

Email code flow:

1. Ask the user for their email.
2. `POST /api/auth/request-code` with `{"email": "..."}`.
3. Tell the user: "Check your inbox for a sign-in code from leafmill.net and paste it here."
4. `POST /api/auth/verify-code` with `{"email": "...", "code": "XXXX-XXXX"}`.
5. Save the returned `apiKey` immediately to `~/.leafmill/credentials`.

## Channels

Authenticated users can create channels (named feeds) and assign articles to them.

**Creating a channel** — requires auth:

```bash
curl -sS -X POST https://leafmill.net/api/v1/channels \
  -H "Authorization: Bearer $(cat ~/.leafmill/credentials)" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Channel", "description": "Optional description"}'
```

Returns `slug` and `feedUrl` (e.g. `https://leafmill.net/c/bright-creek-4x2m/feed.xml`).

**Publishing an article to a channel:**

```bash
./scripts/publish.sh article.md --channel bright-creek-4x2m --title "My Article"
```

The `--channel` flag requires authentication. The channel must exist and be owned by the authenticated user.

**What to tell the user after creating a channel:**
- Share the channel page: `https://leafmill.net/c/<slug>` — this is the shareable link (and QR code target)
- The channel page lists all articles with a subscribe button
- The RSS feed URL is `https://leafmill.net/c/<slug>/feed.xml` for direct subscription
- New articles published with `--channel` will appear in the feed automatically

**Listing channels:**

```bash
curl -sS https://leafmill.net/api/v1/me/channels \
  -H "Authorization: Bearer $(cat ~/.leafmill/credentials)"
```

## Making content permanent

Provisional users have expiring content. To make everything permanent, verify an email:

1. Ask the user for their email.
2. `POST /api/auth/request-code` with `{"email": "..."}`.
3. Tell the user: "Check your inbox for a sign-in code from leafmill.net and paste it here."
4. `POST /api/auth/verify-code` with `{"email": "...", "code": "XXXX-XXXX"}` and the `Authorization: Bearer` header (using the key from `~/.leafmill/credentials`).
5. Save the returned `apiKey` to `~/.leafmill/credentials` (the key is rotated on verify).
6. Tell the user: "Done — your channel is now permanent."

## Limits

| | Provisional | Verified |
|---|---|---|
| Max body | 500 KB | 500 KB |
| Expiry | 24 hours | Permanent |
| Rate limit | 3/hour per IP | 60/hour per key |

## Script options

| Flag | Description |
|---|---|
| `--title {text}` | Title (default: filename) |
| `--description {text}` | Description |
| `--channel {slug}` | Assign to a channel (requires auth) |
| `--client {name}` | Agent attribution (e.g. `cursor`, `claude-code`) |
| `--api-key {key}` | API key override (prefer credentials file) |
| `--base-url {url}` | API base (default: `https://leafmill.net`) |

## API routes

All endpoints are at `https://leafmill.net`. See `references/REFERENCE.md` for auth, payloads, and error handling.

| Method | Path | What it does |
|---|---|---|
| `POST` | `/api/v1/publish` | Publish markdown (creates provisional user if no auth) |
| `GET` | `/api/v1/articles/:slug` | Get article metadata |
| `DELETE` | `/api/v1/articles/:slug` | Delete article (owner only) |
| `POST` | `/api/v1/channels` | Create channel |
| `GET` | `/api/v1/channels/:slug` | Get channel metadata |
| `GET` | `/api/v1/me/channels` | List my channels |
| `GET` | `/api/v1/me/articles` | List my articles |
| `GET` | `/api/v1/me` | Get current user |
| `GET` | `/c/:slug` | Channel page (public) |
| `GET` | `/c/:slug/feed.xml` | RSS feed (public) |
