---
name: managing-codecov
description: |
  Use when working with Codecov — codecov coverage tracking management. Covers
  coverage reporting, PR comments, flag management, component analysis, and
  coverage trend tracking. Use when managing Codecov configuration, analyzing
  coverage reports, debugging coverage uploads, or configuring coverage
  thresholds.
connection_type: codecov
preload: false
---

# Codecov Coverage Management Skill

Manage and analyze Codecov coverage reports, flags, and coverage trends.

## MANDATORY: Discovery-First Pattern

**Always check current Codecov configuration before modifying coverage settings.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Codecov Configuration ==="
cat codecov.yml 2>/dev/null || cat .codecov.yml 2>/dev/null || echo "No codecov.yml found"

echo ""
echo "=== Coverage Upload Config ==="
grep -r 'codecov\|CODECOV' .github/workflows/ 2>/dev/null | head -10

echo ""
echo "=== Coverage Files ==="
find . -name "coverage.xml" -o -name "lcov.info" -o -name "coverage.json" -o -name "*.gcov" 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
REPO="${1:-${CODECOV_REPO}}"

echo "=== Repository Coverage ==="
curl -s -H "Authorization: token ${CODECOV_TOKEN}" \
  "https://codecov.io/api/v2/github/${REPO}" 2>/dev/null | jq '{
  coverage: .coverage,
  language: .language,
  branch: .branch
}' 2>/dev/null

echo ""
echo "=== Coverage by Flag ==="
curl -s -H "Authorization: token ${CODECOV_TOKEN}" \
  "https://codecov.io/api/v2/github/${REPO}/flags" 2>/dev/null | jq '[.results[:10][] | {
  name: .flag_name,
  coverage: .coverage
}]' 2>/dev/null

echo ""
echo "=== Coverage Configuration ==="
cat codecov.yml 2>/dev/null | head -20
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Report coverage percentages with diff from target
- List flags and components with their coverage
- Show coverage trend direction

## Common Operations

### Commit Coverage

```bash
#!/bin/bash
REPO="${1:?Repo required (owner/name)}"
COMMIT="${2:-HEAD}"
echo "=== Commit Coverage ==="
curl -s -H "Authorization: token ${CODECOV_TOKEN}" \
  "https://codecov.io/api/v2/github/${REPO}/commits/${COMMIT}" 2>/dev/null | jq '{
  commitid: .commitid,
  coverage: .totals.coverage,
  files: .totals.files,
  lines: .totals.lines,
  hits: .totals.hits,
  misses: .totals.misses
}' 2>/dev/null
```

### Coverage Thresholds

```bash
#!/bin/bash
echo "=== Threshold Configuration ==="
cat codecov.yml 2>/dev/null | grep -A10 'coverage:' | head -15

echo ""
echo "=== Flag Configuration ==="
cat codecov.yml 2>/dev/null | grep -A10 'flags:' | head -15
```

## Safety Rules

- **Never lower coverage thresholds** without team agreement
- **Codecov tokens** must be stored in CI secrets, not in config files
- **Verify coverage uploads** in CI logs after pipeline changes
- **Review coverage diffs** on PRs before merging to catch regressions

## Output Format

Present results as a structured report:
```
Managing Codecov Report
═══════════════════════
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

