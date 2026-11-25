---
name: improve-ui
description: Audit one selected Figma Design surface or Figma Make prototype against visible design evidence, connected libraries, local styles, variables, components, sibling screens, and user task goals, then return up to three supported UI improvement findings with clear evidence and proposed changes. Do not use for design-system conformance audits (follow-ds-guidelines), Nielsen-heuristic evaluations (heuristic-evaluation), or cross-screen consistency checks (visual-consistency-check).
---

# Improve UI

Use this skill to identify the highest-leverage UI improvements for one coherent product surface.

This is an evidence-based audit. Prefer no finding to an unsupported finding.

Do not redesign immediately. Report findings first unless the user already selected a specific improvement to apply.

Use `follow-ds-guidelines` for design-system conformance audits, `heuristic-evaluation` for Nielsen-method usability evaluations, and `visual-consistency-check` for cross-screen consistency checks.

## Output Mode

Choose the output mode from the user's request:

- If the user asks to `audit`, `find improvements`, or `review`, return findings only.
- If the user asks to `improve`, `fix`, or `apply`, identify the finding being addressed, make only that change, and summarize it.
- If the user asks for broad improvement, return the findings first and ask which one to apply.
- If no supported finding exists, say so instead of making cosmetic changes.

## Scope

Honor the user's selected target.

If the request is broad, narrow to one coherent surface:

- one screen
- one flow
- one component set
- one Figma Make prototype area
- one family of sibling frames that support the same task

State the selected scope before auditing.

## Evidence Sources

Use only evidence available in the current context:

- selected Figma frames, layers, components, or variants
- connected libraries, components, variables, styles, or tokens
- sibling screens or existing product patterns
- attached screenshots, briefs, or reference files
- Figma Make app behavior visible in the current project
- user-stated goals, constraints, or non-goals

Do not infer hidden code, analytics, design-system rules, or product strategy unless provided.

## Reconstruct The Local System

Before findings, summarize:

```markdown
## Design Language
- Audited surface:
- Available design sources:
- Repeated local patterns:
- Connected system elements:
- Explicit exceptions:
```

Write `None visible` when a category is unavailable.

Absence of documentation is not a finding.

## Finding Gate

A candidate becomes a finding only when all three are present:

- `Contract`: A visible pattern, stated requirement, connected system element, sibling-screen convention, or direct contradiction establishes what should happen.
- `Evidence`: The selected target visibly violates or weakens that contract.
- `Correction`: One concrete change can be made without inventing product intent.

Reject candidates when:

- the issue is only personal taste
- the correction requires a product decision the user has not made
- evidence supports multiple equally plausible corrections
- the change primarily concerns hidden implementation, performance, metadata, or code architecture
- the target is outside the selected scope

## Findings Report

Return at most three findings.

```markdown
## Design Language
- Audited surface:
- Available design sources:
- Repeated local patterns:
- Connected system elements:
- Explicit exceptions:

## Findings
| # | Problem | Evidence | Proposed change | Scope | Confidence |
| --- | --- | --- | --- | --- | --- |

## Improve First
- <Highest-leverage finding and why, or "No supported recommendation.">

## Next Step
- Ask which finding to apply, unless the user already chose one.
```

If no finding survives, write:

```markdown
## Findings
No supported findings were found.

## Improve First
No supported recommendation.
```

## Applying A Selected Finding

When the user selects a finding to improve:

- make only the selected improvement
- preserve unrelated frames, copy, layout, variants, and components
- use existing styles, variables, and components when available
- state any uncertainty before changing product intent
- verify the changed target against the original evidence

## Quality Check

Before finalizing:

- Every finding has contract, evidence, and correction.
- Findings are limited to the selected scope.
- Proposed changes are deterministic and actionable in Figma.
- No finding depends on unavailable code or scripts.
- Figma Design and Figma Make concerns are separated.
- The report distinguishes visible evidence from assumptions.
