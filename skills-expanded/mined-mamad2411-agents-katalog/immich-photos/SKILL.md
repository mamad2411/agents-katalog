---
name: immich-photos
description: Self-hosted photo and video management with Immich
version: 1.0.0
tags: [photos, media, backup, ai]
---

# Immich – Self-Hosted Google Photos Alternative

Immich provides high-performance photo and video backup with
AI-powered facial recognition, object detection, and smart search.

- **GitHub**: github.com/immich-app/immich (65 000+ ⭐)
- **License**: AGPL-3.0
- **Security**: Active security-focused development team. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{IMMICH_URL}}` | Base URL of the Immich instance |
| `{{IMMICH_API_KEY}}` | API key for authentication |

## Usage Examples

### Get server info

```bash
curl -s "{{IMMICH_URL}}/api/server/info" \
  -H "x-api-key: {{IMMICH_API_KEY}}"
```

### Search assets

```bash
curl -s -X POST "{{IMMICH_URL}}/api/search/metadata" \
  -H "x-api-key: {{IMMICH_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d '{"originalFileName": "vacation"}'
```

### Upload an asset

```bash
curl -s -X POST "{{IMMICH_URL}}/api/assets" \
  -H "x-api-key: {{IMMICH_API_KEY}}" \
  -F "assetData=@photo.jpg" \
  -F "deviceAssetId=unique-id" \
  -F "deviceId=api" \
  -F "fileCreatedAt=2025-01-01T00:00:00.000Z" \
  -F "fileModifiedAt=2025-01-01T00:00:00.000Z"
```

## AI Agent Tips

- Smart search uses CLIP embeddings for natural-language photo queries.
- Mobile apps auto-backup photos; API enables programmatic uploads.
- Supports RAW file formats and video transcoding.
- Face recognition groups photos by person automatically.
