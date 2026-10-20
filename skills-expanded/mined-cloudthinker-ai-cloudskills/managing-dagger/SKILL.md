---
name: managing-dagger
description: |
  Use when working with Dagger — dagger CI/CD pipeline management. Covers
  pipeline-as-code configuration, module management, function execution, caching
  layers, container builds, and pipeline debugging. Use when managing Dagger
  pipelines, debugging function execution, inspecting modules, or optimizing
  container-based CI workflows.
connection_type: dagger
preload: false
---

# Dagger CI/CD Pipeline Management Skill

Manage and analyze Dagger pipelines, modules, and container-based CI/CD workflows.

## MANDATORY: Discovery-First Pattern

**Always check current Dagger configuration and module structure before modifying pipelines.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Dagger Configuration ==="
cat dagger.json 2>/dev/null || echo "No dagger.json found"

echo ""
echo "=== Dagger Module Structure ==="
ls -la dagger/ 2>/dev/null || ls -la .dagger/ 2>/dev/null
find . -name "dagger.json" -not -path "*/node_modules/*" 2>/dev/null | head -10

echo ""
echo "=== Dagger Version ==="
dagger version 2>/dev/null

echo ""
echo "=== Available Functions ==="
dagger functions 2>/dev/null | head -20
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Module Dependencies ==="
cat dagger.json 2>/dev/null | jq '{
  name: .name,
  sdk: .sdk,
  dependencies: .dependencies
}' 2>/dev/null

echo ""
echo "=== Pipeline Functions ==="
dagger functions --json 2>/dev/null | jq '[.[] | {
  name: .name,
  description: .description,
  args: [.args[]? | .name]
}]' 2>/dev/null | head -30
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- List available functions with their arguments
- Summarize module dependency trees
- Report pipeline execution status concisely

## Common Operations

### Execute Pipeline Function

```bash
#!/bin/bash
FUNC="${1:?Function name required}"
echo "=== Running $FUNC ==="
dagger call "$FUNC" 2>&1 | tail -20
```

### Module Inspection

```bash
#!/bin/bash
echo "=== Installed Modules ==="
dagger mod list 2>/dev/null | head -15

echo ""
echo "=== Module Source ==="
find . -path "*/dagger/*.go" -o -path "*/dagger/*.ts" -o -path "*/dagger/*.py" 2>/dev/null | head -10
```

## Safety Rules

- **Test pipeline changes locally** with `dagger call` before pushing to CI
- **Never expose secrets in function arguments** -- use Dagger secret references
- **Review container images** used in pipelines for vulnerability exposure
- **Cache layers carefully** -- stale caches can cause non-reproducible builds

## Output Format

Present results as a structured report:
```
Managing Dagger Report
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

