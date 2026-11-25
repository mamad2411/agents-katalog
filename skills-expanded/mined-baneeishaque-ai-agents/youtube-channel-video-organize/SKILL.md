---
name: youtube-channel-video-organize
description: 'COMPOSER: List all channel videos and playlists, let the agent categorize videos, then add them to the selected playlists. Delegates listing to youtube-channel-video-list and youtube-playlist-list; delegates assignment to youtube-playlist-item-add.'
category: YouTube / Composition
---

# YouTube Channel Video Organize Skill (v1)

This is a **composer** skill. It orchestrates the end-to-end workflow of organizing existing YouTube videos into topic-specific playlists. Delegates video listing to [`youtube-channel-video-list`](../youtube-channel-video-list/SKILL.md), playlist listing to [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md), playlist creation to [`youtube-playlist-create`](../youtube-playlist-create/SKILL.md), and video-to-playlist assignment to [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md). No component is re-invented — every sub-step delegates to the appropriate base skill.

***

## 1. Scope & Intent

- **In scope**: List all channel videos → list all playlists → agent categorizes videos → create missing playlists → add videos to playlists.
- **Out of scope**:
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Uploading videos (delegated to [`youtube-video-upload`](../youtube-video-upload/SKILL.md)).
    - Updating video metadata or settings.
    - Bulk deletion or reordering of playlist items.

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — orchestrator script uses `argparse`, `json`, `subprocess`, `pathlib`. Verify:

  ```bash
  python3 --version
  ```

- **`requests`** library (for base skill scripts). Verify:

  ```bash
  python3 -c "import requests; print('OK')"
  ```

### 2.2 Required Files

| File | Source |
|---|---|
| `client_secrets.json` | Google Cloud Console |
| OAuth credential cache (after setup) | [`google-oauth-setup`](../google-oauth-setup/SKILL.md) |

### 2.3 Required Skill Loading

Before executing this skill, the agent MUST load all SKILL.md files:

```text
google-oauth-setup/SKILL.md
youtube-channel-video-list/SKILL.md
youtube-playlist-list/SKILL.md
youtube-playlist-create/SKILL.md
youtube-playlist-item-add/SKILL.md
youtube-channel-video-organize/SKILL.md  (this file)
```

If any base skill's script is missing or fails, the agent MUST report the gap immediately — do not proceed.

***

## 3. Protocol

### 3.1 Step 1 — Ensure Valid Credentials

Delegate to [`google-oauth-setup`](../google-oauth-setup/SKILL.md) §3:

```bash
# Refresh if expired
python3 .agents/skills/google-oauth-setup/scripts/oauth-token-refresh.py \
  --client-secrets <client_secrets.json> \
  --credentials <credentials.json> \
  --output <credentials.json>
```

If the refresh fails, run the full PKCE flow:

```bash
python3 .agents/skills/google-oauth-setup/scripts/oauth-setup.py \
  --client-secrets <client_secrets.json> \
  --scopes "https://www.googleapis.com/auth/youtube" \
  --output <credentials.json>
```

### 3.2 Step 2 — List All Channel Videos

Delegate to [`youtube-channel-video-list`](../youtube-channel-video-list/SKILL.md) §3:

```bash
python3 .agents/skills/youtube-channel-video-organize/scripts/organize.py list-videos \
  --credentials <credentials.json>
```

Alternatively, call the base script directly:

```bash
python3 .agents/skills/youtube-channel-video-list/scripts/channel-video-list.py \
  --credentials <credentials.json> \
  --format json
```

The output is one JSON line per video. Present the list to the user and let them choose which videos to organize and which playlists they belong in.

### 3.3 Step 3 — List All Playlists

Delegate to [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) §3:

```bash
python3 .agents/skills/youtube-channel-video-organize/scripts/organize.py list-playlists \
  --credentials <credentials.json>
```

Alternatively:

```bash
python3 .agents/skills/youtube-playlist-list/scripts/list-playlists.py \
  --credentials <credentials.json>
```

### 3.4 Step 4 — Agent Categorization (Judgement)

The agent presents the video list and playlist list to the user. The user decides which videos belong in which playlists. For each desired assignment, note:

- The video ID (from Step 2)
- The playlist ID (from Step 3)

For videos that belong in a new playlist (no existing match), use [`youtube-playlist-create`](../youtube-playlist-create/SKILL.md) §3 to create it, then use the returned playlist ID in Step 5.

