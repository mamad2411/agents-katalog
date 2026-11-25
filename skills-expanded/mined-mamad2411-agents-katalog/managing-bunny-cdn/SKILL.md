---
name: managing-bunny-cdn
description: |
  Use when working with Bunny Cdn — bunny.net CDN management covering pull
  zones, storage zones, edge rules, cache configuration, and bandwidth
  analytics. Use when managing Bunny CDN pull zones, analyzing traffic patterns,
  configuring edge rules, monitoring cache hit ratios, or managing Bunny storage
  for origin content.
connection_type: bunnycdn
preload: false
---

# Bunny CDN Skill

Manage Bunny.net CDN pull zones, storage zones, edge rules, and delivery analytics.

## Core Helper Functions

```bash
#!/bin/bash

BUNNY_API="https://api.bunny.net"

# Bunny API wrapper
bunny_api() {
    local endpoint="$1"
    shift
    curl -s -H "AccessKey: $BUNNY_API_KEY" \
         -H "Content-Type: application/json" \
         "$BUNNY_API/$endpoint" "$@"
}

# Get statistics
bunny_stats() {
    local start="${1:-$(date -u -d '7 days ago' +%Y-%m-%dT00:00:00Z 2>/dev/null || date -u -v-7d +%Y-%m-%dT00:00:00Z)}"
    local end="${2:-$(date -u +%Y-%m-%dT23:59:59Z)}"
    bunny_api "statistics?dateFrom=$start&dateTo=$end"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Pull Zones ==="
bunny_api "pullzone" | jq -r '
    .[] | "\(.Id)\t\(.Name)\t\(.OriginUrl // "storage")\t\(.Enabled)\t\(.MonthlyBandwidthUsed / 1073741824 | round)GB/mo"
' | column -t | head -20

echo ""
echo "=== Storage Zones ==="
bunny_api "storagezone" | jq -r '
    .[] | "\(.Id)\t\(.Name)\t\(.StorageUsed / 1073741824 * 100 | round / 100)GB\t\(.FilesStored) files\tRegion: \(.Region)"
' | column -t | head -15

echo ""
echo "=== Traffic Summary (7d) ==="
bunny_stats | jq '{
    TotalRequests: .TotalRequestsServed,
    CacheHitRate: (.CacheHitRate | round),
    BandwidthUsed: (.TotalBandwidthUsed / 1073741824 | round),
    AverageOriginResponseTime: .AverageOriginResponseTime
}'
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE_ID="${1:?Pull zone ID required}"

echo "=== Pull Zone Config ==="
bunny_api "pullzone/$ZONE_ID" | jq '{
    Name, OriginUrl, Enabled, CacheControlMaxAgeOverride,
    EnableGeoZoneUS: .EnableGeoZoneUS,
    EnableGeoZoneEU: .EnableGeoZoneEU,
    EnableGeoZoneASIA: .EnableGeoZoneASIA,
    EnableCacheSlice: .EnableCacheSlice,
    EnableSmartCache: .EnableSmartCache,
    WAFEnabled: .WAFEnabled,
    AllowedReferrers: .AllowedReferrers,
    BlockedReferrers: .BlockedReferrers
}'

echo ""
echo "=== Edge Rules ==="
bunny_api "pullzone/$ZONE_ID/edgerules" | jq -r '
    .[] | "\(.Guid[:8])\t\(.ActionType)\t\(.TriggerMatchingType)\t\(.Enabled)\t\(.Description // "no desc")"
' | column -t | head -15

echo ""
echo "=== Hostnames ==="
bunny_api "pullzone/$ZONE_ID" | jq -r '
    .Hostnames[] | "\(.Value)\t\(.ForceSSL)\tCert: \(.HasCertificate)"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse Bunny API JSON responses
- Convert bytes to GB for bandwidth display (divide by 1073741824)

## Safety Rules
- **Read-only by default**: Use GET endpoints for inspection
- **Never purge cache** without explicit confirmation -- impacts performance
- **Edge rule changes** take effect within seconds globally
- **Storage zone deletion** is permanent and cannot be undone

## Output Format

Present results as a structured report:
```
Managing Bunny Cdn Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

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
- **API key types**: Account API key vs Storage Zone API key have different permissions
- **Bandwidth is in bytes**: Always convert for human-readable output
- **Cache slice**: Large file optimization -- should only be enabled for video/large file delivery
- **Geo zones**: Disabling a geo zone removes content from that region's POPs
- **Origin shield**: Reduces origin load but adds latency -- enable only for high-traffic zones
