---
name: workflow-and-operations
description: "Use first for work shaped by users, tools, procedures, runtime evidence, operational artifacts, interfaces, or organizational workflows."
---

# Workflow and Operations

Use first for work shaped by users, tools, procedures, runtime evidence, operational artifacts, interfaces, or organizational workflows. This is a router skill: use it to select the
smallest relevant leaf skill, then read that leaf skill before doing the work.

## Route First

Map the work system before choosing a leaf: activity contradiction, distributed representation, human notation, or changing situation.

1. Restate the user's task as one concrete force or uncertainty.
2. Choose the first route that directly names that force.
3. Read the selected linked leaf `SKILL.md` before implementing, reviewing, or advising.
4. Load a second leaf only when the task has two independent forces that both affect the outcome.
5. If no route fits, continue without a leaf skill and say the category did not match.

## Routes

| Leaf Skill | Use When |
| --- | --- |
| [`activity-theory`](../../../../libraries/theory-skills/activity-theory/SKILL.md) | Use when tools, rules, roles, community, division of labor, and outcome interact in a workflow. |
| [`distributed-cognition`](../../../../libraries/theory-skills/distributed-cognition/SKILL.md) | Use when knowledge is spread across code, logs, dashboards, runbooks, queues, schemas, people, or procedures. |
| [`cognitive-dimensions`](../../../../libraries/theory-skills/cognitive-dimensions/SKILL.md) | Use when a human-facing API, DSL, config, prompt, schema, CLI, or code notation must be easier to read or change. |
| [`situated-action`](../../../../libraries/theory-skills/situated-action/SKILL.md) | Use when a plan must adapt to current files, tests, logs, user feedback, or runtime contingencies. |
| [`conways-law`](../../../../libraries/theory-skills/conways-law/SKILL.md) | Use when operational behavior is constrained by ownership or communication paths. |

## Avoid

- If the work is a narrow code invariant, route to code-change-core.
- If repeated failure requires changing assumptions or policies, route to ambiguity-and-learning.

## Prompting Pattern

Before loading a leaf, answer briefly:

- **Category force:** What makes this task belong here?
- **Chosen route:** Which leaf skill most directly matches the force?
- **Why not others:** Which nearby route was rejected and why?

Then load the chosen leaf skill and follow its workflow. Do not blend every
nearby theory into the task; route narrowly and let evidence pull in more context only when needed.
