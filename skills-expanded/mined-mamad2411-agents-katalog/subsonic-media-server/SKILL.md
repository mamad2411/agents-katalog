---
name: subsonic-media-server
description: Manage and interact with a Subsonic-compatible music streaming server (Navidrome or Airsonic); control playback, manage playlists, and trigger library rescans via the OpenSubsonic API.
---

# subsonic-media-server

## Purpose
Provide agent-level control over a self-hosted Subsonic-compatible music streaming server (Navidrome recommended). Enables playlist management, library rescan triggers, now-playing queries, and playback control via the OpenSubsonic REST API.

## Invocation
- "What's playing on Navidrome?"
- "Create a playlist called [name] with [tracks]"
- "Trigger Navidrome library rescan"
- "Search Navidrome for [artist/album/track]"
- "Get recently added albums from Subsonic"
- "Stream [song] via Subsonic"

## Workflow Steps
1. **Authenticate:** Use Subsonic API token auth (`u=`, `t=`, `s=`, `v=`, `c=` params) against configured server URL.
2. **Query:** Call appropriate OpenSubsonic REST endpoint (e.g., `/rest/getArtists`, `/rest/search3`, `/rest/getNowPlaying`).
3. **Parse:** Extract relevant data from XML/JSON response.
4. **Act:** Perform requested action — create/update playlist, return results, trigger scan, etc.
5. **Rescan:** After `music-library-organizer` runs, call `/rest/startScan` to index new files.
6. **Log:** Record significant events (new content indexed, playlist changes) in `homelab-logbook`.

## Safety
- Never expose Subsonic API credentials in logs or responses.
- Do not delete playlists or user data without explicit confirmation.
- Validate server reachability before attempting bulk operations.

## Instance Addendum: Navidrome on CT 101 "homelab-core" (192.168.2.242)

- **Production container** — `deluan/navidrome:0.63.2` in Docker on CT 101, port 4533, up 12+ days at last verify. **Never restart it to apply changes.**
- Health check: `curl -fsS -o /dev/null -w "%{http_code}" http://127.0.0.1:4533/` on the CT → `302` = healthy (login redirect).
- Music volume: `/opt/homelab/navidrome/music` (590 GiB). Library changes happen via beets in the same CT, then trigger a rescan — **via the Subsonic API only**, not container restarts.
- Access from the agent: `ssh root@192.168.2.242` first; the port is local to the CT/LAN.

## MCP
- **subsonic-mcp** (`mcp/subsonic-mcp.json`) — OpenSubsonic REST wrapper; provides search, playlist, scan, stream tools.

## References
- OpenSubsonic API: https://opensubsonic.netlify.app/
- Navidrome: https://www.navidrome.org/
- Subsonic API (original): http://www.subsonic.org/pages/api.jsp

## Companion Skills
- `music-library-organizer` — feeds organized files into the server library
- `slskd-media-acquisition` — upstream acquisition source
- `dj-library-curator` — curates playlists served here
- `media-stack-builder` — deploys and configures this server
- `homelab-logbook` — logs scan and playback events
