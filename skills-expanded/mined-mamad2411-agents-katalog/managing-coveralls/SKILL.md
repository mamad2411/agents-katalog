---
name: managing-coveralls
description: |
  Use when working with Coveralls — coveralls coverage tracking management.
  Covers coverage reporting, PR status checks, repository configuration,
  coverage history, and badge management. Use when managing Coveralls coverage
  reports, configuring coverage thresholds, debugging coverage uploads, or
  analyzing coverage trends.
connection_type: coveralls
preload: false
---

# Coveralls Coverage Management Skill

Manage and analyze Coveralls coverage reports, thresholds, and coverage history.

## MANDATORY: Discovery-First Pattern

**Always check current Coveralls configuration before modifying coverage settings.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Coveralls Configuration ==="
cat .coveralls.yml 2>/dev/null || echo "No .coveralls.yml found"

echo ""
echo "=== CI Coverage Upload ==="
grep -r 'coveralls\|COVERALLS' .github/workflows/ .circleci/ .travis.yml 2>/dev/null | head -10

echo ""
echo "=== Coverage Tool Config ==="
cat .nycrc 2>/dev/null || cat jest.config.* 2>/dev/null | grep -A5 'coverage' | head -10
cat .coveragerc 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash
REPO="${1:-${COVERALLS_REPO}}"

echo "=== Repository Coverage ==="
curl -s "https://coveralls.io/github/${REPO}.json" 2>/dev/null | jq '{
  coverage: .covered_percent,
  badge_url: .badge_url,
  created_at: .created_at,
  commit_sha: .commit_sha
}' 2>/dev/null

echo ""
echo "=== Recent Builds ==="
curl -s "https://coveralls.io/github/${REPO}.json?page=1" 2>/dev/null | jq '{
  coverage: .covered_percent,
  change: .coverage_change,
  relevant_lines: .relevant_lines,
  covered_lines: .covered_lines
}' 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Report coverage percentage with change from previous
- Show relevant vs covered line counts
- Never expose repo tokens in output

## Common Operations

### Build Coverage History

```bash
#!/bin/bash
REPO="${1:?Repo required (owner/name)}"
echo "=== Coverage History ==="
curl -s "https://coveralls.io/github/${REPO}.json?page=1" 2>/dev/null | jq '{
  current: .covered_percent,
  change: .coverage_change,
  repo_token_set: (.repo_token != null)
}' 2>/dev/null
```

### Upload Verification

```bash
#!/bin/bash
echo "=== Recent Upload Status ==="
grep -r 'coveralls' .github/workflows/ 2>/dev/null | head -5
echo ""
echo "=== Coverage File ==="
find . -name "lcov.info" -o -name "coverage.xml" 2>/dev/null | head -5
```

## Safety Rules

- **Never commit `.coveralls.yml` with repo tokens** -- use CI environment variables
- **Verify coverage uploads** after CI pipeline changes
- **Review coverage decreases** on PRs before merging
- **Configure minimum coverage thresholds** to prevent regressions

## Output Format

Present results as a structured report:
```
Managing Coveralls Report
═════════════════════════
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

