---
name: design-sync
description: Sync DESIGN.md with your Figma design library — auto-update colors, typography, spacing, and component tokens
category: devops
triggers:
  - "sync design"
  - "update from figma"
  - "sync design tokens"
---

Keep your DESIGN.md in sync with Figma. The agent reads your design library, extracts tokens, shows a diff, and updates the file.

## How to use

- "Sync DESIGN.md with our Figma library" → full token update
- "Update colors from Figma" → colors only
- "What changed in Figma since last sync?" → diff without writing
- "Rebuild DESIGN.md from Figma file [URL]" → full rebuild

## What it extracts

- Color styles → `tokens.colors`
- Text styles → `tokens.typography.scale`
- Effect styles → `tokens.elevation` / `tokens.shadows`
- Component properties → `tokens.components`
- Spacing from auto layout → `tokens.spacing`

Always shows diff before writing. Preserves markdown rationale.

For full instructions, read `agents/design-sync.md`.
