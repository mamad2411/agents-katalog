---
name: managing-cloudflare-workers-deep
description: |
  Use when working with Cloudflare Workers Deep — deep analysis of Cloudflare
  Workers deployments including script inventory, route mappings, KV namespace
  usage, Durable Objects, cron triggers, CPU time metrics, and error rate
  tracking. Use for comprehensive Workers platform health checks and
  optimization.
connection_type: cloudflare
preload: false
---

# Cloudflare Workers Deep Management

Comprehensive analysis of Cloudflare Workers scripts, bindings, routes, and performance.

## Phase 1: Discovery

```bash
#!/bin/bash
ACCOUNT_ID="${CF_ACCOUNT_ID}"
API_TOKEN="${CF_API_TOKEN}"
BASE="https://api.cloudflare.com/client/v4"

echo "=== Workers Scripts ==="
curl -s "${BASE}/accounts/${ACCOUNT_ID}/workers/scripts" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  | jq '.result[] | {id, modified_on, usage_model, compatibility_date}'

echo ""
echo "=== KV Namespaces ==="
curl -s "${BASE}/accounts/${ACCOUNT_ID}/storage/kv/namespaces" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  | jq '.result[] | {id, title}'

echo ""
echo "=== Durable Object Namespaces ==="
curl -s "${BASE}/accounts/${ACCOUNT_ID}/workers/durable_objects/namespaces" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  | jq '.result[] | {id, name, script, class}'

echo ""
echo "=== Worker Routes (per zone) ==="
for ZONE_ID in $(curl -s "${BASE}/zones" -H "Authorization: Bearer ${API_TOKEN}" | jq -r '.result[].id'); do
  curl -s "${BASE}/zones/${ZONE_ID}/workers/routes" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    | jq -r '.result[] | "\(.pattern)\t\(.script)"'
done | head -30
```

## Phase 2: Analysis

```bash
#!/bin/bash
ACCOUNT_ID="${CF_ACCOUNT_ID}"
API_TOKEN="${CF_API_TOKEN}"
BASE="https://api.cloudflare.com/client/v4"

echo "=== Worker CPU Time & Request Metrics (GraphQL) ==="
SINCE=$(date -u -v-7d +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "7 days ago" +"%Y-%m-%dT%H:%M:%SZ")
UNTIL=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

curl -s "${BASE}/graphql" \
  -H "Authorization: Bearer ${API_TOKEN}" \
  -H "Content-Type: application/json" \
  --data "{\"query\":\"{ viewer { accounts(filter:{accountTag:\\\"${ACCOUNT_ID}\\\"}) { workersInvocationsAdaptive(limit:20, filter:{datetime_gt:\\\"${SINCE}\\\", datetime_lt:\\\"${UNTIL}\\\"}, orderBy:[sum_requests_DESC]) { dimensions { scriptName } sum { requests errors subrequests } quantiles { cpuTimeP50 cpuTimeP99 } } } } }\"}" \
  | jq '.data.viewer.accounts[0].workersInvocationsAdaptive[] | {
      script: .dimensions.scriptName,
      requests: .sum.requests,
      errors: .sum.errors,
      subrequests: .sum.subrequests,
      cpu_p50_ms: .quantiles.cpuTimeP50,
      cpu_p99_ms: .quantiles.cpuTimeP99
    }'

echo ""
echo "=== Cron Triggers ==="
for SCRIPT in $(curl -s "${BASE}/accounts/${ACCOUNT_ID}/workers/scripts" -H "Authorization: Bearer ${API_TOKEN}" | jq -r '.result[].id'); do
  CRONS=$(curl -s "${BASE}/accounts/${ACCOUNT_ID}/workers/scripts/${SCRIPT}/schedules" \
    -H "Authorization: Bearer ${API_TOKEN}" | jq -r '.result[].cron // empty')
  [ -n "$CRONS" ] && echo "${SCRIPT}: ${CRONS}"
done

echo ""
echo "=== KV Key Counts ==="
for NS_ID in $(curl -s "${BASE}/accounts/${ACCOUNT_ID}/storage/kv/namespaces" -H "Authorization: Bearer ${API_TOKEN}" | jq -r '.result[].id'); do
  TITLE=$(curl -s "${BASE}/accounts/${ACCOUNT_ID}/storage/kv/namespaces" -H "Authorization: Bearer ${API_TOKEN}" | jq -r ".result[] | select(.id==\"${NS_ID}\") | .title")
  COUNT=$(curl -s "${BASE}/accounts/${ACCOUNT_ID}/storage/kv/namespaces/${NS_ID}/keys" -H "Authorization: Bearer ${API_TOKEN}" | jq '.result | length')
  echo "${TITLE}: ${COUNT} keys (first page)"
done
```

## Output Format

```
WORKER HEALTH REPORT
====================
Script          Requests   Errors   Error%   CPU-P50   CPU-P99   Model
────────────────────────────────────────────────────────────────────────
my-api          125000     23       0.02%    2.1ms     18.4ms    bundled
auth-worker     89000      1200     1.35%    5.3ms     45.2ms    unbound
cron-job        168        0        0.00%    12.0ms    80.1ms    unbound

KV Namespaces: 3 | Durable Objects: 1 | Cron Triggers: 2
Routes: 5 mapped across 2 zones
```

## Safety Rules

- **Read-only**: Only use GET endpoints against the Cloudflare API
- **Never deploy or delete** scripts without explicit user confirmation
- **Rate limits**: Cloudflare API allows 1200 requests per 5 minutes per user
- **Token scope**: Verify token has `Workers Scripts:Read` and `Account Analytics:Read` permissions

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

