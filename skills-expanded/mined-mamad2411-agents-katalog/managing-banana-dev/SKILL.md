---
name: managing-banana-dev
description: |
  Use when working with Banana Dev — banana.dev ML inference platform management
  covering model inventory, deployment status, API call history, GPU allocation,
  scaling configuration, build logs, and latency metrics. Use for comprehensive
  Banana.dev model deployment assessment and inference performance analysis.
connection_type: banana-dev
preload: false
---

# Banana.dev Management

Analyze Banana.dev model deployments, inference calls, GPU usage, and build status.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${BANANA_API_KEY}"
BASE="https://api.banana.dev/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Models Inventory ==="
curl -s "${BASE}/models" "${AUTH[@]}" \
  | jq -r '.models[] | "\(.name)\t\(.model_key[0:12])\t\(.status)\t\(.gpu_type)\t\(.created_at[0:10])"' \
  | column -t | head -20

echo ""
echo "=== Deployments ==="
curl -s "${BASE}/deployments" "${AUTH[@]}" \
  | jq -r '.deployments[] | "\(.model_name)\t\(.version[0:8])\t\(.status)\t\(.gpu)\t\(.replicas)\t\(.updated_at[0:19])"' \
  | column -t | head -20

echo ""
echo "=== GPU Allocation ==="
curl -s "${BASE}/models" "${AUTH[@]}" \
  | jq -r '.models[] | "\(.name)\t\(.gpu_type)\t\(.min_replicas)-\(.max_replicas) replicas\t\(.cold_start_timeout)s cold start"' \
  | column -t | head -15

echo ""
echo "=== Build History ==="
curl -s "${BASE}/builds?limit=10" "${AUTH[@]}" \
  | jq -r '.builds[] | "\(.model_name)\t\(.build_id[0:8])\t\(.status)\t\(.duration_s // "N/A")s\t\(.created_at[0:19])"' \
  | column -t | head -15
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${BANANA_API_KEY}"
BASE="https://api.banana.dev/v1"
AUTH=(-H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json")

echo "=== Inference Call History ==="
curl -s "${BASE}/calls?limit=20" "${AUTH[@]}" \
  | jq -r '.calls[] | "\(.model_name)\t\(.call_id[0:8])\t\(.status)\t\(.duration_ms)ms\t\(.created_at[0:19])"' \
  | column -t | head -20

echo ""
echo "=== Call Status Summary ==="
curl -s "${BASE}/calls?limit=100" "${AUTH[@]}" \
  | jq -r '.calls | group_by(.status) | .[] | "\(.[0].status): \(length) calls"'

echo ""
echo "=== Latency Metrics ==="
curl -s "${BASE}/calls?limit=50" "${AUTH[@]}" \
  | jq '[.calls[] | select(.duration_ms != null) | .duration_ms] | if length > 0 then {avg_ms: (add/length | round), min_ms: min, max_ms: max, count: length} else {status: "no data"} end'

echo ""
echo "=== Scaling Events ==="
curl -s "${BASE}/scaling-events?limit=10" "${AUTH[@]}" \
  | jq -r '.events[]? | "\(.model_name)\t\(.from_replicas)->\(.to_replicas)\t\(.reason)\t\(.created_at[0:19])"' \
  | column -t | head -10

echo ""
echo "=== Failed Builds ==="
curl -s "${BASE}/builds?limit=20" "${AUTH[@]}" \
  | jq -r '.builds[] | select(.status == "failed") | "\(.model_name)\t\(.build_id[0:8])\t\(.error[0:60])\t\(.created_at[0:19])"' \
  | column -t | head -10

echo ""
echo "=== Resource Summary ==="
echo "Models: $(curl -s "${BASE}/models" "${AUTH[@]}" | jq '.models | length')"
echo "Active: $(curl -s "${BASE}/models" "${AUTH[@]}" | jq '[.models[] | select(.status == "active")] | length')"
```

## Output Format

```
BANANA.DEV ANALYSIS
=====================
Model            GPU      Replicas   Status    Avg Latency  Calls (24h)
──────────────────────────────────────────────────────────────────────────
sd-inference     A100     1-3        active    1,250ms      340
whisper-large    T4       1-2        active    3,400ms      120
llm-server       A100     2-5        active    850ms        890

Models: 3 active | GPUs: A100(2) T4(1) | Builds: 5 (4 ok, 1 failed)
Calls (24h): 1,350 total (1,320 success, 30 failed)
Avg Latency: 1,833ms | Cold Starts: 12
```

## Safety Rules

- **Read-only**: Only use GET endpoints against the Banana.dev API
- **Never deploy, scale, or delete** models without confirmation
- **API keys**: Never output API key or model key values
- **Rate limits**: Respect API rate limits to avoid throttling

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

