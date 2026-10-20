---
name: jellyfin-media
description: Self-hosted media streaming with Jellyfin
version: 1.0.0
tags: [media, streaming, movies, music]
---

# Jellyfin – Open-Source Media Server

Jellyfin is a free, open-source media system for streaming movies,
TV shows, music, and photos to any device.

- **GitHub**: github.com/jellyfin/jellyfin (45 000+ ⭐)
- **License**: GPL-2.0
- **Security**: Volunteer-built; no telemetry, no central servers. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{JELLYFIN_URL}}` | Base URL of the Jellyfin instance |
| `{{JELLYFIN_API_KEY}}` | API key for authentication |

## Usage Examples

### Get system info

```bash
curl -s "{{JELLYFIN_URL}}/System/Info" \
  -H "X-Emby-Token: {{JELLYFIN_API_KEY}}"
```

### List libraries

```bash
curl -s "{{JELLYFIN_URL}}/Library/VirtualFolders" \
  -H "X-Emby-Token: {{JELLYFIN_API_KEY}}"
```

### Search media

```bash
curl -s "{{JELLYFIN_URL}}/Items?searchTerm=inception&Recursive=true" \
  -H "X-Emby-Token: {{JELLYFIN_API_KEY}}"
```

## AI Agent Tips

- API is Emby-compatible; use `X-Emby-Token` header.
- Supports transcoding, subtitles, and multi-user profiles.
- Clients available for web, mobile, TV, and desktop.
- No premium tier — all features are free and open-source.
