---
name: test-coverage
description: Runs coverage report, identifies untested code, and generates missing tests
user-invocable: true
allowed-tools: Bash Read Glob Edit
effort: medium
---

## Test Coverage Analysis

1. Run coverage:
```bash
# Detect test runner from package.json
cat package.json | grep -E '"test"|"coverage"'
```
Then run the appropriate coverage command (e.g., `bun test --coverage`, `npx jest --coverage`, `go test ./... -cover`).

2. Parse results and find:
   - Overall coverage percentage
   - Files below 80% coverage
   - Uncovered functions/branches (not just lines)

3. For the 3 most under-tested files:
   - Read the file
   - Identify exactly which branches/conditions are untested
   - Generate tests to cover them

4. Report:
```
Coverage: X% (was Y% if previous data available)

Files needing attention:
  src/auth/token.ts       42% → generated 8 tests
  src/utils/format.ts     61% → generated 4 tests
  src/api/handler.ts      70% → generated 3 tests
```
