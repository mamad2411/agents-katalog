---
name: figma
description: Compare the current screen implementation against its Figma design and fix visual discrepancies. Use after a significant UI change, new screen, redesign, or design handoff — not for every small tweak.
argument-hint: "<figma_url_or_node_id>"
---

Run a Figma design sync for the current screen using the Figma MCP.

## When to use

Only invoke this after a significant UI change — a new screen, a redesign, or after a design handoff. Do not run on every small tweak.

## Steps

1. **Get the Figma design** — use `mcp__figma__get_figma_data` with `$ARGUMENTS` as the node URL or ID to fetch the design spec

2. **Identify the implementation file** — find the screen component that corresponds to the Figma frame (use `get_routes` if unsure which file to look at)

3. **Compare** — list the visual differences between the Figma spec and the current implementation: spacing, typography, colors, layout, component usage

4. **Fix** — apply corrections using Tamagui design tokens from `src/theme/`:
   - Never use raw hex or rgba — use `$token` references
   - Check `src/theme/themes.ts` for valid token names before using one
   - Use `get_components` to find existing components before creating new ones

5. **Download assets if needed** — use `mcp__figma__download_figma_images` for icons or images that need exporting

6. **Report** — summarise what was changed and what (if anything) could not be matched due to missing tokens or components

## Rules

- Do not redesign — match the Figma spec as closely as possible, don't improve it
- If a Figma token has no equivalent in `src/theme/`, flag it to the user instead of approximating
- Run `tsc --noEmit` after changes to confirm no type errors
