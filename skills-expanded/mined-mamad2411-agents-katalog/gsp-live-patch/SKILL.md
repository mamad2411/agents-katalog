---
name: gsp-live-patch
description: "Use when patching a shipped or live-risky game and changes must stay narrow and rollback-aware."
---

# Game Live Patch

## Goal
Make a safe, reversible, production-minded change in a shipped or operationally risky project.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present findings in conversation.
- **minimal** or **full**: write to `docs/game-studio/release-safety.md`, `docs/game-studio/quality-report.md`.

Use:
- `../../shared/templates/release-safety.md`
- `../../shared/checklists/live-patch-checklist.md`

## Rules
- prefer the smallest change that solves the real issue
- avoid broad refactors unless explicitly authorized
- document blast radius and rollback
- respect compatibility boundaries
- run targeted verification on touched paths and likely regressions

## Important
This skill exists so live work is not treated like greenfield YOLO work.
