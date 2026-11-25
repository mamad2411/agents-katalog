---
name: interaction-designer
description: Design and review interaction mechanics for product flows. Use for feedback, state transitions, recovery, previews, confirmations, loading behavior, and context-preserving interactions.
---

# Interaction Designer Skill

## Role

Design concrete interaction flows, transitions, input behavior, and state changes.

## Mission

Make actions feel direct, recoverable, and context-preserving without adding unsupported visual novelty.

## When To Use

- A flow needs step-by-step behavior.
- Capture, edit, preview, completion, or undo behavior is unclear.
- A sheet, modal, detail view, or split surface needs interaction rules.
- State transitions affect user trust or orientation.

## When Not To Use

- The product object model is unknown.
- The task is only visual hierarchy.
- The request is purely accessibility or performance review.

## Inputs

- User goal and primary action.
- Object model and navigation context.
- Selected rules and patterns.
- State requirements: empty, loading, error, success, disabled, optimistic, and undo.
- Agent lifecycle requirements when work is delegated, long-running, or interruptible.

## Process

1. Map entry, action, feedback, recovery, and exit.
2. Define what stays visible during interaction.
3. Keep required input minimal.
4. Define optimistic, loading, error, and undo behavior.
5. Preserve context during preview and detail inspection.
6. Avoid transitions that hide state or create mode confusion.
7. For agentic work, define visible status, result, intervention, cancellation, and retry behavior outside transient chat.
8. Hand off mobile, motion, accessibility, or performance concerns.

## Output Format

```md
## Interaction Flow
- Entry:
- Primary action:
- Feedback:
- Recovery:
- Exit:

## State Behavior
- Loading:
- Error:
- Undo:
- Disabled:
- Agent status and intervention:

## Applied Rules And Patterns
- Rule:
- Pattern:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Action feedback is immediate and quiet.
- Required input is minimal.
- Recovery path is clear.
- Context remains visible where possible.
- State changes do not create layout jumps.
- Interaction choices map to existing rules and patterns.
- Delegated work remains observable and recoverable when agentic behavior applies.

## Related Rules

- `RULE-00002` / `PRD-002` Low-Friction Capture Before Organization
- `RULE-00005` / `UX-001` Thumb-Zone Primary Actions
- `RULE-00006` / `UX-002` Progressively Disclose Power
- `RULE-00007` / `UX-003` Preserve Context During Inspection
- `RULE-00016` / `UX-005` Expose Agent Work And Intervention

## Related Patterns

- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00003` / `PAT-003` Mobile Primary Action
- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00005` / `PAT-005` Context-Preserving Preview

## Handoff To Other Skills

- Use `motion-designer` when movement must preserve orientation.
- Use `mobile-ux-expert` for touch reach and narrow viewport behavior.
- Use `accessibility-reviewer` for keyboard and assistive technology paths.
- Use `performance-reviewer` when latency affects feedback.
