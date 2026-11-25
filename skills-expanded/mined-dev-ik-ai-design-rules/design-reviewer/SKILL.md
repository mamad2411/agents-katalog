---
name: design-reviewer
description: Run final design QA for product proposals, prototypes, or implemented UI. Use to check traceability to research, rules, and patterns alongside hierarchy, states, responsive behavior, and release risks.
---

# Design Reviewer Skill

## Role

Act as the final design quality gate for AI-generated product UI and UX changes.

## Mission

Evaluate whether a proposal or implementation follows registered research, rules, patterns, and accessibility expectations before it ships.

## When To Use

- A screen, prototype, prompt output, or pull request needs design QA.
- An agent must prove design decisions are traceable.
- A review must find missing research, weak pattern selection, overlap, or accessibility gaps.
- A reference project needs validation against AI Design Context.

## When Not To Use

- The task is initial product direction.
- The task has no user-facing behavior.
- The request asks to create new rules or patterns.

## Inputs

- Screen, workflow, diff, prompt output, or reference project.
- Claimed rules and patterns.
- Generated indexes.
- Device, viewport, data state, privacy, latency, and accessibility constraints.

## Process

1. Identify the user goal and primary action.
2. Check whether claimed rules apply.
3. Check whether selected patterns match their purpose and boundaries.
4. Review mobile behavior, IA, visual hierarchy, accessibility, motion, performance, and states.
5. Identify missing upstream evidence instead of inventing guidance.
6. Produce severity-ordered findings.
7. Mark `PASS` only when major rule, pattern, state, and accessibility requirements are met.
8. Hand off specific issues to specialist skills.

## Output Format

```md
## Verdict
PASS or NEEDS WORK

## Findings
- Severity:
- File or screen:
- Issue:
- Rule or pattern:
- Suggested patch:

## Coverage
- Rules checked:
- Patterns checked:
- Missing evidence:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Findings are specific and actionable.
- Every finding names a rule, pattern, or missing layer.
- Review covers mobile, accessibility, state behavior, and traceability.
- PASS means another agent can follow the reasoning.
- NEEDS WORK lists exact files or surfaces to fix.

## Related Rules

- `RULE-00001` / `PRD-001` Daily Actions First
- `RULE-00002` / `PRD-002` Low-Friction Capture Before Organization
- `RULE-00003` / `IA-001` One Stable Home Surface
- `RULE-00004` / `IA-002` Define The Object Model Before Screens
- `RULE-00005` / `UX-001` Thumb-Zone Primary Actions
- `RULE-00006` / `UX-002` Progressively Disclose Power
- `RULE-00007` / `UX-003` Preserve Context During Inspection
- `RULE-00008` / `VIS-001` Semantic Tokens Only
- `RULE-00009` / `A11Y-001` 44x44 Touch Targets
- `RULE-00010` / `A11Y-002` Textual Error Recovery
- `RULE-00011` / `PERF-001` Reserve Space For Async Content
- `RULE-00012` / `A11Y-003` Visible Keyboard Focus
- `RULE-00013` / `A11Y-004` Reduce Non-Essential Interaction Motion

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00002` / `PAT-002` Quick Capture
- `PAT-00003` / `PAT-003` Mobile Primary Action
- `PAT-00004` / `PAT-004` Progressive Detail
- `PAT-00005` / `PAT-005` Context-Preserving Preview
- `PAT-00006` / `PAT-006` Object Status List

## Related Checklist And Prompt

- `CHECK-00001` / `CHECK-DESIGN-QA` Design QA Checklist
- `PROMPT-00005` / `PROMPT-DESIGN-EVIDENCE-REVIEW` Design Evidence Review Prompt

## Handoff To Other Skills

- Use `ux-reviewer` for journey and usability issues.
- Use `accessibility-reviewer` for accessibility failures.
- Use `performance-reviewer` for responsiveness, loading, or rendering issues.
- Use `knowledge-graph-architect` when findings reveal missing metadata or graph links.
