---
name: wp-theme-json-development
description: Designs and reviews version-compatible WordPress theme.json settings, presets, styles, layouts, custom templates, template parts, and design tokens. Use when building or changing a block theme's design system.
---

# wp-theme-json-development

Use this skill for `theme.json` work anchored to the project's minimum WordPress version.

## Required Inputs

- Minimum and tested WordPress versions.
- Versioned schema URL.
- Existing preset slugs and public compatibility commitments.
- Design tokens and allowed editor freedom.
- Content and wide layout widths.
- Required custom templates and template parts.
- Existing style variations and user customizations.

## Principles

- Validate against the minimum-version schema.
- Prefer presets and generated CSS variables over duplicated literals.
- Keep public slugs stable.
- Enable controls intentionally.
- Separate settings from default styles.
- Use block-level styles only when the global baseline should differ for a block.
- Avoid custom CSS when a supported structured property is available.
- Do not assume living-schema properties exist in the target Core release.

## Workflow

Use [`workflows/build-theme-json-workflow.md`](workflows/build-theme-json-workflow.md).

## Resource

Use [`resources/theme-json-review-checklist.md`](resources/theme-json-review-checklist.md).

## Example

Use [`examples/theme-json-v3-baseline.json`](examples/theme-json-v3-baseline.json) as a conservative starting point, not a universal design.

## Completion Evidence

Record:

- Schema and Core compatibility floor.
- Preset and custom-property inventory.
- Controls intentionally enabled/disabled.
- Custom templates and parts registered.
- Validation results.
- Editor/frontend parity results.
- Migration impact of changed slugs or values.
