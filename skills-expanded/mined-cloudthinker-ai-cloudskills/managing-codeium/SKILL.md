---
name: managing-codeium
description: |
  Use when working with Codeium — codeium (Windsurf) AI coding assistant
  management and analytics. Covers team seat management, usage tracking,
  language analytics, editor adoption metrics, security policy configuration,
  and enterprise deployment review. Use when managing Codeium/Windsurf licenses,
  reviewing team adoption, or analyzing AI-assisted coding productivity.
connection_type: codeium
preload: false
---

# Codeium (Windsurf) AI Coding Assistant Management Skill

Manage Codeium team settings, seats, usage analytics, and security policies.

## Core Helper Functions

```bash
#!/bin/bash

# Codeium API helper
codeium_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${CODEIUM_API_KEY}" \
            -H "Content-Type: application/json" \
            "https://api.codeium.com/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${CODEIUM_API_KEY}" \
            "https://api.codeium.com/v1/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover team and subscription info before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Codeium Team Info ==="
codeium_api GET "team" | jq '{
    team_name: .name,
    plan: .plan,
    member_count: .member_count,
    seat_limit: .seat_limit
}'

echo ""
echo "=== Team Members ==="
codeium_api GET "team/members?limit=30" | jq -r '
    .members[] | "\(.email)\trole=\(.role)\tstatus=\(.status)\tlast_active=\(.last_active_at // "never")"
' | column -t | head -20

echo ""
echo "=== Subscription Details ==="
codeium_api GET "team/subscription" | jq '{
    plan: .plan,
    status: .status,
    seats_used: .seats_used,
    seats_total: .seats_total,
    renewal_date: .renewal_date
}'
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Usage Analytics ==="
codeium_api GET "team/analytics/usage?period=30d" | jq '{
    total_completions: .total_completions,
    total_acceptances: .total_acceptances,
    acceptance_rate: .acceptance_rate,
    active_users: .active_users,
    total_lines_generated: .total_lines_generated
}'

echo ""
echo "=== Language Breakdown ==="
codeium_api GET "team/analytics/languages?period=30d" | jq -r '
    .languages[:10][] | "\(.language)\tcompletions=\(.completions)\tacceptances=\(.acceptances)\trate=\(.acceptance_rate)%"
' | column -t

echo ""
echo "=== Editor Distribution ==="
codeium_api GET "team/analytics/editors?period=30d" | jq -r '
    .editors[] | "\(.editor)\tusers=\(.active_users)\tcompletions=\(.completions)"
' | column -t

echo ""
echo "=== Security Policies ==="
codeium_api GET "team/policies" | jq '{
    telemetry: .telemetry_enabled,
    context_awareness: .context_awareness,
    allowed_domains: .allowed_domains,
    blocked_repos: .blocked_repos
}' 2>/dev/null | head -15

echo ""
echo "=== Inactive Members (30d) ==="
codeium_api GET "team/members?limit=100" | jq -r '
    [.members[] | select(.last_active_at == null or (.last_active_at | fromdateiso8601 < (now - 2592000)))] |
    .[:10][] | "\(.email)\tlast_active=\(.last_active_at // "never")"
' | column -t
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Aggregate usage by period, not individual completions
- Never expose individual developer productivity rankings

## Anti-Hallucination Rules
- NEVER guess team or member details — always query API
- NEVER fabricate usage metrics — query actual analytics data
- NEVER assume API availability — Codeium Teams/Enterprise APIs may differ

## Safety Rules
- NEVER add or remove members without explicit user confirmation
- NEVER change security policies without user approval
- NEVER modify context awareness settings without user consent
- Usage data may be sensitive — respect privacy

## Output Format

Present results as a structured report:
```
Managing Codeium Report
═══════════════════════
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

