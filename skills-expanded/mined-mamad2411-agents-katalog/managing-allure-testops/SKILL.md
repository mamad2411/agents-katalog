---
name: managing-allure-testops
description: |
  Use when working with Allure Testops — allure TestOps test management and
  analytics platform monitoring. Covers project dashboards, launch tracking,
  test case management, defect clustering, environment matrix analysis, and
  CI/CD integration review. Use when managing test cases in Allure TestOps,
  reviewing launch results, analyzing flaky tests, or tracking quality trends.
connection_type: allure-testops
preload: false
---

# Allure TestOps Management Skill

Manage and analyze Allure TestOps projects, launches, test cases, and analytics.

## Core Helper Functions

```bash
#!/bin/bash

# Allure TestOps API helper
allure_api() {
    local method="${1:-GET}"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Api-Token ${ALLURE_TESTOPS_TOKEN}" \
            -H "Content-Type: application/json" \
            "${ALLURE_TESTOPS_URL}/api/rs/${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Api-Token ${ALLURE_TESTOPS_TOKEN}" \
            "${ALLURE_TESTOPS_URL}/api/rs/${endpoint}"
    fi
}
```

## MANDATORY: Discovery-First Pattern

**Always discover projects and launches before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Allure TestOps Projects ==="
allure_api GET "project?page=0&size=20" | jq -r '
    .content[] | "\(.id)\t\(.name)\tstatus=\(.isPublic | if . then "public" else "private" end)"
' | column -t

echo ""
echo "=== Recent Launches ==="
PROJECT_ID="${1:?Project ID required}"
allure_api GET "launch?projectId=${PROJECT_ID}&page=0&size=10&sort=createdDate,desc" | jq -r '
    .content[] | "\(.id)\t\(.name)\tstatus=\(.status)\tpassed=\(.statistic.passed)\tfailed=\(.statistic.failed)"
' | column -t

echo ""
echo "=== Test Case Tree ==="
allure_api GET "testcasetree/leaf?projectId=${PROJECT_ID}&page=0&size=15" | jq -r '
    .content[] | "\(.id)\t\(.name)\tstatus=\(.status // "draft")"
' | column -t

echo ""
echo "=== Environments ==="
allure_api GET "environment?projectId=${PROJECT_ID}" | jq -r '
    .[] | "\(.id)\t\(.name)\t\(.slug)"
' | column -t | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

PROJECT_ID="${1:?Project ID required}"

echo "=== Launch Details ==="
LAUNCH_ID="${2:-}"
if [ -n "$LAUNCH_ID" ]; then
    allure_api GET "launch/${LAUNCH_ID}" | jq '{
        name: .name,
        status: .status,
        stats: .statistic,
        created: .createdDate,
        closed: .closedDate
    }'

    echo ""
    echo "=== Failed Test Results ==="
    allure_api GET "testresult?launchId=${LAUNCH_ID}&status=failed&page=0&size=15" | jq -r '
        .content[] | "\(.testCase.name // "unnamed")\tstatus=\(.status)\tduration=\(.duration // 0)ms"
    ' | column -t
fi

echo ""
echo "=== Flaky Tests ==="
allure_api GET "testcase?projectId=${PROJECT_ID}&flaky=true&page=0&size=10" | jq -r '
    .content[] | "\(.id)\t\(.name)\tflaky=true"
' | column -t

echo ""
echo "=== Defect Categories ==="
allure_api GET "defectcategory?projectId=${PROJECT_ID}" | jq -r '
    .[] | "\(.id)\t\(.name)\tcount=\(.defectCount // 0)"
' | column -t | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Use API pagination (page/size) for large datasets
- Summarize launch statistics, not individual step details

## Anti-Hallucination Rules
- NEVER guess project or launch IDs — always discover via API
- NEVER fabricate test results — query actual launch data
- NEVER assume API version — Allure TestOps API may vary by version

## Safety Rules
- NEVER close or delete launches without explicit user confirmation
- NEVER modify test case status without user approval
- NEVER trigger re-runs without user consent

## Output Format

Present results as a structured report:
```
Managing Allure Testops Report
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

