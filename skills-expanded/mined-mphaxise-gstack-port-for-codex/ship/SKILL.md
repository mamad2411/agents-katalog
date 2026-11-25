---
name: ship
description: Release workflow for Codex. Use when a feature branch is ready to be tested, reviewed, pushed, and opened as a PR.
---

# Ship

Use this skill when a branch is ready for a disciplined ship pass.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Workflow

1. Run the preflight checks in `references/release-gates.md`.
2. Sync the branch with `origin/main`.
3. Run the repo's real test commands.
4. Run a pre-landing review.
5. If the repo uses version files, changelogs, or eval suites, apply those conventions.
6. Commit any release-prep changes, push the branch, and open a PR if the host tooling allows it.

## Codex Adaptation

Unlike upstream gstack, this port assumes repo conventions may differ. Treat these as conditional, not universal:

- `VERSION` and `CHANGELOG.md`
- prompt-specific eval suites
- `gh`-based PR creation

If the repo does not use one of those conventions, skip it and report that it was skipped.

## Guardrails

- Abort on `main`.
- Stop on merge conflicts, failing tests, or unresolved critical review findings.
- Do not invent versioning or changelog files if the repo does not already use them.
- Be explicit about what was automated and what was skipped.

