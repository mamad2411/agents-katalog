---
name: youtube-comments
description: Read YouTube video comments and replies with Stophy CLI. Trigger when the user provides a video URL and asks what viewers are saying, wants top or latest comments, audience reactions, sentiment evidence, customer language, objections, or replies from a comment thread.
metadata:
  author: stophy
  version: "1.0.0"
allowed-tools:
  - Bash(stophy *)
  - Bash(npx @stophy/cli *)
---

# youtube-comments

Read comments and replies for a YouTube video.

## Choose this skill when

- The user asks what people/viewers/commenters are saying.
- The user wants reactions, objections, praise, complaints, or customer language from comments.
- The user needs top comments, latest comments, or replies in a thread.

Use `youtube-transcript` for spoken content. Use `youtube-video` for metadata.

## Commands

```bash
# Top comments
stophy video comments --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --sortBy top

# Latest comments
stophy video comments --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --sortBy latest

# More comments from a previous response
stophy video comments --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --continuation-token <token>

# Replies to a comment thread
stophy video replies --continuation-token <repliesToken>
```

## Options

| Option | Values | Use when |
|--------|--------|----------|
| `--url <url>` | YouTube video URL | Required for comments |
| `--sortBy <sort>` | top, latest | Choose popular or recent comments |
| `--continuation-token <token>` | string | Fetch more comments or replies |
| `--json` | — | Pipe or parse raw JSON |

## Response shape

`comments` returns `comments[]` with fields such as:

- `text`
- `author`
- `likeCount`
- `publishedAt`
- `repliesToken`

Pass `repliesToken` to `stophy video replies` to load the full thread.

## Output guidance

- For research tasks, group comments by theme and include representative quotes.
- Preserve `repliesToken` when the user may want to inspect a thread.
- Use `--sortBy top` for highest-signal reactions; use `--sortBy latest` for recent discussion.
- Do not claim comments represent all viewers. Frame findings as “comments surfaced by the API”.

## Related skills

- [youtube-video](../youtube-video/SKILL.md) — get video metadata
- [youtube-transcript](../youtube-transcript/SKILL.md) — get spoken content
- [youtube-livechat](../youtube-livechat/SKILL.md) — read livestream chat
- [youtube-search](../youtube-search/SKILL.md) — find videos before reading comments
