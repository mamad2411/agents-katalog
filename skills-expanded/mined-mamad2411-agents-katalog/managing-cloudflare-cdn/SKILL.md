---
name: managing-cloudflare-cdn
description: |
  Use when working with Cloudflare Cdn — cloudflare CDN management including
  zone configuration, cache purging, page rules, firewall rules, SSL/TLS
  settings, and performance optimization. Covers cache analytics, bandwidth
  usage, threat detection, and edge certificate management. Use when managing
  Cloudflare CDN zones, analyzing cache performance, configuring page rules, or
  troubleshooting delivery issues.
connection_type: cloudflare
preload: false
---

# Cloudflare CDN Skill

Manage Cloudflare CDN zones, caching, page rules, firewall, and performance settings.

## Core Helper Functions

```bash
#!/bin/bash

CF_API="https://api.cloudflare.com/client/v4"

# Cloudflare API wrapper
cf_api() {
    local endpoint="$1"
    shift
    curl -s -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
         -H "Content-Type: application/json" \
         "$CF_API/$endpoint" "$@"
}

# Get zone ID by name
cf_zone_id() {
    local zone="$1"
    cf_api "zones?name=$zone" | jq -r '.result[0].id'
}
```

## MANDATORY: Discovery-First Pattern

**Always discover zones and current configuration before making changes.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Cloudflare Zones ==="
cf_api "zones?per_page=50" | jq -r '
    .result[] | "\(.id)\t\(.name)\t\(.status)\t\(.plan.name)\t\(.ssl.status // "n/a")"
' | column -t | head -20

echo ""
echo "=== Zone Analytics (24h) ==="
for ZONE_ID in $(cf_api "zones?per_page=10" | jq -r '.result[].id'); do
    cf_api "zones/$ZONE_ID/analytics/dashboard?since=-1440&continuous=true" | jq -r '
        .result.totals | "Requests: \(.requests.all)  Cached: \(.requests.cached)  Bandwidth: \(.bandwidth.all)  Threats: \(.threats.all)"
    '
done | head -10

echo ""
echo "=== SSL/TLS Status ==="
cf_api "zones?per_page=50" | jq -r '
    .result[] | "\(.name)\t\(.ssl.status // "n/a")\tHTTPS Rewrites: \(.https_rewrite // "n/a")"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE_ID="${1:?Zone ID required}"

echo "=== Cache Hit Ratio ==="
cf_api "zones/$ZONE_ID/analytics/dashboard?since=-1440&continuous=true" | jq -r '
    .result.totals | {
        total_requests: .requests.all,
        cached_requests: .requests.cached,
        uncached_requests: .requests.uncached,
        cache_hit_pct: (if .requests.all > 0 then (.requests.cached / .requests.all * 100 | round) else 0 end),
        bandwidth_saved: .bandwidth.cached
    }'

echo ""
echo "=== Page Rules ==="
cf_api "zones/$ZONE_ID/pagerules" | jq -r '
    .result[] | "\(.priority)\t\(.status)\t\(.targets[0].constraint.value)\t\(.actions[].id)"
' | column -t | head -15

echo ""
echo "=== Firewall Rules ==="
cf_api "zones/$ZONE_ID/firewall/rules" | jq -r '
    .result[] | "\(.id[:8])\t\(.action)\t\(.description // "no desc")\t\(.paused)"
' | column -t | head -15

echo ""
echo "=== Active Edge Certificates ==="
cf_api "zones/$ZONE_ID/ssl/certificate_packs" | jq -r '
    .result[] | "\(.type)\t\(.status)\t\(.hosts | join(","))"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse Cloudflare API JSON responses
- Always include zone name/ID for context

## Safety Rules
- **Read-only by default**: Use analytics and list endpoints for inspection
- **Never purge cache** without explicit user confirmation -- impacts performance
- **Page rule changes** can affect routing immediately -- validate before applying
- **Firewall rule caution**: Blocking rules can lock out legitimate traffic

## Output Format

Present results as a structured report:
```
Managing Cloudflare Cdn Report
══════════════════════════════
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
- **API rate limits**: Cloudflare limits to 1200 requests per 5 minutes per user
- **Zone ID vs name**: API endpoints use zone ID, not domain name
- **Cache purge propagation**: Takes up to 30 seconds to propagate globally
- **Page rule limits**: Free plan allows 3 page rules; order/priority matters
- **SSL modes**: Flexible, Full, Full (Strict) behave very differently for origin connections
