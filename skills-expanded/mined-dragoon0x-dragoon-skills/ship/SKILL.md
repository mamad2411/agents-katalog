---
name: ship
description: Pre-PR check orchestrator. Runs /critique with a threshold (default 80), /slop --severity high, gathers git context (branch, changed files), and optionally opens a PR via the gh CLI. Use before opening any PR. Exits non-zero if any check fails. Run as `node ~/.claude/skills/dragoon/skills/ship/scripts/ship.js`.
version: 1.0.0
---

# /ship

Pre-PR check orchestrator. The thing you run before pushing.

## When to use

- Before opening a pull request
- The user says "ship", "open a PR", "ready to merge"
- As a CI step that gates merges

## What it does

1. Loads (or generates) `dragoon.json`
2. Runs /critique and fails if overall < threshold (default 80)
3. Runs /slop and fails on any high-severity finding
4. Detects git state (branch, changed files, remote)
5. Builds a PR description from the run results
6. If `--open` and `gh` CLI is available, opens the PR

## Run it

```
dragoon ship                              # all checks, preview PR body
dragoon ship --threshold 85               # tighter design gate
dragoon ship --title "add invites" --open # actually open the PR
dragoon ship --json                       # for CI
```

## Safety

- The PR title is sanitized before passing to the shell
- The PR body is written to a temp file (`--body-file`), never inlined as argv
- `--open` only runs if all checks pass; pass `--skip-critique`/`--skip-slop` to bypass

## Exit codes

- `0` all checks passed
- `1` one or more checks failed
- `2` bad usage
