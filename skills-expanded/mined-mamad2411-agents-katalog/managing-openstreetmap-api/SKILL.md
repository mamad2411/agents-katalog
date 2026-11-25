---
name: managing-openstreetmap-api
description: |
  Use when working with Openstreetmap Api — openStreetMap API and related
  services management including Nominatim geocoding, Overpass API queries, tile
  server health, changeset monitoring, and data quality checks. Covers API
  endpoint health, usage policy compliance, response latency, and data freshness
  monitoring.
connection_type: openstreetmap-api
preload: false
---

# OpenStreetMap API Management Skill

Monitor and manage OpenStreetMap API services and data access.

## MANDATORY: Discovery-First Pattern

**Always check API endpoint health and usage policies before running queries.**

### Phase 1: Discovery

```bash
#!/bin/bash
OSM_API="https://api.openstreetmap.org/api/0.6"
NOMINATIM="${NOMINATIM_URL:-https://nominatim.openstreetmap.org}"
OVERPASS="${OVERPASS_URL:-https://overpass-api.de/api}"

echo "=== OSM API Status ==="
curl -s "$OSM_API/capabilities" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
api = root.find('.//api')
print(f'Version Range: {api.find(\"version\").get(\"minimum\")}-{api.find(\"version\").get(\"maximum\")}')
print(f'Area Max: {api.find(\"area\").get(\"maximum\")}')
print(f'Changesets Max: {api.find(\"changesets\").get(\"maximum_elements\")}')
print(f'Waynodes Max: {api.find(\"waynodes\").get(\"maximum\")}')
" 2>/dev/null || echo "OSM API not reachable"

echo ""
echo "=== Nominatim Health ==="
curl -s -o /dev/null -w "Status: %{http_code} | Time: %{time_total}s\n" \
  "$NOMINATIM/status.php"
curl -s "$NOMINATIM/status.php" 2>/dev/null

echo ""
echo "=== Overpass API Status ==="
curl -s "$OVERPASS/status" | head -5

echo ""
echo "=== Tile Server Health ==="
curl -s -o /dev/null -w "Tile Server: %{http_code} | Time: %{time_total}s\n" \
  "https://tile.openstreetmap.org/1/0/0.png" \
  -H "User-Agent: ${OSM_USER_AGENT:-SkillCheck/1.0}"
```

**Phase 1 outputs:** API capabilities, Nominatim status, Overpass status, tile server health

### Phase 2: Analysis

```bash
#!/bin/bash
UA="-H 'User-Agent: ${OSM_USER_AGENT:-SkillCheck/1.0}'"

echo "=== Nominatim Geocoding Test ==="
curl -s "$NOMINATIM/search?q=New+York&format=json&limit=1" \
  -H "User-Agent: ${OSM_USER_AGENT:-SkillCheck/1.0}" | \
  jq -r '.[0] | "Result: \(.display_name)\nLat: \(.lat) Lon: \(.lon)\nType: \(.type)"'

echo ""
echo "=== Nominatim Reverse Test ==="
curl -s "$NOMINATIM/reverse?lat=40.748817&lon=-73.985428&format=json" \
  -H "User-Agent: ${OSM_USER_AGENT:-SkillCheck/1.0}" | \
  jq -r '"Address: \(.display_name)\nType: \(.type)"'

echo ""
echo "=== Overpass Query Test (small area) ==="
curl -s "$OVERPASS/interpreter" \
  -H "User-Agent: ${OSM_USER_AGENT:-SkillCheck/1.0}" \
  --data-urlencode 'data=[out:json][timeout:10];node["amenity"="restaurant"](40.74,-73.99,40.75,-73.98);out count;' | \
  jq -r '"Restaurants in sample area: \(.elements[0].tags.total // .elements | length)"'

echo ""
echo "=== Recent Changesets (area sample) ==="
curl -s "$OSM_API/changesets?bbox=-73.99,40.74,-73.98,40.75&limit=5" | \
  python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
for cs in root.findall('.//changeset')[:5]:
    print(f'ID: {cs.get(\"id\")} | User: {cs.get(\"user\")} | Changes: {cs.get(\"changes_count\")} | {cs.get(\"created_at\")}')
" 2>/dev/null || echo "Changeset query complete"
```

## Output Format

```
OPENSTREETMAP API STATUS
========================
OSM API: {status} (v{version})
Nominatim: {status} ({latency}ms)
Overpass: {status} (slots: {available}/{total})
Tile Server: {status}
Data Freshness: {last_update}
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

- **Usage policy**: Public Nominatim requires User-Agent and max 1 req/sec — use your own instance for heavy use
- **Overpass timeouts**: Complex queries can timeout — set timeout parameter and limit area
- **No API key needed**: OSM is open — but rate limits are enforced by policy
- **Tile usage policy**: Max 2 tile downloads/sec on public servers — use commercial providers for production
