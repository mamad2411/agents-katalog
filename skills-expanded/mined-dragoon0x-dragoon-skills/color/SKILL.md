---
name: color
description: Generate a color palette token file (CSS variables, tailwind config, or JS module) from the palette detected by /scan. Uses inferred role names (foreground, background, accent, danger, etc.) where possible, numeric fallback otherwise. Use when the user wants to formalize color tokens, extract a palette from existing code, or scaffold a color system. Defaults to dry-run preview; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/color/scripts/color.js`.
version: 1.0.0
---

# /color

Generates a color token file from the top 8 colors in your palette, using role hints from /scan.

## When to use

- The user wants to formalize their color tokens
- The user asks to "extract a palette", "scaffold colors", "create color tokens"
- Setting up a design system after a /scan reveals the palette

## Output

One file per run. Format auto-selected from the stack:
- `css` → `--color-foreground`, `--color-background`, etc.
- `tailwind` → `colors: { foreground: '#...', accent: '#...' }`
- `js` → `export const colors = { ... }`

## Run it

```
dragoon color
dragoon color --apply
dragoon color --format css --apply
dragoon color --dir src/tokens --apply
```
