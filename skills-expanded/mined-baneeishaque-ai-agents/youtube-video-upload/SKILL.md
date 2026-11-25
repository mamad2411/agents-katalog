---
name: youtube-video-upload
description: Upload a video to YouTube with maximum metadata — delegate pre-processing, OAuth, playlist listing, and post-upload verification to base skills; orchestrate via YouTube Data API v3.
category: YouTube / Composition
---

# YouTube Video Upload Skill (v1)

This is a **composer** skill. It orchestrates video pre-processing (verification, metadata extraction via ffprobe), OAuth credential lifecycle, playlist selection, and YouTube upload into a single workflow. Delegates authentication to [`google-oauth-setup`](../google-oauth-setup/SKILL.md), playlist listing to [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md), and upload execution to the YouTube Data API v3 via `googleapiclient`. No component is re-invented — every sub-step delegates to the appropriate base skill.

***

## 1. Scope & Intent

- **In scope**: End-to-end YouTube video upload: verify video file → ensure valid OAuth → optionally list and select a playlist → upload with full metadata (title, description, tags, privacy, language, recording date, notifySubscribers, containsSyntheticMedia) via YouTube Data API v3 → verify upload succeeded → create URL shortcut file → cleanup source file.
- **Out of scope**:
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Playlist management CRUD (delegated to [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) for listing; no create/update/delete).
    - Video transcoding or format conversion.
    - Bulk uploads.
    - Managing monetization or content ID.

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — orchestrator scripts use `argparse`, `json`, `subprocess`, `os.path`, `datetime`. Verify:

  ```bash
  python3 --version
  ```

- **`ffprobe`** — for video metadata extraction (duration, resolution, codec). Verify:

  ```bash
  ffprobe -version
  ```

- **`google-api-python-client`** — for YouTube Data API v3 resumable upload. Verify:

  ```bash
  python3 -c "import googleapiclient; print('OK')"
  ```

  Install if missing:

  ```bash
  pip install --upgrade google-api-python-client httplib2 oauth2client
  ```

### 2.2 Required Files

| File | Source |
|---|---|
| Video file (`.mp4`, `.webm`, `.mkv`, `.mov`) | User-provided |
| `client_secrets.json` | Google Cloud Console |
| OAuth credential cache (after setup) | [`google-oauth-setup`](../google-oauth-setup/SKILL.md) |

### 2.3 Required Skill Loading

Before executing this skill, the agent MUST load all SKILL.md files:

```
google-oauth-setup/SKILL.md
youtube-playlist-list/SKILL.md
youtube-video-snippet-update/SKILL.md
youtube-video-metadata-update/SKILL.md
media-audio-language-detect/SKILL.md
url-shortcut-creator/SKILL.md
youtube-studio-settings/SKILL.md
youtube-video-upload/SKILL.md  (this file)
```

If any base skill's script is missing or fails, the agent MUST report the gap immediately — do not proceed.

***

## 3. Protocol

### 3.1 Step 1 — Pre-processing

```bash
python3 .agents/skills/youtube-video-upload/scripts/upload-video.py verify \
  --video <path>
```

The script:

1. Verifies the video file exists and has non-zero size.
2. Runs `ffprobe` to extract duration, resolution, codec, file size.
3. Prints a summary. Warns if duration > 12 hours or file size > 256 GB (YouTube upload limits).
4. Exits 0 if valid, 1 if the file is missing, empty, or corrupt.

### 3.2 Step 2 — Ensure Valid OAuth Credentials

Delegate to [`google-oauth-setup`](../google-oauth-setup/SKILL.md) §3:

```bash
# Attempt refresh first
python3 .agents/skills/google-oauth-setup/scripts/oauth-token-refresh.py \
  --client-secrets <client_secrets.json> \
  --credentials <credentials.json> \
  --output <credentials.json>
```

If that fails (invalid_grant), run the full PKCE flow:

```bash
python3 .agents/skills/google-oauth-setup/scripts/oauth-setup.py \
  --client-secrets <client_secrets.json> \
  --scopes "https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.upload" \
  --output <credentials.json>
```

The `oauth-setup.py` script writes credentials in the `oauth2client` legacy format (`access_token`, `refresh_token`, `client_id`, `client_secret`, `token_uri`, `scopes`) which is compatible with `googleapiclient`.

### 3.3 Step 3 — List & Select Playlist (Optional)

