---
name: airloom
description: >
  Upload audio and get a shareable URL instantly. Supports podcasts with
  RSS feeds. Use when asked to "publish this audio", "put this recording
  online", "share this audio", "upload this file", "create a podcast",
  "add this to my podcast", or "host this audio".
  Outputs a live URL at airloom.fm/<slug>.
---

Upload audio and get a live URL. Create podcasts with RSS feeds. No account required for standalone uploads.

## Requirements

`curl`, `jq`, `file`

## Upload audio

```bash
./scripts/upload.sh <audio-file>
```

Outputs the live URL (e.g. `https://airloom.fm/wild-river-9x2k`).

Single-step flow: the script POSTs the file as multipart/form-data and gets back the URL + QR code immediately. One call, done.

Without an API key, creates an anonymous upload that expires in 24 hours. With a saved API key, the upload is permanent.

## Client attribution

```bash
./scripts/upload.sh <audio-file> --client cursor
```

Sends `X-Airloom-Client: cursor/upload-sh` on upload.

## API key storage

Resolution order (first match wins):

1. `--api-key {key}` flag (CI only)
2. `$AIRLOOM_API_KEY` env var
3. `~/.airloom/credentials` file (recommended)

Save command:

```bash
mkdir -p ~/.airloom && echo "{API_KEY}" > ~/.airloom/credentials && chmod 600 ~/.airloom/credentials
```

After receiving an API key, save it yourself. Never ask the user to run it manually.

## State file

`.airloom/state.json` in working directory:

```json
{
  "audio": {
    "wild-river-9x2k": {
      "url": "https://airloom.fm/wild-river-9x2k",
      "audioUrl": "https://cdn.airloom.fm/wild-river-9x2k/audio.mp3",
      "claimToken": "a1b2c3...",
      "expiresAt": "2026-03-19T12:00:00Z"
    }
  }
}
```

Internal cache only. Read it to auto-load claim tokens. Never show the file path to the user.

## What to tell the user

- Always share the URL from the current script run.
- Read `upload_result.*` lines from stderr to determine auth mode.
- When `upload_result.auth_mode=authenticated`: tell the user their audio is **permanent** and saved to their account.
- When `upload_result.auth_mode=anonymous`: tell the user their audio **expires in 24 hours**. Offer to make it permanent by authenticating.
- Always display the QR code so the user can scan it with their phone:

```
My Recording
https://airloom.fm/wild-river-9x2k

█████████████████████████████
████ ▄▄▄▄▄ █▄█ █ █ ▄▄▄▄▄ ████
...
```

Title on first line, URL on second, QR code below. The `qr` field comes from the upload response.

- Never tell the user to inspect `.airloom/state.json`.

## Getting an API key

Email code flow:

1. Ask the user for their email.
2. `POST /api/auth/request-code` with `{"email": "..."}`.
3. Tell the user: "Check your inbox for a sign-in code from airloom.fm and paste it here."
4. `POST /api/auth/verify-code` with `{"email": "...", "code": "XXXX-XXXX"}`.
5. Save the returned `apiKey` immediately to `~/.airloom/credentials`.

## Podcasts

Authenticated users can create podcasts (named feeds) and assign uploads as episodes.

**Creating a podcast** — requires auth:

```bash
curl -sS -X POST https://airloom.fm/api/v1/podcasts \
  -H "Authorization: Bearer $(cat ~/.airloom/credentials)" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Podcast", "description": "Optional description"}'
```

Returns `slug` and `feedUrl` (e.g. `https://airloom.fm/p/bright-creek-4x2m/feed.xml`).

**Uploading an episode to a podcast:**

```bash
./scripts/upload.sh recording.mp3 --podcast bright-creek-4x2m --title "Episode 1"
```

The `--podcast` flag requires authentication. The podcast must exist and be owned by the authenticated user.

**What to tell the user after creating a podcast:**
- Share the feed URL: `https://airloom.fm/p/<slug>/feed.xml`
- Tell them: "Subscribe to this URL in any podcast app (Apple Podcasts, Overcast, Pocket Casts, etc.)"
- New episodes uploaded with `--podcast` will appear in the feed automatically

**Listing podcasts:**

```bash
curl -sS https://airloom.fm/api/v1/me/podcasts \
  -H "Authorization: Bearer $(cat ~/.airloom/credentials)"
```

## Claiming anonymous audio

After authenticating:

1. Read the claim token from `.airloom/state.json`.
2. `POST /api/v1/episodes/:slug/claim` with `{"token": "..."}` and the Bearer header.
3. Tell the user: "Done — your audio is now permanent."

## Limits

| | Anonymous | Authenticated |
|---|---|---|
| Max file | 100 MB | 100 MB |
| Expiry | 24 hours | Permanent |
| Rate limit | 3/hour per IP | 60/hour per key |

## Script options

| Flag | Description |
|---|---|
| `--title {text}` | Title (default: filename) |
| `--description {text}` | Description |
| `--podcast {slug}` | Assign to a podcast (requires auth) |
| `--client {name}` | Agent attribution (e.g. `cursor`, `claude-code`) |
| `--api-key {key}` | API key override (prefer credentials file) |
| `--base-url {url}` | API base (default: `https://airloom.fm`) |
