---
name: managing-groq-cloud
description: |
  Use when working with Groq Cloud — groq Cloud inference platform management
  covering models, API usage, rate limits, and performance metrics. Use when
  monitoring API health, analyzing inference latency, reviewing available
  models, checking rate limit status, or troubleshooting Groq Cloud API issues.
connection_type: groq
preload: false
---

# Groq Cloud Management Skill

Manage and analyze Groq Cloud inference platform resources including models, usage, and performance.

## API Conventions

### Authentication
All API calls use Bearer API key, injected automatically.

### Base URL
`https://api.groq.com/openai/v1`

### Core Helper Function

```bash
#!/bin/bash

groq_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $GROQ_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.groq.com/openai/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $GROQ_API_KEY" \
            "https://api.groq.com/openai/v1${endpoint}"
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
groq_api GET "/models" \
    | jq -r '.data[] | "\(.id)\t\(.owned_by)\t\(.context_window // "N/A")"' \
    | sort | column -t | head -20

echo ""
echo "=== API Health Check ==="
RESULT=$(groq_api POST "/chat/completions" '{"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": "test"}], "max_tokens": 1}')
echo "$RESULT" | jq '{model: .model, usage: .usage}' 2>/dev/null || echo "Error: $(echo $RESULT | jq -r '.error.message // "unknown"')"
```

## Phase 2: Analysis

### Performance & Rate Limits

```bash
#!/bin/bash
echo "=== Latency Benchmark ==="
for model in "llama-3.1-8b-instant" "llama-3.1-70b-versatile" "mixtral-8x7b-32768"; do
    START=$(date +%s%N)
    RESULT=$(groq_api POST "/chat/completions" "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"Say hello\"}], \"max_tokens\": 10}")
    END=$(date +%s%N)
    LATENCY=$(( (END - START) / 1000000 ))
    TOKENS=$(echo "$RESULT" | jq '.usage.total_tokens // 0')
    echo "$model: ${LATENCY}ms (${TOKENS} tokens)"
done

echo ""
echo "=== Rate Limit Status ==="
HEADERS=$(curl -s -D- -o /dev/null -X POST \
    -H "Authorization: Bearer $GROQ_API_KEY" \
    -H "Content-Type: application/json" \
    "https://api.groq.com/openai/v1/chat/completions" \
    -d '{"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": "test"}], "max_tokens": 1}')
echo "$HEADERS" | grep -i "x-ratelimit\|retry-after" | while read line; do
    echo "  $line"
done
```

### Model Availability

```bash
#!/bin/bash
echo "=== Model Availability Check ==="
groq_api GET "/models" | jq -r '.data[].id' | while read model; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -H "Authorization: Bearer $GROQ_API_KEY" \
        -H "Content-Type: application/json" \
        "https://api.groq.com/openai/v1/chat/completions" \
        -d "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"test\"}], \"max_tokens\": 1}")
    echo "$model: HTTP $STATUS"
done | head -15

echo ""
echo "=== Models by Owner ==="
groq_api GET "/models" \
    | jq -r '[.data[] | .owned_by] | group_by(.) | map({(.[0]): length}) | add'
```

## Output Format

```
=== Groq Cloud ===
Models Available: <n>

--- Performance ---
<model>: <latency>ms (<tokens> tokens)

--- Rate Limits ---
Requests: <remaining>/<limit> per minute
Tokens: <remaining>/<limit> per minute

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
- **OpenAI-compatible**: API follows OpenAI chat/completions format
- **Rate limits**: Vary by model and plan; check `x-ratelimit-*` headers
- **Model names**: Use exact model IDs from `/models` endpoint
- **Token limits**: Different models have different context windows
- **No fine-tuning**: Groq does not currently support custom fine-tuning
