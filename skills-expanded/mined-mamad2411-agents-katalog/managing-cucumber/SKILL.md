---
name: managing-cucumber
description: |
  Use when working with Cucumber — cucumber BDD testing management and analysis.
  Covers feature file organization, step definition mapping, scenario tagging,
  Gherkin syntax validation, test report parsing, and step reuse analysis. Use
  when managing Cucumber test suites, investigating BDD scenario failures, or
  reviewing feature file coverage.
connection_type: cucumber
preload: false
---

# Cucumber BDD Testing Management Skill

Manage and analyze Cucumber feature files, step definitions, and test results.

## Core Helper Functions

```bash
#!/bin/bash

# Parse Cucumber JSON report
cucumber_results() {
    local report="${1:-cucumber-report.json}"
    cat "$report" 2>/dev/null | jq '{
        features: length,
        scenarios: [.[].elements[] | select(.type == "scenario")] | length,
        passed: [.[].elements[] | select(.type == "scenario") | select(all(.steps[].result.status; . == "passed"))] | length,
        failed: [.[].elements[] | select(.type == "scenario") | select(any(.steps[].result.status; . == "failed"))] | length
    }'
}
```

## MANDATORY: Discovery-First Pattern

**Always discover feature files and step definitions before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Feature Files ==="
find . -name "*.feature" 2>/dev/null | grep -v node_modules | wc -l | xargs echo "Total feature files:"
find . -name "*.feature" 2>/dev/null | grep -v node_modules | head -15

echo ""
echo "=== Scenario Summary ==="
find . -name "*.feature" 2>/dev/null | grep -v node_modules | while read f; do
    SCENARIOS=$(grep -c "Scenario:" "$f" 2>/dev/null || echo 0)
    echo "$(basename $f)\t${SCENARIOS} scenarios"
done | column -t | head -15

echo ""
echo "=== Step Definition Files ==="
find . -name "*steps*" -o -name "*step_definitions*" 2>/dev/null | grep -v node_modules | head -15

echo ""
echo "=== Tags in Use ==="
grep -rh "@" --include="*.feature" 2>/dev/null | grep -oP "@\w+" | sort | uniq -c | sort -rn | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Test Results ==="
REPORT=$(find . -name "cucumber-report.json" -o -name "cucumber_report.json" 2>/dev/null | head -1)
if [ -n "$REPORT" ]; then
    cucumber_results "$REPORT"

    echo ""
    echo "=== Failed Scenarios ==="
    cat "$REPORT" | jq -r '
        .[].elements[] | select(.type == "scenario") |
        select(any(.steps[].result.status; . == "failed")) |
        "\(.name)\t\(.tags | map(.name) | join(","))"
    ' | column -t | head -15

    echo ""
    echo "=== Failed Steps ==="
    cat "$REPORT" | jq -r '
        .[].elements[].steps[] | select(.result.status == "failed") |
        "\(.keyword)\(.name)\t\(.result.error_message | split("\n")[0] // "unknown")"
    ' | head -10
fi

echo ""
echo "=== Undefined Steps ==="
if [ -n "$REPORT" ]; then
    cat "$REPORT" | jq -r '
        .[].elements[].steps[] | select(.result.status == "undefined") |
        "\(.keyword)\(.name)"
    ' | sort -u | head -10
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Parse JSON or HTML reports for structured data
- Never dump full feature files — summarize scenario names and tags

## Anti-Hallucination Rules
- NEVER guess feature file names — always discover via filesystem
- NEVER fabricate scenario results — parse actual Cucumber reports
- NEVER assume step definitions exist — check for undefined steps

## Safety Rules
- NEVER modify feature files or step definitions without user confirmation
- NEVER delete test reports without user approval
- NEVER change tag configurations without user consent

## Output Format

Present results as a structured report:
```
Managing Cucumber Report
════════════════════════
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