If the user wants to upload to a specific playlist, delegate to [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) §3:

```bash
python3 .agents/skills/youtube-playlist-list/scripts/list-playlists.py \
  --credentials <credentials.json>
```

Present the list to the user and let them choose. After the upload succeeds (Step 5), the video will be added to the chosen playlist via `--playlist-id` (see §3.5).

### 3.4 Step 4 — Auto-Detect Audio Language (Optional)

If the user did not specify `--language`, delegate to [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) §3 before upload:

```bash
python3 .agents/skills/media-audio-language-detect/scripts/detect-audio-language.py \
  --video <path> \
  --format json
```

Parse the `language_code` from the JSON output and pass it as `--language` to the upload script (Step 5).

### 3.5 Step 5 — Upload

```bash
python3 .agents/skills/youtube-video-upload/scripts/upload-video.py upload \
  --video <path> \
  --client-secrets <client_secrets.json> \
  --credentials <credentials.json> \
  --title "<Title>" \
  --description "<Description>" \
  --tags "tag1 tag2" \
  --language "<BCP-47>" \
  --recording-date "<ISO-8601>" \
  [--privacy "private"] \
  [--no-notify-subscribers] \
  [--contains-synthetic-media] \
  [--playlist-id "<PLAYLIST_ID_1>"] \
  [--playlist-id "<PLAYLIST_ID_2>"] \
  [...] \
  [--output "<output-file>"]
```

The orchestrator script uses `googleapiclient` to call the YouTube Data API v3 `videos.insert` endpoint with a resumable upload. Progress is reported via `next_chunk()` — the script prints live percentage updates by polling the upload status after each chunk. If `--playlist-id` is provided, the script adds the video to the specified playlist after upload completes.

#### 3.5.1 Arguments

| Argument | Required | Description |
|---|---|---|
| `--video` | Yes | Path to the video file |
| `--client-secrets` | Yes | Path to Google Cloud `client_secrets.json` |
| `--credentials` | Yes | Path to OAuth credential cache |
| `--title` | Yes | Video title |
| `--description` | Yes | Video description |
| `--tags` | No | Space-separated tags (e.g. `--tags tag1 tag2`) |
| `--language` | Recommended | BCP-47 language tag (e.g. `en`, `en-US`) |
| `--recording-date` | Recommended | ISO-8601 recording date (e.g. `2026-06-14`) |
| `--privacy` | No | `private`, `unlisted`, `public` (default: `private`) |
| `--notify-subscribers` / `--no-notify-subscribers` | No | Notify subscribers (default: `--notify-subscribers`). Use `--no-notify-subscribers` to suppress. |
| `--contains-synthetic-media` | No | Flag: set `containsSyntheticMedia` = true (AI-generated content disclosure) |
| `--playlist-id` | No | Repeatable flag. Playlist ID(s) to add the video to after upload. May be specified multiple times for multi-playlist membership. Supply IDs from Step 3. |
| `--output` | No | Save upload output (video URL) to file for post-upload verification |

### Step 5a — Add to Playlist (Optional)

If `--playlist-id` was not provided during upload, delegate to [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md) to add the already-uploaded video to the playlist:

```bash
python3 .agents/skills/youtube-playlist-item-add/scripts/playlist-item-add.py \
  <VIDEO_ID> <PLAYLIST_ID> \
  --credentials <credentials.json>
```

Use the **playlist ID** (from Step 3 output), not the title.

#### Multi-Playlist Membership

The script natively supports adding a video to multiple playlists in a single upload call. Pass each playlist ID as a separate `--playlist-id` flag:

```bash
python3 .agents/skills/youtube-video-upload/scripts/upload-video.py upload \
  --video <path> \
  ... \
  --playlist-id "<FIRST_PLAYLIST_ID>" \
  --playlist-id "<SECOND_PLAYLIST_ID>"
```

The script iterates over all supplied playlist IDs and calls `playlistItems.insert` for each. No separate [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md) call is needed when using multi-`--playlist-id`.

Use a separate [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md) call only when adding an ALREADY-UPLOADED video to an additional playlist discovered after upload (e.g., backfill).

### 3.6 Step 6 — Post-Upload Metadata Update

After the upload succeeds, delegate to [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md) §3 for fields not set during upload:

