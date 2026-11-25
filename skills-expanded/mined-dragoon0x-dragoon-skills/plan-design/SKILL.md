---
name: plan-design
description: Generate a structured design plan markdown that respects the constraints in dragoon.json (spacing grid, type ratio, palette, font families). Forces a screens-and-flows breakdown, accessibility plan, responsive plan, and design review checklist gated on /critique and /slop. Use after /brief or before any UI work. Output goes to .dragoon/plans/plan-design-{slug}-{date}.md. Defaults to dry-run; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/plan-design/scripts/plan-design.js "<idea>"`.
version: 1.0.0
---

# /plan-design

Generates a design plan template with your codebase's design constraints pre-loaded.

## When to use

- After /brief, before any UI implementation
- The user asks for "a design plan", "a design doc", "wireframes plan"
- Any feature that adds new screens or flows

## Output sections

- constraints (auto-loaded: grid, type ratio, palette, font families)
- the moment that matters (one sentence)
- screens & flows (entry, success, empty, error, loading)
- new tokens needed (colors, spacing, motion, typography)
- accessibility plan (keyboard, focus, screen reader, contrast, motion)
- responsive plan (mobile, tablet, desktop)
- review checklist (gated on /critique 80, /slop --severity high)

## Run it

```
dragoon plan-design "add user invites"
dragoon plan-design "add user invites" --apply
```
