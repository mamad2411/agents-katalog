---
name: managing-baseten
description: |
  Use when working with Baseten — baseten ML deployment platform management
  covering model inventory, deployment status, autoscaling configuration,
  inference call history, GPU allocation, environment management, and
  performance metrics. Use for comprehensive Baseten workspace assessment and ML
  serving optimization.
connection_type: baseten
preload: false
---

# Baseten Management

Analyze Baseten models, deployments, autoscaling, and inference performance.

## Phase 1: Discovery

```bash
#!/bin/bash
TOKEN="${BASETEN_API_KEY}"
BASE="https://api.baseten.co/v1"
AUTH=(-H "Authorization: Api-Key ${TOKEN}" -H "Content-Type: application/json")

echo "=== Models Inventory ==="
curl -s "${BASE}/models" "${AUTH[@]}" \
  | jq -r '.models[] | "\(.name)\t\(.id[0:12])\t\(.status)\t\(.model_type)\t\(.created_at[0:10])"' \
  | column -t | head -20

echo ""
echo "=== Deployments ==="
for MODEL in $(curl -s "${BASE}/models" "${AUTH[@]}" | jq -r '.models[].id'); do
  NAME=$(curl -s "${BASE}/models/${MODEL}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/models/${MODEL}/deployments" "${AUTH[@]}" \
    | jq -r ".deployments[]? | \"${NAME}\t\(.id[0:8])\t\(.status)\t\(.instance_type)\t\(.is_primary)\"" 2>/dev/null
done | column -t | head -20

echo ""
echo "=== Autoscaling Config ==="
for MODEL in $(curl -s "${BASE}/models" "${AUTH[@]}" | jq -r '.models[].id'); do
  NAME=$(curl -s "${BASE}/models/${MODEL}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/models/${MODEL}/deployments" "${AUTH[@]}" \
    | jq -r ".deployments[]? | \"${NAME}\t\(.min_replica // 0)-\(.max_replica // 1)\tscale_down:\(.scale_down_delay // \"default\")\"" 2>/dev/null
done | column -t | head -15

echo ""
echo "=== Environments ==="
curl -s "${BASE}/environments" "${AUTH[@]}" \
  | jq -r '.environments[]? | "\(.name)\t\(.id[0:12])\t\(.is_default)"' \
  | column -t | head -10
```

## Phase 2: Analysis

```bash
#!/bin/bash
TOKEN="${BASETEN_API_KEY}"
BASE="https://api.baseten.co/v1"
AUTH=(-H "Authorization: Api-Key ${TOKEN}" -H "Content-Type: application/json")

echo "=== Model Performance ==="
for MODEL in $(curl -s "${BASE}/models" "${AUTH[@]}" | jq -r '.models[].id'); do
  NAME=$(curl -s "${BASE}/models/${MODEL}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/models/${MODEL}/metrics" "${AUTH[@]}" \
    | jq -r "\"${NAME}\tp50:\(.latency_p50 // \"N/A\")ms\tp99:\(.latency_p99 // \"N/A\")ms\trps:\(.requests_per_second // \"N/A\")\"" 2>/dev/null
done | column -t | head -15

echo ""
echo "=== Active Replicas ==="
for MODEL in $(curl -s "${BASE}/models" "${AUTH[@]}" | jq -r '.models[].id'); do
  NAME=$(curl -s "${BASE}/models/${MODEL}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/models/${MODEL}/deployments" "${AUTH[@]}" \
    | jq -r ".deployments[]? | \"${NAME}\t\(.current_replicas // 0) active\t\(.instance_type)\t\(.status)\"" 2>/dev/null
done | column -t | head -15

echo ""
echo "=== Recent Errors ==="
for MODEL in $(curl -s "${BASE}/models" "${AUTH[@]}" | jq -r '.models[].id'); do
  NAME=$(curl -s "${BASE}/models/${MODEL}" "${AUTH[@]}" | jq -r '.name')
  curl -s "${BASE}/models/${MODEL}/logs?level=error&limit=5" "${AUTH[@]}" \
    | jq -r ".logs[]? | \"${NAME}\t\(.message[0:60])\t\(.timestamp[0:19])\"" 2>/dev/null
done | column -t | head -10

echo ""
echo "=== Secret Names ==="
curl -s "${BASE}/secrets" "${AUTH[@]}" \
  | jq -r '.secrets[]? | "\(.name)\t\(.created_at[0:10])"' \
  | column -t | head -10

echo ""
echo "=== Resource Summary ==="
echo "Models: $(curl -s "${BASE}/models" "${AUTH[@]}" | jq '.models | length')"
echo "Active: $(curl -s "${BASE}/models" "${AUTH[@]}" | jq '[.models[] | select(.status == "active")] | length')"
echo "Environments: $(curl -s "${BASE}/environments" "${AUTH[@]}" | jq '.environments | length' 2>/dev/null)"
```

## Output Format

```
BASETEN ANALYSIS
==================
Model            Instance     Replicas  Latency(p50)  Latency(p99)  Status
──────────────────────────────────────────────────────────────────────────────
llm-serving      A10G         2/5       120ms         450ms         active
image-gen        A100         1/3       2,100ms       5,200ms       active
embeddings       T4           1/2       45ms          120ms         active

Models: 3 active | Replicas: 4 running | Environments: 2
Autoscaling: all configured (min:1 max:5)
Errors (24h): 3 total | Secrets: 5 configured
```

## Safety Rules

- **Read-only**: Only use GET endpoints against the Baseten API
- **Never deploy, scale, or delete** models without confirmation
- **Secrets**: Never output secret values, only list names
- **API keys**: Never expose API key values in output

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

