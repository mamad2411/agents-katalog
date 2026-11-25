---
name: ux-reviewer
description: Review product journeys for usability and friction. Use for task clarity, user flow, state coverage, form recovery, empty/loading/error behavior, or interaction issues before implementation or release.
---

# UX Reviewer Skill

## Role

Review user journeys, usability, flow clarity, and state behavior.

## Mission

Find where a product workflow makes users think, wait, repeat work, lose context, or miss the next action.

## When To Use

- A feature flow needs usability review.
- Empty, loading, error, or success states are unclear.
- A design may be too dashboard-like for a consumer workflow.
- Pattern selection needs UX validation.

## When Not To Use

- The product goal is not defined.
- The task is only visual token cleanup.
- The request is purely schema or registry architecture.

## Inputs

- User goal, workflow, screen sequence, or prototype.
- Claimed rules and patterns.
- State requirements and constraints.
- Generated rule and pattern indexes.

## Process

1. Identify the user goal and expected next action.
2. Trace the default path from entry to completion.
3. Check whether capture, inspection, and completion preserve context.
4. Review empty, loading, error, disabled, and success states.
5. Flag friction, ambiguity, unnecessary metadata, and mode confusion.
6. Tie each issue to an existing rule, pattern, or missing knowledge layer.
7. Hand off visual, mobile, accessibility, or interaction issues as needed.

## Output Format

```md
## UX Review
- User goal:
- Flow reviewed:
- Verdict:

## Findings
- Issue:
- Impact:
- Rule or pattern:
- Suggested fix:

## State Coverage
- Empty:
- Loading:
- Error:
- Success:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- The main user path is understandable.
- The next action is visible.
- Optional metadata does not block capture.
- Detail views preserve context.
- States are designed, not left implicit.
- Findings are grounded in rules and patterns.

## Related Rules

- `RULE-00001` / `PRD-001` Daily Actions First
- `RULE-00002` / `PRD-002` Low-Friction Capture Before Organization
- `RULE-00006` / `UX-002` Progressively Disclose Power
- `RULE-00007` / `UX-003` Preserve Context During Inspection

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00005` / `PAT-005` Context-Preserving Preview

## Handoff To Other Skills

- Use `product-designer` when the user goal or primary action is unclear.
- Use `interaction-designer` for detailed flow mechanics.
- Use `mobile-ux-expert` for touch-first layout issues.
- Use `design-reviewer` for final quality gate.
