---
name: managing-here-maps
description: |
  Use when working with Here Maps — hERE Maps platform management including
  project configuration, API key management, usage statistics, service health,
  and quota monitoring across Geocoding, Routing, Map Tile, and Search APIs.
  Covers request volume tracking, error analysis, and plan limit monitoring.
connection_type: here-maps
preload: false
---

# HERE Maps Management Skill

Monitor and manage HERE Maps location services platform.

## MANDATORY: Discovery-First Pattern

**Always discover projects and API keys before querying usage or service health.**

### Phase 1: Discovery

```bash
#!/bin/bash
HERE_API="https://fleet.ls.hereapi.com/2"
AUTH="apiKey=${HERE_API_KEY}"

echo "=== Account Projects ==="
curl -s "https://account.api.here.com/authorization/v1.1/projects" \
  -H "Authorization: Bearer ${HERE_OAUTH_TOKEN}" | \
  jq -r '.[] | "\(.projectName) | ID: \(.projectId) | Status: \(.status)"' 2>/dev/null || echo "Check projects via HERE Platform Portal"

echo ""
echo "=== Service Endpoints Test ==="
echo "Geocoding:"
curl -s -o /dev/null -w "Status: %{http_code}\n" \
  "https://geocode.search.hereapi.com/v1/geocode?q=test&$AUTH"
echo "Routing:"
curl -s -o /dev/null -w "Status: %{http_code}\n" \
  "https://router.hereapi.com/v8/routes?transportMode=car&origin=52.5,13.4&destination=52.5,13.5&$AUTH"
echo "Search:"
curl -s -o /dev/null -w "Status: %{http_code}\n" \
  "https://discover.search.hereapi.com/v1/discover?at=52.5,13.4&q=restaurant&$AUTH"
echo "Map Tiles:"
curl -s -o /dev/null -w "Status: %{http_code}\n" \
  "https://maps.hereapi.com/v3/base/mc/12/2200/1343/png?style=explore.day&$AUTH"

echo ""
echo "=== API Key Info ==="
curl -s "https://account.api.here.com/authorization/v1.1/apikeys" \
  -H "Authorization: Bearer ${HERE_OAUTH_TOKEN}" | \
  jq -r '.items[] | "\(.id) | Created: \(.createdTime) | Enabled: \(.enabled)"' 2>/dev/null || echo "API key management requires OAuth token"
```

**Phase 1 outputs:** Projects, service health, API keys

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Usage Statistics ==="
curl -s "https://tracking.api.here.com/v2/usage" \
  -H "Authorization: Bearer ${HERE_OAUTH_TOKEN}" 2>/dev/null | \
  jq -r '.[] | "\(.service): \(.count) requests"' || echo "Usage stats require portal access"

echo ""
echo "=== Geocoding Quality Check ==="
curl -s "https://geocode.search.hereapi.com/v1/geocode?q=1600+Pennsylvania+Ave+Washington+DC&$AUTH" | \
  jq -r '.items[0] | "Match: \(.title)\nScore: \(.scoring.queryScore)\nType: \(.resultType)\nPosition: \(.position.lat),\(.position.lng)"'

echo ""
echo "=== Routing Health Check ==="
curl -s "https://router.hereapi.com/v8/routes?transportMode=car&origin=52.5308,13.3847&destination=48.8566,2.3522&return=summary&$AUTH" | \
  jq -r '.routes[0].sections[0].summary | "Distance: \(.length/1000)km\nDuration: \(.duration/60)min\nBaseDuration: \(.baseDuration/60)min"'

echo ""
echo "=== Rate Limit Headers ==="
curl -s -I "https://geocode.search.hereapi.com/v1/geocode?q=test&$AUTH" | \
  grep -i "x-rate-limit\|x-ratelimit" || echo "Rate limit info not in headers"
```

## Output Format

```
HERE MAPS STATUS
================
Projects: {count}
Services: Geocoding={status} Routing={status} Search={status} Tiles={status}
API Keys: {count} ({enabled}/{total} enabled)
Usage (period): {total_requests} requests
Rate Limits: {remaining}/{limit}
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

- **API key vs OAuth**: Simple API key for most services; OAuth 2.0 for management APIs
- **Freemium limits**: 250K transactions/month free — monitor to avoid overage
- **HERE vs legacy Nokia**: Use hereapi.com endpoints — legacy.here.com is deprecated
- **Rate limits**: Vary by plan — check response headers for current limits
