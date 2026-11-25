---
name: typography
description: Generate a type scale token file (CSS variables, tailwind config, or JS module) anchored on the type ratio detected by /scan. Use when the user wants to formalize their typography system, extract a scale from existing code, or scaffold typography tokens. Defaults to dry-run preview; pass --apply to write. Auto-picks format based on stack: tailwind for tailwind projects, JS module for JS-heavy stacks, CSS variables otherwise. Run as `node ~/.claude/skills/dragoon/skills/typography/scripts/typography.js`.
version: 1.0.0
---

# /typography

Generates a 9-step type scale (xs / sm / base / md / lg / xl / 2xl / 3xl / 4xl) anchored on 16px, using the ratio detected by /scan (or a sensible default if none was found).

## When to use

- The user wants to formalize their typography system
- The user asks for a "type scale", "font tokens", or "type tokens"
- After /scan detects a type ratio, to extract it as reusable tokens

## Output

One file per run. Format chosen automatically from the stack, override with `--format`:
- `css` → `:root { --font-size-xs: ... }`
- `tailwind` → `module.exports = { theme: { extend: { fontSize: { ... } } } }`
- `js` → `export const fontSize = { xs: '...', ... }`

Default dir: `src/styles/`. Override with `--dir`.

## Run it

```
dragoon typography                           # preview
dragoon typography --apply                   # write
dragoon typography --format js --apply
dragoon typography --dir src/tokens --apply
```