```bash
python3 .agents/skills/youtube-video-metadata-update/scripts/video-metadata-update.py \
  <VIDEO_ID> \
  --client-secrets <client_secrets.json> \
  --credentials <credentials.json> \
  --category-id "28" \
  --language "en" \
  [--embeddable] \
  [--public-stats] \
  [--contains-synthetic-media] \
  [--age-restricted]
```

Supported fields: category, embeddable, madeForKids, license, language, publicStatsViewable, containsSyntheticMedia, age restriction. See the skill's docs for a full list and the Studio-only caveats.

For silent recordings (`language_code = "silent"` from [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md)), omit `--audio-language` — the video has no spoken content. Set only `--language` for metadata display language.

If the user requests a title, description, or tags change after upload, delegate to [`youtube-video-snippet-update`](../youtube-video-snippet-update/SKILL.md) §3 instead:

```bash
python3 .agents/skills/youtube-video-snippet-update/scripts/video-snippet-update.py \
  <VIDEO_ID> \
  --credentials <credentials.json> \
  --title "<New Title>" \
  [--description "<New Description>"] \
  [--tags "tag1 tag2"]
```

Title is limited to 100 characters by the YouTube Data API. The snippet update skill handles only title/description/tags — all other post-upload metadata fields remain with [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md).

### 3.7 Step 7 — Post-Upload Verification

```bash
python3 .agents/skills/youtube-video-upload/scripts/upload-video.py verify-upload \
  --output <upload-output-file>
```

The script:

1. Parses the last line of the upload output for a `youtube.com/watch?v=` URL.
2. If the URL pattern is found, prints the URL and exits 0 (verified).
3. If no URL is found, prints a warning and exits 1.
4. Does NOT call the YouTube Data API — this is a lightweight text-based check confirming the upload produced a video URL.

### 3.8 Step 8 — Create URL Shortcut File

After verification succeeds, delegate to [`url-shortcut-creator`](../url-shortcut-creator/SKILL.md) §3 to create a clickable `.html` shortcut to the YouTube video:

```bash
python3 .agents/skills/url-shortcut-creator/scripts/create-url-shortcut.py \
  --url "<video-url>" \
  --name "<video-filename-without-ext>" \
  --output-dir "<output-directory>"
```

The script prints the path to the created `.html` file. Present this path to the user so they know where the shortcut lives.

### 3.9 Step 9 — Apply Studio-Only Settings (Optional)

After upload and verification, ask the user if they want to apply Studio-only settings (comments off, 18+ age restriction, disable subscriber feed, disable remixing, caption certification). These cannot be set via the Data API and require browser automation via layered backends (JXA on macOS, undetected_chromedriver cross-platform, Playwright stealth as fallback). Run the one-time setup first if not already done (see below).

Before the first use, run the one-time setup script to create the persistent Chrome profile and enable JXA automation on macOS:

```bash
bash .agents/skills/youtube-studio-settings/scripts/studio-settings--setup.bash
```

If the user agrees, delegate to [`youtube-studio-settings`](../youtube-studio-settings/SKILL.md) §3:

```bash
python3 .agents/skills/youtube-studio-settings/scripts/studio-settings.py \
  <VIDEO_ID> \
  [--comments-off] \
  [--age-restrict-18plus] \
  [--no-subscriber-feed] \
  [--no-remixing] \
  [--caption-cert-not-aired-us] \
  [--backend {auto,jxa,undetected,stealth}] \
  [--dump]
```

The orchestrator auto-selects the best backend (macOS → JXA → undetected → stealth; other → undetected → stealth). JXA controls your real Chrome with zero detection risk using your existing session. Other backends launch Chrome with the persistent profile at `~/.cache/studio-chrome-profile/`. If not logged in, the browser shows the login page — log in and the script continues. Use `--dump` to verify current settings without making changes.

### 3.10 Step 10 — Cleanup Source File

After the URL shortcut is created, ask the user whether they want to delete the original source video file. The agent MUST NOT delete without explicit user confirmation.

If the user confirms, delete the file and report the freed space.

***

## 4. Script Reference

### 4.1 `scripts/upload-video.py`

Main orchestrator script with subcommands: `verify`, `upload`, `verify-upload`.

```
python3 .agents/skills/youtube-video-upload/scripts/upload-video.py <subcommand> [options]
```

Subcommands:

