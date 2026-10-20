---
name: managing-cloudflare-dns-deep
description: |
  Use when working with Cloudflare Dns Deep — advanced Cloudflare DNS management
  covering zone records, DNSSEC configuration, DNS analytics, load balancing
  pools, health checks, and DNS firewall. Use for deep DNS record management,
  DNSSEC troubleshooting, DNS traffic analytics, configuring DNS-based load
  balancing, or auditing DNS security settings.
connection_type: cloudflare
preload: false
---

# Cloudflare DNS Deep Skill

Advanced Cloudflare DNS management including records, DNSSEC, analytics, load balancing, and DNS firewall.

## Core Helper Functions

```bash
#!/bin/bash

CF_API="https://api.cloudflare.com/client/v4"

cf_api() {
    local endpoint="$1"
    shift
    curl -s -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
         -H "Content-Type: application/json" \
         "$CF_API/$endpoint" "$@"
}

cf_zone_id() {
    local zone="$1"
    cf_api "zones?name=$zone" | jq -r '.result[0].id'
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Zones ==="
cf_api "zones?per_page=50" | jq -r '
    .result[] | "\(.id[:12])\t\(.name)\t\(.status)\t\(.name_servers | join(", "))"
' | column -t | head -15

echo ""
echo "=== DNSSEC Status ==="
for ZID in $(cf_api "zones?per_page=50" | jq -r '.result[].id'); do
    cf_api "zones/$ZID/dnssec" | jq -r --arg zid "$ZID" '"\($zid[:12])\t\(.result.status)\t\(.result.algorithm // "n/a")"'
done | column -t | head -15

echo ""
echo "=== DNS Records Summary ==="
for ZID in $(cf_api "zones?per_page=10" | jq -r '.result[].id'); do
    ZONE_NAME=$(cf_api "zones/$ZID" | jq -r '.result.name')
    COUNTS=$(cf_api "zones/$ZID/dns_records?per_page=1000" | jq -r '[.result[].type] | group_by(.) | map("\(.[0]): \(length)") | join("  ")')
    echo "$ZONE_NAME: $COUNTS"
done | head -10

echo ""
echo "=== Load Balancers ==="
cf_api "user/load_balancers/pools" | jq -r '
    .result[]? | "\(.id[:12])\t\(.name)\t\(.enabled)\t\(.origins | length) origins\t\(.healthy)"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
ZONE_ID="${1:?Zone ID required}"

echo "=== All DNS Records ==="
cf_api "zones/$ZONE_ID/dns_records?per_page=500" | jq -r '
    .result[] | "\(.type)\t\(.name)\t\(.content[:50])\t\(.ttl)\t\(.proxied)"
' | sort | column -t | head -30

echo ""
echo "=== DNS Analytics (24h) ==="
cf_api "zones/$ZONE_ID/dns_analytics/report?dimensions=queryType&since=-1440&limit=20" | jq -r '
    .result.data[]? | "\(.dimensions[0])\tQueries: \(.metrics[0])"
' | column -t | head -10

echo ""
echo "=== Health Checks ==="
cf_api "zones/$ZONE_ID/healthchecks" | jq -r '
    .result[]? | "\(.id[:12])\t\(.name)\t\(.status)\t\(.type)\t\(.address)\t\(.interval)s"
' | column -t | head -10

echo ""
echo "=== DNSSEC Details ==="
cf_api "zones/$ZONE_ID/dnssec" | jq '.result | {status, algorithm, digest, digest_type, ds, key_tag, flags}'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Sort DNS records by type for readability
- Truncate long DKIM/TXT record content

## Safety Rules
- **Read-only by default**: Use list/get endpoints for inspection
- **Never delete DNS records** without explicit confirmation -- causes outages
- **DNSSEC changes** can break resolution if DS record is not updated at registrar
- **Proxied vs DNS-only**: Changing proxy status affects security and performance

## Output Format

Present results as a structured report:
```
Managing Cloudflare Dns Deep Report
═══════════════════════════════════
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
- **Proxied records**: Only A, AAAA, and CNAME can be proxied; MX/TXT cannot
- **TTL for proxied records**: Cloudflare auto-manages TTL for proxied records (shows as 1)
- **CNAME flattening**: Cloudflare flattens CNAME at zone apex automatically
- **DNS propagation**: Changes are fast within Cloudflare but downstream caches may hold old records
- **API pagination**: Default is 20 records per page; use per_page=500 for full zone export
