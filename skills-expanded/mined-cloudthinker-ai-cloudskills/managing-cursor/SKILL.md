---
name: managing-cursor
description: |
  Use when working with Cursor — cursor AI-powered editor management and team
  analytics. Covers team seat management, usage tracking, model configuration,
  rules file analysis, project settings review, and workspace configuration. Use
  when managing Cursor team licenses, reviewing AI feature adoption, or
  analyzing Cursor workspace and rules configurations.
connection_type: cursor
preload: false
---

# Cursor AI Editor Management Skill

Manage Cursor team settings, usage analytics, and workspace configurations.

## Core Helper Functions

```bash
#!/bin/bash

# Cursor API helper (team management)
cursor_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${CURSOR_API_KEY}" \
            -H "Content-Type: application/json" \
            "https://api.cursor.com/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${CURSOR_API_KEY}" \
            "https://api.cursor.com/v1/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover team info and workspace configuration before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Cursor Team Info ==="
cursor_api GET "team" | jq '{
    team_name: .name,
    plan: .plan,
    member_count: .member_count,
    seat_limit: .seat_limit
}'

echo ""
echo "=== Team Members ==="
cursor_api GET "team/members?limit=30" | jq -r '
    .members[] | "\(.email)\trole=\(.role)\tstatus=\(.status)\tlast_active=\(.last_active // "never")"
' | column -t | head -20

echo ""
echo "=== Workspace Rules Files ==="
find . -name ".cursorrules" -o -name ".cursor" -type d 2>/dev/null | head -10
if [ -f ".cursorrules" ]; then
    echo "--- .cursorrules ---"
    head -20 .cursorrules
fi
if [ -f ".cursor/rules" ]; then
    echo "--- .cursor/rules ---"
    head -20 .cursor/rules
fi

echo ""
echo "=== Cursor Settings ==="
if [ -f ".cursor/settings.json" ]; then
    cat .cursor/settings.json | jq '.' | head -15
fi
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Usage Analytics ==="
cursor_api GET "team/analytics?period=30d" | jq '{
    total_prompts: .total_prompts,
    total_completions: .total_completions,
    total_chat_messages: .total_chat_messages,
    active_users: .active_users,
    model_usage: .model_breakdown
}'

echo ""
echo "=== Model Usage Breakdown ==="
cursor_api GET "team/analytics/models?period=30d" | jq -r '
    .[] | "\(.model)\trequests=\(.request_count)\ttokens=\(.token_count)"
' | column -t | head -10

echo ""
echo "=== Feature Adoption ==="
cursor_api GET "team/analytics/features?period=30d" | jq -r '
    .[] | "\(.feature)\tusers=\(.active_users)\tusage=\(.usage_count)"
' | column -t

echo ""
echo "=== Project Rules Analysis ==="
if [ -f ".cursorrules" ]; then
    echo "Rules file size: $(wc -c < .cursorrules) bytes"
    echo "Rule sections:"
    grep -E "^#|^##" .cursorrules | head -10
fi

echo ""
echo "=== Subscription ==="
cursor_api GET "team/subscription" | jq '{
    plan: .plan,
    status: .status,
    fast_requests_remaining: .fast_requests_remaining,
    slow_requests_remaining: .slow_requests_remaining,
    renewal_date: .renewal_date
}'
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Aggregate usage by period, not per-request
- Never expose individual developer usage rankings

## Anti-Hallucination Rules
- NEVER guess team or member details — always query API
- NEVER fabricate usage metrics — query actual analytics data
- NEVER assume .cursorrules format — read actual file content

## Safety Rules
- NEVER add or remove members without explicit user confirmation
- NEVER modify .cursorrules without user approval
- NEVER change team policies without user consent
- Usage and prompt data are sensitive — handle with care

## Output Format

Present results as a structured report:
```
Managing Cursor Report
══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

