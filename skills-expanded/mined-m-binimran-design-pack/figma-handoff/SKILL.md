---
name: figma-handoff
description: Pull a Figma design via the Figma connector and produce a developer handoff - tokens, specs, redlines, asset list, and component notes. Use when handing a design to engineering or auditing a Figma file.
---

# figma-handoff

Turn a Figma file into a clean, accurate handoff using the **Figma connector** (never guess values).

## Process
1. **Read the design** via Figma: frames, variables/tokens, text styles, components, screenshots. If Figma
   isn't connected, say so - don't invent frame names or values.
2. **Extract tokens** (hand to `design-tokens`): colours, type scale, spacing, radius, shadows - from Figma
   variables, not eyeballed.
3. **Spec the screens:** spacing, sizes, breakpoints, states (hover/active/disabled/empty/error), interactions.
4. **List assets** to export with names + formats + densities (hand to `asset-export`).
5. **Flag issues:** contrast misses (the `contrast-guard` hook + `accessibility-contrast`), inconsistent
   spacing/type, missing states.

## Output
- A handoff doc: tokens, per-screen specs, asset export list, component notes, and an issues list. Every value
  sourced from Figma or marked `[verify]`.

## Guardrails
- All measurements come from the Figma connector or are flagged - no fabricated pixels.
- Don't claim a file was read if the connector didn't return it.
