---
name: inventory
description: Catalog of components (PascalCase files), hooks (useFoo), pages/routes, story files, and token files in the codebase. Use to understand what already exists before adding more, or to audit a design system. Heuristic-based, no AST. Run as `node ~/.claude/skills/dragoon/skills/inventory/scripts/inventory.js [root]`.
version: 1.0.0
---

# /inventory

What's already in the codebase. Run before scaffolding new things.

## When to use

- Before adding a component (might exist already)
- Auditing a design system
- The user asks "what components do we have", "list everything"

## Categorizes

- components (PascalCase basenames in jsx/tsx/vue/svelte/astro)
- hooks (useFoo*)
- pages (under app/ pages/ routes/)
- stories (*.stories.* / *.story.*)
- token files

## Run it

```
dragoon inventory
dragoon inventory --group components
dragoon inventory --json
```
