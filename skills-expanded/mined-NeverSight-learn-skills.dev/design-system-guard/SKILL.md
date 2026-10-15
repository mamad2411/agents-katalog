---
name: design-system-guard
description: Protect UI consistency by auditing or guiding component implementation against design tokens, spacing, typography, color, radius, variants, reusable patterns, dark mode, and accessibility contrast. Use for React, Next.js, TypeScript, Tailwind CSS, shadcn/ui, and Radix UI work in B2B SaaS, admin, developer, productivity, CRM/ERP, and internal-tool interfaces.
---

# Design System Guard

## When to Use This Skill

Use this skill when reviewing UI code, pull requests, components, pages, or design specifications for consistency with an existing design system. Also use it before implementation when a feature risks introducing new visual primitives or variants.

Enforce the project's actual tokens and components first. Do not invent a replacement design system. Generate refactoring or implementation code only when explicitly requested.

## Inputs

Inspect:

- theme files, CSS variables, Tailwind configuration, and token definitions
- shared component libraries and variant APIs
- existing typography, spacing, color, radius, shadow, and motion scales
- representative tables, cards, lists, forms, and navigation patterns
- dark mode and high-contrast behavior
- the target code, design, screenshot, or component specification

If no formal design system exists, infer only repeated local conventions and label them as inferred.

## What to Enforce

- design-token usage instead of arbitrary values
- consistent spacing and layout rhythm
- explicit typography hierarchy
- consistent border radius, border, shadow, and elevation
- semantic color usage and state meaning
- controlled button sizes, priorities, and variants
- consistent form labels, help text, validation, and disabled states
- consistent table, card, and list structure
- reusable components instead of duplicated styles
- dark mode readiness
- accessibility contrast, focus visibility, and non-color cues

## Decision Rules

1. Resolve values in this order: existing semantic token, existing primitive token, established component variant, then a justified new token.
2. Flag arbitrary Tailwind values such as custom pixel spacing or one-off colors when a suitable token exists.
3. Recommend a new token only when the value represents a repeatable semantic decision, not a single exception.
4. Recommend component reuse when structure, behavior, and semantics match. Do not force reuse based on visual similarity alone.
5. Extend an existing variant when the use case recurs and has stable semantics. Avoid variants named after a single page.
6. Use semantic colors for intent such as success, warning, destructive, muted, and accent. Do not encode meaning with color alone.
7. Keep one typography role consistent across pages; do not select heading size by local appearance.
8. Apply radius and elevation by component role, not personal preference.
9. Require form controls to share label, help, error, required, disabled, and focus behavior.
10. Check light and dark themes whenever raw colors, opacity, borders, shadows, charts, or overlays change.
11. Treat contrast, focus loss, inaccessible disabled states, and missing labels as accessibility concerns, not visual polish.
12. Separate must-fix violations from optional consolidation opportunities.

## Review Procedure

1. Locate the source of truth for tokens and shared components.
2. Compare the target against the closest established pattern.
3. Record exact arbitrary values, duplicated styles, unsupported variants, and semantic mismatches.
4. Identify reuse or extraction opportunities with affected locations.
5. Check dark mode, contrast, keyboard focus, and state communication.
6. Recommend the smallest refactor that restores consistency.

## Output Format

Use these headings in this order:

### Consistency Check

Summarize the system sources inspected, overall alignment, and important assumptions.

### Token Violations

For each violation include location, current value or class, expected token or role, and severity.

### Component Reuse Opportunities

Identify an existing component or shared pattern, the duplicated implementation, and the reuse boundary.

### Accessibility Concerns

Report contrast, focus, semantics, labels, keyboard behavior, and color-only communication issues. State when runtime testing is still required.

### Refactor Recommendations

Order recommendations by user impact, recurrence, and implementation risk. Do not include code unless requested.

## Anti-Patterns to Avoid

- Replacing tokens with arbitrary values to match a screenshot.
- Adding one-off colors, spacing, radii, shadows, or page-specific variants.
- Duplicating shared component styles in feature code.
- Creating a universal component with unrelated responsibilities.
- Forcing visual uniformity across controls with different semantics.
- Using opacity alone for disabled states without checking contrast and affordance.
- Assuming light-theme choices work in dark mode.
- Claiming accessibility compliance from static code or screenshots alone.
- Proposing broad design-system rewrites for a localized violation.
