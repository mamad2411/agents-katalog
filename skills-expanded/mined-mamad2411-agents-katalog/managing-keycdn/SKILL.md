---
name: managing-keycdn
description: |
  Use when working with Keycdn — keyCDN management covering zones, zone aliases,
  cache settings, SSL certificates, and usage analytics. Use when managing
  KeyCDN zones, analyzing bandwidth and request metrics, configuring cache
  behavior, managing SSL, or troubleshooting content delivery through KeyCDN's
  edge network.
connection_type: keycdn
preload: false
---

# KeyCDN Skill

Manage KeyCDN zones, cache settings, zone aliases, and delivery analytics.

## Core Helper Functions

```bash
#!/bin/bash

KEYCDN_API="https://api.keycdn.com"

# KeyCDN API wrapper (uses HTTP Basic Auth)
keycdn_api() {
    local endpoint="$1"
    shift
    curl -s -u "$KEYCDN_API_KEY:" "$KEYCDN_API/$endpoint.json" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== KeyCDN Zones ==="
keycdn_api "zones" | jq -r '
    .data.zones[] | "\(.id)\t\(.name)\t\(.status)\t\(.type)\t\(.originurl)\t\(.sslcert)"
' | column -t | head -20

echo ""
echo "=== Zone Aliases ==="
keycdn_api "zonealiases" | jq -r '
    .data.zonealiases[] | "\(.id)\t\(.zone_id)\t\(.name)\t\(.sslstatus)"
' | column -t | head -15

echo ""
echo "=== Traffic Statistics (24h) ==="
keycdn_api "reports/traffic" | jq -r '
    .data.stats[] | "\(.zone_id)\t\(.amount / 1073741824 | round)GB\tRequests: \(.requests // 0)"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE_ID="${1:?Zone ID required}"

echo "=== Zone Configuration ==="
keycdn_api "zones/$ZONE_ID" | jq '.data.zone | {
    name, status, type, originurl,
    cacheignorecachecontrol, cacheignorequerystring,
    cachestripcookies, cachekeyscheme,
    cachecanonicalheader, expire: .expire,
    sslcert, forcesslconnection,
    gzip, http2, imgproc
}'

echo ""
echo "=== Bandwidth Report ==="
keycdn_api "reports/traffic?zone_id=$ZONE_ID" | jq -r '
    .data.stats[] | "\(.timestamp | todate)\t\(.amount / 1048576 | round)MB\t\(.requests) reqs"
' | column -t | head -15

echo ""
echo "=== Cache Status Report ==="
keycdn_api "reports/statestats?zone_id=$ZONE_ID" | jq -r '
    .data.stats[] | "\(.timestamp | todate)\tHIT: \(.hit // 0)\tMISS: \(.miss // 0)\tSHIELD: \(.shield // 0)"
' | column -t | head -10

echo ""
echo "=== HTTP Status Codes ==="
keycdn_api "reports/credits?zone_id=$ZONE_ID" | jq -r '
    .data.stats[] | "\(.timestamp | todate)\t2xx: \(.s2xx // 0)\t3xx: \(.s3xx // 0)\t4xx: \(.s4xx // 0)\t5xx: \(.s5xx // 0)"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse KeyCDN JSON responses
- Convert bytes to GB/MB for bandwidth display

## Safety Rules
- **Read-only by default**: Use GET endpoints for inspection
- **Never purge zones** without explicit user confirmation
- **Zone alias SSL** provisioning requires DNS validation first
- **Zone deletion** is permanent -- confirm before proceeding

## Output Format

Present results as a structured report:
```
Managing Keycdn Report
══════════════════════
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
- **API authentication**: Uses HTTP Basic Auth with API key as username, empty password
- **Zone types**: Pull vs Push zones have different configuration options
- **Cache expiry**: Default TTL is set per zone; origin headers can override if configured
- **SSL cert provisioning**: Shared SSL is automatic; custom certs require manual upload
- **Rate limits**: API is rate-limited; batch queries when possible
