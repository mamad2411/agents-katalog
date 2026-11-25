---
name: media-downloader
description: Download user-authorized public media while respecting rights, terms, and safe filenames.
category: web
aliases:
- download
- media
- youtube
- audio
triggers:
- Download this video
- Save this audio
- Download the image
- Get this media file
keywords:
- download
- media
- video
- audio
- image
- youtube
- mp3
dependencies:
- optional:media-downloader
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- media-downloader
- web
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- audio
- download
- downloader
- media
- video
- web
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Media Downloader

## Purpose
Download publicly available media files (videos, audio, images) from the web with
proper respect for copyright, terms of service, and safe filename handling. The skill
ensures users have appropriate rights before downloading and provides proper attribution.

## When to Use
- The user explicitly requests to download a media file they have rights to
- Backing up content the user owns (e.g., their own YouTube videos)
- Downloading Creative Commons licensed content

## When NOT to Use
- Downloading copyrighted content without user authorization
- Circumventing paywalls or access controls
- Bulk downloading that violates terms of service
- Content the user doesn't have rights to

## Capabilities
- Support for common platforms (YouTube, Vimeo, SoundCloud, etc.)
- Format conversion (video to audio, different resolutions)
- Progress tracking for large files
- Filename sanitization
- Checksum verification
- Respect robots.txt and platform terms

## Inputs
- `url` (required) — media URL
- `format` (optional) — desired format (mp4, mp3, wav, jpg, etc.)
- `quality` (optional) — resolution/quality preference
- `output_dir` (optional) — destination directory

## Workflow
1. **Validate** — Check URL accessibility and format support
2. **Verify** — Confirm user has rights to this content
3. **Download** — Fetch media with progress tracking
4. **Convert** — Apply format conversion if requested
5. **Verify** — Check file integrity with checksum
6. **Report** — Confirm download with file details

## Tools
- yt-dlp or similar media downloader
- FFmpeg for format conversion
- HTTP client for direct downloads

## Examples
**User:** "Download this video: https://youtube.com/watch?v=..."
**Response:** Downloading video... [â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆ] 100%
Saved: `media/video-title-2026-02-09.mp4` (256MB, sha256:abc123...)

## Safety
- ALWAYS verify user authorization before downloading
- Check terms of service for target platform
- Never download copyrighted content without explicit permission
- Respect rate limits and robots.txt
- Store download receipts for provenance

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical web category.
