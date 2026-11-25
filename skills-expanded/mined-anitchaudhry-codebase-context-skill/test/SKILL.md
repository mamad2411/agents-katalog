---
name: test
description: "Run tests, diagnose failures, suggest or auto-fix"
category: quality
tags: [test, verify, auto-fix]
depends-on: [init]
input: "test scope (file, suite, or all)"
output: "test results + failure analysis + auto-fix suggestions"
token-estimate: 4000
parallel-safe: true
argument-hint: "[scope: all | file path | test name | --fix | --write file]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-sonnet-4-6
context: fork
agent: general-purpose
---

# Test

Run tests, capture results, diagnose every failure, and optionally auto-fix or write new tests.

## Steps

### 1. Discover test setup
- Read `.ccs/conventions.md` for test framework and patterns
- If missing, auto-detect: check `package.json` scripts, config files (`jest.config.*`, `vitest.config.*`, `pytest.ini`, `pyproject.toml`), Glob for test files
- Identify the test runner command

### 2. Determine scope
Parse `$ARGUMENTS`:
- No arg or `all` → full suite
- File path → tests for that file
- Test name → specific test by pattern
- `--fix` → run and auto-fix failures
- `--write <file>` → write new tests for specified file
- `--coverage` → run with coverage

### 3. Run tests
Execute via Bash with verbose, non-interactive flags. Use appropriate runner for the stack.

### 4. Parse results
Extract: total, passed, failed, skipped, duration. For each failure: test name, file, error message, expected vs actual, stack trace (first 10 lines).

### 5. Diagnose failures
For each failing test:
1. Read the test file and source file
2. Classify: assertion failure, runtime error, missing mock, environment issue, outdated snapshot, timeout, dependency error
3. Determine: is the test wrong or the code wrong?

### 6. Auto-fix (if `--fix`)
- Apply high-confidence fixes, re-run to verify
- If new failures appear, rollback and report
- For medium/low confidence → ask user first

### 7. Write tests (if `--write`)
- Read target source file and `.ccs/conventions.md`
- Identify untested code paths (branches, error cases, edge cases)
- Generate test file following conventions, run to verify

### 8. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`:
- Type: `test`, results summary, failures with root causes, fixes applied, tests written

## Rules
- Always use verbose + non-interactive mode
- Read test file AND source file before diagnosing
- After fix → re-run to confirm no regressions
- Run `/ccs-test` after every `/ccs-build` or `/ccs-fix`

## Refs
- Conventions: `.ccs/conventions.md`
- Task log: `.ccs/task.md`
- Strategy: `.claude/skills/_ccs/references/context-strategies.md`

---
*codebase-context-skill v2.0.0*
