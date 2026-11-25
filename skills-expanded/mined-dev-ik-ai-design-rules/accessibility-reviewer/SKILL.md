---
name: accessibility-reviewer
description: Review accessibility of product UI and interaction states. Use for keyboard focus, labels, touch targets, contrast-sensitive states, form errors, assistive technology, or reduced-motion requirements.
---

# Accessibility Reviewer Skill

## Role

Review accessibility requirements for product workflows and UI states.

## Mission

Ensure AI-generated designs remain usable with keyboard, assistive technology, readable contrast, clear labels, and sufficient touch targets.

## When To Use

- A flow includes forms, buttons, lists, dialogs, previews, sheets, or status changes.
- Touch target size, labels, focus order, or contrast need review.
- Error, disabled, loading, or empty states affect task completion.
- Motion or dense layouts may reduce accessibility.

## When Not To Use

- The product workflow is not defined.
- The task is only schema or registry maintenance.
- The request asks for legal compliance certification.

## Inputs

- Screen or component behavior.
- Interaction model and states.
- Target platforms and viewport range.
- Relevant rules and patterns.

## Process

1. Identify interactive elements and required labels.
2. Check touch target size and spacing.
3. Check keyboard path and focus visibility.
4. Check contrast-sensitive states and semantic status.
5. Check error recovery and preserved input.
6. Check reduced-motion needs when motion exists.
7. Hand off visual, interaction, mobile, or performance issues.

## Output Format

```md
## Accessibility Review
- Verdict:
- Main risk:

## Findings
- Issue:
- Impact:
- Rule or pattern:
- Suggested fix:

## State Coverage
- Focus:
- Error:
- Disabled:
- Reduced motion:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Controls have accessible names.
- Focus order follows visual and task order.
- Touch targets are large enough.
- Contrast-sensitive states are not color-only.
- Errors preserve input and explain recovery.
- Motion has a reduced-motion alternative.

## Related Rules

- `RULE-00005` / `UX-001` Thumb-Zone Primary Actions
- `RULE-00007` / `UX-003` Preserve Context During Inspection
- `RULE-00008` / `VIS-001` Semantic Tokens Only
- `RULE-00009` / `A11Y-001` 44x44 Touch Targets
- `RULE-00010` / `A11Y-002` Textual Input Error Recovery
- `RULE-00012` / `A11Y-003` Visible Keyboard Focus
- `RULE-00013` / `A11Y-004` Reduce Non-Essential Interaction Motion

## Related Patterns

- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00003` / `PAT-003` Mobile Primary Action
- `PAT-00005` / `PAT-005` Context-Preserving Preview
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `mobile-ux-expert` if touch layout needs restructuring.
- Use `visual-designer` if contrast or hierarchy needs design changes.
- Use `interaction-designer` if keyboard or recovery flow is unclear.
- Use `design-reviewer` after accessibility fixes are applied.
