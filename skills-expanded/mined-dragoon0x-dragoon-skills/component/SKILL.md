---
name: component
description: Generate a UI component scaffold in the codebase's actual style. Reads dragoon.json to match framework (react/vue/svelte), styling layer (tailwind/css-modules/plain), language (typescript/javascript), and design tokens (radius, spacing, palette). Defaults to dry-run preview; pass --apply to write files. Use when the user wants to create a new component, scaffold UI primitives, or add a component to their codebase. Run as `node ~/.claude/skills/dragoon/skills/component/scripts/component.js <Name>`.
version: 1.0.0
---

# /component

Generates a component scaffold that matches the codebase's existing style.

## When to use

- The user asks to "create a component", "scaffold a UI primitive", "add a Card / Button / etc."
- The user wants a starting point that fits the existing design system
- Setting up a new feature that needs new UI

## How it works

1. Reads `dragoon.json` (or runs /scan if missing) to detect the stack.
2. Picks a template based on framework + styling layer:
   - react + tailwind → tsx with tailwind utility classes derived from your tokens
   - react + css-modules → tsx + .module.css using your spacing grid and radius
   - react + plain css → tsx + .css with kebab-case class
   - vue → SFC with scoped styles
   - svelte → .svelte single file
3. Substitutes manifest tokens: spacing grid → padding, palette → bg/fg, radius scale → border-radius.
4. Defaults to dry-run preview. `--apply` actually writes files.

## Run it

```
dragoon component <Name> [--dir path] [--apply]

# preview
dragoon component Card

# write to default src/components/
dragoon component Card --apply

# custom directory
dragoon component UserMenu --dir src/ui --apply

# overwrite existing
dragoon component Card --apply --overwrite
```

## Safety

- Component name must be PascalCase identifier (rejects shell metacharacters, reserved words).
- Output directory is resolved inside the project root (rejects path traversal).
- Refuses to overwrite existing files unless `--overwrite` is passed.
- All writes are atomic (temp file + rename), so a failed write never leaves a half-written file.
