---
name: managing-fastly-compute
description: |
  Use when working with Fastly Compute — fastly Compute@Edge service management
  covering service inventory, package deployments, backend health, domain
  mappings, VCL/Wasm configuration, real-time analytics, cache hit ratios, and
  edge dictionary inspection. Use for Fastly CDN and edge compute analysis.
connection_type: fastly
preload: false
---

# Fastly Compute Management

Analyze Fastly Compute@Edge services, backends, and edge performance.

## Phase 1: Discovery

```bash
#!/bin/bash
API_TOKEN="${FASTLY_API_TOKEN}"
BASE="https://api.fastly.com"

echo "=== Services Inventory ==="
curl -s "${BASE}/service" \
  -H "Fastly-Key: ${API_TOKEN}" \
  | jq -r '.[] | "\(.id)\t\(.name)\t\(.type)\t\(.active_version)\t\(.updated_at)"' \
  | column -t | head -20

echo ""
echo "=== Service Details with Backends ==="
for SVC_ID in $(curl -s "${BASE}/service" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.[].id'); do
  VERSION=$(curl -s "${BASE}/service/${SVC_ID}" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.active_version // .versions[-1].number')
  echo "--- Service: ${SVC_ID} (v${VERSION}) ---"
  curl -s "${BASE}/service/${SVC_ID}/version/${VERSION}/backend" \
    -H "Fastly-Key: ${API_TOKEN}" \
    | jq -r '.[] | "\(.name)\t\(.address):\(.port)\t\(.ssl_cert_hostname // "no-ssl")\t\(.weight)"' \
    | column -t
done | head -30

echo ""
echo "=== Domains ==="
for SVC_ID in $(curl -s "${BASE}/service" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.[].id'); do
  VERSION=$(curl -s "${BASE}/service/${SVC_ID}" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.active_version')
  curl -s "${BASE}/service/${SVC_ID}/version/${VERSION}/domain" \
    -H "Fastly-Key: ${API_TOKEN}" \
    | jq -r ".[] | \"${SVC_ID}\t\(.name)\""
done | column -t | head -20
```

## Phase 2: Analysis

```bash
#!/bin/bash
API_TOKEN="${FASTLY_API_TOKEN}"
BASE="https://api.fastly.com"
FROM=$(date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -u -v-1d +"%Y-%m-%dT%H:%M:%S")
TO=$(date -u +"%Y-%m-%dT%H:%M:%S")

echo "=== Real-Time Stats (last 120s) ==="
for SVC_ID in $(curl -s "${BASE}/service" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.[].id' | head -5); do
  curl -s "${BASE}/service/${SVC_ID}/stats?from=-120seconds" \
    -H "Fastly-Key: ${API_TOKEN}" \
    | jq '.data[] | {
        service_id: .service_id,
        requests: .requests,
        hits: .hits,
        miss: .miss,
        hit_ratio: (if .requests > 0 then (.hits / .requests * 100 | floor | tostring + "%") else "N/A" end),
        bandwidth_mb: (.bandwidth / 1048576 | floor),
        errors: .errors,
        status_5xx: .status_5xx
      }' 2>/dev/null
done

echo ""
echo "=== Edge Dictionaries ==="
for SVC_ID in $(curl -s "${BASE}/service" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.[].id'); do
  VERSION=$(curl -s "${BASE}/service/${SVC_ID}" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.active_version')
  curl -s "${BASE}/service/${SVC_ID}/version/${VERSION}/dictionary" \
    -H "Fastly-Key: ${API_TOKEN}" \
    | jq -r ".[] | \"${SVC_ID}\t\(.name)\t\(.item_count) items\""
done | column -t

echo ""
echo "=== Health Check Status ==="
for SVC_ID in $(curl -s "${BASE}/service" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.[].id'); do
  VERSION=$(curl -s "${BASE}/service/${SVC_ID}" -H "Fastly-Key: ${API_TOKEN}" | jq -r '.active_version')
  curl -s "${BASE}/service/${SVC_ID}/version/${VERSION}/healthcheck" \
    -H "Fastly-Key: ${API_TOKEN}" \
    | jq -r '.[] | "\(.name)\t\(.host)\t\(.path)\t\(.threshold)"'
done | column -t
```

## Output Format

```
FASTLY COMPUTE ANALYSIS
========================
Service            Backends  Domains  Hit%   Requests  5xx  BW-MB
───────────────────────────────────────────────────────────────────
my-app-prod        3         2        94%    125000    12   4500
api-gateway        2         1        78%    89000     45   1200

Edge Dictionaries: 3 | Health Checks: 4 configured
```

## Safety Rules

- **Read-only**: Only use GET endpoints on the Fastly API
- **Never activate versions** or purge caches without explicit confirmation
- **Token scope**: Ensure token has read-only global scope
- **Rate limits**: Fastly API allows 1000 requests per hour per token

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

