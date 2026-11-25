---
name: verification-and-reliability
description: "Use first when the user asks for tests, correctness, high reliability, static reasoning, proof, or safety evidence."
---

# Verification and Reliability

Use first when the user asks for tests, correctness, high reliability, static reasoning, proof, or safety evidence. This is a router skill: use it to select the
smallest relevant leaf skill, then read that leaf skill before doing the work.

## Route First

Choose the proof style before changing code: test-first behavior discovery, specification-driven prevention, or sound approximation.

1. Restate the user's task as one concrete force or uncertainty.
2. Choose the first route that directly names that force.
3. Read the selected linked leaf `SKILL.md` before implementing, reviewing, or advising.
4. Load a second leaf only when the task has two independent forces that both affect the outcome.
5. If no route fits, continue without a leaf skill and say the category did not match.

## Routes

| Leaf Skill | Use When |
| --- | --- |
| [`test-driven-development`](../../../../libraries/theory-skills/test-driven-development/SKILL.md) | Use when the next observable behavior can be captured by a failing test before implementation. |
| [`cleanroom-software-engineering`](../../../../libraries/theory-skills/cleanroom-software-engineering/SKILL.md) | Use when reliability risk requires precise specification, defect prevention, and small verifiable increments. |
| [`abstract-interpretation`](../../../../libraries/theory-skills/abstract-interpretation/SKILL.md) | Use when many possible executions must be reasoned about with a sound over-approximation. |
| [`design-by-contract`](../../../../libraries/theory-skills/design-by-contract/SKILL.md) | Use when reliability depends on explicit preconditions, postconditions, or invariants at a boundary. |
| [`stepwise-refinement`](../../../../libraries/theory-skills/stepwise-refinement/SKILL.md) | Use when proof depends on preserving a high-level specification through implementation steps. |

## Avoid

- If the behavior is still ambiguous, route to ambiguity-and-learning before writing tests.
- If the issue is primarily human workflow evidence, route to workflow-and-operations.

## Prompting Pattern

Before loading a leaf, answer briefly:

- **Category force:** What makes this task belong here?
- **Chosen route:** Which leaf skill most directly matches the force?
- **Why not others:** Which nearby route was rejected and why?

Then load the chosen leaf skill and follow its workflow. Do not blend every
nearby theory into the task; route narrowly and let evidence pull in more context only when needed.
