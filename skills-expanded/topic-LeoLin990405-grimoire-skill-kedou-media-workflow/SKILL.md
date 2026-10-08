---
name: kedou-media-workflow
description: >-
  Plan and operate safe Kedou media workflows for authorized content: online
  video parsing, desktop downloader batch jobs, subtitle/danmaku/lyric
  extraction, Xiaohongshu/Zhihu/CSDN-style text extraction, and handoff to local
  CLI or Knowledge Hub processing. Use when the user mentions Kedou, 蝌蚪,
  kedou.life, video parsing/download, batch subtitle download, danmaku download,
  lyrics extraction, text/image extraction from supported platforms, or
  troubleshooting Kedou downloader/cookie/proxy/save-path issues.
---

# Kedou Media Workflow

## Core Rule

Use Kedou only for content where the user has rights, permission, membership access, or a clear personal learning/research basis. Never request, store, or echo raw cookies, auth headers, account tokens, paid-content URLs, or private media links.

## Decision Tree

1. **Single public video or image**: use Kedou web parser.
   - Copy browser URL or app share link.
   - Paste into Kedou.
   - Choose direct parse for the current visible media.
   - Choose list parse when the page contains a playlist, collection, homepage, or media list.

2. **Batch videos, homepage, playlist, favorites, search, or high-resolution work**: use Kedou desktop downloader.
   - Prefer the downloader for repeated jobs, batch input, playlist/homepage extraction, subtitles/danmaku in bulk, and sniffing.
   - Batch input expects one URL per line.
   - Keep task count small, usually `2` or `4`.

3. **Subtitles, danmaku, lyrics, or text only**: use the matching Kedou extraction page first.
   - Subtitle pages return language-specific files, usually `.srt`, with view/download options.
   - Danmaku pages return platform danmaku where supported.
   - Text extraction pages return article/copy/image material, often Markdown-like.

4. **Need fresh docs or current platform support**: use `$opencli-browser-first` to read Kedou public pages, then update the workflow. Do not rely on stale memory for platform-specific support changes.

## Downloader Operating Notes

- Use clipboard import for one copied link.
- Use manual link input when a URL or request headers must be supplied locally.
- Use batch input for multiple URLs, one URL per line.
- Use homepage/list workflows for supported user spaces, channels, playlists, collections, favorites, likes, history, and search results.
- Use right-click table actions to clear completed/failed tasks and open downloaded files/folders.
- Use toolbox functions for audio/video merge, TS segment merge, file merge, and audio extraction.
- If no proxy is configured in the downloader, it follows the system proxy.

## Troubleshooting

- **No result / low quality**: verify membership/login state on Kedou and target platform; for platform-specific list or high-quality content, the user may need a fresh cookie configured locally in the downloader.
- **Batch list empty**: cookie may be expired, target page may be inaccessible, or the target platform changed its API. Refresh cookie locally and retry.
- **Download starts but no file appears**: check points/credits, task failure state, duplicate task detection, save path, and disk space.
- **Browser download opens playback page**: use the player/browser download control.
- **Timeout / interrupted parse**: wait and retry; some platforms queue or rate-limit parsing.
- **Mac install warning**: only apply Gatekeeper/quarantine workarounds to a trusted official Kedou installer.

## Local Handoff

After Kedou produces files, prefer local CLI tools:

- `ffmpeg` for media conversion, audio extraction, or merging.
- `magick`/ImageMagick for thumbnail contact sheets or image post-processing.
- `rg`, `fd`, `yazi`, and `fzf` for file discovery and review.
- `mlx_whisper` or `whisper-cli` when subtitles are absent and transcription is needed.
- Knowledge Hub notes should store durable summaries, file paths, source page families, and processing decisions, not raw credentials or private URLs.

## Bilibili subtitle → note (automated recipe)

For a Bilibili video/space URL the repo ships an automated path:
`scripts/kedou-bili-subs.sh` drives this caption page via OpenCLI and
prints the downloaded Chinese `.srt`; pipe it into
`scripts/forge.sh <srt> --from-text --only both`. Full steps + gotchas:
`references/bilibili-subtitle-to-note.md`. Note shape:
`templates/subtitle-note-template.md` (agent fills it; scripts never write
the vault).

## References

- Read `references/kedou-capabilities.md` for supported page families, workflows, and OpenCLI-derived source notes.
- Read `references/bilibili-subtitle-to-note.md` for the validated B站
  字幕→笔记 recipe (OpenCLI + Kedou web, filesystem download wait).

