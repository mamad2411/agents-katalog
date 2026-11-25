---
name: spacing
description: Generate a spacing scale token file based on the spacing grid detected by /scan (4px, 8px, etc). Produces an 8-step t-shirt scale (xs/sm/md/lg/xl/2xl/3xl/4xl) anchored on the grid. Use when the user wants to formalize spacing tokens or scaffold a layout system. Defaults to dry-run; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/spacing/scripts/spacing.js`.
version: 1.0.0
---

# /spacing

Generates a spacing scale token file anchored on your detected grid.

## When to use

- The user wants to formalize spacing tokens
- The user asks to "extract spacing", "create a spacing scale", "scaffold layout tokens"
- Cleaning up a codebase that has many off-grid values

## Scale produced

8 steps as multiples of the detected grid:
- xs (0.5x), sm (1x), md (2x), lg (3x), xl (4x), 2xl (6x), 3xl (8x), 4xl (12x)

For an 8px grid: 4, 8, 16, 24, 32, 48, 64, 96.

## Run it

```
dragoon spacing
dragoon spacing --apply
dragoon spacing --format tailwind --apply
```
