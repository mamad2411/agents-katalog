---
name: game-prototype-test
description: Use only for video game projects; design playable prototype tests and success criteria for fun, clarity, and replay
type: planning
version: v0.1
context_intake: scoped
visual_tier: prototype
---

# Game Prototype Test

Invoke as `$game-prototype-test`.

Design the smallest playable test that can prove or disprove the game's core fun.

## Output

Write or update `research/game-prototype-test.md` with prototype scope, test questions, playtest script, observation checklist, success criteria, and cut/keep/amplify decisions.

## Next-Step Routing

After writing the artifact, recommend the next contextual game-pack skill in the final response as `Recommended next skill: <command>`.

Default recommendation: `$game-playtest-metrics`.

If prototype, playtest, or market evidence invalidates an upstream assumption, route back to the earliest affected artifact (`$game-audience`, `$game-fantasy`, `$game-genre-map`, or `$game-comparables`) and explain the evidence. Otherwise, follow the default game sequence:

`$game-audience` -> `$game-fantasy` -> `$game-genre-map` -> `$game-comparables` -> `$game-core-loop` -> `$game-prototype-test` -> `$game-playtest-metrics` -> `$game-store-page-test` -> `$game-launch` -> `$game-roadmap`

If the next artifact already exists and is current, recommend `$game-workflow` to identify the first missing or stale game-pack artifact.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/game-prototype-test-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

