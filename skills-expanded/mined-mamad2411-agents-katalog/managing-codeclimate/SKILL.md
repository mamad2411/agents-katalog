---
name: managing-codeclimate
description: |
  Use when working with Codeclimate — code Climate quality management. Covers
  maintainability analysis, test coverage tracking, issue detection, GPA
  scoring, and repository configuration. Use when managing Code Climate
  projects, reviewing maintainability ratings, tracking test coverage trends, or
  configuring analysis engines.
connection_type: codeclimate
preload: false
---

# Code Climate Quality Management Skill

Manage and analyze Code Climate maintainability, coverage, and issue tracking.

## MANDATORY: Discovery-First Pattern

**Always check current Code Climate configuration before modifying analysis settings.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Code Climate Configuration ==="
cat .codeclimate.yml 2>/dev/null || echo "No .codeclimate.yml found"

echo ""
echo "=== Repository Summary ==="
curl -s -H "Authorization: Token token=${CC_TOKEN}" \
  "https://api.codeclimate.com/v1/repos?github_slug=${CC_REPO}" 2>/dev/null | jq '{
  id: .data[0].id,
  score: .data[0].attributes.score,
  badge: .data[0].attributes.badge_token
}' 2>/dev/null

echo ""
echo "=== Enabled Engines ==="
cat .codeclimate.yml 2>/dev/null | grep -A1 'engines\|plugins' | head -15
```

### Phase 2: Analysis

```bash
#!/bin/bash
REPO_ID="${CC_REPO_ID:?Repo ID required}"

echo "=== Maintainability Rating ==="
curl -s -H "Authorization: Token token=${CC_TOKEN}" \
  "https://api.codeclimate.com/v1/repos/${REPO_ID}/snapshots" 2>/dev/null | jq '{
  gpa: .data[0].attributes.gpa,
  ratings: [.data[0].attributes.ratings[] | {
    letter: .letter,
    measure: .measure.value,
    pillar: .pillar
  }]
}' 2>/dev/null

echo ""
echo "=== Test Coverage ==="
curl -s -H "Authorization: Token token=${CC_TOKEN}" \
  "https://api.codeclimate.com/v1/repos/${REPO_ID}/test_reports" 2>/dev/null | jq '{
  coverage: .data[0].attributes.coverage_pct,
  lines_of_code: .data[0].attributes.lines_of_code,
  covered_percent: .data[0].attributes.covered_percent
}' 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Report GPA and letter ratings concisely
- Show coverage percentages with trends
- Group issues by category and severity

## Common Operations

### Issue Summary

```bash
#!/bin/bash
REPO_ID="${CC_REPO_ID:?Repo ID required}"
echo "=== Open Issues ==="
curl -s -H "Authorization: Token token=${CC_TOKEN}" \
  "https://api.codeclimate.com/v1/repos/${REPO_ID}/issues?page[size]=10" 2>/dev/null | jq '[.data[] | {
  check: .attributes.check_name,
  severity: .attributes.severity,
  location: .attributes.location.path,
  description: .attributes.description[:60]
}]' 2>/dev/null
```

### Local Analysis

```bash
#!/bin/bash
echo "=== Local Analysis ==="
codeclimate analyze 2>&1 | tail -20
```

## Safety Rules

- **Never disable engines** without understanding coverage gaps
- **Review GPA trends** before merging large PRs
- **Code Climate tokens** should be stored in CI secrets
- **Configure exclusion patterns** carefully to avoid hiding real issues

## Output Format

Present results as a structured report:
```
Managing Codeclimate Report
═══════════════════════════
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

