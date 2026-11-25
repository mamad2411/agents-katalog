---
name: "naming-and-abstraction-reviewer"
pack: "oop-code-structure-pack"
purpose: "Review whether names, interfaces, and abstractions communicate intent cleanly and match the underlying domain."
inputs: ["type names", "method names", "field names", "domain vocabulary", "usage examples"]
outputs: ["naming issues", "abstraction mismatches", "domain-language notes", "rename/refactor suggestions", "recommended changes"]
handoffs: ["class-responsibility-checker", "method-cohesion-checker", "visibility-modifier-reviewer"]
---
# naming-and-abstraction-reviewer

## Purpose
Review whether names, interfaces, and abstractions communicate intent cleanly and match the underlying domain.

## Trigger this skill when
- Names do not match domain intent.
- Interfaces or classes feel too generic or misleading.
- The abstraction layer is unclear to readers.

## Expected inputs
- type names
- method names
- field names
- domain vocabulary
- usage examples

## Deliverables
- naming issues
- abstraction mismatches
- domain-language notes
- rename/refactor suggestions
- recommended changes

## Operating procedure
1. Identify the object-oriented concern this skill is meant to assess.
2. Separate facts from inferred design intent.
3. Review the current structure against OOP fundamentals: responsibility, invariants, ownership, exposure, abstraction, and lifecycle where relevant.
4. Surface concrete risks, tradeoffs, and improvement options.
5. Prefer minimal structural change that materially improves clarity or safety.
6. Hand off to the next most relevant skill if the issue is broader than this skill alone can resolve.

## Quality gates
- Findings are tied to concrete code structure or stated design intent.
- Recommendations explain *why*, not just *what*.
- Tradeoffs are stated when multiple designs could work.
- Output avoids style nitpicks unless they affect abstraction or maintainability.

## Handoff targets
- class-responsibility-checker
- method-cohesion-checker
- visibility-modifier-reviewer

## Output style
- Be explicit about uncertainty.
- Prefer short, evidence-based findings over long vague critique.
- Distinguish design defects from mere preference.
- End with recommended next actions.

## Failure modes to avoid
- Do not invent framework constraints without evidence.
- Do not recommend sweeping refactors without naming the benefit.
- Do not confuse naming/style issues with true design problems unless they affect abstraction.
- Do not force inheritance, immutability, or statics as ideology.

## Minimum output skeleton
```md
## Summary
## Findings
## Risks
## Recommendations
## Tradeoffs
## Recommended next skill
```
