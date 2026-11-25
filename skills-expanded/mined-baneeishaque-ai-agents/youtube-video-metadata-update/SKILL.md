---
name: youtube-video-metadata-update
description: Update advanced YouTube video metadata via Data API v3 — category, embeddable, madeForKids, license, language, publicStatsViewable, containsSyntheticMedia, and age restriction.
category: YouTube
---

# YouTube Video Metadata Update Skill (v1)

This is a **base** skill. It updates YouTube video metadata fields that are not supported during the initial upload via the Data API v3 `videos.insert`, using the `videos.update` endpoint. It requires existing OAuth credentials obtained via [`google-oauth-setup`](../google-oauth-setup/SKILL.md).

***

## 1. Scope & Intent

- **In scope**: Update `snippet.categoryId`, `snippet.defaultLanguage`, `snippet.defaultAudioLanguage`, `status.selfDeclaredMadeForKids`, `status.embeddable`, `status.license`, `status.publicStatsViewable`, `status.containsSyntheticMedia`, `contentDetails.contentRating.ytRating` (age restriction).
- **Out of scope**:
    - Uploading videos (delegated to [`youtube-video-upload`](../youtube-video-upload/SKILL.md)).
    - OAuth token management (delegated to [`google-oauth-setup`](../google-oauth-setup/SKILL.md)).
    - Fields that require YouTube Studio (comments, subscriber notifications, remixing, advanced age restriction, caption certification) — documented in §5.

***

## 2. Environment & Dependencies

### 2.1 Runtime

- **Python 3.12+** — scripts use `argparse`, `json`, `httplib2`, `oauth2client`, `googleapiclient`. Verify:
  ```bash
  python3 --version
  ```
- **`google-api-python-client`**, **`oauth2client`**, **`httplib2`** — Verify:
  ```bash
  python3 -c "import googleapiclient, oauth2client, httplib2; print('OK')"
  ```

### 2.2 Required Files

| File | Source |
|---|---|
| Valid OAuth credential cache | [`google-oauth-setup`](../google-oauth-setup/SKILL.md) |
| `client_secrets.json` | Google Cloud Console |

***

## 3. Protocol

### 3.1 Step 1 — Ensure Valid Credentials

```bash
python3 .agents/skills/google-oauth-setup/scripts/oauth-token-refresh.py \
  --client-secrets <client_secrets.json> \
  --credentials <credentials.json> \
  --output <credentials.json>
```

### 3.2 Step 2 — Update Video Metadata

```bash
python3 .agents/skills/youtube-video-metadata-update/scripts/video-metadata-update.py \
  <VIDEO_ID> \
  --client-secrets <path> \
  --credentials <path> \
  [--category-id "28"] \
  [--language "en"] \
  [--audio-language "ml"] \
  [--made-for-kids] \
  [--embeddable] \
  [--public-stats] \
  [--license "youtube"] \
  [--contains-synthetic-media] \
  [--age-restricted]
```

#### 3.2.1 Arguments

| Argument | Required | Description |
|---|---|---|
| `video_id` | Yes | YouTube video ID (positional) |
| `--client-secrets` | Yes | Path to `client_secrets.json` |
| `--credentials` | Yes | Path to OAuth credential cache |
| `--category-id` | No | YouTube category ID (default: `28` = Science & Technology) |
| `--language` | No | BCP-47 language tag for **metadata** (title/description display language; default: `en`) |
| `--audio-language` | No | BCP-47 language tag for **audio** (default: same as `--language`). Use when metadata language differs from spoken language (e.g., `--language en --audio-language ml`). |
| `--made-for-kids` | No | Flag: set `madeForKids` = true (default: false) |
| `--embeddable` | No | Flag: set `embeddable` = true (default: false) |
| `--public-stats` | No | Flag: show like count (default: hidden) |
| `--license` | No | `youtube` or `creativeCommon` (default: `youtube`) |
| `--contains-synthetic-media` | No | Flag: set `containsSyntheticMedia` = true (AI-generated content disclosure) |
| `--age-restricted` | No | Flag: restrict to 18+ (may not persist for all accounts — set via Studio) |

***

## 4. Edge Cases

- **`ytAgeRestricted` may not persist**: YouTube's API does not guarantee that setting `contentRating.ytRating = ytAgeRestricted` will stick for all account types. The script prints a warning if the value does not persist. Fall back to YouTube Studio → Advanced → Age restriction.
- **Video not found**: If `video_id` is invalid or the authenticated user does not own the video, the API returns 404. The script exits 1.
- **Missing OAuth scope**: The credentials must include `https://www.googleapis.com/auth/youtube` scope. Re-run `oauth-setup.py` if needed.

***

## 5. Studio-Only Fields

The following fields CANNOT be set via the public YouTube Data API v3 and MUST be configured via [`youtube-studio-settings`](../youtube-studio-settings/SKILL.md) or manually in YouTube Studio:

| Field | Studio Location |
|---|---|---|
| Age restriction (advanced) | YouTube Studio → Content → video → Advanced |
| Comments off | YouTube Studio → Comments |
| Don't publish to subscriber feed | YouTube Studio → Advanced |
| Don't allow remixing | YouTube Studio → Video details |
| Caption certification (never aired in US) | YouTube Studio → Advanced → Caption certification |

***

## 6. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|---|---|
| [`youtube-video-upload`](../youtube-video-upload/SKILL.md) | Calls `scripts/video-metadata-update.py` as a post-upload step after upload via `youtube-video-upload` completes; passes `--embeddable`, `--public-stats`, `--made-for-kids`, `--language`, `--category-id`, `--license`, `--contains-synthetic-media`, `--age-restricted`. |
| [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) | Detects the spoken language during pre-processing and passes the BCP-47 code as `--language` to the metadata update script. |

***

## 7. Composition Rationale

This skill is a **base** skill: it owns only the YouTube Data API v3 `videos.update` PATCH call for metadata fields that must be set post-upload. It delegates all OAuth lifecycle management to [`google-oauth-setup`](../google-oauth-setup/SKILL.md) and is itself composed by:

- [`youtube-video-upload`](../youtube-video-upload/SKILL.md) — invokes `scripts/video-metadata-update.py` as a post-upload step, passing metadata flags the user selected before upload.
- [`media-audio-language-detect`](../media-audio-language-detect/SKILL.md) — calls `scripts/video-metadata-update.py --language <bcp47>` after audio language detection to set the video's default audio language.

Separating metadata update from upload allows other workflows (bulk metadata audit, automated language tagging) to reuse the same API call without re-uploading the video.

For updates to title, description, or tags — which are set during initial upload and corrected only post-upload — see the complementary [`youtube-video-snippet-update`](../youtube-video-snippet-update/SKILL.md) skill.