### 3.5 Step 5 — Create Assignment Mapping

Build a JSON mapping file with the user's decisions:

```json
{
  "assignments": [
    {"video_id": "v8M-tvdJV9I", "playlist_id": "PL1Bh2vwTl5j3K5TL7jBZzTkk7gHS48ElR"},
    {"video_id": "wSngIP_PR7k", "playlist_id": "PL1Bh2vwTl5j1d91zh4vLnZJe7aMS8EZYx"}
  ]
}
```

### 3.6 Step 6 — Execute Assignments

Delegate to the [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md) base skill via the orchestrator:

```bash
python3 .agents/skills/youtube-channel-video-organize/scripts/organize.py assign \
  --credentials <credentials.json> \
  --mapping <mapping.json>
```

The orchestrator calls `scripts/playlist-item-add.py` for each assignment:

```text
Adding v8M-tvdJV9I → PL1Bh2vwTl5j3K5TL7jBZzTkk7gHS48ElR ... OK
Adding wSngIP_PR7k → PL1Bh2vwTl5j1d91zh4vLnZJe7aMS8EZYx ... OK

Done: 2 succeeded, 0 failed.
```

If any assignment fails, the orchestrator reports which ones and exits 1.

***

## 4. Script Reference

### 4.1 `scripts/organize.py`

Orchestrator script with subcommands: `list-videos`, `list-playlists`, `assign`.

```text
python3 .agents/skills/youtube-channel-video-organize/scripts/organize.py <subcommand> [options]
```

Subcommands:

- **`list-videos`**: Delegates to `youtube-channel-video-list/scripts/channel-video-list.py --format json`. Outputs one JSON line per video.
- **`list-playlists`**: Delegates to `youtube-playlist-list/scripts/list-playlists.py`. Outputs the playlist listing table.
- **`assign`**: Takes a JSON mapping file (`--mapping`) and calls `youtube-playlist-item-add/scripts/playlist-item-add.py` for each entry. Reports per-assignment success/failure and exits 0 only if all succeed.

All scripts resolve relative paths anchored to their own location — invocation works regardless of the caller's `cwd`.

***

## 5. Edge Cases

- **Video already in playlist**: The API does not error on duplicates. The agent SHOULD check via [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) before adding.
- **Missing base script**: The orchestrator checks for each base script before executing. If a base script is missing, it exits with a clear error message.
- **Invalid mapping file**: If the mapping JSON is malformed or `assignments` is missing, the script exits 1 with a parse error.
- **Partial failure**: If some assignments succeed and some fail, the orchestrator reports counts for both and exits 1 for the overall result.
- **Quota**: Each `playlistItems.insert` call costs 50 units. For large organization tasks (>50 assignments), warn the user about quota consumption.
- **Empty channel or playlists**: If no videos or no playlists exist, inform the user and exit gracefully.

***

## 6. Prohibited Actions

- The agent MUST NOT re-implement the base skills' API calls in this skill's scripts — always delegate.
- The agent MUST NOT hardcode playlist IDs or video IDs — always derive from listing output and user choice.
- The agent MUST NOT modify video metadata or delete videos during organization.
- The agent MUST NOT reorganize without user confirmation of the mapping.

***

## 7. Composition Rationale

This skill is a **composer**: it owns the end-to-end video organization workflow but delegates every sub-step to base skills:

1. **[`youtube-channel-video-list`](../youtube-channel-video-list/SKILL.md)** — invoked FIRST via `scripts/channel-video-list.py --format json`. Produces the video inventory (JSON lines with video_id, title, published_at).
2. **[`youtube-playlist-list`](../youtube-playlist-list/SKILL.md)** — invoked SECOND via `scripts/list-playlists.py`. Produces the playlist inventory (ID, title, video count).
3. **[`youtube-playlist-create`](../youtube-playlist-create/SKILL.md)** — invoked (via its script) when no matching playlist exists for a category. Produces the new playlist ID.
4. **[`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md)** — invoked LAST via `scripts/playlist-item-add.py` for each assignment. Consumes video_id + playlist_id and confirms insertion.

The composer's domain-specific value-add over any base alone: it orchestrates the full lifecycle from inventory to assignment with a consistent credential path and sequential execution with per-assignment reporting. Inlining any base would duplicate logic that other YouTube workflows also consume.

Bidirectional discoverability: each base skill lists this composer in its `## Composition by Higher-Level Skills` table.
