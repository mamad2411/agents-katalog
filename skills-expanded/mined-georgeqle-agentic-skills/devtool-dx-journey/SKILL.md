---
name: devtool-dx-journey
description: Use only for developer-facing products; analyze install, quickstart, first success, debugging, and production adoption journeys
type: analysis
version: v0.4
required_conventions: [alignment-page]
context_intake: artifact_only
visual_tier: visual
---

# Devtool DX Journey

Invoke as `$devtool-dx-journey`.

Map the developer experience from discovery to production use.

## Output

Write or update `research/devtool-dx-journey.md` with install, quickstart, first success, error recovery, production adoption, team rollout, and retention journeys. In the final response, include `Recommended next skill: <command>` using the `## Next-Skill Routing` rules below.

## Next-Step Routing

After writing the artifact, recommend the next contextual skill:

1. If `tasks/todo.md` has an unchecked devtool item in `## Priority Documentation Todo`, recommend the first unchecked devtool command from that queue.
2. Otherwise, follow the default devtool sequence: `$devtool-adoption` after this skill.
3. If the sequence is ambiguous or multiple devtool artifacts are stale: check `.agents/project.json.enabled_packs` for `research-admin` — if `research-admin` is not enabled, recommend `npx skillpacks install research-admin` from the project shell; if `research-admin` is enabled, recommend `$research-roadmap` — to rebuild the ordered documentation queue.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/devtool-dx-journey-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
