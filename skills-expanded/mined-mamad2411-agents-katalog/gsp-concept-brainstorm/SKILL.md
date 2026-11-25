---
name: gsp-concept-brainstorm
description: "Use when a game idea is still vague and needs pillars, verbs, and an acceptance bar before implementation."
---

# Game Concept Brainstorm

## Goal
Lock the game fantasy before architecture or implementation.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present concept brainstorm and requirements in conversation.
- **minimal** or **full**: write `docs/game-studio/concept-brainstorm.md` and `docs/game-studio/requirements.md`.

Use `../../shared/templates/concept-brainstorm.md`.

## Workflow
1. Restate the player fantasy in one sentence.
2. Lock the primary verb, the reward loop, and the first 30-second promise.
3. Lock the game shape before coding: camera / view model, movement grammar, obstacle or encounter grammar, fail / retry rhythm, and visual anchor.
4. Define 3-4 design pillars.
5. Separate must-haves from experiments.
6. Ask enough high-value questions to remove shape ambiguity. Good question types: subtype, references, control grammar, failure rhythm, visual anchor, and “what must beat baseline.”
7. For benchmark or one-prompt builds, spend more tokens here than feels comfortable if ambiguity remains.
8. Feed the result into `gsp-requirements-brainstorm`, `gsp-scope-profile`, and `gsp-ux-flow-designer`.

## Important
If the prompt uses an archetype word that can imply multiple valid game forms, do not silently choose one and move on.
Examples: `runner`, `shooter`, `breakout`.
Write the chosen interpretation explicitly so downstream skills inherit a locked shape instead of improvising.
Do not optimize for asking fewer questions. Optimize for asking the fewest questions that still fully lock the concept.
