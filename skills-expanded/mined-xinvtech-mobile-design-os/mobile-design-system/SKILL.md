---
name: mobile-design-system
description: Extract, define, and govern reusable mobile design tokens, foundations, components, themes, accessibility semantics, and platform variants from Design DNA, UI specifications, or an existing app. Use when Codex needs a standalone mobile design system instead of product-specific screen styling, or when a UI package must become a maintainable implementation library.
---

# Mobile Design System

Turn visual intent and repeated UI behavior into a small, semantic, accessible system that can survive new screens and platform variants.

## Establish the input contract

Prefer `design-dna.json`, `ui-design.json`, and the selected `visual-direction.md`. For new or replacement visual work, require the `ui-design.json` visual lock and consume its selected style family, reference IDs, theme variant, and exact theme tokens. Preserve provenance: inherited values come from an upstream artifact, specified values are deliberate target decisions, and estimated values remain estimates. Never turn a screenshot guess into an observed token.

## Build the system in layers

1. Define foundations: color roles, type roles, spacing, shape, elevation/material, iconography, motion, content voice, and accessibility rules.
2. Copy the locked reference fingerprint into the system thesis and keep the selected semantic theme tokens as the renderer source of truth.
3. Define tokens as `primitive → semantic → component` where the system benefits from the extra layer. Prefer semantic roles over raw values in screen contracts.
4. Define components by user meaning and repeated anatomy, not by a generic “card” bucket.
5. Specify default, pressed, focused, selected, disabled, loading, success, warning, failure, stale, expired, and permission states as applicable.
6. Record light/dark, compact/regular, iOS/Android, large-text, keyboard, Reduce Motion, and localization variants.
7. Establish governance: naming, deprecation, change ownership, contrast/target-size checks, and acceptance signals.

Read [references/system-rules.md](references/system-rules.md) for token and component boundaries. Use [references/design-system-schema.md](references/design-system-schema.md) before creating structured output.

## Produce and validate

Create:

- `design-system.md` using [assets/design-system-template.md](assets/design-system-template.md).
- `design-system.json` using [assets/design-system-template.json](assets/design-system-template.json).

Run `python3 scripts/validate_design_system.py <path-to-design-system.json>` and fix every error. When a UI artifact is available, also validate that every referenced UI token and component has a system definition.

If `ui-design.json` contains `visualExploration`, run the validator with `--source-ui` and reject any Design System whose `visualLock` is missing, unlocked, or inconsistent with the chosen direction. Never rebuild the system from Design DNA alone after a visual lock exists.

## Enforce the output order

1. System thesis, scope, and provenance.
2. Foundations and semantic tokens.
3. Component contracts and state behavior.
4. Themes, platform variants, and accessibility pressure.
5. Governance, coverage, open questions, and confidence.

Do not finish with a color palette alone, a component gallery with no state semantics, or a system that cannot explain how a new screen consumes its roles.
