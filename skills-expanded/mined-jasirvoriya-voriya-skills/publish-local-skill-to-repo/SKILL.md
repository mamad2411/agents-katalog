---
name: publish-local-skill-to-repo
description: Publish a local skill folder to a target git repository that contains `skills/`. Use when you need to import a local skill into `skills/`, commit the change, and push it to a remote branch.
---

# Publish Local Skill To Repo

## Overview

Publish a local skill directory into a target repository under
`skills/<skill-name>`. This workflow validates source files, copies the skill
folder, commits the change, and pushes the current branch.

## Required input

Prepare a local source skill directory that contains at least:

- `SKILL.md`
- Optional folders such as `agents/`, `scripts/`, `references/`, and `assets/`

## Publish workflow

Use the bundled script for deterministic publish steps.

1. Validate your source skill folder and publish plan.
2. Copy source files into the target repository's `skills/` directory.
3. Stage, commit, and push changes to `origin/<current-branch>`.

Run this command:

```bash
python3 scripts/publish_local_skill.py --source-skill-dir <path-to-local-skill>
```

## Common options

Use these flags when needed:

- `--target-skill-name <name>`: Override destination skill name.
- `--commit-message "<message>"`: Override default commit message.
- `--remote <name>`: Override push remote name (default `origin`).
- `--no-push`: Commit locally without pushing.
- `--dry-run`: Validate and print plan without writing files.
- `--repo-root <path>`: Explicitly set target repository root.

## Safety rules

Follow these constraints during publish:

1. Keep skill names in lowercase hyphen format.
2. Never publish from a source path that equals destination path.
3. Keep source skill content complete before publish to avoid partial updates.
4. Ensure target repository has both `.git` and `skills/`.
5. Use `--dry-run` before first publish from a new source location.
