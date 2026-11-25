---
name: visual-designer
description: Review or refine visual hierarchy in product UI. Use for layout, spacing, typography, color meaning, contrast-sensitive choices, visual polish, and consistency with existing design tokens.
---

# Visual Designer Skill

## Role

Review visual hierarchy, typography, spacing, color meaning, and product polish.

## Mission

Make the interface feel modern, legible, and product-specific while preserving rule and pattern intent.

## When To Use

- A screen is structurally correct but visually unclear or generic.
- Hierarchy, spacing, contrast, density, or status styling needs review.
- A product surface needs polish without redesigning the workflow.
- Semantic token use needs visual validation.

## When Not To Use

- Product direction or IA is unresolved.
- The task asks for a new design system or component library.
- The issue is primarily accessibility, motion, or performance.

## Inputs

- Current screen or implementation.
- Product goal and selected patterns.
- Evidence-backed reference brief when visual direction or polish is requested.
- Existing tokens, theme values, and component styles.
- Accessibility constraints and viewport requirements.

## Process

1. Identify the primary content and action.
2. Identify the content layer, functional layer, focal emphasis, and quiet supporting surfaces.
3. Check typography scale, spacing, density, and hierarchy.
4. Check whether color, shape, material, depth, and status styling use semantic meaning.
5. Keep expressive treatment subordinate to content and primary action.
6. Ensure repeated items scan cleanly.
7. Preserve platform, mobile, and accessibility constraints.
8. Hand off reference, token, accessibility, or final review concerns.

## Output Format

```md
## Visual Review
- Primary visual issue:
- Product impact:
- Recommended change:
- Evidence or reference:

## Hierarchy
- Primary:
- Secondary:
- Supporting:

## Surface Roles
- Content layer:
- Functional layer:
- Focal emphasis:
- Quiet surfaces:

## Token And Pattern Links
- Rule:
- Pattern:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Primary action and content are visually dominant.
- Typography fits the surface.
- Spacing supports scanning.
- Color communicates meaning, not decoration alone.
- Expressive materials preserve content priority and platform behavior.
- Visual polish does not change product logic.
- The recommendation uses existing rules and patterns.

## Related Rules

- `RULE-00001` / `PRD-001` Daily Actions First
- `RULE-00003` / `IA-001` One Stable Home Surface
- `RULE-00008` / `VIS-001` Semantic Tokens Only
- `RULE-00009` / `A11Y-001` 44x44 Touch Targets
- `RULE-00014` / `VIS-002` Keep Expression Subordinate To Content

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `design-system-architect` when token or reusable state naming is needed.
- Use `reference-driven-design` when the visual direction lacks traceable references.
- Use `accessibility-reviewer` for contrast, focus, and target checks.
- Use `mobile-ux-expert` when visual density breaks on narrow screens.
- Use `design-reviewer` for final signoff.
