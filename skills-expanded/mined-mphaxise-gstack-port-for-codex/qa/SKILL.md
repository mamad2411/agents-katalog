---
name: qa
description: Structured QA workflow for Codex using Browser, Chrome, Computer Use, or repo-local tests. Use for site QA, feature-branch testing, or evidence-backed quality reports.
---

# QA

Use this skill for systematic QA on a web application or feature branch.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Modes

- `diff-aware`: default when on a feature branch and no explicit URL is given
- `full`: broad exploratory QA on a target URL or app
- `quick`: smoke test
- `regression`: compare against a prior baseline or report

## Workflow

1. Choose a browser/runtime path using the `browse` skill guidance, including `@Browser`, `@Chrome`, Computer Use, or repo-local test tooling as appropriate.
2. Identify the target URL or feature-branch scope.
3. Use `references/issue-taxonomy.md` while exploring.
4. Write results into the structure from `templates/qa-report-template.md`.
5. End with a health score, top issues, and any blockers or blind spots.

## Branch-Aware Behavior

If the user asks for QA on a feature branch with no URL:

- inspect the diff against `origin/main`
- infer the pages or routes likely affected
- test the changed surface first
- check adjacent pages for regressions

## Guardrails

- Be explicit when runtime/tooling limits prevented full coverage.
- Document issues as you find them instead of batching vague notes.
- Prefer reproducible evidence over general impressions.
