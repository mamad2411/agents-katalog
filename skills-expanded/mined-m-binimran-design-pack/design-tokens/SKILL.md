---
name: design-tokens
description: Define or extract a design token system (color, type, spacing, radius, shadow) and output it as JSON/CSS variables. Use when setting up a design system or converting a Figma/brand palette to tokens.
---

# design-tokens

A single source of truth for visual values, so every asset and screen stays consistent.

## Process
1. **Source the values** from Figma variables (via the connector), a brand kit, or Brand.dev - not from memory.
2. **Structure the tokens:**
   - Colour: a base scale + semantic aliases (`--color-text`, `--color-bg`, `--color-brand`, success/warn/danger).
   - Type: family pairing, a fluid scale, weights, line-heights.
   - Spacing: a consistent step scale; radius; shadow set.
3. **Name semantically** (by role, not by raw value) so components read by meaning.
4. **Check contrast** of text/bg semantic pairs (the `contrast-guard` hook checks CSS; aim >= 4.5:1).
5. **Output** as `tokens.json` and/or CSS custom properties / Tailwind `@theme`.

## Output
- The token file(s), the semantic aliases, and a note on which tokens are brand-specific vs. structural,
  plus any contrast warnings.

## Guardrails
- No raw hex/px in components once tokens exist - reference the token.
- Values come from a real source; don't invent a palette and call it the brand's.
