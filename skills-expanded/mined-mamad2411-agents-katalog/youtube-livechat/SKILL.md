---
name: youtube-livechat
description: Read YouTube live-stream chat with Stophy CLI. Trigger when the user provides a livestream URL and wants live chat messages, to follow chat over time, Super Chats, moderator/owner messages, or to check whether a video is live, upcoming, or a past stream.
metadata:
  author: stophy
  version: "1.0.0"
allowed-tools:
  - Bash(stophy *)
  - Bash(npx @stophy/cli *)
---

# youtube-livechat

Read live chat messages and stream status for a YouTube livestream.

## Choose this skill when

- The user gives a livestream URL and asks what people are saying in chat right now.
- The user wants to follow live chat over time, or capture Super Chats and moderator/owner messages.
- The user needs to know whether a video is live, upcoming, a past stream, or has chat disabled.

Use `youtube-comments` for posted comments on a normal video. Use `youtube-transcript` for spoken content. Use `youtube-video` for metadata.

## Commands

```bash
# Top chat (moderated, default)
stophy video livechat --url "https://www.youtube.com/watch?v=h6ukrWyqOm4"

# Live chat (every message)
stophy video livechat --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --chat-type live

# Fetch new messages from a previous response
stophy video livechat --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --continuation-token <token>
```

## Options

| Option | Values | Use when |
|--------|--------|----------|
| `--url <url>` | YouTube video URL | Always required |
| `--chat-type <type>` | top, live | `top` for moderated chat, `live` for every message. Set on the first request and kept afterward |
| `--continuation-token <token>` | string | Fetch new messages since the previous response |
| `--json` | — | Pipe or parse raw JSON |

## Response shape

`livechat` returns:

- `status` — `live`, `upcoming`, `replay`, `chat_disabled`, or `not_live`
- `isLive`
- `concurrentViewers`
- `pollIntervalMs` — suggested wait before the next request
- `messages[]` — `text`, `author`, `isOwner`, `isModerator`, `isVerified`, `superChatAmount`
- `continuationToken` — pass back to fetch new messages; `null` once chat has ended

## Output guidance

- Only `status: "live"` returns messages and a `continuationToken`. For `upcoming`, `replay`, `chat_disabled`, and `not_live`, tell the user the stream state instead of expecting messages.
- To follow chat, repeat the command with the returned `continuationToken`, waiting `pollIntervalMs` between requests. Stop when the token is `null`.
- An empty `messages` array on a live stream just means nothing new arrived — keep polling.
- Highlight Super Chats and moderator/owner messages when summarizing.

## Related skills

- [youtube-video](../youtube-video/SKILL.md) — get video metadata
- [youtube-comments](../youtube-comments/SKILL.md) — read posted comments and replies
- [youtube-transcript](../youtube-transcript/SKILL.md) — get spoken content
- [youtube-search](../youtube-search/SKILL.md) — find videos or livestreams
