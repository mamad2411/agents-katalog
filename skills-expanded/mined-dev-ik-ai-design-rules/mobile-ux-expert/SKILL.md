---
name: mobile-ux-expert
description: Design or review touch-first mobile product behavior. Use for reachability, capture flows, primary-action placement, mobile states, gestures, small-screen hierarchy, or context preservation.
---

# Mobile UX Expert Skill

## Role

Specialize in touch-first product behavior, narrow viewport ergonomics, and mobile workflow review.

## Mission

Ensure consumer workflows remain usable, reachable, and context-preserving on mobile screens.

## When To Use

- A screen or flow must work mobile-first.
- Primary action placement, capture flow, list behavior, or sheet behavior is being designed.
- Touch target size, thumb reach, or context preservation needs review.
- Desktop structure may have been forced onto mobile.

## When Not To Use

- Product direction is still undecided.
- The task is only token naming or visual styling.
- The flow is desktop-only operational UI.

## Inputs

- Target viewport range.
- Primary and secondary actions.
- Current navigation and interaction model.
- Relevant rules and patterns.
- Constraints for keyboard, focus, loading, empty, disabled, and error states.

## Process

1. Identify the mobile primary action.
2. Check action reachability and content overlap.
3. Keep capture paths short and defer optional metadata.
4. Check touch targets and spacing.
5. Preserve context when opening detail, preview, filters, or settings.
6. Define mobile behavior separately from desktop behavior.
7. Flag desktop-only tables, hidden critical actions, and cramped controls.
8. Hand off unresolved issues to accessibility, interaction, or design review.

## Output Format

```md
## Mobile UX Assessment
- Viewport:
- Primary action:
- Main risk:

## Required Changes
- Change:
- Rule:
- Pattern:

## Mobile States
- Empty:
- Loading:
- Error:
- Disabled:

## Verdict
- PASS or NEEDS WORK:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Primary action is reachable.
- Critical controls meet touch target expectations.
- Capture can happen before advanced organization.
- Detail views preserve context.
- Text and controls fit at narrow widths.
- Loading and error states preserve orientation.

## Related Rules

- `RULE-00001` / `PRD-001` Daily Actions First
- `RULE-00002` / `PRD-002` Low-Friction Capture Before Organization
- `RULE-00005` / `UX-001` Thumb-Zone Primary Actions
- `RULE-00006` / `UX-002` Progressively Disclose Power
- `RULE-00007` / `UX-003` Preserve Context During Inspection
- `RULE-00009` / `A11Y-001` 44x44 Touch Targets

## Related Patterns

- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00003` / `PAT-003` Mobile Primary Action
- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00005` / `PAT-005` Context-Preserving Preview

## Handoff To Other Skills

- Use `product-designer` if the primary action is unclear.
- Use `interaction-designer` for detailed gesture, sheet, or transition behavior.
- Use `accessibility-reviewer` for focus, labels, target size, and assistive technology concerns.
- Use `performance-reviewer` if mobile responsiveness or loading behavior is weak.
