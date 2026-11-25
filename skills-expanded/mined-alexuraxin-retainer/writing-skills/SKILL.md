---
name: writing-skills
description: "The discipline of authoring SKILL.md: RED-GREEN, SDO (name and description for findability), token budget, model- vs user-invoked, authoring failure modes. Trigger words (RU+EN): написать скилл, SKILL.md, авторинг скилла, описание под находимость / write a skill, SKILL.md, skill authoring, description for findability."
disable-model-invocation: true
---

# Authoring skills

Retainer stamps out skills — the engine IS skills. A skill is valuable not for describing a
technique but for the agent taking **the same PROCESS every run** (the predictability root, donor
mattpocock/writing-great-skills). Not "one output" — one way to act. Two runs by one skill diverged
in behavior → the skill is underwritten.

Whether a skill is needed at all is [[complexity-budget]] on the skill itself (the deletion test:
remove it → what drifts). Here — once writing is decided, HOW to write it so it is found and runs
the same way.

## RED-GREEN-REFACTOR for skills (donor superpowers/writing-skills)

A skill is born as a test, not as an essay (deepens the "a technique, not a story" thesis from
`docs/SKILLS.md`).

- **RED** — see the failure WITHOUT the skill: where the agent actually errs on this task, not
  hypothetically. No observed failure — no skill (that is a `no-op`, below).
- **GREEN** — the minimal text closing exactly this failure. Not an encyclopedia of the topic.
- **REFACTOR** — close the loopholes: name explicitly every rationalization by which the agent would
  bypass the rule. **Match form to failure** — the form to the class of failure (a checklist / a
  table / a single ban), not a universal template.

RED-GREEN for FEATURES/code lives in [[task-cycle]]; here the same rhythm applied to skills.

## SDO — how a skill is found (donor superpowers)

A skill that did not activate does not exist. `name` and `description` are the only thing the model
sees BEFORE loading the body.

- **`name`** == the folder name, lowercase/hyphens, descriptive (`writing-skills`, not `helper`) —
  otherwise it will not load by the agentskills.io spec.
- **`description`** — TRIGGERS ("when to call"), not a retelling of the workflow: what it does AND on
  which words/tasks to activate. Keep within the ≤1024-character limit. Keyword coverage: include the
  words a task will be named by.

## Budget and information hierarchy (donor mattpocock)

- **Token budget** — the body <150 lines (our default ~<130). With a model-invoked description it
  hangs in the window every turn; a bloated skill is a tax on EVERY task, not only its own.
- **Links instead of duplicates** — a fact lives in one home, a copy rots out of sync. Three
  delivery levels: **in-skill step** (runs now) · **in-skill reference** (nearby, on hand) ·
  **external reference** (a context pointer to a file, loaded on demand — progressive disclosure).
- **Completion criterion** — a checkable/exhaustive "done" condition, otherwise premature completion
  (below).

## Invocation: model- vs user-invoked (donor mattpocock)

- **model-invoked** (auto by `description`) — a discipline firing on a task trigger (writing-skills,
  gate). The cost is context load: the description in the window every turn. Keep the description
  sharp.
- **user-invoked** (`/skill`) — the owner decides when to call it. The cost is cognitive load: one
  must remember the skill exists.
- A user-invoked set grew → a **router skill** (an index pointing to the right one). Do not breed
  dozens of user-invoked ones without an index.

## Leading words

A compact pretrained concept anchors behavior in a minimum of tokens: "tracer bullets", "tight
loop", "RED/GREEN", "the deletion test". A precise anchor word replaces a paragraph — the model
already knows the concept. Pick words that drag BEHAVIOR along, not only meaning.

## Authoring failure modes (donor mattpocock)

| Failure | What it is | Cure |
|---|---|---|
| **premature completion** | "done" without meeting the criterion | a checkable completion criterion |
| **duplication** | a fact copied from another skill | a `[[…]]` link, one home |
| **sediment** | layers of edits, the skill bloated | a periodic refactor, cut the dead |
| **sprawl** | one skill about everything at once | one skill = one class of failure |
| **no-op** | a rule the model follows anyway | delete — no RED, no skill |
| **negation** | "do not do X" → the model thinks about X | steer by the POSITIVE: what to do instead |

## Armor against rationalizations (donor superpowers)

The agent will bypass a discipline rule if a gap is left. Close each explicitly:

- **a rationalization table** — "the agent will say … → the answer …" right in the skill (as in
  [[receiving-review]], [[guardrails]]).
- **red flags** — bypass-signal phrases ("this time it's fine", "it's obvious anyway", "formally
  satisfied").
- **spirit vs letter** — name the rule's INTENT so letter-reading does not hollow it out.
- **a subagent test** — give a fresh subagent a task under the skill and watch whether it fails. A
  micro-test: the `description` alone → "when would you apply it?" (a findability check), before a
  full scenario. An authoring practice, not a gate.

## When NOT to apply

A one-off instruction for a specific task is not a skill (a skill is portable, a technique ≠ an
episode). A rule the model follows anyway is a `no-op`, do not write it. Writing/editing the code
itself — not here ([[task-cycle]], [[gate]]).

Related: [[complexity-budget]] (is a skill needed), [[task-cycle]] (RED-GREEN for code),
[[receiving-review]], [[guardrails]] (rationalization tables).
