---
name: managing-anthropic-api
description: |
  Use when working with Anthropic Api — anthropic API platform management
  covering models, usage tracking, rate limits, and message analytics. Use when
  monitoring API usage and costs, analyzing model request patterns, reviewing
  rate limit health, or troubleshooting Anthropic Claude API issues.
connection_type: anthropic
preload: false
---

# Anthropic API Management Skill

Manage and analyze Anthropic API resources including models, usage, and rate limit health.

## API Conventions

### Authentication
All API calls use `x-api-key` header, injected automatically.

### Base URL
`https://api.anthropic.com/v1`

### Core Helper Function

```bash
#!/bin/bash

anthropic_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            -H "Content-Type: application/json" \
            "https://api.anthropic.com/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "x-api-key: $ANTHROPIC_API_KEY" \
            -H "anthropic-version: 2023-06-01" \
            "https://api.anthropic.com/v1${endpoint}"
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
anthropic_api GET "/models?limit=20" \
    | jq -r '.data[] | "\(.id)\t\(.display_name)\t\(.created_at[0:10])"' \
    | column -t | head -20

echo ""
echo "=== API Health Check ==="
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "Content-Type: application/json" \
    "https://api.anthropic.com/v1/messages" \
    -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 1, "messages": [{"role": "user", "content": "hi"}]}')
echo "API Status: $RESPONSE"

echo ""
echo "=== Rate Limit Info ==="
curl -s -D- -o /dev/null -X POST \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "Content-Type: application/json" \
    "https://api.anthropic.com/v1/messages" \
    -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 1, "messages": [{"role": "user", "content": "hi"}]}' \
    | grep -i "anthropic-ratelimit\|retry-after\|x-ratelimit"
```

## Phase 2: Analysis

### Usage & Rate Limits

```bash
#!/bin/bash
echo "=== Rate Limit Status ==="
HEADERS=$(curl -s -D- -o /dev/null -X POST \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "Content-Type: application/json" \
    "https://api.anthropic.com/v1/messages" \
    -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 1, "messages": [{"role": "user", "content": "test"}]}')

echo "$HEADERS" | grep -i "ratelimit" | while read line; do
    echo "  $line"
done

echo ""
echo "=== Model Availability ==="
for model in "claude-sonnet-4-20250514" "claude-opus-4-20250514" "claude-haiku-35-20241022"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -H "Content-Type: application/json" \
        "https://api.anthropic.com/v1/messages" \
        -d "{\"model\": \"$model\", \"max_tokens\": 1, \"messages\": [{\"role\": \"user\", \"content\": \"test\"}]}")
    echo "$model: HTTP $STATUS"
done
```

### API Configuration Check

```bash
#!/bin/bash
echo "=== API Key Validation ==="
RESULT=$(anthropic_api POST "/messages" '{"model": "claude-sonnet-4-20250514", "max_tokens": 1, "messages": [{"role": "user", "content": "test"}]}')
echo "$RESULT" | jq '{model: .model, type: .type, stop_reason: .stop_reason, usage: .usage}' 2>/dev/null || echo "Error: $(echo $RESULT | jq -r '.error.message // "unknown"')"
```

## Output Format

```
=== Anthropic API ===
Models Available: <list>
API Status: <healthy|degraded>

--- Rate Limits ---
Requests: <used>/<limit> per minute
Tokens: <used>/<limit> per minute

--- Model Availability ---
<model>: <available|unavailable>
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
- **Version header required**: Always include `anthropic-version: 2023-06-01` header
- **Rate limit headers**: Check `anthropic-ratelimit-*` headers for current limits
- **Token counting**: Input and output tokens are counted separately for billing
- **Model names**: Use full model IDs (e.g., `claude-sonnet-4-20250514`) not aliases
- **No usage API**: Anthropic does not expose a usage/billing API; use Console for cost tracking
