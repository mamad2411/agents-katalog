---
name: youtube-playlist-create
description: Create a YouTube playlist via the Data API v3 — prints the new playlist ID.
category: YouTube
---

# YouTube Playlist Create Skill (v1)

This is a **base** skill. It calls the YouTube Data API v3 `playlists.insert` endpoint to create a new playlist with a given title, description, and privacy status. Requires valid OAuth credentials obtained via [`google-oauth-setup`](../google-oauth-setup/SKILL.md). Reusable by any YouTube workflow needing playlist creation (upload, content organization, channel management).

***

## 1. Scope & Intent

- **In scope**: Authenticate via cached OAuth credentials, call `playlists.insert` with title, description, and privacy status, print the new playlist ID.
- **Out of scope**:
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Listing, updating, or deleting playlists.
    - Adding videos to a playlist (delegated to [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md)).
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

Before creating a playlist, verify the credential cache exists and the access token is valid. Delegate to [`google-oauth-setup`](../google-oauth-setup/SKILL.md):

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

### 3.2 Step 2 — Create Playlist

```bash
python3 .agents/skills/youtube-playlist-create/scripts/playlist-create.py \
  --credentials <path> \
  --title "<Playlist Title>" \
  --description "<Description>" \
  --privacy private
```

#### 3.2.1 Flag Breakdown

| Argument | Required | Description |
|---|---|---|
| `--credentials` | Yes | Path to OAuth credential cache JSON (must contain `access_token`). |
| `--title` | Yes | Playlist title. |
| `--description` | No | Playlist description (default: empty). |
| `--privacy` | No | `private`, `unlisted`, or `public` (default: `private`). |

### 3.3 Step 3 — Interpret Output

The script prints the new playlist ID on stdout:

```text
PL1Bh2vwTl5j3K5TL7jBZzTkk7gHS48ElR
```

Capture this ID for subsequent operations (e.g., adding videos to the playlist via [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md)).

***

## 4. Script Reference

### 4.1 `scripts/playlist-create.py`

Create a YouTube playlist and print the new playlist ID.

```text
python3 .agents/skills/youtube-playlist-create/scripts/playlist-create.py \
  --credentials <path> \
  --title "<Title>" \
  [--description "<Description>"] \
  [--privacy private]
```

The script:

1. Loads credentials JSON and validates required fields.
2. Builds the request body with `snippet.title`, `snippet.description`, and `status.privacyStatus`.
3. Calls `POST https://www.googleapis.com/youtube/v3/playlists?part=snippet,status`.
4. On success, prints the new playlist ID and exits 0.
5. On failure (auth error, network error), prints diagnostic and exits 1.

***

## 5. Edge Cases

- **401 Unauthorized**: Access token is expired or invalid. Run `oauth-token-refresh.py` from [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and retry.
- **403 Forbidden**: The OAuth scope does not include YouTube. Re-run `oauth-setup.py` with `--scopes "https://www.googleapis.com/auth/youtube"`.
- **Duplicate title**: YouTube allows multiple playlists with the same title. The script does not check for duplicates. Use [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) first to verify the title does not already exist.
- **Title length**: YouTube limits playlist titles to 150 characters. The script does not validate this server-side limit.
- **Privacy mismatch**: Some brand accounts may restrict `unlisted` or `public` privacy. Use `private` by default.

***

## 6. Prohibited Actions

- The agent MUST NOT hardcode a playlist title or description — always ask the user.
- The agent MUST NOT create a playlist without user confirmation of the title and description.
- The agent MUST NOT skip the credential refresh step — a stale token will return 401.

***

## 7. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|---|---|
| [`youtube-channel-video-organize`](../youtube-channel-video-organize/SKILL.md) | Calls `scripts/playlist-create.py` during its categorization step when no matching playlist exists; captures the playlist ID for subsequent playlist-item-add calls. |
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | (Optional) May call `scripts/playlist-create.py` when the user wants to upload to a new topic-specific playlist that does not yet exist. |

***

## 8. Composition Rationale

This skill is a **base** skill: it owns only the YouTube playlist-creation API call. It delegates all OAuth lifecycle management to [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and is itself composed by video upload and channel organization workflows. Separating playlist creation from listing and item-add allows each operation to be reused independently.
