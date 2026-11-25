---
name: verification-loop
description: Comprehensive verification system for Antigravity sessions. Run after completing features, before PRs, or after refactoring to ensure all quality gates pass.
model: gemini-2.0-flash
---

# Verification Loop Skill

A comprehensive verification system for Antigravity sessions.

## When to Use

- After completing a feature or significant code change
- Before creating a PR
- After refactoring
- When you want to ensure quality gates pass

## Verification Phases

### Phase 1: Build Verification

```bash
npm run build 2>&1 | tail -20
```

If build fails, STOP and fix before continuing.

### Phase 2: Type Check

```bash
npx tsc --noEmit 2>&1 | head -30
```

Report all type errors. Fix critical ones before continuing.

### Phase 3: Lint Check

```bash
npm run lint 2>&1 | head -30
```

### Phase 4: Test Suite

```bash
npm run test -- --coverage 2>&1 | tail -50
```

Report: total tests, passed, failed, coverage %.
Target: 80% minimum.

### Phase 5: Security Scan

```bash
# Check for secrets
grep -rn "sk-\|api_key\|password" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# Check for console.log
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

### Phase 6: Diff Review

```bash
git diff --stat
git diff HEAD~1 --name-only
```

Review each changed file for unintended changes, missing error handling, and edge cases.

## Output Format

```
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Continuous Mode

Run verification after each major change:
- After completing each function
- After finishing a component
- Before moving to next task

Use `/verify` command to trigger this skill.

## Integration with Commands

- `/verify quick` - Build + types only
- `/verify full` - All phases (default)
- `/verify pre-pr` - Full + security scan
- `/checkpoint create` - Runs quick verify first
