---
name: youtube-channel-video-list
description: List all uploaded videos on the authenticated YouTube channel via Data API v3 — outputs video ID, title, and published date.
category: YouTube
---

# YouTube Channel Video List Skill (v1)

This is a **base** skill. It queries the YouTube Data API v3 to discover the authenticated user's uploads playlist, then lists every video in it via `playlistItems.list`. Outputs video ID, title, and published date in tabular or JSON format. Requires valid OAuth credentials obtained via [`google-oauth-setup`](../google-oauth-setup/SKILL.md). Reusable by any YouTube workflow needing a full video inventory (channel audit, content organization, analytics migration).

***

## 1. Scope & Intent

- **In scope**: Discover the authenticated channel's uploads playlist, paginate through all videos, output video ID + title + published date.
- **Out of scope**:
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Playlist management (listing, creating, updating playlists).
    - Video metadata beyond ID, title, and published date.
    - Any non-YouTube API.

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — scripts use `argparse`, `json`, `requests`. Verify:

  ```bash
  python3 --version
  ```

- **`requests`** library. Verify:

  ```bash
  python3 -c "import requests; print('OK')"
  ```

### 2.2 Required Files

| File | Source |
|---|---|
| Valid OAuth credential cache (with `access_token`) | [`google-oauth-setup`](../google-oauth-setup/SKILL.md) §3 |

***

## 3. Protocol

### 3.1 Step 1 — Ensure Valid Credentials

Before listing channel videos, verify the credential cache exists and the access token is valid. Delegate to [`google-oauth-setup`](../google-oauth-setup/SKILL.md):

```bash
# Refresh if expired
python3 .agents/skills/google-oauth-setup/scripts/oauth-token-refresh.py \
  --client-secrets <client_secrets.json> \
  --credentials <credentials.json> \
  --output <credentials.json>
```

If the refresh fails (expired refresh token), run the full PKCE flow:

```bash
python3 .agents/skills/google-oauth-setup/scripts/oauth-setup.py \
  --client-secrets <client_secrets.json> \
  --scopes "https://www.googleapis.com/auth/youtube" \
  --output <credentials.json>
```

### 3.2 Step 2 — List Channel Videos

```bash
python3 .agents/skills/youtube-channel-video-list/scripts/channel-video-list.py \
  --credentials <path>
```

#### 3.2.1 Flag Breakdown

| Argument | Purpose |
|---|---|
| `--credentials` | Path to OAuth credential cache JSON (must contain `access_token`). |
| `--format` | Output format: `table` (default) or `json`. |

### 3.3 Step 3 — Interpret Output

Table format:

```text
VIDEO_ID       | PUBLISHED            | TITLE
v8M-tvdJV9I   | 2026-04-11           | OleoVista – 2026-04-11 – Call with Dileena Beegum – Unexpected Staging Server Behaviour
wSngIP_PR7k   | 2026-04-11           | OleoVista – 2026-04-11 – Cross-Team – Unexpected Staging Server Behaviour Discussion
```

JSON format (one JSON object per line):

```json
{"video_id": "v8M-tvdJV9I", "title": "OleoVista ...", "published_at": "2026-04-11T..."}
{"video_id": "wSngIP_PR7k", "title": "OleoVista ...", "published_at": "2026-04-11T..."}
```

Use the video ID for subsequent operations (adding to playlists via [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md), updating metadata via [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md)).

***

## 4. Script Reference

### 4.1 `scripts/channel-video-list.py`

List all uploaded videos on the authenticated channel.

```text
python3 .agents/skills/youtube-channel-video-list/scripts/channel-video-list.py \
  --credentials <path> \
  [--format table|json]
```

The script:

1. Loads credentials JSON and validates required fields.
2. Calls `GET https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true` to get the uploads playlist ID.
3. Iterates over `playlistItems.list` on the uploads playlist, following pagination.
4. For each item, extracts `videoId`, `title`, and `publishedAt`.
5. Outputs in table or JSON format.
6. Exits 0 on success, 1 on error.

***

## 5. Edge Cases

- **401 Unauthorized**: Access token is expired or invalid. Run `oauth-token-refresh.py` from [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and retry.
- **403 Forbidden**: The OAuth scope does not include YouTube. Re-run `oauth-setup.py` with `--scopes "https://www.googleapis.com/auth/youtube"`.
- **Empty channel**: No videos uploaded. Inform the user.
- **Pagination**: The script follows `nextPageToken` automatically (up to 50 per page, no limit).
- **No uploads playlist**: If the channel has no uploads, the API returns an empty list. Inform the user.
- **Brand account**: If the authenticated user manages multiple channels, the credentials are scoped to one channel. Run `oauth-setup.py` again for a different channel.

***

## 6. Prohibited Actions

- The agent MUST NOT hardcode a video ID or title — always present the list and let the user choose.
- The agent MUST NOT skip the credential refresh step.
- The agent MUST NOT modify channel or video data — this is a read-only operation.

***

## 7. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|---|---|
| [`youtube-channel-video-organize`](../youtube-channel-video-organize/SKILL.md) | Calls `scripts/channel-video-list.py` with `--format json` as the first step; parses the JSON output to build a video inventory for categorization. |

***

## 8. Composition Rationale

This skill is a **base** skill: it owns only the YouTube channel video listing API call (channel discovery + uploads playlist pagination). It delegates all OAuth lifecycle management to [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and is itself composed by the channel video organization workflow. Separating video listing from playlist management and organization allows each operation to be reused independently (e.g., bulk video audit, content migration planning).
