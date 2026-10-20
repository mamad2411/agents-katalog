---
name: managing-github-copilot
description: |
  Use when working with Github Copilot — gitHub Copilot management and usage
  analytics. Covers organization seat management, usage metrics tracking, policy
  configuration, content exclusion rules, suggestion acceptance analysis, and
  billing review. Use when managing GitHub Copilot licenses, reviewing adoption
  metrics, configuring policies, or analyzing developer productivity impact.
connection_type: github-copilot
preload: false
---

# GitHub Copilot Management Skill

Manage GitHub Copilot organization settings, seats, usage metrics, and policies.

## Core Helper Functions

```bash
#!/bin/bash

# GitHub API helper for Copilot endpoints
gh_copilot_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github+json" \
            -H "X-GitHub-Api-Version: 2022-11-28" \
            "https://api.github.com/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover organization and billing info before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

ORG="${1:?Organization name required}"

echo "=== Copilot Billing Summary ==="
gh_copilot_api GET "orgs/${ORG}/copilot/billing" | jq '{
    seat_management_setting: .seat_management_setting,
    seat_breakdown: .seat_breakdown,
    plan_type: .plan_type
}'

echo ""
echo "=== Seat Assignments ==="
gh_copilot_api GET "orgs/${ORG}/copilot/billing/seats?per_page=30" | jq -r '
    .seats[] | "\(.assignee.login)\tlast_active=\(.last_activity_at // "never")\teditor=\(.last_activity_editor // "unknown")\tcreated=\(.created_at | split("T")[0])"
' | column -t | head -20

echo ""
echo "=== Active vs Inactive ==="
gh_copilot_api GET "orgs/${ORG}/copilot/billing/seats?per_page=100" | jq '{
    total_seats: (.seats | length),
    active_last_30d: [.seats[] | select(.last_activity_at != null)] | length,
    never_used: [.seats[] | select(.last_activity_at == null)] | length,
    editors_used: [.seats[] | select(.last_activity_editor != null) | .last_activity_editor] | group_by(.) | map({editor: .[0], count: length})
}'
```

### Phase 2: Analysis

```bash
#!/bin/bash

ORG="${1:?Organization name required}"

echo "=== Copilot Usage Metrics ==="
gh_copilot_api GET "orgs/${ORG}/copilot/usage" | jq -r '
    .[] | "\(.day)\tacceptances=\(.total_acceptances_count)\tsuggestions=\(.total_suggestions_count)\tlines_accepted=\(.total_lines_accepted)\tactive_users=\(.total_active_users)"
' | column -t | tail -14

echo ""
echo "=== Language Breakdown ==="
gh_copilot_api GET "orgs/${ORG}/copilot/usage" | jq '
    [.[-1].breakdown[] | {language: .language, suggestions: .suggestions_count, acceptances: .acceptances_count, acceptance_rate: (if .suggestions_count > 0 then (.acceptances_count / .suggestions_count * 100 | floor) else 0 end)}] |
    sort_by(-.suggestions) | .[:10]
'

echo ""
echo "=== Content Exclusions ==="
gh_copilot_api GET "orgs/${ORG}/copilot/content_exclusions" 2>/dev/null | jq '.' | head -15 || echo "No content exclusions configured"

echo ""
echo "=== Policy Settings ==="
gh_copilot_api GET "orgs/${ORG}/copilot/policies" 2>/dev/null | jq '.' | head -10 || echo "Default policies in effect"
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Aggregate usage metrics by day/week, not individual suggestions
- Never expose individual developer productivity metrics without context

## Anti-Hallucination Rules
- NEVER guess organization names — verify via GitHub API
- NEVER fabricate usage metrics — query actual Copilot API data
- NEVER assume API endpoint availability — some require Copilot Business/Enterprise

## Safety Rules
- NEVER add or remove seat assignments without explicit user confirmation
- NEVER change policies without user approval
- NEVER modify content exclusions without user consent
- Usage data may be sensitive — be mindful of privacy implications

## Output Format

Present results as a structured report:
```
Managing Github Copilot Report
══════════════════════════════
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

