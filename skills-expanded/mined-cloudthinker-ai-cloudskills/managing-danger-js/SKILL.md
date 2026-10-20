---
name: managing-danger-js
description: |
  Use when working with Danger Js — danger JS automated code review management.
  Covers Dangerfile configuration, PR rule enforcement, plugin management, CI
  integration, and custom rule development. Use when managing Danger JS rules,
  configuring PR checks, debugging Dangerfile execution, or enforcing team code
  review policies.
connection_type: danger-js
preload: false
---

# Danger JS Code Review Management Skill

Manage and analyze Danger JS PR rules, plugins, and automated code review enforcement.

## MANDATORY: Discovery-First Pattern

**Always check current Dangerfile configuration before modifying PR rules.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Dangerfile ==="
cat dangerfile.ts 2>/dev/null || cat dangerfile.js 2>/dev/null || cat Dangerfile 2>/dev/null | head -30

echo ""
echo "=== Danger Dependencies ==="
cat package.json 2>/dev/null | jq '{
  danger: .devDependencies.danger,
  plugins: [.devDependencies | to_entries[] | select(.key | startswith("danger-plugin")) | .key]
}' 2>/dev/null

echo ""
echo "=== CI Integration ==="
grep -r 'danger' .github/workflows/ 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Danger Rules Summary ==="
grep -E 'warn\(|fail\(|message\(|markdown\(' dangerfile.ts dangerfile.js Dangerfile 2>/dev/null | head -15

echo ""
echo "=== Plugins Configured ==="
grep -E 'import.*danger-plugin\|require.*danger-plugin' dangerfile.ts dangerfile.js 2>/dev/null | head -10

echo ""
echo "=== Danger Version ==="
npx danger --version 2>/dev/null
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- List PR rules with their severity (warn/fail/message)
- Show plugin configurations
- Report CI integration method

## Common Operations

### Dry Run

```bash
#!/bin/bash
echo "=== Danger Dry Run ==="
npx danger pr --dry-run 2>&1 | tail -20
```

### Local Run Against PR

```bash
#!/bin/bash
PR_URL="${1:?PR URL required}"
echo "=== Danger PR Check ==="
npx danger pr "$PR_URL" 2>&1 | tail -20
```

## Safety Rules

- **Use `warn()` for suggestions and `fail()` only for blocking issues**
- **Test Dangerfile changes** with `danger pr --dry-run` before merging
- **Danger tokens** must have minimum required GitHub permissions
- **Review plugin updates** -- plugins execute in CI with repository access

## Output Format

Present results as a structured report:
```
Managing Danger Js Report
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

