---
name: managing-imperva-cdn
description: |
  Use when working with Imperva Cdn — imperva (Incapsula) CDN and application
  security management covering site configuration, caching rules, WAF policies,
  DDoS protection, SSL settings, and performance analytics. Use when managing
  Imperva CDN delivery, analyzing security events, configuring WAF rules, or
  troubleshooting content delivery and protection settings.
connection_type: imperva
preload: false
---

# Imperva CDN & Security Skill

Manage Imperva CDN delivery, WAF policies, DDoS protection, caching, and security analytics.

## Core Helper Functions

```bash
#!/bin/bash

IMPERVA_API="https://my.imperva.com/api/prov/v1"
IMPERVA_API_V2="https://api.imperva.com"

# Imperva API wrapper (v1)
imperva_api() {
    local endpoint="$1"
    shift
    curl -s -X POST "$IMPERVA_API/$endpoint" \
        -d "api_id=$IMPERVA_API_ID&api_key=$IMPERVA_API_KEY" "$@"
}

# Imperva API wrapper (v2/v3)
imperva_api_v2() {
    local endpoint="$1"
    shift
    curl -s -H "x-API-Id: $IMPERVA_API_ID" \
         -H "x-API-Key: $IMPERVA_API_KEY" \
         -H "Content-Type: application/json" \
         "$IMPERVA_API_V2/$endpoint" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Sites ==="
imperva_api "sites/list" -d "page_size=50" | jq -r '
    .sites[]? | "\(.site_id)\t\(.domain)\t\(.status)\t\(.acceleration_level)\t\(.ssl.origin_server.detected)"
' | column -t | head -20

echo ""
echo "=== WAF Rules Summary ==="
for SITE_ID in $(imperva_api "sites/list" -d "page_size=10" | jq -r '.sites[]?.site_id'); do
    echo "--- Site $SITE_ID ---"
    imperva_api "sites/configure/security" -d "site_id=$SITE_ID&rule_id=api.threats.sql_injection" | jq -r '.security.waf | "\(.rules | length) rules active"' 2>/dev/null
done | head -15

echo ""
echo "=== DDoS Protection Status ==="
imperva_api "sites/list" -d "page_size=50" | jq -r '
    .sites[]? | "\(.domain)\tDDoS: \(.ddos_protection // "default")\tBot: \(.bot_management // "default")"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
SITE_ID="${1:?Site ID required}"

echo "=== Site Configuration ==="
imperva_api "sites/status" -d "site_id=$SITE_ID" | jq '{
    domain: .domain, status: .status,
    acceleration_level, active_ssl: .ssl,
    dns: [.dns[]? | {set_type_to: .set_type_to, set_data_to: .set_data_to}]
}'

echo ""
echo "=== Cache Settings ==="
imperva_api "sites/performance/cache-mode" -d "site_id=$SITE_ID" | jq '{
    cache_mode, aggressive_cache, dynamic_cache,
    cache_headers, cache_300x, cache_404
}'

echo ""
echo "=== Security Events (24h) ==="
imperva_api_v2 "api/v1/sites/$SITE_ID/visits?security=true&page_size=20" | jq -r '
    .visits[]? | "\(.country)\t\(.client_type)\t\(.action)\t\(.threats[0]?.id // "none")"
' | column -t | head -15

echo ""
echo "=== WAF Policy Status ==="
for rule in sql_injection cross_site_scripting illegal_resource_access remote_file_inclusion; do
    STATUS=$(imperva_api "sites/configure/security" -d "site_id=$SITE_ID&rule_id=api.threats.$rule" | jq -r '.security_rule.action // "N/A"')
    echo "$rule: $STATUS"
done

echo ""
echo "=== Performance Metrics ==="
imperva_api "sites/stats" -d "site_id=$SITE_ID&stats=visits_timeseries,bandwidth_timeseries,caching_timeseries&time_range=last_7_days" | jq '{
    total_visits: .visits_timeseries[-1:],
    bandwidth: .bandwidth_timeseries[-1:],
    cache_hit_rate: .caching_timeseries[-1:]
}' 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse Imperva API JSON responses
- Note that v1 API uses POST with form data, v2/v3 use JSON

## Safety Rules
- **Read-only by default**: Use list/status endpoints for inspection
- **WAF rule changes** take effect immediately -- test in alert-only mode first
- **Never disable DDoS protection** without explicit confirmation
- **Cache purge** impacts performance -- confirm before executing

## Output Format

Present results as a structured report:
```
Managing Imperva Cdn Report
═══════════════════════════
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
- **API v1 vs v2**: Different authentication and request formats; check endpoint version
- **WAF action modes**: alert (log only), block, captcha -- start with alert
- **SSL integration**: Origin SSL must be configured separately from edge SSL
- **Bot management**: Aggressive settings can block legitimate crawlers/bots
- **Rate limiting**: API has rate limits; batch queries when possible
