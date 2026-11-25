---
name: youtube-for-ai
description: YouTube data for AI agents. Get transcripts, comments, search results, channels, and playlists via Stophy CLI. Trigger when the user wants any YouTube content, provides a YouTube URL, or needs structured YouTube data from the terminal or MCP.
metadata:
  author: stophy
  version: "1.0.0"
allowed-tools:
  - Bash(stophy *)
  - Bash(npx @stophy/cli *)
---

# youtube-for-ai

**YouTube data for AI agents.** Search, transcripts, comments, channels, playlists — all as structured JSON via Stophy CLI.

## Before running commands

1. Prefer `stophy ...` when the CLI is installed.
2. Use `npx @stophy/cli ...` only when `stophy` is not available.
3. If authentication fails, help the user log in instead of inventing output.
4. Do not expose API keys in responses. Use `$STOPHY_API_KEY` or `st_xxx` placeholders.

## Authentication

```bash
stophy login                      # interactive browser/API-key login
stophy login --browser            # browser login
stophy login --api-key st_xxx     # store an API key directly
export STOPHY_API_KEY="st_xxx"    # environment variable also works
```

## Command map

| Need | Command |
|------|---------|
| Search YouTube | `stophy search --q "query"` |
| Get suggestions | `stophy suggest --q "partial query"` |
| Video metadata | `stophy video details --url "<video-url>"` |
| Transcript | `stophy video transcript --url "<video-url>"` |
| Comments | `stophy video comments --url "<video-url>" --sortBy top` |
| Replies | `stophy video replies --continuation-token <repliesToken>` |
| Live chat | `stophy video livechat --url "<video-url>"` |
| Channel catalog | `stophy channel --url "<channel-url-or-handle>"` |
| Channel about page | `stophy channel --url "<channel-url-or-handle>" --tab about` |
| Playlist videos | `stophy playlist --url "<playlist-url>"` |
| Credits | `stophy credits` |
| Usage | `stophy usage --days 7` |
| Request logs | `stophy logs --days 7` |
| Config/auth status | `stophy view-config` |

## Recommended workflow

1. Start with the user’s intent:
   - topic discovery → `youtube-search`
   - one video’s metadata → `youtube-video`
   - spoken content → `youtube-transcript`
   - viewer reactions → `youtube-comments`
   - livestream chat → `youtube-livechat`
   - creator/channel research → `youtube-channel`
   - course/playlist research → `youtube-playlist`
2. Run the narrowest command that answers the question.
3. Use `--json` when the next step needs machine-readable output or `jq` filtering.
4. Use `--continuation-token` only when the user needs more results.

## Examples

```bash
# Search, then inspect one result manually
stophy search --q "AI coding agents" --type video --sortBy popularity

# Transcript text for another tool
stophy video transcript --url "https://www.youtube.com/watch?v=h6ukrWyqOm4" --json   | jq '.data.segments[].text' -r

# Channel's most popular videos
stophy channel --url "https://www.youtube.com/@t3dotgg" --tab video --sortBy popular
```

## Output rules

- Summarize what the command returned; do not dump huge JSON unless the user asks.
- Preserve useful IDs, URLs, titles, counts, timestamps, and continuation tokens.
- If a transcript is unavailable because captions are disabled, say that directly.
- If an API call fails, report the error and suggest the next concrete command.

## Related skills

- [youtube-search](../youtube-search/SKILL.md) — search YouTube by keyword
- [youtube-video](../youtube-video/SKILL.md) — get video metadata
- [youtube-transcript](../youtube-transcript/SKILL.md) — get transcript text with timestamps
- [youtube-comments](../youtube-comments/SKILL.md) — read comments and replies
- [youtube-livechat](../youtube-livechat/SKILL.md) — read livestream chat
- [youtube-channel](../youtube-channel/SKILL.md) — inspect a channel catalog
- [youtube-playlist](../youtube-playlist/SKILL.md) — fetch playlist videos
