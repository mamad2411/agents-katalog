---
name: managing-browserstack
description: |
  Use when working with Browserstack — browserStack cloud testing platform
  monitoring and analysis. Covers Automate session management, live testing
  status, App Automate tracking, build and session analysis, device/browser
  usage metrics, and account quota monitoring. Use when managing BrowserStack
  test sessions, reviewing cross-browser results, or monitoring cloud testing
  infrastructure.
connection_type: browserstack
preload: false
---

# BrowserStack Cloud Testing Management Skill

Manage and analyze BrowserStack Automate, Live, and App Automate resources.

## Core Helper Functions

```bash
#!/bin/bash

# BrowserStack API helper
browserstack_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -u "${BROWSERSTACK_USERNAME}:${BROWSERSTACK_ACCESS_KEY}" \
            -H "Content-Type: application/json" \
            "https://api.browserstack.com/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -u "${BROWSERSTACK_USERNAME}:${BROWSERSTACK_ACCESS_KEY}" \
            "https://api.browserstack.com/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover account status and builds before querying sessions.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== BrowserStack Account ==="
browserstack_api GET "automate/plan.json" | jq '{
    plan: .automate_plan,
    parallel_sessions_max: .parallel_sessions_max_allowed,
    parallel_sessions_running: .parallel_sessions_running,
    queued_sessions: .queued_sessions,
    team_parallel_sessions_max: .team_parallel_sessions_max_allowed
}'

echo ""
echo "=== Recent Builds (Automate) ==="
browserstack_api GET "automate/builds.json?limit=10" | jq -r '
    .[].automation_build | "\(.hashed_id)\t\(.name)\tstatus=\(.status)\tduration=\(.duration // 0)s"
' | column -t

echo ""
echo "=== Available Browsers ==="
browserstack_api GET "automate/browsers.json" | jq -r '
    group_by(.browser) | .[] | "\(.[0].browser)\tversions=\(length)\tos=\([.[].os] | unique | join(","))"
' | column -t | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Build Details ==="
BUILD_ID="${1:-}"
if [ -n "$BUILD_ID" ]; then
    browserstack_api GET "automate/builds/${BUILD_ID}/sessions.json?limit=20" | jq -r '
        .[].automation_session | "\(.name)\tstatus=\(.status)\tbrowser=\(.browser)\tos=\(.os)\tduration=\(.duration)s"
    ' | column -t

    echo ""
    echo "=== Build Summary ==="
    browserstack_api GET "automate/builds/${BUILD_ID}/sessions.json" | jq '{
        total: length,
        passed: [.[] | select(.automation_session.status == "done")] | length,
        failed: [.[] | select(.automation_session.status == "error")] | length,
        browsers: [.[].automation_session.browser] | unique
    }'
fi

echo ""
echo "=== App Automate Builds ==="
browserstack_api GET "app-automate/builds.json?limit=5" | jq -r '
    .[].automation_build | "\(.hashed_id)\t\(.name)\tstatus=\(.status)\tsessions=\(.session_count // 0)"
' | column -t 2>/dev/null || echo "No App Automate builds found"

echo ""
echo "=== Uploaded Apps ==="
browserstack_api GET "app-automate/recent_apps" | jq -r '
    .[:5][] | "\(.app_id)\t\(.app_name)\t\(.app_version)\tuploaded=\(.uploaded_at)"
' | column -t 2>/dev/null || echo "No uploaded apps"
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use limit parameter for large build/session lists
- Summarize session metadata, never include session logs inline

## Anti-Hallucination Rules
- NEVER guess build or session IDs — always discover via API
- NEVER fabricate session results — query actual BrowserStack data
- NEVER assume available browsers — check browsers.json endpoint

## Safety Rules
- NEVER terminate running sessions without explicit user confirmation
- NEVER delete builds without user approval
- NEVER upload apps without user consent
- Be mindful of parallel session limits — check plan before starting

## Output Format

Present results as a structured report:
```
Managing Browserstack Report
════════════════════════════
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

