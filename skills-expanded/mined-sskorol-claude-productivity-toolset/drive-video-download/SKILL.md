---
name: drive-video-download
description: Download a protected Google Drive video (canDownload:false) via active browser session (Brave or Chrome). Use when Drive API returns 403, yt-dlp fails, or the file has download restrictions set by the owner.
---

# Drive Video Download

Downloads Google Drive videos that have download restrictions (`canDownload: false`) by piggybacking on the user's active browser session (Brave or Chrome) via CDP.

## When to use

- Drive API returns `"cannotDownloadFile"` or `canDownload: false`
- yt-dlp returns HTTP 403 on the Drive URL
- File is a Google Meet/Workspace recording with admin-disabled downloads
- Any shared corporate video the user can *view* but not *download*

## Prerequisites

1. **Brave or Chrome is running** and the user is logged in to Google
2. **Remote debugging enabled**:
   - Brave: `brave://inspect/#devices` → toggle the switch
   - Chrome: `chrome://inspect/#devices` → toggle "Discover network targets"
3. The user can view the file in their browser (even if download is blocked)
4. Node.js 22+ (uses built-in WebSocket)

## Usage

```bash
# Basic — outputs to /tmp/drive-<fileId>.m4a
node ~/.claude/skills/drive-video-download/scripts/download.mjs <file-id-or-url>

# With custom output path
node ~/.claude/skills/drive-video-download/scripts/download.mjs <file-id-or-url> /tmp/recording.m4a
```

Both full Drive URLs and bare file IDs work:
```bash
node ~/.claude/skills/drive-video-download/scripts/download.mjs "https://drive.google.com/file/d/<your-file-id>/view"
node ~/.claude/skills/drive-video-download/scripts/download.mjs <your-file-id>
```

The script prints the output file path to stdout on success.

## What the script does

1. **Reads `DevToolsActivePort`** from the browser profile — auto-detects Brave, Chrome, or Chromium on macOS/Linux
2. **Finds or opens** the Drive file tab in the browser
3. **Reloads the tab** and intercepts the `workspacevideo-pa` manifest response via CDP Network domain — this gives a signed streaming URL for `itag=140` (audio-only m4a, ~128kbps, ideal for transcription)
4. **Opens a same-origin tab** at the videoplayback URL and calls `Network.getCookies` — this is necessary because `rqh=1` in the signed URL requires session cookies that are tied to the videoplayback origin
5. **Downloads 8 parallel chunks** via curl with exact browser headers (Referer = URL itself, matching User-Agent and sec-ch-ua from live browser)
6. **Assembles** chunks in order into the output file

## Key technical findings (learned 2026-03-18)

- `canDownload: false` blocks the Drive API (`alt=media`), yt-dlp, and plain curl with any headers
- The `workspacevideo-pa` endpoint returns a signed streaming URL that bypasses download restrictions — it's what the Drive web player uses internally
- The signed URL has `rqh=1` (required request hash) — blocks curl without the right cookies+headers
- Critical: **Referer must be the videoplayback URL itself** — NOT `youtube.googleapis.com` (common wrong assumption from other YouTube-based approaches)
- **No `x-client-data` or `origin` headers needed** — the browser doesn't send them for this endpoint
- The `Network.getCookies` on the videoplayback tab (same origin as the streaming server) returns the right cookies; Drive tab cookies are insufficient

## After downloading

Pass the output file to the `video-transcribe` skill for transcription.
