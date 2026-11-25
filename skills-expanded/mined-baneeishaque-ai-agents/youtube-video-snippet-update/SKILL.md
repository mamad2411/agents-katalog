---
name: youtube-video-snippet-update
description: Update YouTube video title, description, and tags via Data API v3 videos.update — post-upload snippet correction.
category: YouTube
---

# YouTube Video Snippet Update Skill (v1)

This is a **base** skill. It calls the YouTube Data API v3 `videos.update` endpoint to modify a
video's title, description, and/or tags. Requires valid OAuth credentials obtained via
[`google-oauth-setup`](../google-oauth-setup/SKILL.md). Reusable by any YouTube workflow needing to
correct or update basic video metadata post-upload (backfill rename, bulk title fix, description
update).

***

## 1. Scope & Intent

- **In scope**: Authenticate via cached OAuth credentials, fetch current video snippet via
  `videos.list`, apply deltas for title/description/tags, PUT updated snippet via `videos.update`,
  print confirmation.
- **Out of scope**:
    - OAuth token management (delegated to
      [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Uploading videos (delegated to
      [`youtube-video-upload`](../youtube-video-upload/SKILL.md)).
    - Advanced metadata fields (category, language, embeddable, madeForKids, license,
      publicStatsViewable, containsSyntheticMedia, age restriction — delegated to
      [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md)).
    - Playlist management or adding videos to playlists.
    - Any non-YouTube API.

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — scripts use `argparse`, `json`, `os.path`, `requests`. Verify:

  ```bash
  python3 --version
  ```

- **`requests`** library. Verify:

  ```bash
  python3 -c "import requests; print('OK')"
  ```

### 2.2 Required Files

| File                    | Source                                                          |
|-------------------------|-----------------------------------------------------------------|
| Valid OAuth credential cache (with `access_token`) | [`google-oauth-setup`](../google-oauth-setup/SKILL.md) §3 |

***

## 3. Protocol

### 3.1 Step 1 — Ensure Valid Credentials

Before updating video metadata, verify the credential cache exists and the access token is valid.
Delegate to [`google-oauth-setup`](../google-oauth-setup/SKILL.md):

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

### 3.2 Step 2 — Update Video Snippet

```bash
python3 .agents/skills/youtube-video-snippet-update/scripts/video-snippet-update.py \
  <VIDEO_ID> \
  --credentials <path> \
  [--title "<New Title>"] \
  [--description "<New Description>"] \
  [--tags "tag1 tag2"]
```

#### 3.2.1 Arguments

| Argument       | Required | Description                                                                   |
|----------------|----------|-------------------------------------------------------------------------------|
| `video_id`     | Yes (positional) | YouTube video ID (e.g., `dQw4w9WgXcQ`).                                       |
| `--credentials` | Yes      | Path to OAuth credential cache JSON (must contain `access_token`).             |
| `--title`      | No       | New video title (max 100 characters).                                         |
| `--description` | No      | New video description.                                                        |
| `--tags`       | No       | Space-separated tags (e.g., `--tags "tag1 tag2"`).                            |

At least one of `--title`, `--description`, or `--tags` must be provided. If none are provided, the
script prints an error and exits 1.

### 3.3 Step 3 — Interpret Output

The script prints the updated snippet:

```text
Updated: https://youtu.be/dQw4w9WgXcQ
  Title:       Sanath Next.js Website – 2025-12-01 – Standup
  Description: Discussion about Supabase admin panel work with Sanath...
  Tags:        sanath, nextjs, supabase
```

Confirm the video URL and new values are correct.

***

## 4. Edge Cases

- **401 Unauthorized**: Access token is expired or invalid. Run `oauth-token-refresh.py` from
  [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and retry.
- **403 Forbidden**: The OAuth scope does not include YouTube. Re-run `oauth-setup.py` with
  `--scopes "https://www.googleapis.com/auth/youtube"`.
- **Video not found (404)**: The specified video ID does not exist or the authenticated user does
  not own it. The script exits 1.
- **Title too long**: YouTube limits video titles to 100 characters. The API returns a 400
  `invalidTitle` error — the script prints the diagnostic and exits 1.
- **No changes requested**: If `--title`, `--description`, and `--tags` are all omitted, the script
  prints an error and exits 1.
- **Tags source**: Tags from the API are comma-separated in the output but provided as a
  space-separated string in the CLI. If tags contain spaces (multi-word tags), use the YouTube
  Studio or the API directly.
- **Concurrent edits**: If another process modifies the video between the GET and PUT, the PUT
  overwrites those changes. Ensure no other session is editing the same video.

***

## 5. Prohibited Actions

- The agent MUST NOT hardcode a video ID or new title/description — always present current state and
  let the user confirm changes.
- The agent MUST NOT update a video without user confirmation of the video ID and the new values.
- The agent MUST NOT skip the credential refresh step — a stale token will return 401.
- The agent MUST NOT use this skill to change video category, language, privacy, or any field
  outside `snippet.title`, `snippet.description`, and `snippet.tags` — those are handled by
  [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md) and the primary
  upload script.

***

## 6. Composition by Higher-Level Skills

| Composer Skill           | Composition Mechanism                                                                                       |
|--------------------------|-------------------------------------------------------------------------------------------------------------|
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | May call `scripts/video-snippet-update.py` as a post-upload correction step when the user requests a title/description/tags fix after the initial upload completes. |
| [`youtube-channel-video-organize`](../youtube-channel-video-organize/SKILL.md) | May call `scripts/video-snippet-update.py` during channel organization to standardize video titles and add consistent descriptions/tags across a batch. |

***

## 7. Composition Rationale

This skill is a **base** skill: it owns only the YouTube Data API v3 `videos.update` PATCH call for
snippet fields. It delegates all OAuth lifecycle management to
[`google-oauth-setup`](../google-oauth-setup/SKILL.md) and is itself composed by video upload and
channel organization workflows. Separating snippet update from upload and advanced metadata update
allows each to be reused independently (e.g., bulk title correction, automated description
generation pipeline).
