# Sidecar Memory Skill Project

This project is the working home for the `sidecar-memory` Codex skill.

## Purpose

Use this folder for all future development of the sidecar-memory skill, helper scripts, references, tests, and review artifacts.

## Layout

- `skill/`: canonical editable skill source.
- `work/`: scratch files, fixtures, and local experiments.
- `outputs/`: user-facing deliverables or packaged copies.

## Install Target

The active installed copy lives at:

`$CODEX_HOME/skills/sidecar-memory`

After editing `skill/`, sync it with:

`rsync -a --delete skill/ "$CODEX_HOME/skills/sidecar-memory/"`

Restart Codex after install/sync if skill discovery needs to refresh.

## Sidecar Policy

Sidecar memory files have standing user approval for read/write maintenance. Live project, repo, vault, or application files do not inherit that approval.
