---
name: design-crit
description: Critique selected Figma frames, components, flows, or Figma Make prototype output with structured design feedback, severity, visible evidence, user impact, and actionable next changes. Use when the user asks for UX critique, design review, conversion review, accessibility feedback, or quality assessment before making changes.
---

# Design Crit

Use this skill to review one coherent Figma target and return actionable design feedback.

The output is a critique report. Do not redesign the work unless the user explicitly asks for a follow-up revision.

## Output Mode

Choose the output mode from the user's request:

- If the user asks for `critique`, `review`, `audit`, or `feedback`, return the critique report only.
- If the user asks to `fix` or `improve` after critique, first identify the highest-leverage finding and ask for confirmation unless the edit is narrow and explicit.
- If the user asks for a score, include score only after findings and explain the basis.
- If the target is too broad, narrow to one selected frame, flow, component set, or Make prototype area.

## Target Rule

Resolve the target before critique:

- selected frame, section, component set, or flow in Figma Design
- current Figma Make app or prototype area
- attached screenshot or reference if no editable Figma context is available

If the target is too broad, choose one coherent surface and state the boundary.

Do not critique an entire product, brand, and design system in one pass.

## Evidence Standard

Base findings on visible design evidence, user task impact, and stated product constraints.

Separate:

- visible issues in the selected work
- assumptions about intended behavior or audience
- questions that need product clarification

Do not claim hidden implementation defects, analytics problems, or accessibility violations that cannot be inferred from the visible design or provided context.

## Critique Pass

Evaluate the target across these lenses:

- Purpose: Can a first-time user understand what this is and what to do next?
- Hierarchy: Is there a clear primary action, secondary action, and supporting content order?
- Layout: Are grouping, rhythm, density, alignment, and responsive expectations coherent?
- Content: Is copy specific, scannable, truthful, and matched to the user's decision?
- Components: Are states, variants, affordances, and repeated patterns consistent?
- Accessibility: Are contrast, touch targets, readable type, focus expectations, and non-color cues visibly considered?
- System fit: Does the work use available styles, variables, components, and brand conventions when provided?
- Make behavior: For Figma Make, are navigation, form handling, empty/error/loading states, and feedback paths clear?

## Severity

Assign each finding one severity:

- `P0`: Blocks the primary task or creates serious misunderstanding.
- `P1`: Likely harms comprehension, conversion, accessibility, or successful completion.
- `P2`: Noticeable quality issue with moderate user impact.
- `P3`: Minor polish issue or optional improvement.

Return at most five findings. Prefer fewer, stronger findings over exhaustive commentary.

## Report Format

```markdown
## Critique Scope
- Target:
- User/task assumption:
- Evidence available:
- Confidence:

## Findings
| Priority | Problem | Evidence | User impact | Recommended change |
| --- | --- | --- | --- | --- |

## Improve First
- <One highest-leverage change and why.>

## Questions or Assumptions
- <Only include if needed.>
```

## Recommendation Rules

- Recommend one concrete change per finding.
- Preserve the existing visual direction unless the issue is conceptual.
- Do not use generic advice such as "improve hierarchy" without naming what should move, change, shrink, grow, or be clarified.
- If a finding depends on a connected library, style, variable, or component, name the exact system element when visible or provided.
- If evidence is weak, downgrade confidence instead of overstating the critique.
- If no supported findings are visible, say so and name the remaining uncertainty.

## Quality Check

Before returning:

- Every finding has evidence.
- Every recommendation is actionable in Figma.
- Severity reflects user impact, not personal taste.
- Figma Design issues and Figma Make behavior issues are separated.
- The report stops after critique unless the user asked for edits.
