---
name: automate-project-maintenance
description: Orchestrate repository maintenance. Use when Codex needs one entry point to refresh tests, docs, README, and GitHub metadata.
---

# Automate Project Maintenance

Use this skill after the focused maintenance skills are available. Detect the repo type from local facts, not from naming guesses.

## Detection

Inspect the repo before acting.

- Python signals:
  - `pyproject.toml`
- TypeScript signals:
  - `package.json`

## Workflow

1. Determine whether the repo is Python, TypeScript, or other.
2. Run only the applicable focused skills.
3. Keep remote GitHub updates preview-first.

## Python Branch

1. Use `$write-python-tests`.
2. Use `$rewrite-python-docs`.
3. Use `$write-root-readme`.
4. Run `rumdl fmt .` and treat findings as weak hints.
5. Run `mise run lint`.
6. Run `mise run docs:build`.
7. Run `nox`.
8. Use `$sync-github-repo-metadata` in preview mode.

## TypeScript Branch

1. Use `$write-root-readme`.
2. Run `rumdl fmt .` and treat findings as weak hints.
3. If TypeScript or JavaScript files were edited, run `biome check --write`.
4. Use `$sync-github-repo-metadata` in preview mode.

## Other Repos

- Apply the appropriate maintenance steps based on the detected technology stack.
- Do not assume both branches must edit files in the same run.
