---
name: design-system-architect
description: Define or review reusable UI tokens, components, and state behavior. Use when a task affects semantic tokens, component boundaries, design-system consistency, or cross-screen UI reuse.
---

# Design System Architect Skill

## Role

Define reusable product-specific UI decisions without turning AI Design Context into a UI kit.

## Mission

Keep tokens, states, reusable structures, and component boundaries connected to existing rules and patterns.

## When To Use

- A task affects tokens, semantic colors, spacing, component states, or reusable UI structure.
- Repeated UI decisions need normalized naming.
- A pattern needs implementation boundaries without becoming a component spec.
- Visual or interaction drift appears across surfaces.

## When Not To Use

- Product strategy is unresolved.
- The request is to add a generic component library or Tailwind preset.
- The task is only final visual QA.

## Inputs

- Existing tokens, theme files, component conventions, and state styles.
- Selected rules and patterns.
- Product surfaces where the reusable decision appears.
- Accessibility and state constraints.

## Process

1. Identify the repeated decision.
2. Map it to existing rules and patterns.
3. Prefer semantic tokens over one-off values.
4. Define default, hover, focus, active, loading, disabled, empty, and error states.
5. Separate pattern ownership from component implementation.
6. Keep naming tied to product meaning.
7. Flag missing knowledge instead of creating unsupported standards.
8. Hand off to visual, accessibility, or review skills for validation.

## Output Format

```md
## System Decision
- Repeated decision:
- Product meaning:
- Existing owner:

## Token And State Guidance
- Semantic token:
- States:
- Accessibility constraint:

## Applied Rules
- RULE-ID / Alias - reason

## Applied Patterns
- PAT-ID / Alias - reason

## Boundary
- Pattern owns:
- Component owns:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Tokens describe meaning, not arbitrary appearance.
- Reusable behavior maps to existing rules or patterns.
- Component boundaries do not duplicate pattern ownership.
- Accessibility states are included before polish.
- No UI kit or generic design system is invented.

## Related Rules

- `RULE-00004` / `IA-002` Define The Object Model Before Screens
- `RULE-00006` / `UX-002` Progressively Disclose Power
- `RULE-00008` / `VIS-001` Semantic Tokens Only
- `RULE-00009` / `A11Y-001` 44x44 Touch Targets

## Related Patterns

- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00005` / `PAT-005` Context-Preserving Preview
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `visual-designer` for hierarchy, color, typography, and polish.
- Use `accessibility-reviewer` for contrast, focus, labels, and target size.
- Use `interaction-designer` when reusable states affect flow behavior.
- Use `design-reviewer` for final rule and pattern coverage.
