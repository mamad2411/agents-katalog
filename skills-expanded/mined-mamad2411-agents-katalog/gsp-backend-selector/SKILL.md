---
name: gsp-backend-selector
description: "Use when choosing a backend profile for a game based on capabilities, project state, and quality target."
---

# Game Backend Selector

## Goal
Select the backend profile that best serves the requested outcome.
Use `../../shared/reference/backend-profiles.md`.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present backend decisions in conversation.
- **minimal** or **full**: write `docs/game-studio/backend-decision.md`.

## Rules
- Prefer capabilities over brand or fandom.
- If the project already has a workable backend, bias toward it unless it is the blocker.
- Optimize for the chosen quality target, not just the fastest toy result.
- Respect project state: live iteration and greenfield do not deserve the same backend decision policy.

## Compare mode
Use compare mode only when:
- the backend choice is genuinely uncertain,
- or the user explicitly requests comparison.

When compare mode is used:
- warn that it will usually cost more tokens and time,
- keep the comparison narrow,
- define the winner criteria before exploring.

## Specialist follow-through
After choosing a backend profile, route to a concrete specialist when needed:
- `gsp-web-2d-specialist` for `web-2d-ui-first` or `web-2d-world-first`
- `gsp-web-3d-specialist` for `web-3d-preview`

Top-level planning remains stack-neutral.
Implementation guidance should still become concrete once a backend family is chosen.
