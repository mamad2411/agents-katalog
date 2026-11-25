---
name: plan-ceo-review
description: Founder-style plan review for Codex. Use when a user wants to pressure-test a product or feature plan before implementation.
---

# Plan CEO Review

Use this skill when the task is still in planning or discovery and the highest-leverage move is to rethink the problem before coding.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Goals

- challenge the stated request, not just polish it
- identify the real user outcome behind the ask
- find leverage in what already exists
- surface risks, edge cases, and explicit "not in scope" decisions
- leave the user with a sharper next move

## Mode Selection

Pick exactly one mode and make the choice explicit in the response:

- `SCOPE EXPANSION`: default for greenfield ideas or when the user wants the ambitious version
- `HOLD SCOPE`: default for bug fixes, refactors, or plans whose scope is already accepted
- `SCOPE REDUCTION`: default when the user wants the thinnest useful MVP

Decision rule:

- If one mode is clearly right, choose it and confirm the choice plainly: "I'm using `MODE` because ..."
- If the mode is not clear enough and the choice would materially change the advice, ask one concise scope-choice question and wait.

Do not hedge between modes or silently switch later.

For the detailed defaults, read `references/mode-cheatsheet.md`.

## Workflow

1. Read only the materials needed to understand the plan, repo, and relevant constraints.
2. Identify the actual outcome the user wants, not just the literal feature request.
3. Choose a mode. If it is clear, confirm the choice and any key assumption explicitly. If it is not clear, ask one concise question and wait.
4. Map existing leverage before suggesting new work.
5. In `SCOPE EXPANSION`, say the bigger opportunity plainly and review the expanded plan directly.
6. Review the plan using the selected mode.
7. Produce a structured output using `references/output-template.md`.

## Review Standard

- Be opinionated and concrete.
- Name the biggest risks, not every imaginable one.
- Prefer explicit tradeoffs over fuzzy advice.
- Keep the plan realistic for the current repo and team context.
- Call out anything that should be deferred in a `Not in scope` section.

## Guardrails

- Do not start implementation unless the user explicitly pivots from planning to coding.
- Ask at most one concise question at a time, and only when a real ambiguity blocks a good recommendation.
- When you choose a mode without asking, state the assumption plainly so the user can correct it quickly.
- In `SCOPE EXPANSION`, state the bolder framing directly and defend it with concrete tradeoffs.
- If a better framing exists, say so directly.
- If the current plan is good, say that too and focus on the highest-value refinements.

## Outputs

Always include:

- selected mode and why
- problem framing
- what already exists
- recommended plan
- risks and failure modes
- not in scope
- next 1-3 actions

For the full structure and tables, read `references/output-template.md`.
