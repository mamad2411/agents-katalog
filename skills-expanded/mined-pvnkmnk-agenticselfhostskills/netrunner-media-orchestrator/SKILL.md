---
name: netrunner-media-orchestrator
description: Orchestrates the full acquisition-to-playback media pipeline for the netrunner project.
category: media
tags: [media, netrunner, soulseek, subsonic, orchestration, pipeline]
agents: [opencode, freebuff, antigravity, codex]
---

# netrunner-media-orchestrator

## Purpose

Encodes how netrunner agents should coordinate across acquisition (Soulseek/slskd), library serving (Subsonic/OpenSubsonic), organization, and DJ/listening workflows. This is the top-level skill for netrunner media pipeline sessions.

## Invocation

**OpenCode / Codex:** `Invoke netrunner-media-orchestrator`
**Freebuff:** `/skill netrunner-media-orchestrator`

## Pipeline Architecture

```
Soulseek Network
    │
    └─ slskd / Slsk MCP ──────────── [slskd-media-acquisition / slsk-mcp-client]
            │
    music-library-organizer (tagging, file structure)
            │
    Subsonic/OpenSubsonic (Navidrome) ── [subsonic-media-server]
            │
    netrunner API ─────────────────── [subsonic-api-client]
            │
    Clients: DJ tools, mobile apps, web
            │
    Obsidian vault ──────────────────── [obsidian-music-journal]
```

## Workflow Steps

1. **Define goal:** What kind of content? What context (listening, DJ prep, curation)?
2. **Acquire:** Use `soulseek-network-orienter` + `slskd-media-acquisition` or `slsk-mcp-client`.
3. **Organize:** Run `music-library-organizer` on downloaded files.
4. **Ingest:** Trigger `subsonic-media-server` rescan; verify new files appear.
5. **Curate:** Use `dj-library-curator` or `music-listening-journal` as appropriate.
6. **Build/plan:** Use `dj-set-architect` for DJ sessions; `music-project-planner` for production.
7. **Document:** Log to `obsidian-music-journal` and `dj-mix-documentarian`.

## Inputs

- Session goal: content type and context (listening, DJ prep, curation, production)
- Configured skill dependencies (Soulseek credentials, Subsonic URL/key, Obsidian vault path)

## Outputs

- Downloaded, organized, and ingested music files in Subsonic library
- Curated playlists or DJ set plan
- Obsidian vault notes documenting the session

## Safety

- All network operations go through vetted MCP servers or APIs only.
- No raw shell commands against homelab without `homelab-safe-ops`.
- Credentials in env files; never in prompts or code.

## Failure Modes

- Soulseek network unavailable — pause acquisition, notify user.
- Subsonic scan stalled — poll `getScanStatus`; retry after timeout.
- Obsidian vault write conflict — queue writes and retry on next sync.

## Companion Skills

- `soulseek-network-orienter`, `slskd-media-acquisition`, `slsk-mcp-client`
- `subsonic-media-server`, `subsonic-api-client`
- `music-library-organizer`, `dj-library-curator`, `dj-set-architect`
- `obsidian-music-journal`, `dj-mix-documentarian`
