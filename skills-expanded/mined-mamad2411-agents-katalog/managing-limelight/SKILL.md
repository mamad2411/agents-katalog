---
name: managing-limelight
description: |
  Use when working with Limelight — limelight Networks (Edgio) CDN management
  covering delivery configurations, origin settings, cache policies, SSL
  certificates, and real-time analytics. Use when managing Limelight/Edgio CDN
  properties, analyzing delivery performance, configuring caching behavior, or
  troubleshooting content delivery issues across edge POPs.
connection_type: limelight
preload: false
---

# Limelight Networks (Edgio) CDN Skill

Manage Limelight/Edgio CDN delivery configurations, origins, caching, and performance.

## Core Helper Functions

```bash
#!/bin/bash

LL_API="https://apis.llnw.com/config-api/v1"

# Limelight API wrapper
ll_api() {
    local endpoint="$1"
    shift
    curl -s -u "$LIMELIGHT_USERNAME:$LIMELIGHT_API_KEY" \
         -H "Content-Type: application/json" \
         "$LL_API/$endpoint" "$@"
}

# Edgio API wrapper (newer platform)
edgio_api() {
    local endpoint="$1"
    shift
    curl -s -H "Authorization: Bearer $EDGIO_API_TOKEN" \
         -H "Content-Type: application/json" \
         "https://edgioapis.com/$endpoint" "$@"
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Delivery Service Instances ==="
ll_api "delivery/service-instances" | jq -r '
    .list[]? | "\(.uuid[:12])\t\(.shortname)\t\(.status)\t\(.serviceProfileName)"
' | column -t | head -20

echo ""
echo "=== Published Hostnames ==="
ll_api "delivery/service-instances" | jq -r '
    .list[]? | .publishedHostnames[]? | "\(.hostname)\t\(.status)"
' | column -t | head -15

echo ""
echo "=== Origin Configurations ==="
ll_api "delivery/service-instances" | jq -r '
    .list[]? | "\(.shortname)\t\(.sourceHostname)\t\(.sourceProtocol // "HTTP")"
' | column -t | head -15

echo ""
echo "=== SSL Certificates ==="
ll_api "certs" | jq -r '
    .list[]? | "\(.uuid[:12])\t\(.commonName)\t\(.status)\t\(.expirationDate[:10])"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
SERVICE_ID="${1:?Service instance UUID required}"

echo "=== Service Configuration ==="
ll_api "delivery/service-instances/$SERVICE_ID" | jq '{
    shortname, status, serviceProfileName,
    sourceHostname, sourceProtocol,
    publishedHostnames: [.publishedHostnames[]?.hostname],
    cacheControl: .cacheControl,
    protocolSettings: .protocolSettings
}'

echo ""
echo "=== Cache Configuration ==="
ll_api "delivery/service-instances/$SERVICE_ID" | jq '{
    cacheControlHeaderOverride: .cacheControlHeaderOverride,
    honorOriginCacheControl: .honorOriginCacheControl,
    defaultTTL: .defaultTTL,
    maxTTL: .maxTTL,
    cacheKeyModifiers: .cacheKeyModifiers
}'

echo ""
echo "=== Performance Settings ==="
ll_api "delivery/service-instances/$SERVICE_ID" | jq '{
    gzipEnabled: .gzipEnabled,
    http2Enabled: .http2Enabled,
    prefetchEnabled: .prefetchEnabled,
    originShield: .originShield
}'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use jq to parse Limelight/Edgio API JSON responses
- Identify platform version (legacy Limelight vs Edgio) in output

## Safety Rules
- **Read-only by default**: Use GET endpoints for inspection
- **Never invalidate cache** without explicit user confirmation
- **Configuration changes** require publishing before taking effect
- **SSL certificate updates** may cause brief connection disruptions

## Output Format

Present results as a structured report:
```
Managing Limelight Report
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
- **Limelight vs Edgio APIs**: Platform is transitioning; some accounts use legacy APIs
- **Published vs draft**: Configuration changes are drafted first, then published
- **Cache key normalization**: Query string handling varies by configuration
- **Origin shield**: Reduces origin load but may add latency for cache misses
- **Service profiles**: Different profiles have different feature sets and pricing
