---
name: ambiguity-and-learning
description: "Use first for ambiguous failures, messy project context, surprising results, repeated failures, postmortems, or contested product and architecture framing."
---

# Ambiguity and Learning

Use first for ambiguous failures, messy project context, surprising results, repeated failures, postmortems, or contested product and architecture framing. This is a router skill: use it to select the
smallest relevant leaf skill, then read that leaf skill before doing the work.

## Route First

Do not pick a design leaf until the uncertainty shape is clear: cues, surprise, repeated governing assumption, or stakeholder conflict.

1. Restate the user's task as one concrete force or uncertainty.
2. Choose the first route that directly names that force.
3. Read the selected linked leaf `SKILL.md` before implementing, reviewing, or advising.
4. Load a second leaf only when the task has two independent forces that both affect the outcome.
5. If no route fits, continue without a leaf skill and say the category did not match.

## Routes

| Leaf Skill | Use When |
| --- | --- |
| [`sensemaking`](../../../../libraries/theory-skills/sensemaking/SKILL.md) | Use when logs, errors, reports, or legacy context need a plausible working story before action. |
| [`reflective-practice`](../../../../libraries/theory-skills/reflective-practice/SKILL.md) | Use when a surprising result during work should reframe the next move. |
| [`double-loop-learning`](../../../../libraries/theory-skills/double-loop-learning/SKILL.md) | Use when repeated failures point to a bad assumption, default, policy, metric, or governing variable. |
| [`wicked-problems`](../../../../libraries/theory-skills/wicked-problems/SKILL.md) | Use when problem definition, stakeholder criteria, or product/architecture tradeoffs are contested. |
| [`situated-action`](../../../../libraries/theory-skills/situated-action/SKILL.md) | Use when new local evidence invalidates the current plan and the next step must adapt. |

## Avoid

- If the problem is already well-bounded and technical, route to the matching implementation category.
- If the next action would require a product, legal, security, or organizational decision, stop and gather context.

## Prompting Pattern

Before loading a leaf, answer briefly:

- **Category force:** What makes this task belong here?
- **Chosen route:** Which leaf skill most directly matches the force?
- **Why not others:** Which nearby route was rejected and why?

Then load the chosen leaf skill and follow its workflow. Do not blend every
nearby theory into the task; route narrowly and let evidence pull in more context only when needed.
