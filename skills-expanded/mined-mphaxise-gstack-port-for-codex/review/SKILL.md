---
name: review
description: Pre-landing PR review for Codex. Use when the user asks for a code review or wants structural issues found before a branch lands.
---

# Review

Use this skill to review the current branch against `origin/main` and find bugs or risks that tests often miss.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Workflow

1. Confirm the current branch is not `main` and a real diff exists against `origin/main`.
2. Read `references/checklist.md`.
3. Review the full diff in two passes:
   - critical: safety, concurrency, trust boundaries
   - informational: consistency, tests, frontend, prompt drift, maintenance risks
4. If GitHub CLI and Greptile comments are available, optionally apply `references/greptile-triage.md`.
5. Report findings with the most severe issues first.

## Output Rules

- Findings come first.
- Each finding should include file and line references when possible.
- Distinguish blocking issues from non-blocking issues.
- If there are no issues, say so explicitly.

## Guardrails

- Do not modify code unless the user explicitly asks for fixes.
- Read the full diff before flagging an issue.
- Skip stylistic nitpicks unless they create real risk.
- Prefer terse, concrete findings over long summaries.

