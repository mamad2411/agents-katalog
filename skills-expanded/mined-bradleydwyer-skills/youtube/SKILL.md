---
name: youtube
description: "Fetch data from YouTube using the YouTube Data API v3. Use this skill whenever the user wants to search YouTube videos, get video details (title, description, view counts, likes, tags), list a channel's uploads, read comments on a video, browse playlist contents, or get video transcripts and captions. Also trigger when the user pastes a YouTube URL and wants info about it, or when they're doing any kind of YouTube research, content analysis, or data gathering — even if they don't explicitly say 'YouTube API'."
---

# YouTube Data API v3

Access YouTube data through the Data API v3 and yt-dlp.

## Setup

The API key is loaded from (checked in order):
1. `YOUTUBE_API_KEY` environment variable
2. `~/.config/youtube-api-key` file (plaintext, just the key)

For operations requiring OAuth (downloading caption tracks you own):
1. Save OAuth client credentials to `~/.config/youtube-oauth-client.json`
2. Run: `python3 ~/.claude/skills/youtube/scripts/oauth_setup.py`
3. Tokens are saved to `~/.config/youtube-oauth.json`

Most operations only need the API key. OAuth is optional.

## CLI Tool

All operations go through `yt.py`:

```bash
python3 ~/.claude/skills/youtube/scripts/yt.py <command> [options]
```

### Commands

**search** — Find videos, channels, or playlists
```bash
python3 yt.py search "query" [--max-results N] [--type video|channel|playlist] \
  [--channel-id ID] [--order relevance|date|rating|viewCount|title] \
  [--published-after 2024-01-01T00:00:00Z] [--published-before ...]
```

**video** — Get video metadata (snippet, stats, tags, duration)
```bash
python3 yt.py video VIDEO_ID_OR_URL [--parts snippet,statistics,contentDetails,topicDetails]
```
Accepts comma-separated IDs for batch lookups (up to 50).

**channel** — Get channel info or list uploads
```bash
python3 yt.py channel --channel-id ID
python3 yt.py channel --handle @username
python3 yt.py channel --channel-id ID --list-uploads [--max-results N]
```

**comments** — Get video comments
```bash
python3 yt.py comments VIDEO_ID_OR_URL [--max-results N] [--order relevance|time] [--search "term"]
```

**playlist** — List playlist items
```bash
python3 yt.py playlist PLAYLIST_ID_OR_URL [--max-results N]
```

**captions** — List available caption tracks (API key)
```bash
python3 yt.py captions VIDEO_ID_OR_URL
```

**transcript** — Get actual transcript text (uses yt-dlp)
```bash
python3 yt.py transcript VIDEO_ID_OR_URL [--lang en]
```
Requires `yt-dlp` installed (`brew install yt-dlp`). Falls back to auto-generated captions if manual ones aren't available.

### Pagination

List commands include `nextPageToken` in the response. Pass it to get more results:
```bash
python3 yt.py search "query" --page-token CDIQAA
```

### URL Parsing

All commands that take a video/playlist ID also accept full YouTube URLs:
```bash
python3 yt.py video "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python3 yt.py comments "https://youtu.be/dQw4w9WgXcQ"
python3 yt.py playlist "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
```

## Presenting Results

Adapt output format to the user's needs:
- Quick lookup → conversational summary
- Research/analysis → tables with key metrics
- Data extraction → raw JSON or CSV
- Multiple videos → title, channel, view count, publish date

## Quota Awareness

YouTube Data API has a daily quota of 10,000 units. Costs:
- **search**: 100 units (expensive — prefer direct lookups when you have IDs)
- **video/channel/playlist/comments list**: 1 unit each
- **captions list**: 50 units

When doing bulk operations, warn the user about quota impact. Prefer `video` with comma-separated IDs over repeated `search` calls.

## Reference

See `references/endpoints.md` for detailed parameter documentation and response field descriptions.
