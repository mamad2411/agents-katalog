---
name: edit-with-use-scripts
description: alias → /use-scripts (edit files via scripts — reproducible, dry-run + backup + confirm)
argument-hint: "[target]"
related:
  - use-scripts
---

## Goal

Alias of `/use-scripts` — edit many files via reproducible, verifiable scripts (dry-run by default, backup, validate, confirm before executing)

## Scope

Use when the user invokes `/edit-with-use-scripts` — this skill is only an alias stub; the real workflow lives in `use-scripts/SKILL.md` (`### Edit Files Via Scripts`)

## Execute

Run the full `/use-scripts` workflow — section `### Edit Files Via Scripts`

## Rules

- Never duplicate the `/use-scripts` workflow in this file
- If the alias lacks steps → always read `use-scripts/SKILL.md`

## Expected Outcome

- `/use-scripts` is executed through every step — files edited via reproducible scripts with dry-run, backup, and audit trail
