---
name: managing-gcp-cloud-cdn
description: |
  Use when working with Gcp Cloud Cdn — google Cloud CDN management covering
  backend services, URL maps, cache configuration, SSL policies, Cloud Armor
  integration, and CDN metrics. Use when managing GCP Cloud CDN backends,
  analyzing cache hit ratios, configuring cache keys, or troubleshooting content
  delivery via Google's global edge network.
connection_type: gcp
preload: false
---

# GCP Cloud CDN Skill

Manage Google Cloud CDN backends, cache policies, URL maps, and edge performance.

## Core Helper Functions

```bash
#!/bin/bash

# List backend services with CDN enabled
gcp_cdn_backends() {
    gcloud compute backend-services list --filter="enableCDN=true" --format=json 2>/dev/null
}

# Get backend service detail
gcp_cdn_backend() {
    local name="$1" scope="${2:---global}"
    gcloud compute backend-services describe "$name" "$scope" --format=json 2>/dev/null
}

# Get CDN metrics
gcp_cdn_metric() {
    local filter="$1" days="${2:-7}"
    local end_time start_time
    end_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    start_time=$(date -u -d "$days days ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -v-${days}d +"%Y-%m-%dT%H:%M:%SZ")
    gcloud monitoring time-series list --filter="$filter" \
        --interval-start-time="$start_time" --interval-end-time="$end_time" \
        --format=json 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== CDN-Enabled Backend Services ==="
gcloud compute backend-services list --filter="enableCDN=true" \
    --format="table(name,protocol,backends[0].group.basename(),cdnPolicy.cacheMode,loadBalancingScheme)" 2>/dev/null | head -20

echo ""
echo "=== URL Maps ==="
gcloud compute url-maps list \
    --format="table(name,defaultService.basename(),hostRules.len())" 2>/dev/null | head -15

echo ""
echo "=== SSL Certificates ==="
gcloud compute ssl-certificates list \
    --format="table(name,type,managed.status,managed.domainStatus,expireTime)" 2>/dev/null | head -15

echo ""
echo "=== Target HTTPS Proxies ==="
gcloud compute target-https-proxies list \
    --format="table(name,urlMap.basename(),sslCertificates.len(),sslPolicy.basename())" 2>/dev/null | head -10

echo ""
echo "=== Cloud Armor Policies ==="
gcloud compute security-policies list \
    --format="table(name,type,rules.len())" 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
BACKEND="${1:?Backend service name required}"

echo "=== Backend CDN Config ==="
gcloud compute backend-services describe "$BACKEND" --global --format=json 2>/dev/null | jq '{
    name, enableCDN,
    cacheMode: .cdnPolicy.cacheMode,
    defaultTtl: .cdnPolicy.defaultTtl,
    maxTtl: .cdnPolicy.maxTtl,
    clientTtl: .cdnPolicy.clientTtl,
    negativeCaching: .cdnPolicy.negativeCaching,
    serveWhileStale: .cdnPolicy.serveWhileStale,
    cacheKeyPolicy: .cdnPolicy.cacheKeyPolicy
}'

echo ""
echo "=== Backend Health ==="
gcloud compute backend-services get-health "$BACKEND" --global --format=json 2>/dev/null | jq '
    .[].status.healthStatus[]? | "\(.instance | split("/") | last)\t\(.healthState)\t\(.ipAddress)"
' | column -t | head -15

echo ""
echo "=== Cache Hit Metrics ==="
gcloud logging read "resource.type=http_load_balancer AND resource.labels.backend_service_name=$BACKEND AND timestamp>=\"$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-1H +%Y-%m-%dT%H:%M:%SZ)\"" \
    --format=json --limit=100 2>/dev/null | jq -r '
    [.[] | .jsonPayload.cacheHit // false] | {total: length, hits: [.[] | select(. == true)] | length} |
    "Total: \(.total)  Hits: \(.hits)  Ratio: \(if .total > 0 then (.hits / .total * 100 | round) else 0 end)%"
'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Use `gcloud` CLI with `--format=json` and jq for parsing
- Use `--format=table(...)` for quick summaries

## Safety Rules
- **Read-only by default**: Use list/describe/get-health for inspection
- **Never disable CDN** on production backends without confirmation
- **Cache invalidation** can take several minutes to propagate to all edge POPs
- **Security policy changes** via Cloud Armor take effect immediately

## Output Format

Present results as a structured report:
```
Managing Gcp Cloud Cdn Report
═════════════════════════════
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
- **CDN is per-backend-service** not per-URL-map -- must enable on each backend
- **Cache modes**: CACHE_ALL_STATIC, USE_ORIGIN_HEADERS, FORCE_CACHE_ALL behave differently
- **Signed URLs/cookies**: Required for private content; misconfiguration causes 403s
- **Cache key includes host by default**: Different domains hitting same backend get separate cache entries
- **Health checks**: CDN does not cache responses from unhealthy backends
