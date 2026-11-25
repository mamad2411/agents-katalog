---
name: bugfix-and-verify
description: Fixes bugs or test failures using debugger → fix → verify. Use when the user reports an error, test failure, or unexpected behavior and wants a fix confirmed.
---

# Bugfix and Verify Framework

This skill runs a **bugfix** workflow: debug, fix, then verify.

## Steps

1. **Debug**
   - Invoke the **debugger** subagent with:
     - The error message, stack trace, or failing test output (from the user or from the conversation), and
     - The relevant file(s) or area of the codebase if known.
   - Capture the debugger’s output: root cause, location, suggested fix, and how to confirm the fix.

2. **Fix**
   - Apply the fix (or a minimal variant). Prefer the debugger’s suggestion unless it’s incomplete or wrong; then extend or correct as needed.
   - Make the smallest change that addresses the root cause; avoid refactors unless the user asked for them.

3. **Verify**
   - Invoke the **verifier** subagent to confirm:
     - The original error or test failure is resolved.
     - Related behavior still works (e.g. run the test suite or the steps that previously failed).
   - Report: fixed vs still broken; if broken, summarize what the verifier found.

## Notes

- If the user only wants a diagnosis, stop after step 1 and present the debugger’s report.
- If the user says “skip verification,” do steps 1–2 only and note that verification was skipped.
