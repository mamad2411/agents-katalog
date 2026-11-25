---
name: managing-lambdatest
description: |
  Use when working with Lambdatest — lambdaTest cloud testing platform
  monitoring and analysis. Covers Selenium/Cypress test session management,
  tunnel monitoring, build tracking, screenshot testing, real-time testing
  status, and usage analytics. Use when managing LambdaTest sessions, reviewing
  cross-browser results, or monitoring cloud testing infrastructure.
connection_type: lambdatest
preload: false
---

# LambdaTest Cloud Testing Management Skill

Manage and analyze LambdaTest test sessions, builds, tunnels, and screenshots.

## Core Helper Functions

```bash
#!/bin/bash

# LambdaTest API helper
lambdatest_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "${LAMBDATEST_USERNAME}:${LAMBDATEST_ACCESS_KEY}" \
            -H "Content-Type: application/json" \
            "https://api.lambdatest.com/automation/api/v1/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "${LAMBDATEST_USERNAME}:${LAMBDATEST_ACCESS_KEY}" \
            "https://api.lambdatest.com/automation/api/v1/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover account status and builds before querying sessions.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== LambdaTest Account ==="
lambdatest_api GET "platforms" | jq '{
    platforms_available: length
}' 2>/dev/null

echo ""
echo "=== Recent Builds ==="
lambdatest_api GET "builds?limit=10" | jq -r '
    .data[] | "\(.build_id)\t\(.name)\tstatus=\(.status_ind)\tsessions=\(.session_count // 0)"
' | column -t

echo ""
echo "=== Active Tunnels ==="
lambdatest_api GET "tunnels" | jq -r '
    .data[] | "\(.tunnel_id)\t\(.tunnel_name)\tstatus=\(.status)\towner=\(.launched_by)"
' | column -t 2>/dev/null || echo "No active tunnels"

echo ""
echo "=== Available Platforms ==="
lambdatest_api GET "platforms" | jq -r '
    .platforms[:10][] | "\(.platform)\t\(.browsers | length) browsers"
' | column -t
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Build Sessions ==="
BUILD_ID="${1:-}"
if [ -n "$BUILD_ID" ]; then
    lambdatest_api GET "builds/${BUILD_ID}/sessions?limit=20" | jq -r '
        .data[] | "\(.session_id)\t\(.name // "unnamed")\tstatus=\(.status_ind)\tbrowser=\(.browser)\tos=\(.os)"
    ' | column -t

    echo ""
    echo "=== Build Summary ==="
    lambdatest_api GET "builds/${BUILD_ID}/sessions" | jq '{
        total: (.data | length),
        passed: [.data[] | select(.status_ind == "passed")] | length,
        failed: [.data[] | select(.status_ind == "failed")] | length,
        browsers: [.data[].browser] | unique,
        os_list: [.data[].os] | unique
    }'
fi

echo ""
echo "=== Session Details ==="
SESSION_ID="${2:-}"
if [ -n "$SESSION_ID" ]; then
    lambdatest_api GET "sessions/${SESSION_ID}" | jq '{
        name: .data.name,
        status: .data.status_ind,
        browser: .data.browser,
        browser_version: .data.browser_version,
        os: .data.os,
        os_version: .data.os_version,
        duration: .data.duration,
        console_logs_url: .data.console_logs_url,
        video_url: .data.video_url
    }'
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use limit parameter for pagination
- Reference log/video URLs rather than embedding content

## Anti-Hallucination Rules
- NEVER guess build or session IDs — always discover via API
- NEVER fabricate session results — query actual LambdaTest data
- NEVER assume platform availability — check platforms endpoint

## Safety Rules
- NEVER terminate running sessions without explicit user confirmation
- NEVER delete builds without user approval
- NEVER modify tunnel configuration without user consent

## Output Format

Present results as a structured report:
```
Managing Lambdatest Report
══════════════════════════
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

