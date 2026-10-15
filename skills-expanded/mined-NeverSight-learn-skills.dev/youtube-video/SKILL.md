---
name: youtube-video
description: Get YouTube video metadata with Stophy CLI. Trigger when the user provides a video URL or ID and needs title, description, channel, publish date, duration, views, likes, thumbnails, or general structured details about a single video.
metadata:
  author: stophy
  version: "1.0.0"
allowed-tools:
  - Bash(stophy *)
  - Bash(npx @stophy/cli *)
---

# youtube-video

Get structured metadata for a single YouTube video.

## Choose this skill when

- The user gives a YouTube video URL and asks “what is this?”, “get details”, “metadata”, or “video info”.
- You need title/channel/date/view data before deciding whether to fetch transcript or comments.
- The task is about the video object itself, not the spoken content or audience discussion.

Use `youtube-transcript` for spoken text and `youtube-comments` for viewer discussion.

## Commands

```bash
# Full video metadata
stophy video details --url "https://www.youtube.com/watch?v=h6ukrWyqOm4"

# Raw JSON for parsing
stophy video details --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --json

# Print only the title
stophy video details --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --json   | jq '.data.title' -r
```

## Options

| Option | Values | Use when |
|--------|--------|----------|
| `--url <url>` | YouTube video URL | Always required |
| `--json` | — | Pipe or parse raw JSON |

## Response shape

`details` returns fields such as:

- `title`
- `description`
- `viewCount`
- `likeCount`
- `publishedAt`
- `channel`
- `thumbnails`

## Output guidance

- For a human-facing answer, summarize the important fields instead of dumping JSON.
- Preserve the video URL and channel name.
- If the next step is likely, recommend one command:
  - transcript: `stophy video transcript --url "<url>"`
  - comments: `stophy video comments --url "<url>" --sortBy top`

## Related skills

- [youtube-transcript](../youtube-transcript/SKILL.md) — get transcript text with timestamps
- [youtube-comments](../youtube-comments/SKILL.md) — read comments and replies
- [youtube-livechat](../youtube-livechat/SKILL.md) — read livestream chat
- [youtube-search](../youtube-search/SKILL.md) — find videos before fetching metadata
- [youtube-channel](../youtube-channel/SKILL.md) — inspect the creator’s channel
- [youtube-playlist](../youtube-playlist/SKILL.md) — fetch videos from a playlist
