---
name: managing-mapbox
description: |
  Use when working with Mapbox — mapbox platform management including map
  styles, tilesets, datasets, tokens, usage statistics, and geocoding. Covers
  API usage monitoring, tileset processing status, token permission auditing,
  and rate limit tracking across Maps, Navigation, and Search APIs.
connection_type: mapbox
preload: false
---

# Mapbox Management Skill

Monitor and manage Mapbox mapping and location services.

## MANDATORY: Discovery-First Pattern

**Always discover account tokens and usage tiers before querying specific services.**

### Phase 1: Discovery

```bash
#!/bin/bash
MB_API="https://api.mapbox.com"
AUTH="access_token=${MAPBOX_ACCESS_TOKEN}"

echo "=== Account Info ==="
curl -s "$MB_API/tokens/v2?$AUTH" | \
  jq -r '.[] | "\(.note // .id) | Scopes: \(.scopes | join(",")) | Created: \(.created)"' | head -10

echo ""
echo "=== Styles ==="
curl -s "$MB_API/styles/v1/${MAPBOX_USERNAME}?$AUTH" | \
  jq -r '.[] | "\(.name) | ID: \(.id) | Created: \(.created) | Modified: \(.modified)"'

echo ""
echo "=== Tilesets ==="
curl -s "$MB_API/tilesets/v1/${MAPBOX_USERNAME}?$AUTH&limit=20" | \
  jq -r '.[] | "\(.name // .id) | ID: \(.id) | Type: \(.type) | Status: \(.status) | Size: \(.filesize // "N/A")"'

echo ""
echo "=== Datasets ==="
curl -s "$MB_API/datasets/v1/${MAPBOX_USERNAME}?$AUTH" | \
  jq -r '.[] | "\(.name) | ID: \(.id) | Features: \(.features) | Size: \(.size)"'
```

**Phase 1 outputs:** Tokens, styles, tilesets, datasets

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== API Usage (current period) ==="
curl -s "$MB_API/usage/v4/${MAPBOX_USERNAME}?$AUTH&period=current" | \
  jq -r '.[] | "\(.api): \(.quantity) requests"' 2>/dev/null || \
curl -s "https://api.mapbox.com/usage/v1/${MAPBOX_USERNAME}?$AUTH&start=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d '30 days ago' +%Y-%m-%d)&end=$(date +%Y-%m-%d)" | \
  jq -r 'to_entries[] | "\(.key): \(.value)"'

echo ""
echo "=== Token Audit ==="
curl -s "$MB_API/tokens/v2?$AUTH" | \
  jq -r '.[] | "\(.note // .id) | Public: \(.default // false) | Scopes: \(.scopes | length) | AllowedURLs: \(.allowedUrls // ["any"] | join(","))"'

echo ""
echo "=== Tileset Processing Jobs ==="
curl -s "$MB_API/tilesets/v1/${MAPBOX_USERNAME}/jobs?$AUTH&limit=5" | \
  jq -r '.[] | "\(.tilesetId) | Stage: \(.stage) | Created: \(.created) | Errors: \(.errors // 0)"' 2>/dev/null || echo "No recent jobs"

echo ""
echo "=== Geocoding Test ==="
curl -s "$MB_API/geocoding/v5/mapbox.places/test.json?$AUTH&limit=1" | \
  jq -r '"Geocoding API: \(if .features then "OK" else "Error" end)"'
```

## Output Format

```
MAPBOX STATUS
=============
Account: {username}
Styles: {count} | Tilesets: {count} | Datasets: {count}
API Usage (period): Maps={count} Geocoding={count} Navigation={count}
Tokens: {count} ({public}/{private})
Tileset Jobs: {processing}/{completed}
Issues: {list_of_warnings}
```

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Public vs Secret tokens**: Public tokens are for client-side — never use secret tokens in browsers
- **URL restrictions**: Restrict tokens to specific URLs in production
- **Rate limits**: Vary by API and plan — Maps tiles are 100k/min, Geocoding is 600/min on free
- **Tileset size limits**: 20GB per tileset on free tier — check before uploading
