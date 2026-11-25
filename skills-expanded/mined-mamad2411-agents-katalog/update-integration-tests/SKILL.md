---
name: "update-integration-tests"
description: "Detect codebase changes, update or create integration tests to cover them, run ALL integration tests, and fix every failure until the full suite passes. Use when code changes need integration test coverage, when asked to update or sync integration tests, or after implementing features that affect API behavior."
---

# Update Integration Tests

Detects what changed across the monorepo, updates or creates integration tests in `repos/integration/` to cover those changes, then runs the full test suite and fixes every failure until everything is green.

Optional arguments: $ARGUMENTS

## Workflow

### Step 1: Detect Changes

Run these git commands in parallel to identify all changed source files:
- `git diff --name-only` (unstaged changes)
- `git diff --name-only --cached` (staged changes)
- `git diff --name-only main...HEAD` (all branch changes vs main)

Deduplicate the results and group by sub-repo (`repos/<name>/`).

Filter out non-source files — skip anything matching: `*.md`, `*.lock`, `*.json` (except `package.json` with dependency changes), `.claude/`, `docs/`, `deploy/`, `configs/` (unless vitest/playwright config changed).

If no source changes are detected, tell the user and stop.

Output a change summary: which repos changed, how many files, which areas (models, routes, services, types, utils).

### Step 2: Load Context

1. Load the `tdsk-integration` skill for integration test infrastructure knowledge.
2. For each changed repo, load its corresponding skill (e.g., changes in `repos/backend/` → load `tdsk-backend` skill).
3. Use parallel sub-agents (one per changed repo) to:
   - Read the changed source files to understand what behavior changed (new fields, renamed properties, new endpoints, modified response shapes, changed validation)
   - Grep `repos/integration/src/` for references to the affected endpoints, models, or features
   - Identify which existing integration tests exercise the changed code paths
4. Compile a mapping: changed code → existing test coverage (or lack thereof).

### Step 3: Plan Test Changes

For each changed area, determine the action:

- **Update existing test**: A test file exists but its assertions or setup need updating to match new behavior (new fields, renamed properties, changed response shapes, updated validation rules).
- **Write new test**: No existing integration test covers this code path. Determine the appropriate tier:
  - **Tier 1**: API contract tests — CRUD operations, auth checks, field persistence, validation. No live infrastructure required beyond the API.
  - **Tier 3**: Live infrastructure tests — sandbox pod lifecycle, SSH tunneling, WebSocket connections, K8s exec. Requires real K8s pods.
- **No test change needed**: Internal refactoring without behavior change; existing tests already cover the public behavior.

Present the plan to the user before proceeding. List each test file to update or create with a brief rationale.

### Step 4: Implement Test Changes

Use sub-agents for parallel work across independent test files and tiers.

**Before writing any new test file**, read 1-2 neighboring test files in the same tier to match the local style and patterns.

Follow existing test conventions:
- Import from `../utils/api-client`, `../utils/test-context`, `../utils/cleanup`, `../utils/unique-name`
- Use `readContext()` for shared test state (orgId, apiKey, userId)
- Use `uniqueName(prefix)` for test resource names
- Use `tryDelete()` in `afterAll` for best-effort cleanup
- Backtick strings for all `describe`/`test` names
- Tier-prefixed test names (e.g., `` `Tier 1: Sandbox Config CRUD` ``)
- NEVER use fake API keys — real keys come from env vars via `loadEnvs()`

After implementing changes, run `pnpm types` in `repos/integration/` to catch type errors early before running the full suite.

### Step 5: Run Full Integration Test Suite

Create the `.temp/` directory at the project root if it doesn't exist.

Determine which test command to run based on the changes detected in Step 1:
- If `repos/admin/` or `repos/backend/` changed: run `cd repos/integration && pnpm test:all 2>&1 | tee ../../.temp/tests-output.txt` (includes tier2 Playwright tests)
- Otherwise: run `cd repos/integration && pnpm test 2>&1 | tee ../../.temp/tests-output.txt` (tier1 + tier3 only)

