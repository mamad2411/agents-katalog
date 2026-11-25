---
name: plan-eng
description: Generate a structured engineering plan markdown for an idea, pre-filled with codebase facts (stack, dependencies, current critique score) from dragoon.json. Forces a test matrix, edge cases, migration plan, and review checklist. Use after /brief or before any non-trivial feature implementation. Output goes to .dragoon/plans/plan-eng-{slug}-{date}.md. Defaults to dry-run; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/plan-eng/scripts/plan-eng.js "<idea>"`.
version: 1.0.0
---

# /plan-eng

Generates an engineering plan template that respects the codebase's stack and current quality bar.

## When to use

- After /brief, before implementation
- The user asks for "an engineering plan", "an architecture doc", "a design doc"
- Non-trivial features (anything more than a one-file change)

## Output sections

- architecture (data model, api, state)
- edge cases (forces at least 5)
- test matrix (unit, integration, e2e, perf)
- existing dependencies (auto-loaded from package.json)
- migration / rollout (flags, backfill, rollback, observability)
- review checklist (gated on /critique threshold)

## Run it

```
dragoon plan-eng "add user invites"
dragoon plan-eng "add user invites" --apply
```
