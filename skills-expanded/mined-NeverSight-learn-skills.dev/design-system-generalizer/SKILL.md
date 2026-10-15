---
name: design-system-generalizer
description: Scans token and component usage patterns from a golden reference page and diffs violations on other routes. Use when spreading a well-built page's patterns across the app in PR-sized chunks.
disable-model-invocation: true
---


# Design System Generalizer

## When to use

- One route is the "golden" reference (e.g. /settings)
- Other routes drift from tokens or component reuse
- Planning incremental migration PRs

## Instructions

1. `python scripts/scan_patterns.py --route /golden --project-root <root>`
2. `python scripts/diff_violations.py --golden /golden --target /other --project-root <root>`
3. Use `--check` on diff to exit non-zero when target has hex colors or missing route files.
4. Propose small PRs — never whole-app rewrite in one shot.
