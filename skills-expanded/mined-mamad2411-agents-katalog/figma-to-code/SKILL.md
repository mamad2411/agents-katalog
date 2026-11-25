---
name: figma-to-code
description: Translate Figma designs into production-ready frontend code and design-system rules. Inspired by OpenAI Figma implementation skills and adapted for Codex v4.1. Use when implementing a Figma design, extracting design tokens, matching visual fidelity, or converting design specs to components.
---

# Figma To Code

## Workflow

1. Inspect the target app's existing component system, tokens, and styling approach.
2. Read Figma structure: frames, variants, auto-layout, constraints, typography, colors, effects, and component names.
3. Map Figma components to existing code components first.
4. Extract tokens only when the project lacks an equivalent.
5. Implement layout with responsive constraints, not fixed screenshot positioning.
6. Verify visual fidelity with browser screenshots when possible.

## Fidelity Checks

- Typography: font family, size, weight, line height, spacing.
- Layout: spacing, alignment, constraints, density, breakpoints.
- Components: states, variants, disabled, selected, focus, hover.
- Assets: icons, images, masks, gradients, shadows.
- Behavior: scrolling, overflow, dialogs, menus, inputs.

## Engineering Rules

- Do not create duplicate components when an existing design-system component fits.
- Do not hardcode one-off values if tokens exist.
- Do not copy Figma layer names into code blindly.
- Preserve accessibility semantics even if the design omits them.

## Output

State mapping from Figma elements to code components, new tokens/components, fidelity checks, and verification result.
