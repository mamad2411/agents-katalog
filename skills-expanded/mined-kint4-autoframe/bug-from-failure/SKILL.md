---
name: bug-from-failure
description: Turn a test failure into a structured bug report with repro steps, severity, and expected vs actual. Use when the user runs /bug-from-failure or asks to file a bug from a failing test.
---

# /bug-from-failure — Failure to Bug Report

**Type:** Functional
**Description:** Turns a test failure into a structured, shareable bug report with repro steps, severity, environment, and expected vs actual behavior.

---

## Input Format

Any of:
- A failing test name or spec path
- A pasted failure log / stack trace / screenshot description
- A description of what went wrong

## Output Format

A structured bug report in markdown:

```
### Title
[concise summary]

**Severity:** Critical / High / Medium / Low
**Environment:** [browser, base URL, env]
**Feature / Area:** [feature]

**Steps to Reproduce**
1. ...

**Expected Result**
...

**Actual Result**
...

**Evidence**
[log excerpt / screenshot / trace reference]

**Notes**
[suspected cause, related tests]
```

## Step-by-Step Instructions

1. Read the failing spec and its Page Object(s) to understand the intended behavior.
2. Extract the failure signal (assertion that failed, error, step that broke).
3. Before writing, confirm it's a real bug — if it looks like flake, route to `/flake-check`.
4. Derive concrete, numbered repro steps from the test's actions.
5. State expected vs actual clearly and factually.
6. Assign severity based on user impact (blocking flow = Critical/High; cosmetic/edge = Medium/Low).
7. Capture environment from `playwright.config.ts` / `.env` variables (never paste secret values).
8. Output the report in the format above, ready to paste into Jira / Linear / GitHub Issues.

## Rules

- Report behavior, not implementation.
- Never include secret values from `.env`.
- If the cause is flake, defer to `/flake-check` instead of filing a bug.
