---
name: design-judgment-scorecard
description: Evaluate a product design against its user task, product intent, evidence, and quality bar, producing explainable findings rather than vague taste. Use for comparing or reviewing flows, prototypes, and implemented interfaces. Do not claim complete product evaluation when context is missing.
---

# Design Judgment Scorecard

Turn “this feels wrong” into evidence, impact, tradeoffs, and a next decision while preserving human ownership of ambiguous taste.

## Review

1. Confirm the artifact, intended user, critical task, product decision, and known constraints.
2. If the goal or task is missing, limit the review to observable craft and accessibility issues and state the limitation.
3. Select only relevant dimensions: intent alignment, conceptual coherence, hierarchy, interaction clarity, state coverage, content, accessibility, visual craft, trust, and distinctiveness.
4. For each finding, write `evidence → impact → recommendation → confidence → verification`.
5. When comparison helps, use 0–3 behavioral anchors within the current brief. Do not calculate a context-free total score.
6. Separate automatic fixes, human tradeoffs, and questions requiring user evidence.
7. Recommend at most three next actions ranked by failure risk and learning value.

## Output

```markdown
## Decision under review
## Context and missing evidence
## Scorecard
| Dimension | 0–3 | Evidence | Impact | Confidence |
## Priority findings
## Human decisions required
## Next validation
```

## Boundaries

- Do not turn personal style preference into a universal UX law.
- Avoid labels such as “premium” or “clean” without observable criteria.
- Visual polish does not repair an incorrect conceptual model.
- Accessibility checks do not replace usability evidence.
- Record what should remain unchanged so revision does not erase confirmed intent.
