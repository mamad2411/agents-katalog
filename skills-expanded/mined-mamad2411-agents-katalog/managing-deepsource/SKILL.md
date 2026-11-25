---
name: managing-deepsource
description: |
  Use when working with Deepsource — deepSource code analysis management. Covers
  automated code reviews, issue detection, antipattern analysis, coverage
  tracking, and analyzer configuration. Use when managing DeepSource projects,
  reviewing detected issues, configuring analyzers, or tracking code health
  metrics.
connection_type: deepsource
preload: false
---

# DeepSource Code Analysis Management Skill

Manage and analyze DeepSource issues, analyzers, and code health metrics.

## MANDATORY: Discovery-First Pattern

**Always check current DeepSource configuration before modifying analyzer settings.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== DeepSource Configuration ==="
cat .deepsource.toml 2>/dev/null || echo "No .deepsource.toml found"

echo ""
echo "=== Enabled Analyzers ==="
grep -A5 '\[\[analyzers\]\]' .deepsource.toml 2>/dev/null | head -20

echo ""
echo "=== Transformers ==="
grep -A3 '\[\[transformers\]\]' .deepsource.toml 2>/dev/null | head -10

echo ""
echo "=== Exclude Patterns ==="
grep 'exclude_patterns' .deepsource.toml 2>/dev/null
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Project Issues (via API) ==="
curl -s -H "Authorization: Bearer ${DEEPSOURCE_TOKEN}" \
  "https://api.deepsource.com/v1/repos/${DEEPSOURCE_REPO}/issues/?status=open&limit=10" 2>/dev/null | jq '{
  total: .count,
  issues: [.results[:10][] | {
    title: .title,
    category: .category,
    severity: .severity,
    occurrences: .occurrences_count
  }]
}' 2>/dev/null

echo ""
echo "=== Analyzer Status ==="
grep -E 'name|enabled' .deepsource.toml 2>/dev/null | head -10
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Group issues by category (bug risk, antipattern, performance, security)
- Report occurrence counts per issue type
- Never expose API tokens in output

## Common Operations

### Issue Categories

```bash
#!/bin/bash
echo "=== Issues by Category ==="
curl -s -H "Authorization: Bearer ${DEEPSOURCE_TOKEN}" \
  "https://api.deepsource.com/v1/repos/${DEEPSOURCE_REPO}/issues/?status=open" 2>/dev/null | jq '{
  by_category: (.results | group_by(.category) | map({
    category: .[0].category,
    count: length
  }))
}' 2>/dev/null
```

### Configuration Validation

```bash
#!/bin/bash
echo "=== Config Validation ==="
cat .deepsource.toml 2>/dev/null
echo ""
echo "=== Supported Analyzers ==="
echo "python, go, javascript, ruby, java, rust, sql, docker, terraform, shell"
```

## Safety Rules

- **Review analyzer configurations** before enabling new analyzers on active repos
- **DeepSource tokens** must be stored in CI secrets
- **Do not suppress issues globally** -- use inline comments for justified cases only
- **Monitor false positive rates** and adjust analyzer settings accordingly

## Output Format

Present results as a structured report:
```
Managing Deepsource Report
══════════════════════════
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

