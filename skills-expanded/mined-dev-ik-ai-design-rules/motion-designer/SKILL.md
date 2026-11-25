---
name: motion-designer
description: Design or review purposeful UI motion. Use when animations affect orientation, feedback, transitions, loading, performance, or reduced-motion behavior in product interfaces.
---

# Motion Designer Skill

## Role

Define purposeful motion and transition behavior for product orientation.

## Mission

Use motion only when it clarifies continuity, preserves context, or explains state change.

## When To Use

- A screen opens detail, preview, sheet, or split context.
- Users may lose orientation during navigation or state change.
- Loading, completion, undo, or error feedback needs motion guidance.
- Existing animation feels decorative, slow, or distracting.

## When Not To Use

- Motion is requested only as decoration.
- Accessibility or performance constraints make motion unsafe.
- The interaction model is not defined.

## Inputs

- Interaction flow and affected surfaces.
- State transitions and user goal.
- Performance and reduced-motion constraints.
- Related rules and patterns.

## Process

1. Identify what orientation problem motion must solve.
2. Define start state, end state, and preserved context.
3. Select or define a reusable motion role with inspectable timing and easing.
4. Keep duration short and purpose clear.
5. Provide reduced-motion and unsupported-platform behavior.
6. Avoid hiding loading, errors, or state changes behind animation.
7. Hand off performance and accessibility checks.

## Output Format

```md
## Motion Decision
- Transition:
- Purpose:
- Start state:
- End state:
- Motion role:
- Timing and easing:
- Reduced motion:
- Platform fallback:

## Risks
- Accessibility:
- Performance:

## Related Rules And Patterns
- Rule:
- Pattern:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Motion explains a spatial or state relationship.
- Motion does not delay the primary action.
- Reduced-motion behavior is defined.
- Loading and error states remain clear.
- Motion supports context preservation.
- Repeated transitions use consistent named roles.
- Unsupported APIs have a progressive fallback.

## Related Rules

- `RULE-00006` / `UX-002` Progressively Disclose Power
- `RULE-00007` / `UX-003` Preserve Context During Inspection
- `RULE-00009` / `A11Y-001` 44x44 Touch Targets
- `RULE-00013` / `A11Y-004` Reduce Non-Essential Interaction Motion
- `RULE-00015` / `UX-004` Use Motion To Explain State Continuity

## Related Patterns

- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00005` / `PAT-005` Context-Preserving Preview

## Handoff To Other Skills

- Use `interaction-designer` if flow mechanics are undefined.
- Use `accessibility-reviewer` for reduced-motion and focus concerns.
- Use `performance-reviewer` for animation cost and responsiveness.
- Use `design-reviewer` for final quality gate.
