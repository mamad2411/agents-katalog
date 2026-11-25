---
name: youtube-playlist-list
description: List authenticated user's YouTube playlists via the Data API v3 — prints playlist ID, title, and video count.
category: YouTube
---

# YouTube Playlist List Skill (v1)

This is a **base** skill. It queries the YouTube Data API v3 `playlists.list?part=snippet,contentDetails&mine=true` endpoint and outputs a tabular listing of the authenticated user's playlists. Requires valid OAuth credentials obtained via [`google-oauth-setup`](../google-oauth-setup/SKILL.md). Reusable by any YouTube workflow needing playlist selection (upload, analytics, content migration).

***

## 1. Scope & Intent

- **In scope**: Authenticate via cached OAuth credentials, call `playlists.list` with `mine=true`, print a table of playlist ID + title + video count.
- **Out of scope**:
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Creating, updating, or deleting playlists.
    - Querying playlist contents (videos within a playlist).
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

- **`google-api-python-client`** (optional) — if using the Google client library instead of raw HTTP. Verify:

  ```bash
  python3 -c "from googleapiclient.discovery import build; print('OK')"
  ```

### 2.2 Required Files

| File | Source |
|---|---|
| Valid OAuth credential cache (with `access_token`) | [`google-oauth-setup`](../google-oauth-setup/SKILL.md) §3 |

***

## 3. Protocol

### 3.1 Step 1 — Ensure Valid Credentials

Before listing playlists, verify the credential cache exists and the access token is valid. Delegate to [`google-oauth-setup`](../google-oauth-setup/SKILL.md):

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

### 3.2 Step 2 — List Playlists

```bash
python3 .agents/skills/youtube-playlist-list/scripts/list-playlists.py \
  --credentials <path>
```

The script:

1. Reads the credential cache and extracts the `access_token`.
2. Calls `GET https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&mine=true&maxResults=50` with `Authorization: Bearer <token>`.
3. Prints a tabular listing: `PLAYLIST_ID  |  TITLE  |  VIDEO_COUNT`.
4. Exits 0 on success, 1 on failure (auth error, network error, empty result).

#### 3.2.1 Flag Breakdown

| Argument | Purpose |
|---|---|
| `--credentials` | Path to OAuth credential cache JSON (must contain `access_token`). |

### 3.3 Step 3 — Interpret Output

Example output:

```
PL1Bh2vwTl5j1d91zh4vLnZJe7aMS8EZYx  |  Oleovista Technologies  |  13 videos
PL1Bh2vwTl5j2QqDUPiyctVmwvVw8s7WcM  |  TVK  |  1 videos
```

The user selects a playlist by its title or ID. The agent MUST NOT assume a specific playlist exists — always present the list and ask the user to choose.

***

## 4. Script Reference

### 4.1 `scripts/list-playlists.py`

Query YouTube playlists and print tabular output.

```
python3 .agents/skills/youtube-playlist-list/scripts/list-playlists.py \
  --credentials <path>
```

The script:

1. Loads credentials JSON and validates required fields.
2. Calls the YouTube Data API v3 playlists endpoint.
3. Iterates over `response["items"]` and prints each playlist as `ID  |  TITLE  |  N videos`.
4. Handles pagination via `nextPageToken` (fetches up to 50 per page, no limit).
5. Exits 0 on success, 1 if the API returns an error.

***

## 5. Edge Cases

- **401 Unauthorized**: Access token is expired or invalid. Run `oauth-token-refresh.py` from [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and retry.
- **403 Forbidden**: The OAuth scope does not include YouTube. Re-run `oauth-setup.py` with `--scopes "https://www.googleapis.com/auth/youtube"`.
- **Empty playlist list**: The user has no playlists. Inform the user and offer to create one or upload without a playlist.
- **Pagination**: If the user has > 50 playlists, the script follows `nextPageToken` automatically.
- **`--playlist-id` requires a playlist ID, not a title**: When adding a video to a playlist after upload, use the **playlist ID** (the first column of this skill's output). The playlist ID is stable — unlike titles, it never changes due to renames.

***

## 6. Prohibited Actions

- The agent MUST NOT hardcode a playlist ID or name — always present the list and let the user choose.
- The agent MUST NOT skip the credential refresh step — a stale token will return 401.

***

## 7. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|---|---|
| [`youtube-channel-video-organize`](../youtube-channel-video-organize/SKILL.md) | Calls `scripts/list-playlists.py` during its Step 3 (list playlists); the agent categorizes videos and the orchestrator passes playlist IDs to `youtube-playlist-item-add` for each assignment. |
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | Calls `scripts/list-playlists.py` during its pre-processing step; the user chooses a playlist, and the composer passes the playlist **ID** to the upload script as `--playlist-id`. |

***

## 8. Composition Rationale

This skill is a **base** skill: it owns only the YouTube playlist-listing API call. It delegates all OAuth lifecycle management to [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and is itself composed by [`youtube-video-upload`](../youtube-video-upload/SKILL.md) for the upload workflow. Separating playlist listing from upload allows reuse by other YouTube workflows (e.g. bulk playlist audit, content migration, analytics).
