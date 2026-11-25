---
name: managing-codacy
description: |
  Use when working with Codacy — codacy code quality management. Covers
  automated code reviews, pattern configuration, coverage tracking, security
  analysis, and repository settings. Use when managing Codacy projects,
  reviewing code patterns, configuring quality gates, or tracking code quality
  trends.
connection_type: codacy
preload: false
---

# Codacy Code Quality Management Skill

Manage and analyze Codacy code reviews, patterns, coverage, and quality metrics.

## MANDATORY: Discovery-First Pattern

**Always check current Codacy configuration before modifying quality settings.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Codacy Configuration ==="
cat .codacy.yml 2>/dev/null || cat .codacy.yaml 2>/dev/null || echo "No .codacy.yml found"

echo ""
echo "=== Repository Info ==="
curl -s -H "api-token: ${CODACY_TOKEN}" \
  "https://app.codacy.com/api/v3/organizations/gh/${CODACY_ORG}/repositories/${CODACY_REPO}" 2>/dev/null | jq '{
  name: .data.name,
  language: .data.language,
  grade: .data.grade
}' 2>/dev/null

echo ""
echo "=== Tool Configuration ==="
cat .codacy.yml 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Quality Overview ==="
curl -s -H "api-token: ${CODACY_TOKEN}" \
  "https://app.codacy.com/api/v3/organizations/gh/${CODACY_ORG}/repositories/${CODACY_REPO}/dashboard" 2>/dev/null | jq '{
  grade: .data.grade,
  coverage: .data.coverage,
  issues: .data.issues,
  complexity: .data.complexity,
  duplication: .data.duplication
}' 2>/dev/null

echo ""
echo "=== Open Issues ==="
curl -s -H "api-token: ${CODACY_TOKEN}" \
  "https://app.codacy.com/api/v3/organizations/gh/${CODACY_ORG}/repositories/${CODACY_REPO}/issues?limit=10" 2>/dev/null | jq '[.data[:10][] | {
  pattern: .patternInfo.id,
  category: .patternInfo.category,
  level: .patternInfo.level,
  file: .filePath
}]' 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Report grade and coverage as summary metrics
- Group issues by category and severity
- Never expose API tokens in output

## Common Operations

### PR Analysis

```bash
#!/bin/bash
PR_NUMBER="${1:?PR number required}"
echo "=== PR Quality ==="
curl -s -H "api-token: ${CODACY_TOKEN}" \
  "https://app.codacy.com/api/v3/organizations/gh/${CODACY_ORG}/repositories/${CODACY_REPO}/pull-requests/${PR_NUMBER}" 2>/dev/null | jq '{
  isUpToStandards: .data.isUpToStandards,
  newIssues: .data.newIssues,
  fixedIssues: .data.fixedIssues,
  coverage: .data.coverage
}' 2>/dev/null
```

### Pattern Management

```bash
#!/bin/bash
echo "=== Enabled Patterns ==="
curl -s -H "api-token: ${CODACY_TOKEN}" \
  "https://app.codacy.com/api/v3/organizations/gh/${CODACY_ORG}/repositories/${CODACY_REPO}/patterns?enabled=true&limit=10" 2>/dev/null | jq '[.data[:10][] | {
  id: .id,
  category: .category,
  level: .level
}]' 2>/dev/null
```

## Safety Rules

- **Never disable security patterns** without documented justification
- **Codacy API tokens** must be stored in CI secrets
- **Review quality gate changes** with the team before applying
- **Monitor false positive rates** and adjust patterns to maintain developer trust

## Output Format

Present results as a structured report:
```
Managing Codacy Report
══════════════════════
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

