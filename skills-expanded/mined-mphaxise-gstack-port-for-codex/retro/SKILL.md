---
name: retro
description: Team-aware engineering retrospective for Codex. Use when the user wants a weekly or windowed retrospective based on git history.
---

# Retro

Use this skill to generate a retrospective from commit history, work patterns, and contribution trends.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Supported Inputs

- default retrospective window: `7d`
- explicit windows such as `24h`, `14d`, or `4w`
- compare mode: compare the current window against the prior equal-length window

## Workflow

1. Parse the time window.
2. Gather git history, file hotspots, commit timing, and contributor data.
3. Compute the metrics in `references/metrics-checklist.md`.
4. Produce the writeup using `references/output-template.md`.
5. If the repo uses retrospective history files, save a snapshot for later comparison.

## Output Goals

- show the overall team picture
- give the current user the deepest treatment
- identify the biggest ship, streaks, hotspots, and session patterns
- turn raw git activity into actionable coaching and momentum signals

## Guardrails

- Treat the current git user as "you" unless the repo clearly documents otherwise.
- Use Pacific time if the user or repo context expects it; otherwise state the timezone you used.
- Skip unavailable metrics instead of fabricating them.

