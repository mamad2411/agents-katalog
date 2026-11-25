---
name: youtube-playlist-item-add
description: Add an existing video to a YouTube playlist via the Data API v3 — prints confirmation.
category: YouTube
---

# YouTube Playlist Item Add Skill (v1)

This is a **base** skill. It calls the YouTube Data API v3 `playlistItems.insert` endpoint to add an existing video to a playlist. Requires valid OAuth credentials obtained via [`google-oauth-setup`](../google-oauth-setup/SKILL.md). Reusable by any YouTube workflow needing to add videos to playlists (upload dual-playlist membership, channel organization, content migration).

***

## 1. Scope & Intent

- **In scope**: Authenticate via cached OAuth credentials, call `playlistItems.insert` with a video ID and playlist ID, print confirmation with the new playlist item ID.
- **Out of scope**:
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Creating, listing, updating, or deleting playlists.
    - Uploading videos (delegated to [`youtube-video-upload`](../youtube-video-upload/SKILL.md)).
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

Before adding a video to a playlist, verify the credential cache exists and the access token is valid. Delegate to [`google-oauth-setup`](../google-oauth-setup/SKILL.md):

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

### 3.2 Step 2 — Add Video to Playlist

```bash
python3 .agents/skills/youtube-playlist-item-add/scripts/playlist-item-add.py \
  <VIDEO_ID> \
  <PLAYLIST_ID> \
  --credentials <path>
```

#### 3.2.1 Arguments

| Argument | Required | Description |
|---|---|---|
| `video_id` | Yes (positional) | YouTube video ID (e.g., `v8M-tvdJV9I`). |
| `playlist_id` | Yes (positional) | Target playlist ID (e.g., `PL1Bh2vwTl5j3K5TL7jBZzTkk7gHS48ElR`). |
| `--credentials` | Yes | Path to OAuth credential cache JSON (must contain `access_token`). |

### 3.3 Step 3 — Interpret Output

The script prints:

```text
Added: https://youtu.be/v8M-tvdJV9I to playlist PL1Bh2vwTl5j3K5TL7jBZzTkk7gHS48ElR (item ID: UExXRUxUTU5hNlpTd...)
```

Confirm the video URL and playlist ID are correct. The item ID is an internal identifier for the playlist entry.

***

## 4. Script Reference

### 4.1 `scripts/playlist-item-add.py`

Add an existing video to a YouTube playlist.

```text
python3 .agents/skills/youtube-playlist-item-add/scripts/playlist-item-add.py \
  <VIDEO_ID> <PLAYLIST_ID> \
  --credentials <path>
```

The script:

1. Loads credentials JSON and validates required fields.
2. Builds the request body with `snippet.playlistId` and `snippet.resourceId.videoId`.
3. Calls `POST https://www.googleapis.com/youtube/v3/playlistItems?part=snippet`.
4. On success, prints confirmation with the video URL, playlist ID, and playlist item ID.
5. On failure (auth error, network error, duplicate), prints diagnostic and exits 1.

***

## 5. Edge Cases

- **401 Unauthorized**: Access token is expired or invalid. Run `oauth-token-refresh.py` from [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and retry.
- **403 Forbidden**: The OAuth scope does not include YouTube. Re-run `oauth-setup.py` with `--scopes "https://www.googleapis.com/auth/youtube"`.
- **Video already in playlist**: YouTube silently allows duplicates. The API does not return an error for duplicate playlist items. The agent MUST check manually using [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) or a playlist items query before adding.
- **Invalid video ID**: The API returns 400 if the video ID does not exist. The script exits 1.
- **Invalid playlist ID**: The API returns 404 if the playlist ID does not exist or belongs to another user. The script exits 1.
- **Brand account playlists**: If the authenticated user manages multiple channels, the credentials may not have access to the target playlist. Verify the playlist belongs to the authenticated channel.
- **Quota**: Each `playlistItems.insert` call costs 50 quota units (YouTube Data API v3).

***

## 6. Prohibited Actions

- The agent MUST NOT add a video to a playlist without user confirmation of the playlist ID and video ID.
- The agent MUST NOT hardcode a playlist ID — always present options and let the user choose.
- The agent MUST NOT skip the credential refresh step.
- The agent MUST NOT determine multi-playlist membership policy — that decision belongs to the composer
  skill. A video CAN be in multiple playlists; the base skill accepts whatever video_id + playlist_id pair
  it is given and inserts it. The composer orchestrates how many playlists a video joins.

***

## 7. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|---|---|
| [`youtube-channel-video-organize`](../youtube-channel-video-organize/SKILL.md) | Calls `scripts/playlist-item-add.py` for every video-to-playlist assignment during the organization workflow; processes videos sequentially. |
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | Calls `scripts/playlist-item-add.py` (or equivalent API call) after upload to implement dual-playlist membership — adds to both topic-specific playlist and org-wide playlist. |

***

## 8. Related Skills

- [`youtube-video-snippet-update`](../youtube-video-snippet-update/SKILL.md) — base skill for updating video title/description/tags (often paired with playlist item add in backfill workflows).

## 9. Composition Rationale

This skill is a **base** skill: it owns only the YouTube playlist item insertion API call. It delegates all OAuth lifecycle management to [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and is itself composed by video upload and channel organization workflows. Separating playlist item insertion from upload and organization allows each to be reused independently (e.g., bulk playlist migration, adding multiple videos to a playlist).
