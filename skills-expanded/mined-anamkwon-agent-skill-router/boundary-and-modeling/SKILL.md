---
name: boundary-and-modeling
description: "Use first for API boundaries, module ownership, domain modeling, contracts, architecture seams, and recurring design structures."
---

# Boundary and Modeling

Use first for API boundaries, module ownership, domain modeling, contracts, architecture seams, and recurring design structures. This is a router skill: use it to select the
smallest relevant leaf skill, then read that leaf skill before doing the work.

## Route First

Identify what kind of boundary is under pressure: domain meaning, volatile decision, caller contract, ownership seam, or recurring design force.

1. Restate the user's task as one concrete force or uncertainty.
2. Choose the first route that directly names that force.
3. Read the selected linked leaf `SKILL.md` before implementing, reviewing, or advising.
4. Load a second leaf only when the task has two independent forces that both affect the outcome.
5. If no route fits, continue without a leaf skill and say the category did not match.

## Routes

| Leaf Skill | Use When |
| --- | --- |
| [`domain-driven-design`](../../../../libraries/theory-skills/domain-driven-design/SKILL.md) | Use when business/domain language, bounded contexts, aggregates, or invariants should shape the model. |
| [`information-hiding`](../../../../libraries/theory-skills/information-hiding/SKILL.md) | Use when a volatile design decision should be hidden behind a stable interface. |
| [`design-by-contract`](../../../../libraries/theory-skills/design-by-contract/SKILL.md) | Use when caller obligations, provider guarantees, and invariants must be explicit at a boundary. |
| [`conways-law`](../../../../libraries/theory-skills/conways-law/SKILL.md) | Use when architecture should match ownership, team communication, review, deployment, or support paths. |
| [`design-patterns`](../../../../libraries/theory-skills/design-patterns/SKILL.md) | Use when a known recurring design solution may fit current forces better than a simpler structure. |

## Avoid

- If the task is just a bounded code edit with no boundary question, route to code-change-core.
- If stakeholders disagree about the problem frame, route to ambiguity-and-learning first.

## Prompting Pattern

Before loading a leaf, answer briefly:

- **Category force:** What makes this task belong here?
- **Chosen route:** Which leaf skill most directly matches the force?
- **Why not others:** Which nearby route was rejected and why?

Then load the chosen leaf skill and follow its workflow. Do not blend every
nearby theory into the task; route narrowly and let evidence pull in more context only when needed.
