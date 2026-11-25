---
name: handoff
description: Generate a markdown dev handoff doc with everything the next engineer needs - stack, design tokens, palette, type scale, spacing grid, motion, existing components, and conventions - all pulled from dragoon.json. Use when handing off work to another engineer or documenting the codebase for new contributors. Output goes to .dragoon/handoff/handoff-{slug}.md. Defaults to dry-run; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/handoff/scripts/handoff.js [feature]`.
version: 1.0.0
---

# /handoff

Generates a handoff doc with codebase facts and conventions pre-loaded.

## When to use

- Handing off a feature to another engineer
- Onboarding a new contributor
- Capturing the design system shape for documentation
- The user asks for "a handoff doc", "context for the next engineer", "design system summary"

## What's in it

- Stack
- Top 8 colors with role and usage count (table)
- Type scale and font families
- Spacing grid
- Radius variants
- Motion durations and easings
- Existing components (sample of up to 25)
- Conventions for adding new code in this codebase
- A pre-merge checklist gated on /critique, /slop, /review

## Run it

```
dragoon handoff                          # general handoff
dragoon handoff "user invites" --apply   # specific feature
```

## Output

`.dragoon/handoff/handoff-{slug}.md`
