---
name: tokens-before-components
description: Lock the visual system (palette, type, spacing) as tokens before building UI, and re-state them every refinement to prevent token drift.
---

# Tokens before components

When the visual system is specific — a real palette, a distinctive type pairing, an opinionated spacing scale — everything built from it inherits that personality automatically. Define the tokens first; then build to them. Components without a locked system drift toward defaults.

## Patterns

- Establish design tokens (colors as hex, type as font/size/weight/line-height/letter-spacing, a numbered spacing scale, radii) before generating components.
- Pass the tokens as explicit values in build prompts. The model reads exact values from text, never from a screenshot.
- Re-paste the tokens in every refinement, even when it feels redundant — they fade from active context and the model reaches for "standard" values (a default blue, a uniform padding) when it can no longer see them.
- Reuse existing shared tokens and components before introducing new ones; keep naming consistent across the workspace.

## Examples

```text
// BAD — building a component with no design tokens defined
"Build a primary button component."
→ Result: #3b82f6 blue, 4px border-radius, Inter — all defaults

// GOOD — tokens defined first, passed explicitly in the build prompt
Tokens:
  color.brand:      #1a1a2e
  color.accent:     #e94560
  font.heading:     "PP Mori", sans-serif — 600, -0.02em tracking
  spacing.scale:    4 / 8 / 16 / 24 / 40 / 64px
  radius.default:   2px

"Build a primary button using color.accent (#e94560), radius.default (2px),
 font.heading at 14px/600. No shadows."
```

## Token drift

The classic failure: the first build looks right, then three prompts later a color has quietly become a standard blue. The cause is tokens falling out of context. The fix is restating them — or starting a fresh session with the working version and tokens pasted in.
