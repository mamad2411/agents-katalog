---
name: pre-merge-gate
description: Runs pre-merge checks (tests, build, types, optional UI audit) and returns a markdown pass/fail report. Use when QA approves a PR or before merge to main.
disable-model-invocation: true
---


# Pre-merge Gate

## Subagents (default)

Run gate via **Task** `shell` subagent — `pre_merge_gate.py`. Main chat triages FAIL lines and re-delegates fixes. See `reference/subagents.md`.

## When to use

- QA wants a single green/red report before approving a PR
- Before merging frontend-heavy changes
- After addressing review feedback — confirm all gates pass

## Instructions

1. Run `python scripts/pre_merge_gate.py --project-root <root>`.
2. Read the markdown report — each check shows PASS/FAIL/SKIP.
3. Fix failing checks and re-run until all required checks pass.

**Eval / harness turns:** When the eval harness captures Playwright proof separately, run with `--skip-visual-audit` so the gate does not invoke `audit_ui.py` (no dev server in agent turn).

## Checks

- npm test (if script exists)
- verify build
- vue-tsc (if available)
- duplicate UI scan (`no-duplicate-ui` when installed)
- visual audit on product routes (`visual-auditor` when installed; skips if Playwright missing)

Use `--skip-duplicate-ui` or `--skip-visual-audit` to omit optional UI gates.
