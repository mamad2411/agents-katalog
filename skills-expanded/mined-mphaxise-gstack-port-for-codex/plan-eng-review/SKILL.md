---
name: plan-eng-review
description: Engineering-manager style plan review for Codex. Use when the product direction is chosen and the user needs architecture, test, and execution rigor before coding.
---

# Plan Eng Review

Use this skill after the product framing is mostly settled and the team needs a practical execution review before implementation.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Goals

- stress-test the implementation plan before code is written
- find the smallest safe set of changes that achieves the chosen outcome
- surface edge cases, test gaps, and performance risks
- produce a plan that a strong engineer can implement without hidden ambiguity

## Mode Selection

Choose one mode and state it explicitly:

- `SCOPE REDUCTION`: use when the plan is overbuilt or the user wants the thinnest valuable version
- `BIG CHANGE`: use for broad or architectural plans that need a full review section by section
- `SMALL CHANGE`: use for localized plans where one combined pass is enough

If mode choice would materially change the recommendation and the right answer is unclear, ask one concise question. Otherwise choose the best mode and keep going.

Read `references/mode-cheatsheet.md` for the defaults.

## Workflow

1. Read only the materials needed to understand the plan and repo context.
2. Run a Step 0 scope challenge before reviewing details.
3. Review the plan using the sections in `references/review-sections.md`.
4. Produce the final review using `references/output-template.md`.

## Guardrails

- Do not start implementation unless the user explicitly pivots from planning to coding.
- Once the mode is chosen, do not silently reduce or expand scope.
- Use ASCII diagrams for non-trivial flows.
- Always include `Not in scope`, `What already exists`, and concrete next actions.

