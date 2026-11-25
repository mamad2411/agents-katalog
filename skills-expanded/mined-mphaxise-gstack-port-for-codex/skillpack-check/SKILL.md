---
name: skillpack-check
description: Health check for the local GStack/GBrain skillpack: repo validation, tests, Codex docs freshness, upstream drift, symlink install, brain doctor, and citations.
---

# Skillpack Check

Use this skill when the user asks whether the installed skillpack is healthy.

## Workflow

1. Run repository validation.
2. Run unit tests.
3. Check the installed Codex version and, when the check is part of portwork or an install refresh, refresh the current official Codex manual:
   - `codex --version`
   - `node "${CODEX_HOME:-$HOME/.codex}/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs"`
4. Check registry coverage against upstream snapshots when available:
   - `python3 scripts/check_upstream_drift.py`
   - `python3 scripts/check_upstream_drift.py --map gbrain`
5. Check local user skills under `~/.agents/skills`. Separate this package's
   receipted copies from shared symlinks and other user-owned skills.
6. Run `brain_doctor.py` when the local brain substrate is in scope.
7. Run `brain_citations.py --verbose` when citation quality is in scope.
8. Report pass/fail with exact gaps, separating repo health, local install health, upstream parity, and Codex-doc freshness.

## Guardrails

- Do not say healthy if local install or registry validation failed.
- Do not mutate files during a check.
- Separate repo health from upstream parity.
- Do not treat memories as the source of truth for Codex host behavior; use current docs when host behavior matters.
