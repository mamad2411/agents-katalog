---
tags: [frontend, figma, code, connect, react]
name: figma-code-connect-react
description: Map Figma component variants to React props using @figma/code-connect with co-located *.figma.tsx files
category: frontend
trigger: When bridging Figma designs to React components with Code Connect for design-dev handoff
version: 0.1.0-draft
source_project: lucida-ui
---

# Figma Code Connect for React

Bridge Figma component variants to React code using `@figma/code-connect`.

## When to use

- Team uses Figma for design and React for implementation
- Want Figma Dev Mode to show real component code snippets
- Components have variant props that map to Figma enum properties

## Steps

1. **Install** — `@figma/code-connect` package
2. **Configure** — `figma.config.json` at project root with `parser: "react"` and include/exclude globs
3. **Create `*.figma.tsx`** — Co-locate with the component, one file per Figma component node
4. **Map variants** — Use `figma.enum()`, `figma.string()`, `figma.boolean()`, `figma.instance()` for prop mapping
5. **Multiple connections** — Use `variant` filter in `figma.connect()` for different states (e.g., icon-only vs text button)

## Key patterns

See `content.md` for file structure and mapping examples.
