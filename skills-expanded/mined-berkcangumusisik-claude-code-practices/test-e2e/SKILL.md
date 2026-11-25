---
name: test-e2e
description: Generates end-to-end tests for a user flow using Playwright or Cypress
argument-hint: <flow-description>
user-invocable: true
allowed-tools: Read Glob Edit Bash
effort: medium
---

## Generate E2E Tests

Flow to test: **$ARGUMENTS**

1. Detect the E2E framework:
```bash
cat package.json | grep -E "playwright|cypress|puppeteer"
ls e2e/ tests/ cypress/ playwright/ 2>/dev/null | head -20
```

2. Read 2-3 existing E2E test files to understand the project's patterns, selectors, and helpers.

3. Generate the E2E test covering:
   - Setup (auth if needed, navigation to starting point)
   - The full user flow step by step
   - Assertions at each key step
   - Teardown / cleanup

4. Use data-testid selectors by preference, then aria labels, then text - avoid CSS class selectors.

5. Place the test in the correct directory matching project conventions.

6. Note any test data or environment variables required.
