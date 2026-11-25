---
name: tailwind
description: Generate one consolidated tailwind.config.js combining colors, spacing, fontFamily, fontSize, borderRadius, transitionDuration, and transitionTimingFunction from the manifest. Single file instead of four separate token cjs files. Use when setting up tailwind for the first time or refreshing the config after major token changes. Run as `node ~/.claude/skills/dragoon/skills/tailwind/scripts/tailwind.js`.
version: 1.0.0
---

# /tailwind

One config to rule them all.

## When to use

- Setting up tailwind for the first time on a codebase that already has a design system
- Consolidating after running /typography, /color, /spacing, /motion
- After a major token refresh

## What's in the output

- `colors` from your top palette (with role names)
- `spacing` t-shirt scale on your detected grid
- `fontFamily.sans` from your detected family
- `fontSize` derived from your detected ratio
- `borderRadius` from your detected radii
- `transitionDuration` and `transitionTimingFunction` defaults

## Run it

```
dragoon tailwind --apply
```
