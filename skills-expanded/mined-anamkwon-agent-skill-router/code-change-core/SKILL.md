---
name: code-change-core
description: "Use first for bounded code edits, refactors, implementation, simplification, control-flow cleanup, or maintainer clarity before choosing a more specific theory skill."
---

# Code Change Core

Use first for bounded code edits, refactors, implementation, simplification, control-flow cleanup, or maintainer clarity before choosing a more specific theory skill. This is a router skill: use it to select the
smallest relevant leaf skill, then read that leaf skill before doing the work.

## Route First

Classify the code-change force first. Read exactly one primary leaf skill unless the task clearly spans two forces.

1. Restate the user's task as one concrete force or uncertainty.
2. Choose the first route that directly names that force.
3. Read the selected linked leaf `SKILL.md` before implementing, reviewing, or advising.
4. Load a second leaf only when the task has two independent forces that both affect the outcome.
5. If no route fits, continue without a leaf skill and say the category did not match.

## Routes

| Leaf Skill | Use When |
| --- | --- |
| [`programming-as-theory-building`](../../../../libraries/theory-skills/programming-as-theory-building/SKILL.md) | Default for non-trivial code changes where domain rules must map to code behavior. |
| [`essential-complexity`](../../../../libraries/theory-skills/essential-complexity/SKILL.md) | Use when simplification is requested and the risk is erasing real domain complexity. |
| [`structured-programming`](../../../../libraries/theory-skills/structured-programming/SKILL.md) | Use when the main problem is tangled branching, loops, exits, callbacks, or mutable control state. |
| [`stepwise-refinement`](../../../../libraries/theory-skills/stepwise-refinement/SKILL.md) | Use when implementing a feature or algorithm from a high-level specification in small refinements. |
| [`literate-programming`](../../../../libraries/theory-skills/literate-programming/SKILL.md) | Use when the main problem is maintainer understanding, examples, comments, or explanatory order. |

## Avoid

- If the dominant issue is API or module boundary ownership, route to boundary-and-modeling.
- If the dominant issue is tests, reliability, or proof, route to verification-and-reliability.

## Prompting Pattern

Before loading a leaf, answer briefly:

- **Category force:** What makes this task belong here?
- **Chosen route:** Which leaf skill most directly matches the force?
- **Why not others:** Which nearby route was rejected and why?

Then load the chosen leaf skill and follow its workflow. Do not blend every
nearby theory into the task; route narrowly and let evidence pull in more context only when needed.