If exit code is 0 (all tests pass), jump to Step 8.

### Step 6: Analyze Failures

Read `.temp/tests-output.txt` and parse each failure:
- Which test file failed
- Which test name failed
- The assertion error or exception message
- The line number
- Whether failures cascade from a shared setup failure (look for `setupFailed` guard patterns — if setup fails, all tests in that suite fail with the same guard)

Every failure gets investigated and resolved. The code base was written by you, so nothing is "out of scope". It does not matter if the failed tests are related to the changes or NOT. If a test is failing, it gets fixed. **THERE ARE NO EXCEPTIONS TO THIS RULE!**

For cascade failures, focus on the root setup failure first — fixing it will likely resolve all downstream failures in that suite.

### Step 7: Fix and Iterate

For each failure, determine the root cause:
1. Read the failing test to understand what it asserts
2. Read the current application code it tests
3. Compare: does the test expectation match what the code should do now?
4. If the test is outdated → update the test expectations
5. If the application code has a bug → fix the application code
6. Both cases may apply across different failures — handle each independently

**CRITICAL**: Follow the "no fixes without proven root cause" rule. Read the actual code. An assumption is NOT a confirmation. If you can't prove the root cause, say so and gather more data.

After applying fixes, re-run only the previously-failing test files individually for faster feedback:
```
cd repos/integration && npx vitest run --config configs/vitest.config.ts src/<tier>/<file>.test.ts
```
GOTCHA: Do NOT put `--` before the file path when running vitest directly.

Once individual files pass, go back to **Step 5** to run the full suite and check for regressions.

**Iteration cap**: Maximum 5 full-suite cycles. If tests are still failing after 5 iterations, report the remaining failures with full diagnostic context (file, test name, error, what was tried) and stop.

### Step 8: Final Verification and Report

Run `pnpm types` in `repos/integration/` and in each sub-repo where application code was modified.

Present a summary report:
- **Changes detected**: Which repos, which areas
- **Tests updated**: List of test files modified with brief description of what changed
- **Tests created**: List of new test files with brief description of what they cover
- **Application code fixes**: If any source code was fixed (not just tests), explain the root cause
- **Test results**: Final pass/total count, number of iterations needed
- **Tier2 status**: Whether Playwright tests ran or were skipped (and why)

Remind the user that no commits were made.

## Key Rules

- **NEVER commit or modify git history** — user handles all git operations. Include this rule in every sub-agent prompt.
- **NEVER use fake API keys** — real keys from env vars via `loadEnvs()`. Use `TDSK_IT_API_KEY`, `TDSK_IT_ORG_ID`, etc.
- **NEVER add TODO comments** — implement fully or explain why you cannot.
- **NEVER propose fixes without proven root cause** — read the actual code and gather evidence before any code change.
- **NEVER use `--` before file paths** when running vitest directly — only use `--` for `pnpm` script passthrough.
- **K8s services are always running** — do not suggest starting them or ask if they're running.
- **Save test output** to `.temp/tests-output.txt` after every test run.
- **Use sub-agents** for parallel work across independent repos and test files.
- **Run `pnpm types`** before reporting completion — in `repos/integration/` and any modified sub-repos.
- **Max 5 full-suite iterations** — report remaining failures with diagnostics if still failing after 5 cycles.
- **NEVER send destructive requests against seeded/shared resources** — only DELETE resources the test itself created, or use nonexistent UUIDs for error-path testing.
- **NEVER skip failing tests** — fix ALL failures. It does not matter if they are unrelated to current changes. There is no alternative.
- Every failure gets investigated and resolved. The code base was written by you, so nothing is "out of scope". It does not matter if the failed tests are related to the changes or NOT. If a test is failing, it gets fixed. **THERE ARE NO EXCEPTIONS TO THIS RULE!**