---
name: design-unity-and-systems
description: "Unify aesthetic design across pages and components with reusable primitive, semantic and component design tokens, coherent brand style and appropriately scoped design systems."
---

# Design unity and systems

## Scope

Use this specialist when the actual task involves systems issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **systems**. Related governing principles: unity, pattern. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **one-off-design-constants**: Define primitive→semantic→component tokens; migrate one component family at a time. Verify: Static checks show component values draw from intended tokens; theme change propagates.
- **cross-page-style-drift**: Inventory variants; consolidate shared components while preserving semantic differences. Verify: Screenshot matrix covers default, hover, focus, active, disabled, error and dark mode.
- **theme-inconsistency**: Use role-named semantic colors and validate each theme state independently. Verify: Contrast/legibility pass on both themes; design identity remains recognizable.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
