---
name: qodana-scan
description: Read-only Qodana static analysis. Reports issues without fixing.
---

# /qodana-scan [path]

**Read-only** static analysis using Qodana. Reports issues without making any changes.

> **No arguments?** Describe this skill and stop. Do not execute.

## Target

If a path argument is provided, analyze that directory.
If no argument, analyze the current project.

## Process

### Step 1: Detect Project Type

Determine the appropriate Qodana linter:
- `qodana-jvm-community` - Java, Kotlin (free)
- `qodana-js` - JavaScript, TypeScript
- `qodana-python-community` - Python (free)
- `qodana-go` - Go
- `qodana-php` - PHP

Or use `mcp__qodana__qodana_detect` if available.

### Step 2: Run Qodana Scan (MANDATORY)

If Qodana MCP is available:
```
mcp__qodana__qodana_scan
  projectDir: <project path>
```

Otherwise, run via CLI:
```bash
qodana scan --linter <detected-linter> --project-dir <path> --results-dir .qodana
```

### Step 3: Get All Problems

If Qodana MCP is available:
```
mcp__qodana__qodana_problems
  projectDir: <project path>
```

Otherwise, parse the SARIF output:
```bash
cat .qodana/qodana.sarif.json | python3 -c "..."
```

### Step 4: Run Linting (if applicable)

```bash
npx tsc --noEmit 2>&1 || true
npm run lint 2>&1 || true
```

### Step 5: Detect AI-Generated Antipatterns

In addition to static analysis issues, flag these signs of AI-generated code:

| Antipattern | What to Look For |
|-------------|------------------|
| Over-abstraction | Factory/Builder/Wrapper used once |
| Defensive paranoia | Null checks where type says never null |
| Unused parameters | Parameters passed but never used |
| Comment spam | Comments restating obvious code |
| Over-engineered types | Deep generic hierarchies for simple data |

Report these separately from Qodana findings.

### Step 6: Compile Report (DO NOT FIX)

Collect all issues and organize by severity.

**DO NOT edit any files. Report only.**

## Output Format

```markdown
## Static Analysis Scan: [target]

### Summary

| Metric | Value |
|--------|-------|
| Files scanned | N |
| Critical issues | N |
| High issues | N |
| Moderate issues | N |
| Low issues | N |
| Lint errors | N |
| Type errors | N |

### Critical Issues 🔴

Must fix before shipping:

1. **[file:line]** — [description]
   - Rule: [rule-id]
   - Source: Qodana/ESLint/TSC

### High Issues 🟠

Should fix:

1. **[file:line]** — [description]
   - Rule: [rule-id]

### Moderate Issues 🟡

Consider fixing:

1. **[file:line]** — [description]

### Low Issues 💭

Minor improvements:

1. **[file:line]** — [description]

### By Category

| Category | Count |
|----------|-------|
| Security | N |
| Performance | N |
| Code Style | N |
| Best Practices | N |
| Type Safety | N |

### Files with Most Issues

| File | Issues |
|------|--------|
| path/to/file.ts | 5 |
| ... | ... |

---
QODANA_RESULT: called - [N] issues
LINT_RESULT: [N] errors, [N] warnings
TSC_RESULT: [N] errors
SCAN_ONLY: no fixes applied
```

## Rules

- **READ ONLY** - Do not edit any files
- **COMPLETE** - Report all issues from all tools
- **ORGANIZE** - Group issues by severity and category
- **ACTIONABLE** - Include rule IDs and file locations

## When to Use

- Pre-commit quality check (before deciding to fix)
- Assessing technical debt
- Baseline measurement before refactoring
- Quick health check on unfamiliar code
- CI pipeline reporting (without blocking)

## Anti-Patterns (Don't Do)

- Making any edits to files
- Skipping the Qodana scan
- Hiding or downplaying issues
- Summarizing without specific locations
- Applying fixes (use /qodana-review for that)

## Comparison

| Skill | Analyzes | Fixes |
|-------|----------|-------|
| `/qodana-scan` | ✓ | ✗ (read-only) |
| `/qodana-review` | ✓ | ✓ (mandatory) |
