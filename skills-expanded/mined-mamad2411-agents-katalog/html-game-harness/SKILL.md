---
name: html-game-harness
description: Use for developing browser-only HTML games in this repository with pure game-rule tests, Playwright verification, and the runtime AI harness.
---

# HTML Game Harness

Use this skill whenever modifying the game, stages, rendering, persistence, or tests.

## Workflow

1. Read `AGENTS.md`.
2. Read `PLAN.md` and update it first if the game concept, loop, controls, or milestones change.
3. Put deterministic rules in `src/core`.
4. Add or update Vitest tests in `tests/unit` before changing behavior.
5. Run `npm run eval:game` before and after hard level or algorithm changes.
6. Keep DOM and storage code thin.
7. Use `tests/harness/gameDriver.ts` for Playwright tests.
8. For visual changes, run `npm run artifact:browser` and inspect the screenshot.
9. Log long-running iteration notes under `.logs/`.
10. Save image generation prompts under `.prompts/`.
11. Run `npm run check` before delivery.

## Harness Requirements

The page must expose `window.__GAME_HARNESS__` with:

- `snapshot()`
- `dispatch(action)`
- `press(key)`
- `reset(seedOrState?)`
- `loadStage(stageIndex)`

Do not expose unstable internal DOM nodes through the harness.

## Review Focus

Flag missing tests, weakened harness coverage, undocumented changes to `PLAN.md`, missing visual prompts for generated assets, and any network or server-side persistence added to this static game.
