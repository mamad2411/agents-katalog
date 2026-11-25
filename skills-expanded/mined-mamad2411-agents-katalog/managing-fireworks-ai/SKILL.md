---
name: managing-fireworks-ai
description: |
  Use when working with Fireworks Ai — fireworks AI inference platform
  management covering models, deployments, fine-tuning, and usage analytics. Use
  when monitoring API usage, analyzing model performance, reviewing fine-tuning
  jobs, checking available models, or troubleshooting Fireworks AI API issues.
connection_type: fireworks-ai
preload: false
---

# Fireworks AI Management Skill

Manage and analyze Fireworks AI platform resources including models, deployments, and fine-tuning.

## API Conventions

### Authentication
All API calls use Bearer API key, injected automatically.

### Base URL
`https://api.fireworks.ai/inference/v1` (inference) and `https://api.fireworks.ai/v1` (management)

### Core Helper Function

```bash
#!/bin/bash

fireworks_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $FIREWORKS_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.fireworks.ai${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $FIREWORKS_API_KEY" \
            "https://api.fireworks.ai${endpoint}"
    fi
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Available Models ==="
fireworks_api GET "/inference/v1/models" \
    | jq -r '.data[] | "\(.id)\t\(.context_length // "N/A")"' \
    | head -25

echo ""
echo "=== Account Info ==="
fireworks_api GET "/v1/accounts/me" \
    | jq '{id: .id, name: .name, tier: .tier}'

echo ""
echo "=== Fine-Tuning Jobs ==="
fireworks_api GET "/v1/accounts/me/fineTuningJobs" \
    | jq -r '.jobs[] | "\(.id[0:16])\t\(.model[0:30])\t\(.status)\t\(.createdAt[0:10])"' \
    | column -t | head -10

echo ""
echo "=== Deployments ==="
fireworks_api GET "/v1/accounts/me/deployedModels" \
    | jq -r '.deployedModels[] | "\(.id[0:16])\t\(.model[0:30])\t\(.state)\t\(.createdAt[0:10])"' \
    | head -10
```

## Phase 2: Analysis

### Usage & Health

```bash
#!/bin/bash
echo "=== API Health Check ==="
RESULT=$(fireworks_api POST "/inference/v1/chat/completions" '{"model": "accounts/fireworks/models/llama-v3p1-8b-instruct", "messages": [{"role": "user", "content": "test"}], "max_tokens": 1}')
echo "$RESULT" | jq '{model: .model, usage: .usage}' 2>/dev/null || echo "Error: $(echo $RESULT | jq -r '.error.message // "unknown"')"

echo ""
echo "=== Model Categories ==="
fireworks_api GET "/inference/v1/models" \
    | jq -r '[.data[] | .owned_by // "fireworks"] | group_by(.) | map({(.[0]): length}) | add'
```

### Fine-Tuning & Deployment Health

```bash
#!/bin/bash
echo "=== Fine-Tuning Status Summary ==="
fireworks_api GET "/v1/accounts/me/fineTuningJobs" \
    | jq -r '.jobs[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Active Deployments ==="
fireworks_api GET "/v1/accounts/me/deployedModels" \
    | jq -r '.deployedModels[] | select(.state == "DEPLOYED") | "\(.id[0:16])\t\(.model[0:30])\t\(.state)\t\(.replicas // 1) replicas"' \
    | head -10

echo ""
echo "=== Custom Models ==="
fireworks_api GET "/v1/accounts/me/models" \
    | jq -r '.models[] | "\(.id[0:20])\t\(.displayName // .id)\t\(.createdAt[0:10])"' \
    | head -10
```

## Output Format

```
=== Fireworks AI Account: <name> | Tier: <tier> ===

--- Models ---
Available: <n>  Custom: <n>

--- Fine-Tuning ---
Active: <n>  Completed: <n>  Failed: <n>

--- Deployments ---
Active: <n>  Total Replicas: <n>
```

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
- **Model IDs**: Use full path format (e.g., `accounts/fireworks/models/llama-v3p1-8b-instruct`)
- **Two API bases**: Inference endpoints use `/inference/v1`, management uses `/v1`
- **OpenAI-compatible**: Inference API follows OpenAI chat/completions format
- **Rate limits**: Vary by tier; check response headers
