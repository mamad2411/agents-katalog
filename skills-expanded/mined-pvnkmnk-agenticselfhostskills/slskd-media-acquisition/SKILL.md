---
name: slskd-media-acquisition
description: Manage and automate music downloads via slskd (Soulseek daemon), including search, queue management, and transfer monitoring.
---

# slskd-media-acquisition

## Purpose
Provide an agent interface to slskd for discovering and downloading music from the Soulseek network. Handles search queries, download queue management, transfer monitoring, and post-download handoff to the music library pipeline.

## Invocation
- "Download [artist] - [album] from Soulseek"
- "Search Soulseek for [query]"
- "Check slskd download queue"
- "Monitor active transfers in slskd"
- "Clear completed downloads in slskd"

## Workflow Steps
1. **Authenticate:** Connect to slskd REST API (default: http://localhost:5030) using configured credentials.
2. **Search:** Submit search query; retrieve results ranked by quality (bitrate, format, source reputation).
3. **Select:** Choose best match — prefer FLAC > 320kbps MP3 > lower bitrate; prefer well-seeded users.
4. **Queue download:** Enqueue selected files via slskd API `/transfers/downloads` endpoint.
5. **Monitor:** Poll transfer status until complete; handle stalled or failed transfers with retry.
6. **Post-download:** Notify `music-library-organizer` skill to import and tag newly downloaded files.
7. **Log:** Record acquisition event in `homelab-logbook`.

## Safety
- Never download files from users flagged as abusive or known bad actors.
- Respect Soulseek community norms: maintain upload/download ratio.
- Do not bypass slskd authentication even in local network contexts.
- Validate file extensions before passing to library pipeline (audio files only).

## MCP
- **slskd-mcp** (`mcp/slskd-mcp.json`) — REST wrapper for slskd API; provides search, download, transfer tools.

## References
- slskd GitHub: https://github.com/slskd/slskd
- slskd API docs: https://slskd.github.io/slskd/
- Soulseek protocol: https://www.slsknet.org/

## Companion Skills
- `music-library-organizer` — tag and organize downloaded files
- `subsonic-media-server` — stream acquired music
- `media-stack-builder` — deploy the full acquisition stack
- `homelab-logbook` — log download events
