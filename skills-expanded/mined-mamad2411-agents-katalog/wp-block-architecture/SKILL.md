---
name: wp-block-architecture
description: Plans WordPress block architecture, rendering mode, data ownership, compatibility floors, and package boundaries. Use before creating a block or changing its persistence model.
---

# WordPress Block Architecture

Use this skill before implementation or when a block's responsibilities are unclear.

## Required Inputs

Identify:

- Minimum and tested WordPress versions.
- PHP, Node.js, package-manager, and browser support.
- Distribution boundary: existing plugin, new plugin, theme, or project-local code.
- Data owner and source of truth.
- Static, dynamic, hybrid, or interactive rendering needs.
- Saved-content and migration constraints.
- Editor and front-end acceptance criteria.

## Procedure

1. Read `resources/architecture-decision-matrix.md`.
2. Inspect existing `block.json`, registration code, saved markup, PHP rendering, and build setup.
3. Select the narrowest rendering and persistence model that meets the requirements.
4. Decide which values belong in attributes, InnerBlocks, entity data, block context, bindings, or server state.
5. Define the compatibility floor before selecting supports or APIs.
6. Define failure behavior when JavaScript, the plugin, remote data, or the render callback is unavailable.
7. Produce an implementation plan with tests and a migration strategy.

## Workflow

Use `workflows/plan-block-workflow.md`.

## Resources

- `resources/architecture-decision-matrix.md`
- `resources/official-docs-map.md`

## Example

- `examples/static-dynamic-decision-example.md`

## Output

Return:

- Architecture choice and rejected alternatives.
- Persistence contract.
- Compatibility assumptions.
- Security and accessibility boundaries.
- Required tests and migration steps.
