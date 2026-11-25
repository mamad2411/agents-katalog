---
name: kos-docs-drift-detection
description: Detect documentation drift and update ONLY allowed doc files (README.md, docs/**, .planning/**, .github/workflows/documentation.md) to reflect reality — no source edits, no git/gh, no push, no whole-file prettier on docs.
user-invocable: true
when_to_use: "When the docs-drift workflow runs (review codebase vs .planning/docs), or when such a run soft-failed."
category: utilities
argument-hint: "[scope or doc-file]"
keywords: [docs, drift, documentation, planning, docs-update, prettier, allowed-scope, no-push]
related: [kos-zai-agent-runtime-contract, kos-zai-run-failure-prevention, kos-claude-turn-budget, kos-gh-automation-tooling]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from docs-drift.yml prompt + soft-failure runs
  license: repo
  version: "1.1"
---

# Idea

`docs-drift` compares the implementation against `.planning/` + docs and updates **only documentation files** to match reality. The agent edits docs only; it does **not** edit source, does **not** run git/gh, does **not** push (the workflow handles that). Two pitfalls drive soft-failures: drifting into editing code, and running whole-file prettier on docs (huge noisy table-padding diff; CI `format:check` is src-only anyway).

## When to invoke this skill directly
- Running the docs-drift check.
- A docs-drift run soft-failed and you are rescoping.

## References
- `docs-drift.yml` prompt (`/gsd:docs-update`; allowed scope; do NOT run git/gh; do NOT push; if no drift → no changes).
- Allowed edit scope: `README.md`, `docs/**`, `.planning/**`, `.github/workflows/documentation.md`.
- [[kos-zai-agent-runtime-contract]]; repo fact: whole-file `prettier --write` on docs pads every table — avoid it.

## Communication Style
Drift items: doc-file → code reality → the doc fix. State explicitly: source untouched.

## Core Principles
YAGNI / KISS / DRY. Update docs to match code, never code to match docs. Minimum diff per doc. No whole-file prettier on docs.

## Hard rules (the prompt)
- Edit **only** allowed doc files (`README.md`, `docs/**`, `.planning/**`, `.github/workflows/documentation.md`). Do NOT edit app source, tests, package manifests, or workflow logic (other than `documentation.md`).
- **Do NOT run `git` or `gh`. Do NOT commit/push/merge/open a PR** — the workflow handles that.
- If there is no meaningful drift → make no file changes.

## Your Approach
1. Survey what changed in code (recent commits / current state) vs what `.planning/` + `docs/` claim.
2. For each mismatch, edit **only the doc** (within allowed scope), minimal patch.
3. Do not run whole-file prettier on docs; if formatting is needed, scope it to the lines touched (CI format check is src-only, so usually unnecessary).
4. Summarize drift fixed; if none, exit cleanly (no-drift = success-with-no-changes).

## Failure modes to avoid
- **Editing source** — out of scope; docs only.
- **Running git/gh or pushing** — forbidden.
- **Whole-file prettier on docs** — massive table-padding diff; unnecessary.
- **Rewriting docs wholesale** — patch the stale fact only.
- **Soft failure** — usually scope/turn blowout or a wrapper hiccup; read `claude_soft_success_reason`, rescope — don't blindly re-run.

## Process Flow (Authoritative)
1. diff code reality vs `.planning/` + `docs/`.
2. enumerate drift items.
3. edit only allowed doc files, minimal patches.
4. no whole-file prettier on docs; no git/gh; no push.
5. summary or clean no-op exit.

## Output Format
```text
DRIFT: n items
- <doc-file>: <code reality> => <doc fix>
SOURCE CHANGES: none (docs-only); GIT/GH: not run; PUSH: none (workflow handles)
```

## Critical Constraints
- Never edit source; never run git/gh; never push — docs-only, the workflow commits.
- Never whole-file `prettier --write` on docs.
- No-drift is a clean success, not a failure.
