---
name: media-stack-builder
description: Assembles and configures the full homelab media stack including slskd, Navidrome/Subsonic, and beets.
---

# media-stack-builder

Orchestrates the deployment and wiring of the complete homelab media stack. Connects Soulseek downloads (slskd), music organization (beets), and the Subsonic/Navidrome media server into a cohesive pipeline.

## Invocation

**OpenCode / Codex:** `Invoke media-stack-builder`
**Freebuff:** `/skill media-stack-builder`

## Stack Components

| Component | Role | Skill |
|---|---|---|
| slskd | Soulseek download daemon | `slskd-media-acquisition` |
| beets | Music tagger and organizer | `music-library-organizer` |
| Navidrome / Subsonic | Music streaming server | `subsonic-media-server` |
| Cloudflare / Caddy | Secure access | `reverse-proxy-and-tunnel` |

## Workflow Steps

1. **Deploy slskd:** Use `docker-app-deployer` to deploy slskd container.
2. **Configure slskd:** Set username, download directory, shared folders.
3. **Deploy Navidrome:** Deploy Navidrome container; point at music library directory.
4. **Configure beets:** Install and configure beets with MusicBrainz tagger; point at slskd download dir.
5. **Wire pipeline:** slskd downloads → beets imports → music library → Navidrome scans.
6. **Expose:** Configure reverse proxy for Navidrome (internal or Cloudflare Tunnel).
7. **Verify:** Test download → organize → stream end-to-end flow.
8. **Log:** Record stack deployment in `homelab-logbook`.

## Companion Skills

- `docker-app-deployer` — deploy containers
- `reverse-proxy-and-tunnel` — configure access
- `slskd-media-acquisition` — download management
- `music-library-organizer` — organize and tag
- `subsonic-media-server` — streaming server management

## References

- slskd: https://github.com/slskd/slskd
- Navidrome: https://www.navidrome.org/
- beets: https://beets.readthedocs.io/
