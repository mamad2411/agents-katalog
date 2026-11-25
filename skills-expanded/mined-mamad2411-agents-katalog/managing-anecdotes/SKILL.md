---
name: managing-anecdotes
description: |
  Use when working with Anecdotes — anecdotes compliance automation platform for
  managing security programs, controls, evidence, and multi-framework
  compliance. Covers control monitoring, evidence automation, plugin
  integrations, gap analysis, and audit readiness. Use when reviewing compliance
  status across frameworks, tracking evidence collection, analyzing control
  gaps, or preparing for security compliance audits.
connection_type: anecdotes
preload: false
---

# Anecdotes Management Skill

Manage and analyze Anecdotes compliance controls, evidence, plugins, and audit readiness.

## API Conventions

### Authentication
All API calls use `Authorization: Bearer $ANECDOTES_API_TOKEN` -- injected automatically. Never hardcode tokens.

### Base URL
`https://api.anecdotes.ai/v1`

### Core Helper Function

```bash
#!/bin/bash

anecdotes_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $ANECDOTES_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.anecdotes.ai/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $ANECDOTES_API_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.anecdotes.ai/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

```bash
#!/bin/bash
echo "=== Frameworks ==="
anecdotes_api GET "/frameworks" \
    | jq -r '.data[] | "\(.id)\t\(.name)\t\(.status)"' | column -t | head -10

echo ""
echo "=== Controls Overview ==="
anecdotes_api GET "/controls?limit=1" \
    | jq '"Total controls: \(.meta.total // "N/A")"' -r

echo ""
echo "=== Plugins (Integrations) ==="
anecdotes_api GET "/plugins" \
    | jq -r '.data[] | "\(.name)\t\(.status)\t\(.type)"' | column -t | head -10
```

## Analysis Phase

### Control Status

```bash
#!/bin/bash
echo "=== Controls by Status ==="
CONTROLS=$(anecdotes_api GET "/controls?limit=200")
echo "$CONTROLS" | jq '{
    total: (.data | length),
    met: ([.data[] | select(.status == "met")] | length),
    not_met: ([.data[] | select(.status == "not_met")] | length),
    partially_met: ([.data[] | select(.status == "partially_met")] | length),
    not_applicable: ([.data[] | select(.status == "not_applicable")] | length)
}'

echo ""
echo "=== Unmet Controls ==="
echo "$CONTROLS" | jq -r '.data[] | select(.status == "not_met") | "\(.status)\t\(.name[0:50])\t\(.framework[0:15])"' \
    | column -t | head -15

echo ""
echo "=== Control Coverage ==="
echo "$CONTROLS" | jq -r '[.data[] | {fw: .framework, status: .status}] | group_by(.fw) | map({framework: .[0].fw[0:20], total: length, met: ([.[] | select(.status == "met")] | length)}) | .[] | "\(.framework)\t\(.met)/\(.total)\t\((.met * 100 / .total | floor))%"' | column -t
```

### Evidence Tracking

```bash
#!/bin/bash
echo "=== Evidence Summary ==="
anecdotes_api GET "/evidence?limit=200" \
    | jq '{
        total: (.data | length),
        collected: ([.data[] | select(.collectionStatus == "collected")] | length),
        pending: ([.data[] | select(.collectionStatus == "pending")] | length),
        failed: ([.data[] | select(.collectionStatus == "failed")] | length)
    }'

echo ""
echo "=== Failed Evidence Collection ==="
anecdotes_api GET "/evidence?limit=50&collectionStatus=failed" \
    | jq -r '.data[] | "\(.controlName[0:30])\t\(.name[0:35])\t\(.source // "manual")"' \
    | column -t | head -15
```

### Plugin Health

```bash
#!/bin/bash
echo "=== Plugin Status ==="
anecdotes_api GET "/plugins" \
    | jq -r '.data[] | "\(.status)\t\(.name[0:25])\t\(.type)\tlastSync:\(.lastSyncTime[0:16] // "Never")"' \
    | sort | column -t | head -20

echo ""
echo "=== Disconnected Plugins ==="
anecdotes_api GET "/plugins" \
    | jq -r '.data[] | select(.status != "connected") | "\(.name)\t\(.status)\terror:\(.lastError[0:40] // "N/A")"' | column -t
```

### Gap Analysis

```bash
#!/bin/bash
FRAMEWORK_ID="${1:-}"

echo "=== Framework Gap Analysis ==="
ENDPOINT="/controls?limit=200"
[ -n "$FRAMEWORK_ID" ] && ENDPOINT="/frameworks/${FRAMEWORK_ID}/controls?limit=200"

anecdotes_api GET "$ENDPOINT" \
    | jq -r '.data[] | select(.status == "not_met" or .status == "partially_met") | "\(.status)\t\(.name[0:45])\t\(.evidenceCount) evidence items"' \
    | column -t | head -20

echo ""
echo "=== Controls Without Evidence ==="
anecdotes_api GET "$ENDPOINT" \
    | jq -r '.data[] | select(.evidenceCount == 0 and .status != "not_applicable") | "\(.name[0:50])\t\(.framework[0:15])\tno evidence"' \
    | column -t | head -10
```

## Output Format

Present results as a structured report:
```
Managing Anecdotes Report
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

- **Plugin-driven evidence**: Most evidence is auto-collected via plugins -- check plugin health first
- **Multi-framework mapping**: Controls can map to multiple frameworks simultaneously
- **Pagination**: Use `limit` and `offset` parameters -- check `meta.total`
- **Rate limits**: Check response headers for rate limiting information
- **Evidence freshness**: Auto-collected evidence has expiry -- check collection timestamps
