---
name: verification-gates
description: Use before claiming completion, closing acceptance criteria, or validating user-specified gates.
---

# Verification Gates

Verification must be external to confidence.

## Gate Definition

A gate is valid only if it has:

1. Observable: file, route, API response, log line, data row, UI screenshot, command output, metric, or artifact render.
2. Capture method: command, test, query, browser check, render, or direct read.
3. Pass/fail rule: exact value, regex, threshold, visual condition, or explicit acceptance criterion.

If any part is missing, return to `design-brief` or `implementation-planning`.

## Accepted Evidence

- Test/build/lint/typecheck exit code.
- Runtime route/API/job observed.
- Rendered UI or artifact inspected.
- Schema validation with valid and invalid inputs.
- Database query for persisted state.
- Primary source read for factual claims.
- Hand-trace with concrete boundary inputs when execution is impossible.

## Rejected Evidence

- "Looks good."
- "Should work."
- "Straightforward."
- "Tests pass" as a substitute for behavior.
- Subagent claims without main-agent verification.

## Final Gate

Run one skeptic check:

- What would make the conclusion false?
- Is there a legacy path, mobile view, empty state, permission state, retry, or weird input that bypasses the fix?
- Did any claim drift from verified to assumed?

