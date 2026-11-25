---
name: pre-ship
description: Pre-merge verification pipeline — runs typecheck, lint, affected tests, then security and a11y review passes scoped to what changed, and reports a single pass/fail table. Use before claiming any change is done, before opening a PR, and whenever the user asks to verify/finalize work. 日本語の依頼例:「出荷前チェック」「マージ前に確認して」「これで完成か確認」「PR出す前のチェック」。
---

# Pre-ship pipeline

Run the gates below in order against the current change set (`git diff` + untracked files). Report every result **verbatim** — a failing gate is reported, never worked around, and the change is not "done" until all gates pass or the human explicitly accepts a documented exception.

## Gates

1. **Scope** — `git status` + `git diff --stat`: list changed files; classify what they touch (boundary code? UI? styles? tests? sensitive paths?). This decides which later gates apply.
2. **Typecheck** — `typecheck` script (`tsc --noEmit`).
3. **Lint** — `lint` script (ESLint + Stylelint).
4. **Affected tests** — tests colocated with changed files plus anything importing them; the full suite when shared config, tokens, or shared utilities changed. Storybook play-function tests run via the Vitest addon; touched E2E specs via `test:e2e`.
5. **Security pass** (only if gate 1 found boundary code) — delegate to the `security-reviewer` agent; its verdict gates the pipeline.
6. **A11y pass** (only if gate 1 found UI changes) — delegate to the `a11y-auditor` agent; blocking findings gate the pipeline.
7. **Local scanners, if installed** — `gitleaks protect --staged` and `semgrep --config .semgrep/` when the tools exist; when they don't, mark the gate SKIPPED (tool not installed) in the report. These duplicate CI gates early, they don't replace them.
8. **Sensitive paths** — if gate 1 touched CI workflows, auth/payment, headers/CSP config, lockfile-only changes, or `.claude/**`: stop and get explicit human sign-off before proceeding.

## Report format

One table: gate → command run → result (verbatim exit/summary line) → PASS/FAIL/SKIPPED(why). Then the verdict: **READY TO SHIP** or **NOT READY** with the blocking items listed first. Never summarize a failure as "minor".
