---
name: design-color-theory
description: "Design and diagnose UI color palettes, color harmony, complementary and analogous schemes, neutral/brand accents, light and dark modes, semantic tokens and accessible actual color pairings."
---

# Color theory

## Scope

Use this specialist when the actual task involves color issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **color**. Related governing principles: contrast, unity. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **palette-sprawl**: Inventory colors; define neutral ramp, primary accent, semantic feedback roles and light/dark mappings as tokens. Verify: Every new UI color maps to an explicit semantic role and works in every supported theme.
- **accent-saturation**: Reserve high-chroma accent for primary action/highest hierarchy; use neutral and muted supporting surfaces. Verify: Attention test identifies intended focal element without relying solely on hue.
- **state-without-pair**: Build pairing matrix for text, backgrounds, borders, links, focus and status; measure contrast for each rendered state. Verify: selected WCAG 2.1/2.2 AA SC 1.4.3 and 1.4.11 evaluated for applicable actual color pairings; status never color-only.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
