---
name: sage-workflow-verification-loop
description: SAGE — run build, types, lint, tests, quick security sanity, then review diff before merge.
---

# SAGE workflow — Verification loop

## Purpose

Before declaring a **SAGE** task complete or opening a PR, run the **project’s** quality gates in order. Adapt commands to the repo (Python, Node, Go, etc.).

## Suggested phases (pick what exists)

1. **Build** — `npm run build`, `cargo build`, `poetry build`, etc. Exit 0 required.
2. **Types** — `mypy`, `tsc --noEmit`, `pyright`, as applicable.
3. **Lint** — `ruff check`, `eslint`, `golangci-lint`, etc.
4. **Tests** — full unit/integration suite; note pass/fail counts.
5. **Secrets sanity** — grep for obvious API key patterns in diff (do not paste secrets into logs).
6. **Diff review** — `git diff --stat`; confirm every change is intentional.

## Reporting

Summarize each phase: command, pass/fail, and one line of evidence. If something is skipped, say why (e.g. no typechecker in project).

## Cross-links

- **sage:discipline:verification-before-completion** for claim discipline.
- **sage:workflow:tdd-workflow** for test coverage expectations.
