---
name: managing-cypress-deep
description: |
  Use when working with Cypress Deep — cypress end-to-end testing management and
  analysis. Covers test execution monitoring, dashboard integration, screenshot
  and video analysis, test report parsing, flaky test detection, and
  configuration auditing. Use when investigating test failures, reviewing
  Cypress Cloud results, or managing Cypress test suites.
connection_type: cypress
preload: false
---

# Cypress E2E Testing Management Skill

Manage and analyze Cypress test suites, results, and configurations.

## Core Helper Functions

```bash
#!/bin/bash

# Cypress Cloud API helper
cypress_cloud_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer ${CYPRESS_API_TOKEN}" \
        "https://cloud.cypress.io/api/v1/${endpoint}"
}

# Parse Cypress test results
cypress_results() {
    local results_dir="${CYPRESS_RESULTS_DIR:-cypress/results}"
    cat "${results_dir}/results.json" 2>/dev/null || echo '{"stats":{},"results":[]}'
}
```

## MANDATORY: Discovery-First Pattern

**Always discover test configuration and project structure before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Cypress Configuration ==="
if [ -f "cypress.config.ts" ]; then
    grep -E "(baseUrl|specPattern|viewportWidth|viewportHeight|video|screenshotOnRunFailure|retries|projectId)" cypress.config.ts | head -15
elif [ -f "cypress.config.js" ]; then
    grep -E "(baseUrl|specPattern|viewportWidth|viewportHeight|video|screenshotOnRunFailure|retries|projectId)" cypress.config.js | head -15
fi

echo ""
echo "=== Test File Summary ==="
SPEC_DIR="${CYPRESS_SPEC_DIR:-cypress/e2e}"
find "$SPEC_DIR" -name "*.cy.ts" -o -name "*.cy.js" -o -name "*.spec.ts" -o -name "*.spec.js" 2>/dev/null | wc -l | xargs echo "Total spec files:"
find "$SPEC_DIR" -name "*.cy.ts" -o -name "*.cy.js" 2>/dev/null | head -15

echo ""
echo "=== Cypress Version ==="
npx cypress --version 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Last Run Results ==="
REPORT="cypress/results/results.json"
if [ -f "$REPORT" ]; then
    cat "$REPORT" | jq '{
        total: .stats.tests,
        passed: .stats.passes,
        failed: .stats.failures,
        pending: .stats.pending,
        skipped: .stats.skipped,
        duration_sec: (.stats.duration / 1000 | floor)
    }'

    echo ""
    echo "=== Failed Tests ==="
    cat "$REPORT" | jq -r '
        .results[].suites[].tests[] | select(.fail == true) |
        "\(.title)\t\(.duration/1000|floor)s\t\(.err.message // "unknown" | split("\n")[0])"
    ' | column -t | head -15
fi

echo ""
echo "=== Cypress Cloud Project Runs ==="
if [ -n "$CYPRESS_API_TOKEN" ]; then
    cypress_cloud_api "projects/${CYPRESS_PROJECT_ID}/runs?page=1&per_page=5" | jq -r '
        .data[] | "\(.buildNumber)\t\(.status)\t\(.totalPassed)/\(.totalTests) passed\t\(.createdAt | split("T")[0])"
    ' | column -t
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Parse mochawesome or built-in JSON reports
- Never dump full video files — reference paths only

## Anti-Hallucination Rules
- NEVER guess spec file names — always discover via filesystem first
- NEVER fabricate test results — parse actual report files
- NEVER assume Cypress Cloud is configured — check for projectId first

## Safety Rules
- NEVER modify test files without explicit user confirmation
- NEVER delete screenshots, videos, or results without user approval
- Running tests may launch browsers — warn user before execution

## Output Format

Present results as a structured report:
```
Managing Cypress Deep Report
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

