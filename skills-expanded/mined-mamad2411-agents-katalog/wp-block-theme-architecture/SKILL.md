---
name: wp-block-theme-architecture
description: Plans a WordPress block theme's responsibilities, compatibility floor, file structure, source-of-truth model, child-theme boundary, and implementation sequence. Use before starting a new block theme or restructuring an existing one.
---

# wp-block-theme-architecture

Use this skill before implementation or when a block theme has unclear ownership boundaries.

## Required Inputs

- Theme purpose, audience, distribution model, and ownership.
- Exact WordPress and PHP compatibility floors.
- Whether the Gutenberg plugin is part of the supported runtime.
- Existing templates, parts, patterns, styles, plugins, and user customizations.
- Required content types, business behavior, and custom blocks.
- Deployment, update, child-theme, and rollback expectations.

## Decisions

- Separate theme presentation from plugin-owned behavior.
- Decide which artifacts are theme source, site content, or user customization.
- Choose the minimum template hierarchy needed.
- Decide whether a child theme is required or whether a separate theme/plugin is safer.
- Establish stable namespaces and slugs.
- Define a clean-site verification environment without database overrides.

## Workflow

Use [`workflows/plan-block-theme-workflow.md`](workflows/plan-block-theme-workflow.md).

## Resource

Use [`resources/theme-boundary-decision-matrix.md`](resources/theme-boundary-decision-matrix.md).

## Example

Use [`examples/minimal-block-theme-structure.md`](examples/minimal-block-theme-structure.md).

## Completion Evidence

Record:

- Compatibility range and schema.
- Theme/plugin/content ownership decisions.
- Planned file tree.
- Required templates and fallbacks.
- Source-of-truth strategy.
- Test environments and release evidence.
