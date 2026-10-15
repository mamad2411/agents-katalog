---
name: eng-review-fix
description: Systematically remediate and fix issues identified in a code review report. Use when applying review feedback, resolving findings, and verifying fixes with automated tests.
---

# Code Review Fix

Address, refactor, and resolve findings from a code review report systematically.

## Process

### 1. Ingest Review Findings
1. Read the provided review report or issue list (e.g. `.agents/eng-code-reviews/...md`).
2. Triage findings by priority (`Critical` $\rightarrow$ `Warning` $\rightarrow$ `Suggestion`).

### 2. Remediate Step by Step
For each issue:
1. **Understand Root Cause**: Locate the exact file and lines, analyzing why the issue exists.
2. **Apply Minimal Fix**: Implement the cleanest, safest fix adhering to codebase conventions.
3. **Verify Locally**: Run or add regression tests covering the specific failure condition.

### 3. Comprehensive Verification Gate
After all fixes are applied:
1. Run linting, type checks, and project test suites.
2. Ensure no new warnings or regressions were introduced.

---

## Completion Report

Provide a summary detailing:
- Issues addressed and files modified.
- Verification test results.
- Any remaining items requiring human architectural decisions.

---

## Checkable Completion Criteria

- [ ] Findings triaged by priority: Critical resolved before Warning before Suggestion.
- [ ] Each fix targets root cause with minimal changes following codebase conventions.
- [ ] Linting, type checks, and full test suites pass with zero new warnings or regressions.
- [ ] Completion report lists issues addressed, files modified, verification results, and any items deferred to human decisions.
