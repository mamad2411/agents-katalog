---
name: managing-openai-api
description: |
  Use when working with Openai Api — openAI API platform management covering
  models, usage, fine-tuning jobs, files, assistants, and billing. Use when
  monitoring API usage and costs, analyzing model performance, reviewing
  fine-tuning status, managing assistants and files, or troubleshooting OpenAI
  API issues.
connection_type: openai
preload: false
---

# OpenAI API Management Skill

Manage and analyze OpenAI API resources including models, usage, fine-tuning, and billing.

## API Conventions

### Authentication
All API calls use Bearer API key, injected automatically.

### Base URL
`https://api.openai.com/v1`

### Core Helper Function

```bash
#!/bin/bash

openai_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.openai.com/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            "https://api.openai.com/v1${endpoint}"
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
openai_api GET "/models" \
    | jq -r '.data[] | "\(.id)\t\(.owned_by)\t\(.created | strftime("%Y-%m-%d"))"' \
    | sort | head -25

echo ""
echo "=== Fine-Tuning Jobs ==="
openai_api GET "/fine_tuning/jobs?limit=10" \
    | jq -r '.data[] | "\(.id[0:20])\t\(.model)\t\(.status)\t\(.created_at | strftime("%Y-%m-%d"))"' \
    | column -t | head -10

echo ""
echo "=== Uploaded Files ==="
openai_api GET "/files" \
    | jq -r '.data[] | "\(.id[0:20])\t\(.filename[0:30])\t\(.purpose)\t\(.bytes) bytes"' \
    | column -t | head -15

echo ""
echo "=== Assistants ==="
openai_api GET "/assistants?limit=20" \
    | jq -r '.data[] | "\(.id[0:20])\t\(.name // "unnamed")\t\(.model)\t\(.created_at | strftime("%Y-%m-%d"))"' \
    | column -t | head -15
```

## Phase 2: Analysis

### Usage & Billing

```bash
#!/bin/bash
echo "=== Usage Summary (current billing period) ==="
START=$(date -d 'first day of this month' +%Y-%m-%d)
END=$(date +%Y-%m-%d)
openai_api GET "/organization/usage?start_date=${START}&end_date=${END}" \
    | jq '{total_tokens: .total_usage, daily_costs: [.daily_costs[-7:][] | {date: .timestamp | strftime("%Y-%m-%d"), cost_usd: (.line_items | map(.cost) | add / 100)}]}'

echo ""
echo "=== Cost by Model (current month) ==="
openai_api GET "/organization/usage?start_date=${START}&end_date=${END}" \
    | jq -r '.daily_costs[] | .line_items[] | "\(.name)\t$\(.cost / 100)"' \
    | awk -F'\t' '{costs[$1] += $2} END {for (m in costs) printf "%s\t$%.2f\n", m, costs[m]}' \
    | sort -t$'\t' -k2 -rn | head -15
```

### Fine-Tuning Health

```bash
#!/bin/bash
echo "=== Fine-Tuning Job Status ==="
openai_api GET "/fine_tuning/jobs?limit=20" \
    | jq -r '.data[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Active/Recent Fine-Tuning ==="
openai_api GET "/fine_tuning/jobs?limit=10" \
    | jq -r '.data[] | "\(.id[0:20])\t\(.model)\t\(.status)\t\(.trained_tokens // 0) tokens\t\(.finished_at // "in progress" | if type == "number" then strftime("%Y-%m-%d") else . end)"' \
    | column -t

echo ""
echo "=== Fine-Tuned Models ==="
openai_api GET "/models" \
    | jq -r '.data[] | select(.owned_by != "openai" and .owned_by != "system") | "\(.id)\t\(.owned_by)\t\(.created | strftime("%Y-%m-%d"))"' \
    | head -10
```

## Output Format

```
=== OpenAI Account ===
Models Available: <n>  Custom Fine-Tuned: <n>

--- Usage (current month) ---
Total Cost: $<amount>
Top Models: <model>: $<cost>

--- Fine-Tuning ---
Active: <n>  Completed: <n>  Failed: <n>

--- Resources ---
Files: <n>  Assistants: <n>
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
- **Rate limits**: Vary by model and tier (TPM and RPM limits); check response headers
- **Usage API**: May require organization-level API key for billing endpoints
- **Timestamps**: Unix epoch seconds in responses
- **Fine-tuning models**: Only specific base models support fine-tuning
- **Pagination**: Use `limit` and `after` cursor; check `has_more` in response
