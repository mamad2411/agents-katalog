---
name: subsonic-api-client
description: Integration guidance for using Subsonic/OpenSubsonic client libraries in netrunner and other projects.
category: media
tags: [media, subsonic, opensubsonic, api, netrunner, development]
agents: [opencode, freebuff, antigravity, codex]
---

# subsonic-api-client

## Purpose

Guides development of applications that consume Subsonic/OpenSubsonic APIs, specifically for netrunner and related projects.

## Invocation

**OpenCode / Codex:** `Invoke subsonic-api-client`
**Freebuff:** `/skill subsonic-api-client`

## Recommended Client Libraries

- **TypeScript/JS:** `explodingcamera/subsonic-api` (OpenSubsonic support)
  - npm: `subsonic-api`
  - Supports API key auth, all core endpoints
- **Python:** `libsonic` or `py-sonic`
- **Go:** `deluan/navidrome` internal client patterns

## Auth Pattern (TypeScript)

```typescript
import { createSubsonicAPI } from 'subsonic-api';

const api = createSubsonicAPI({
  url: process.env.SUBSONIC_URL,
  auth: { apiKey: process.env.SUBSONIC_API_KEY }
});

const { artists } = await api.getArtists();
```

## Key Patterns for netrunner

- Store `SUBSONIC_URL` and `SUBSONIC_API_KEY` in `.env`, never in code.
- Implement exponential backoff for API rate limits.
- Cache artist/album metadata locally to reduce API calls.
- Use `startScan` after new downloads; poll `getScanStatus` before querying new files.
- Handle `error.code === 70` (data not found) gracefully — file may still be scanning.

## Inputs

- Subsonic server URL and API key (from environment variables)
- Query parameters: artist, album, playlist, search term, or scan trigger

## Outputs

- Artist/album/track metadata objects
- Streaming URLs or download links for tracks
- Scan status responses

## Safety

- Never hardcode credentials; always use environment variables.
- Never expose API keys in client-side bundles.

## Failure Modes

- `error.code === 70` — data not found; file may still be scanning. Poll `getScanStatus`.
- Rate limit exceeded — apply exponential backoff before retrying.
- Subsonic server unreachable — surface error to user; check `subsonic-media-server` status.

## References

- subsonic-api (npm): https://www.npmjs.com/package/subsonic-api
- OpenSubsonic spec: https://opensubsonic.netlify.app
- Subsonic API: https://subsonic.org/pages/api.jsp

## Companion Skills

- `subsonic-media-server` — server-side operations
- `netrunner-media-orchestrator` — pipeline context
