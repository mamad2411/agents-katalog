---
name: wp-divi-5-design-system
description: Builds or repairs a Divi 5 design system with Design Variables, Option Group Presets, Element Presets, naming conventions, and controlled local exceptions. Use when starting a site, standardizing repeated styles, or reducing design drift.
---

# wp-divi-5-design-system

Use this skill before broad page construction or when repeated styles have drifted across a Divi 5 site.

## Required Inputs

Collect:

- Exact Divi 5 version.
- Brand colors and required contrast pairs.
- Typography roles and available font files/services.
- Spacing, container width, border, radius, shadow, and button requirements.
- Repeated assets, text, and external links that should be centrally managed.
- Existing variables, Option Group Presets, Element Presets, and local overrides.
- Pages and Theme Builder templates that consume shared styling.

## Decision Order

1. Decide whether the value is genuinely shared.
2. Put shared primitive values in Design Variables.
3. Put reusable option-group styling in Option Group Presets.
4. Compose complete reusable variants as Element Presets.
5. Use local styles only for content-specific exceptions.
6. Repair repeated drift at the highest shared layer that owns the decision.

## Naming Guidance

- Name by role: `color-brand-primary`, `color-text-body`, `space-section`, `color-border-subtle`, `radius-button`.
- Avoid names tied to one page position such as `homepage-blue-box` unless the value is intentionally page-specific.
- Separate concerns that may diverge later, such as image radius and form-field radius.
- Keep the project's naming vocabulary consistent across variables and presets.

## Workflow

Use [`workflows/build-divi-design-system-workflow.md`](workflows/build-divi-design-system-workflow.md).

## Resources

- [`resources/design-system-decision-matrix.md`](resources/design-system-decision-matrix.md)
- [`examples/design-system-blueprint.md`](examples/design-system-blueprint.md)

## Review Expectations

- Confirm shared styles reference variables rather than copied literals.
- Confirm Option Group Presets are reusable across compatible elements.
- Confirm Element Presets describe meaningful complete variants.
- Confirm defaults do not create unexpected changes in unrelated content.
- Test representative pages and Theme Builder templates after shared changes.
- Document intentional local overrides and why they should remain local.
