---
name: run-verification
description: Run the full verification pipeline (lint, unit tests, E2E if UI changed) — invoke after code changes
---

# Run Verification Pipeline

Run after every code change to ensure nothing is broken. Execute in order — stop on first failure.

## Pipeline

### 1. Lint Check
```bash
# Run your project's linter
$LINT_CMD 2>&1 | tail -20
```
- If errors: report them and STOP
- If warnings only: continue (note the count)

### 2. Unit Tests
```bash
# Run your project's test suite
$TEST_CMD 2>&1
```
- All tests must pass
- If failures: report failing test names and STOP

### 3. E2E Tests (conditional)
Only run if frontend files were modified in this session.
```bash
# Run your project's E2E test suite (e.g., Playwright, Cypress)
$E2E_CMD 2>&1
```
- All tests must pass
- If failures: report and STOP

### 4. Frontend Build Check (conditional)
Only run if frontend files were modified.
```bash
# Run your project's frontend build
$BUILD_CMD 2>&1 | tail -10
```

## Output Format

Report results as:
```
VERIFICATION:
- Lint: PASS (N warnings) / FAIL
- Unit tests: PASS (N tests) / FAIL (list failures)
- E2E tests: PASS / FAIL / SKIPPED (no UI changes)
- Build: PASS / SKIPPED (no UI changes)
```

## Stack Resolution

Read `.claude/enterprise-state/stack-profile.json` to resolve the actual commands:
- `$LINT_CMD` = `commands.lint`
- `$TEST_CMD` = `commands.test_all`
- `$E2E_CMD` = `commands.e2e_test`
- `$BUILD_CMD` = `commands.build_frontend`

If no stack profile exists, use the commands from CLAUDE.md or package.json scripts.