- **`verify`**: Validates the video file exists, has non-zero size, and extracts metadata via `ffprobe`. Prints a summary. Use before upload to confirm the file is valid.
- **`upload`**: Uploads the video via YouTube Data API v3 `videos.insert` with a resumable upload. Requires `--video`, `--credentials`, `--title`, `--description`. Optionally accepts `--tags`, `--language`, `--recording-date`, `--playlist-id`, `--privacy`, `--notify-subscribers`, `--contains-synthetic-media`, `--output`. Outputs the resulting YouTube video URL (`https://youtu.be/{id}`).
- **`verify-upload`**: Confirms the video was uploaded by parsing the last line of the upload output for a YouTube URL. This is a lightweight text-based check — does NOT call the YouTube Data API. Reads the upload output file and checks for a `youtube.com/watch?v=` pattern.

***

## 5. YouTube Studio Limitations

The following fields CANNOT be set via API and require browser automation ([`youtube-studio-settings`](../youtube-studio-settings/SKILL.md)) or manual configuration in YouTube Studio:

| Field | Studio Location |
|---|---|
| Age restriction (advanced) | YouTube Studio → Content → video → Advanced |
| Comments off | YouTube Studio → Comments |
| Don't publish to subscriber feed | YouTube Studio → Advanced |
| Don't allow remixing | YouTube Studio → Video details |
| Caption certification (never aired in US) | YouTube Studio → Advanced → Caption certification |

The agent MUST offer to apply these settings via [`youtube-studio-settings`](../youtube-studio-settings/SKILL.md) after upload completes (§3.9).

***

## 6. Edge Cases

- **Upload interrupted (network, timeout)**: The YouTube Resumable Upload Protocol supports resumption. The agent SHOULD NOT retry automatically — instead, report the failure and let the user decide.
- **Quota exceeded**: YouTube API has a daily upload quota (typically 10,000 units). The script catches `HttpError` with `reason == "quotaExceeded"` and reports it clearly.
- **Invalid credentials**: If credentials are expired or invalid, the script exits with an instruction to run `oauth-setup.py`. Use the refresh step (§3.2) first.
- **Duplicate uploads**: The script does not prevent re-uploading the same video. The agent MUST ask the user whether they intend to re-upload (e.g. as an unlisted re-edit) rather than assuming.
- **Playlist ID required**: The playlist listing (Step 3) outputs both playlist ID and title. When adding to a playlist via `--playlist-id` (Step 5), use the **playlist ID** (not the title). The ID is the first column of the playlist listing output.
- **Language detection returns "unknown"**: When [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) returns `"unknown"`, the agent MUST follow the deterministic volume analysis protocol documented in `media-audio-language-detect/SKILL.md` §4 Edge Cases to determine whether the video is a silent recording or has unrecognized audio. Do NOT set `defaultAudioLanguage` for silent recordings.

***

## 7. Prohibited Actions

- The agent MUST NOT embed YouTube OAuth client secrets or token values in markdown files or script source.
- The agent MUST NOT use the `youtube-upload` CLI (tokland) for uploads — use the Data API v3 via `scripts/upload-video.py` instead.
- The agent MUST NOT upload videos without user confirmation of the metadata summary.
- The agent MUST NOT modify the video file (transcoding, re-encoding, metadata injection) — this is a pure upload skill.
- The agent MUST NOT assume the user wants `public` privacy — default to `private` unless explicitly asked.

***

## 8. Composition Reference

Project-specific composers in separate organization-private repos may wrap this skill with
org conventions. Such composers reference this skill by name only (per the redaction-portability
protocol for cross-repo references).

