---
name: flake-check
description: Diagnose failing or unstable tests: flaky selector vs timing issue vs real bug, with a concrete fix. Use when the user runs /flake-check or reports a flaky or intermittent test.
---

# /flake-check — Diagnose Flaky Tests

**Type:** Functional
**Description:** Analyzes failing or unstable tests and diagnoses whether the cause is a flaky selector, a timing/race issue, test data, or a real product bug — then proposes a fix.

---

## Input Format

Any of:
- A path to a spec file or test name
- A pasted failure log / stack trace
- A description of the intermittent behavior

## Output Format

A diagnosis report containing:
- **Classification:** flaky selector / timing issue / test data / environment / real bug
- **Evidence:** the specific lines or signals that point to the cause
- **Recommended fix:** concrete code change following Autoframe conventions
- **Confidence:** high / medium / low

## Step-by-Step Instructions

1. Read the relevant spec and its Page Object(s).
2. Inspect the failure signal (log, trace, or description).
3. Check for the common flake causes, in order:
   - **Selectors:** brittle CSS / `page.$()` / nth-based locators → recommend semantic `getByRole`/`getByLabel`.
   - **Timing:** hard waits (`waitForTimeout`), missing auto-waiting assertions, race conditions → recommend web-first `expect` assertions and removing fixed sleeps.
   - **Test data:** shared/mutable state, ordering dependencies → recommend factories and isolation.
   - **Environment:** network, auth token expiry, base URL.
   - **Real bug:** behavior is genuinely wrong → recommend `/bug-from-failure`.
4. State the classification with evidence and a confidence level.
5. Propose the fix as a concrete diff that follows POM and spec conventions.
6. If it's a real bug, route the user to `/bug-from-failure`.

## Rules

- Prefer fixing the root cause over adding retries.
- Never recommend `waitForTimeout` as a fix.
- Always classify before proposing a change.
