---
name: big-model-smell
description: Simplify an oversized prompt, plan, workflow, document, system, or build when its complexity, context, automation, or model cost is not earning its keep.
---

# Big Model Smell

Find where complexity, context, automation, or model capability exceeds the actual job, then simplify without losing the required outcome.

## Job contract

- Owns: simplification of one supplied artifact, workflow, prompt, system, or plan.
- Does not own: retrospective analysis across recent sessions (`operator-audit`).
- Finished deliverable: complexity diagnosis, smallest viable design, migration steps, and verification criteria.

## Smells to inspect

- One giant prompt trying to perform unrelated jobs.
- A frontier model used for deterministic extraction or formatting.
- Too many agents, tools, files, approval steps, or moving parts.
- Context loaded “just in case” rather than for a decision.
- An automation that costs more to maintain than the task costs to do.
- A document or system no operator can confidently change.

## Workflow

1. State the outcome and non-negotiable constraints.
2. Map every component to the outcome it supports.
3. Mark components as essential, useful, unproven, duplicate, or decorative.
4. Identify the cheapest adequate level for each step: rule, template, small model, large model, human judgment, or automation.
5. Design the smallest version that preserves safety and quality.
6. Give a reversible migration order and a test that proves nothing important was lost.

## Output

```markdown
# Complexity Review

## Required Outcome
[What must remain true]

## Big-Model Smells
[Evidence and cost of each]

## Keep, Simplify, Remove, Test
[Decision table]

## Smaller Working Design
[New flow]

## Safe Migration
[Reversible sequence]

## Verification
[Tests and stop conditions]
```

## Guardrails

- Do not simplify away approval, privacy, security, accessibility, or recovery controls.
- Do not assume a cheaper model is adequate; define a representative test.
- Never modify or delete the original artifact without explicit approval.
