---
name: design-change-diff
description: "Explains verified changes between two supplied or accessible design states in language useful to product and engineering teams. Use when before-and-after frames, versions, screenshots, or a documented change list are available."
---

# Design Change Diff

## Capability Mode

`Compare available evidence`. Do not assume access to version history, branch history, or an automatic visual diff.

## Workflow

1. Name the two states being compared and the evidence available for each.
2. Identify verified additions, removals, and modifications.
3. Group changes by user flow, layout, component, content, token, and behavior.
4. Explain likely implementation or user impact, labeling inference clearly.
5. Call out breaking changes, migration needs, unresolved questions, and inaccessible areas.
6. Keep cosmetic noise separate from meaningful product changes.

## Guardrails

- Do not describe unobserved areas as unchanged.
- Do not invent rationale, dates, authors, or merge status.
- Distinguish direct evidence, supplied rationale, and inference.
- State when the comparison is partial or manually assembled.

## Output Contract

Return the compared states, verified change summary, detailed changes by area, impact, risks, unresolved questions, and coverage limitations.
