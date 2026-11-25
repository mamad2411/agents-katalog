---
name: youtube-channel
description: Inspect YouTube channel data with Stophy CLI. Trigger when the user provides a channel URL or @handle and asks for a creator's videos, Shorts, playlists, about page, most popular uploads, recent uploads, catalog, subscriber info, channel links, or creator research.
metadata:
  author: stophy
  version: "1.0.0"
allowed-tools:
  - Bash(stophy *)
  - Bash(npx @stophy/cli *)
---

# youtube-channel

Inspect a YouTube channel’s videos, Shorts, playlists, or about page.

## Choose this skill when

- The user provides a channel URL or @handle.
- The user asks what a creator has uploaded recently or what their most popular videos are.
- The user needs channel-level research: catalog, playlists, about page, links, subscriber info, or positioning.

Use `youtube-search` when the user has only a topic, not a specific channel.

## Commands

```bash
# Latest videos from a channel
stophy channel --url "https://www.youtube.com/@t3dotgg"

# Most popular videos
stophy channel --url "https://www.youtube.com/@t3dotgg" --tab video --sortBy popular

# Channel about page: description, links, subscriber info when available
stophy channel --url "https://www.youtube.com/@t3dotgg" --tab about

# Shorts
stophy channel --url "https://www.youtube.com/@t3dotgg" --tab short

# Playlists
stophy channel --url "https://www.youtube.com/@t3dotgg" --tab playlist

# Paginate
stophy channel --url "https://www.youtube.com/@t3dotgg" --continuation-token <token>
```

## Options

| Option | Values | Use when |
|--------|--------|----------|
| `--url <url>` | Channel URL or @handle | Always required |
| `--tab <tab>` | video, short, playlist, about | Choose the channel section |
| `--sortBy <sort>` | latest, popular, oldest | Sort videos; only applies to `--tab video` |
| `--continuation-token <token>` | string | Fetch the next page |
| `--json` | — | Pipe or parse raw JSON |

## Decision rules

- Use `--tab about` for descriptions, links, and channel-level facts.
- Use `--tab video --sortBy popular` for the creator’s strongest historical content.
- Use `--tab video --sortBy latest` for recent uploads.
- Use `--tab playlist` before `youtube-playlist` when the user asks for a channel’s courses or series.
- Do not use `--sortBy` with `short`, `playlist`, or `about`; it only applies to videos.

## Output guidance

- For channel research, summarize patterns instead of listing every item.
- Include video URLs or playlist URLs for follow-up work.
- Preserve `continuationToken` when more results are available.

## Related skills

- [youtube-video](../youtube-video/SKILL.md) — get metadata for a specific video
- [youtube-transcript](../youtube-transcript/SKILL.md) — get transcript text for a video
- [youtube-comments](../youtube-comments/SKILL.md) — read comments for a video
- [youtube-playlist](../youtube-playlist/SKILL.md) — fetch a playlist found on a channel
- [youtube-search](../youtube-search/SKILL.md) — discover channels by topic
