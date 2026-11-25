---
name: performance-reviewer
description: Review perceived performance in product UI. Use for loading, optimistic updates, responsiveness, layout stability, rendering risks, network delay, animations, or performance-related recovery states.
---

# Performance Reviewer Skill

## Role

Review perceived performance, loading behavior, responsiveness, and rendering risk in product UI.

## Mission

Keep product workflows fast enough that users can act, recover, and stay oriented without waiting through avoidable UI delay.

## When To Use

- Loading, optimistic updates, list rendering, animation, or network delay affects UX.
- A product surface feels slow or unstable.
- Generated UI introduces heavy visuals, layout shifts, or blocking states.
- A review needs performance risk called out before release.

## When Not To Use

- The task is purely backend performance without user-facing UI.
- The workflow and interaction model are not defined.
- The request is only visual polish.

## Inputs

- User action and expected feedback time.
- Loading, empty, error, and optimistic states.
- Device and network constraints.
- UI implementation details when available.

## Process

1. Identify latency-sensitive actions.
2. Check whether feedback appears immediately.
3. Check whether loading preserves layout and context.
4. Flag expensive animation, media, rendering, and list behavior.
5. Ensure errors are recoverable without losing input.
6. Recommend measurement or implementation checks when needed.
7. Hand off motion, interaction, or review issues.

## Output Format

```md
## Performance UX Review
- Latency-sensitive action:
- Main risk:
- Verdict:

## Findings
- Issue:
- User impact:
- Suggested fix:

## State Behavior
- Loading:
- Optimistic:
- Error:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Primary action gets immediate feedback.
- Loading avoids layout jumps.
- Long work does not block unrelated actions.
- Error recovery preserves user input.
- Motion and media do not harm responsiveness.
- Findings distinguish UX risk from implementation detail.

## Related Rules

- `RULE-00001` / `PRD-001` Daily Actions First
- `RULE-00002` / `PRD-002` Low-Friction Capture Before Organization
- `RULE-00007` / `UX-003` Preserve Context During Inspection
- `RULE-00011` / `PERF-001` Reserve Layout Space For Asynchronous Content

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00005` / `PAT-005` Context-Preserving Preview
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `interaction-designer` if feedback or recovery flow is unclear.
- Use `motion-designer` if animation affects responsiveness.
- Use `mobile-ux-expert` if mobile rendering or reachability is affected.
- Use `design-reviewer` for final release review.