| Base / Support Skill | Usage | Composition Mechanism |
|---|---|---|---|
| [`google-oauth-setup`](../google-oauth-setup/SKILL.md) | OAuth credential lifecycle | Calls `scripts/oauth-setup.py` or `scripts/oauth-token-refresh.py` before upload; passes credential cache path to upload |
| [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) | Playlist selection | Calls `scripts/list-playlists.py` when user wants a playlist; passes chosen playlist ID as `--playlist-id` to the upload script |
| [`youtube-playlist-update`](../youtube-playlist-update/SKILL.md) | Playlist rename | (Optional) Calls `scripts/playlist-update.py` during playlist setup when user needs to rename an existing playlist before upload |
| [`youtube-playlist-create`](../youtube-playlist-create/SKILL.md) | Playlist creation | (Optional) Calls `scripts/playlist-create.py` when the user wants to upload to a new topic-specific playlist that does not yet exist; captures the new playlist ID for the upload |
| [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md) | Dual-playlist membership | (Optional) Calls `scripts/playlist-item-add.py` after upload to add the video to a second playlist (e.g., org-wide playlist) when dual-playlist membership is desired |
| [`youtube-video-snippet-update`](../youtube-video-snippet-update/SKILL.md) | Post-upload snippet correction | (Optional) Calls `scripts/video-snippet-update.py` after upload when the user needs to fix the title, description, or tags of an already-uploaded video |
| [`ffmpeg-lossless-concat`](../ffmpeg-lossless-concat/SKILL.md) | Pre-upload video merging | (Optional) When the user needs to merge video segments before upload |
| [`webm-recording-merge-with-filler`](../webm-recording-merge-with-filler/SKILL.md) | Segmented recording merge | (Optional) When the user needs to merge partitioned recordings before upload |
| [`lower-case-hyphen-naming`](../lower-case-hyphen-naming/SKILL.md) | File naming standardization | (Optional) Rename files to kebab-case before upload for consistent naming |
| [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md) | Post-upload metadata | Calls `scripts/video-metadata-update.py` after upload to set fields not configured during initial upload |
| [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) | Language auto-detection | Calls `scripts/detect-audio-language.py` during pre-processing when `--language` not provided |
| [`url-shortcut-creator`](../url-shortcut-creator/SKILL.md) | Post-upload URL shortcut | Calls `scripts/create-url-shortcut.py` after verification to create a clickable `.html` shortcut to the YouTube video |
| [`youtube-studio-settings`](../youtube-studio-settings/SKILL.md) | Studio-only settings | Calls `scripts/studio-settings.py` after verification to apply settings not available via API (comments, age restriction, subscriber feed, remixing, caption certification) using layered browser automation backends |

***

## 9. Composition Rationale

This skill is a **composer**: it owns the end-to-end upload workflow but delegates every meaningful sub-step to base skills. The key design principles are:

- **OAuth is not re-implemented** — [`google-oauth-setup`](../google-oauth-setup/SKILL.md) handles all token lifecycle logic; this skill simply calls its scripts.
- **Playlist listing is not re-implemented** — [`youtube-playlist-list`](../youtube-playlist-list/SKILL.md) owns the API query; this skill consumes its output.
- **Video processing is not re-implemented** — pre-processing only validates the file; actual merging/transcoding is delegated to the appropriate `ffmpeg`-based skills.
- **Upload uses Data API v3 directly** — Uses `googleapiclient` to call `videos.insert` with resumable upload, replacing the previous `youtube-upload` CLI dependency. This gives full control over all API parameters including `notifySubscribers` and `containsSyntheticMedia`.
- **Metadata update is not re-implemented** — [`youtube-video-metadata-update`](../youtube-video-metadata-update/SKILL.md) owns the Data API v3 patch call; this skill delegates post-upload field updates to it.
- **Language detection is not re-implemented** — [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) handles the SpeechRecognition + Google Web Speech API call; this skill consumes its output if the user did not specify a language.
- **URL shortcut creation is not re-implemented** — [`url-shortcut-creator`](../url-shortcut-creator/SKILL.md) owns the HTML redirect file generation; this skill delegates post-upload shortcut creation to it.
- **Studio-only settings are not re-implemented** — [`youtube-studio-settings`](../youtube-studio-settings/SKILL.md) owns the layered browser automation backends (JXA, undetected_chromedriver, Playwright stealth) for settings the API cannot touch; this skill delegates post-upload Studio configuration to it.
- **Cleanup is a user-gated step** — the source file is only deleted after explicit user confirmation.

- **Playlist creation is not re-implemented** — [`youtube-playlist-create`](../youtube-playlist-create/SKILL.md) owns the `playlists.insert` API call; this skill optionally delegates to it when the user wants to upload to a new playlist.
- **Playlist item addition is not re-implemented** — [`youtube-playlist-item-add`](../youtube-playlist-item-add/SKILL.md) owns the `playlistItems.insert` API call; this skill delegates dual-playlist membership to it.

This separation means each skill can be tested, updated, and composed independently. Adding a new upload destination (e.g. Vimeo) would require a new composer and new base skills, without modifying existing YouTube skills.
