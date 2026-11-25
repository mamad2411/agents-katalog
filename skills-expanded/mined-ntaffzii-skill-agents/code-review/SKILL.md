---
name: code-review
description: Code review skill for finding bugs, regressions, risky behavior, missing tests, and maintainability problems in diffs, pull requests, or local changes. Use when the user asks for review, scrutinize, audit, inspect, or feedback on code.
---

# Code Review

Use a reviewer stance. Findings come first. Summaries are secondary.

## Review Order

1. Understand the intent
   - Read the user request, PR description, issue, or nearby docs.
   - Identify the expected behavior change.

2. Ask whether the change should exist
   - Look for simpler alternatives, existing helpers, smaller scope, or a better layer for the change.
   - Flag avoidable risk when the same outcome can be achieved with less behavioral surface.

3. Inspect the actual diff
   - Trace changed code paths end to end.
   - Check callers, data shapes, error paths, async paths, and boundary conditions.
   - Look for behavior that differs from the stated intent.

4. Verify tests
   - Check whether tests cover the changed behavior.
   - Prefer tests that would fail on the discovered issue.
   - Flag missing regression coverage when risk is real.

5. Report findings
   - Lead with issues ordered by severity.
   - Include file and line references.
   - Explain why the issue matters and how it can fail.
   - Keep praise and general commentary out of the findings section.

## Severity

- P0: breaks core production behavior, data loss, security exposure, or prevents release.
- P1: likely user-facing bug, broken important workflow, serious regression.
- P2: edge-case bug, missing important test, maintainability risk with plausible impact.
- P3: minor issue or cleanup suggestion.

## Output Format

If issues exist:

```text
Findings
- [P1] Title - path:line
  Explanation.

Open Questions
- ...

Summary
Brief context only.
```

If no issues:

```text
No findings.

Residual risk: mention any tests not run or areas not inspected.
```

## Rules

- Do not rewrite the code unless the user asks.
- Do not bury findings under a long summary.
- Avoid style comments unless style creates a real defect or conflicts with established local patterns.
- Distinguish what the code claims from what was actually verified.
