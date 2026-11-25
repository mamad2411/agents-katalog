---
name: zno-roadmap
description: Use when the user writes /zno-roadmap or wants to adjust project phases, priorities, MVP boundary, or milestones. Updates docs/product/06-roadmap.md and keeps it consistent with the current status and changelog.
---

# Zno-Roadmap — Roadmap / Priorities

`<skills-root>` below means the directory containing all zno-* skills (e.g. `~/.claude/skills` or `~/.agents/skills`).

## Workflow

1. Read `docs/product/06-roadmap.md`, plus `docs/development/10-current-status.md` and `docs/development/03-feature-changelog.md` if they exist, to see plan vs reality.
2. Restate the requested adjustment: phase scope change, priority reorder, MVP boundary move, or milestone date change.
3. Ask clarification only if the adjustment conflicts with completed work, acceptance criteria, or an agreed MVP boundary.
4. Update `docs/product/06-roadmap.md`: phases, per-phase scope, priorities, and launch readiness. Mark deferred items explicitly instead of deleting them.
5. If the adjustment changes what should be built next, say so in the final response and suggest the matching next command (`/zno-feature`, `/zno-plan`, ...).
6. Do not implement features from this command; it only re-plans.

## Shared references (read only when needed)

- `<skills-root>/zno-init/references/docs-map.md` — full doc set, doc update rules, scaffold triggers.
