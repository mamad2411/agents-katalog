---
name: verification-loop
description: Comprehensive verification system for code quality. Use after completing features, before PRs, or after refactoring.
---

# Verification Loop Skill

Comprehensive verification system for ensuring code quality across Fusion Labs projects.

## When to Activate

- After completing a feature or significant code change
- Before creating a pull request
- When you want to ensure quality gates pass
- After refactoring

## Verification Phases

### Phase 1: Build Verification

```bash
# Go projects
go build ./...

# TypeScript/React projects (Vite)
npm run build 2>&1 | tail -20
```

If the build fails, **stop** and fix before continuing.

### Phase 2: Type Checking

```bash
# TypeScript projects
npx tsc --noEmit 2>&1 | head -30

# Go projects (go vet acts as type checker + static analysis)
go vet ./...
```

Report all type errors. Fix critical ones before continuing.

### Phase 3: Lint Check

```bash
# Go
golangci-lint run 2>&1 | head -30

# TypeScript/JavaScript
npm run lint 2>&1 | head -30
```

### Phase 4: Test Suite

```bash
# Go — with coverage
go test -cover ./... 2>&1 | tail -50

# TypeScript/React — with coverage
npm run test -- --coverage 2>&1 | tail -50

# Coverage target: minimum 80%
```

Report:
- Total tests: X
- Passed: X
- Failed: X
- Coverage: X%

### Phase 5: Security Scan

```bash
# Check for hardcoded secrets
grep -rn "sk-" --include="*.go" --include="*.ts" --include="*.tsx" . 2>/dev/null | head -10
grep -rn "password.*=" --include="*.go" --include="*.ts" . 2>/dev/null | grep -v "_test\." | head -10

# Check for console.log in production code
grep -rn "console.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10

# Check for fmt.Println in production code
grep -rn "fmt.Println" --include="*.go" . 2>/dev/null | grep -v "_test\." | head -10

# Go dependency check
go list -m all | nancy sleuth 2>/dev/null

# Node dependency check
npm audit 2>/dev/null
```

### Phase 6: Diff Review

```bash
# Show what changed
git diff --stat
git diff HEAD~1 --name-only
```

Review each changed file for:
- Unintended changes
- Missing error handling
- Potential edge cases
- Security implications

## Output Format

After running all phases, produce a verification report:

```
Verification Report
==================

Build:      [PASS/FAIL]
Types:      [PASS/FAIL] (X errors)
Lint:       [PASS/FAIL] (X warnings)
Tests:      [PASS/FAIL] (X/Y passed, Z% coverage)
Security:   [PASS/FAIL] (X issues)
Diff:       [X files changed]

Overall:    PR Ready [YES/NO]

Issues to Fix:
1. ...
2. ...
```

## Continuous Mode

For long sessions, run verification every 15 minutes or after major changes:

```markdown
Set mental checkpoints:
- After completing each function
- After completing a component
- Before moving to the next task

Run: /verify
```

## Integration with Hooks

This skill complements PostToolUse hooks but provides deeper verification.
Hooks catch issues immediately; this skill provides comprehensive review.

## Quick Verify Commands

```bash
# Go — full check
go build ./... && go vet ./... && go test -race -cover ./...

# TypeScript — full check
npx tsc --noEmit && npm run lint && npm run test -- --coverage

# Docker — verify services are healthy
docker-compose ps
docker-compose exec postgres pg_isready -U devuser
docker-compose exec redis redis-cli -a devpassword ping
```

---

**Remember**: Verification is not a final step — it's a continuous practice. The earlier you catch issues, the cheaper they are to fix.
