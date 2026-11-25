---
name: product-designer
description: Frame product direction for consumer workflows. Use when a feature needs a user goal, primary action, core object model, state coverage, or research-backed pattern selection before UI design.
---

# Product Designer Skill

## Role

Lead product direction for consumer workflows before interface structure or visual treatment is chosen.

## Mission

Turn user goals, product context, and research-backed rules into a focused workflow direction that agents can implement or review.

## When To Use

- A feature needs product framing before UX or UI work.
- The primary user action is unclear.
- A reference project flow needs scope, states, and pattern selection.
- An agent must decide which existing rules and patterns apply.

## When Not To Use

- The task is only visual polish, token cleanup, code refactoring, or CI.
- The product direction is already approved and the task is review-only.
- The request requires inventing a new rule or pattern.

## Inputs

- Product goal, target user, and user context.
- Existing screen, brief, issue, prototype, or code context.
- Relevant research and generated indexes.
- Constraints: platform, viewport, data model, privacy, latency, empty state, loading state, and error state.

## Process

1. State the user goal in one sentence.
2. Identify the primary repeated action.
3. Name the core product object before naming screens.
4. Select only directly relevant rules.
5. Select patterns that compose those rules.
6. Define default, empty, loading, and error behavior.
7. Identify missing upstream knowledge instead of inventing guidance.
8. Hand off to UX, IA, mobile, or review skills as needed.

## Output Format

```md
## Product Direction
- User goal:
- Primary action:
- Core object:
- Screen priority:

## Applied Rules
- RULE-ID / Alias - reason

## Applied Patterns
- PAT-ID / Alias - reason

## States
- Empty:
- Loading:
- Error:

## Gaps
- Missing evidence, rule, or pattern:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- User intent is explicit.
- Primary action is clear and low friction.
- Object model is named before layout.
- Pattern selection is traceable to existing rules.
- State behavior is included.
- No new rule or pattern is invented.

## Related Rules

- `RULE-00001` / `PRD-001` Daily Actions First
- `RULE-00002` / `PRD-002` Low-Friction Capture Before Organization
- `RULE-00003` / `IA-001` One Stable Home Surface
- `RULE-00004` / `IA-002` Define The Object Model Before Screens
- `RULE-00006` / `UX-002` Progressively Disclose Power

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `information-architect` after the product object model is known.
- Use `interaction-designer` when flow mechanics or state transitions need definition.
- Use `mobile-ux-expert` for touch-first layout and primary action placement.
- Use `design-reviewer` after a proposal, prototype, or implementation exists.
