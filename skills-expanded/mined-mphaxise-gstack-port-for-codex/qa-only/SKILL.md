---
name: qa-only
description: Report-only QA workflow for Codex using Browser, Chrome, Computer Use, or repo-local tests when no code changes should be made.
---

# QA Only

Use this skill when the user wants QA coverage and a bug report, but no fixes.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Important Adaptation

This skill shares the same browser and evidence strategy as `qa` and `browse`, but it never modifies code. Reuse:

- `qa/references/issue-taxonomy.md`
- `qa/templates/qa-report-template.md`

## Workflow

1. Choose a browser/runtime path using the `browse` skill guidance, including `@Browser`, `@Chrome`, Computer Use, or repo-local test tooling as appropriate.
2. Identify the target URL, route set, or diff-aware scope.
3. Test the changed or requested surface first.
4. Use the QA issue taxonomy while exploring.
5. Produce a structured report with:
   - health score
   - issues by severity
   - repro steps
   - evidence collected
   - blind spots and blockers

## Guardrails

- Never change code, even if the fix looks obvious.
- Never blur the line between verified bugs and suspicions.
- Be explicit when runtime limitations reduced coverage.
- If the user wants fixes, hand off to `qa` instead of quietly doing both jobs.
