---
name: gsp-web-2d-specialist
description: "Use when implementing browser-first 2D game work after the route and backend are already chosen."
---

# Game Web 2D Specialist

## Goal
Turn a backend decision into concrete browser 2D implementation guidance without collapsing the whole system into library fandom.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present 2D implementation guidance in conversation.
- **minimal** or **full**: write or update `docs/game-studio/backend-implementation.md`.

## Use when
- the chosen backend profile is `web-2d-ui-first` or `web-2d-world-first`
- the project is browser-first and needs sharper implementation guidance
- the team wants a concrete 2D route without losing stack-neutral top-level planning

## Use
- `../../shared/reference/backend-profiles.md`
- `../../shared/reference/browser-2d-specialist.md`
- `../../shared/checklists/ui-ux-hard-rules.md`

## Cover
- recommended route archetype and why
- simulation state vs presentation state split
- HUD layer decision and whether a dedicated UI layer is needed
- action-state, fail-state, and restart-state handling
- mobile and desktop input expectations
- procedural-art constraints when relevant
- top implementation risks

## Important
Be concrete about architecture patterns, layering, and tradeoffs.
Do not pretend the backend is irrelevant once the route is chosen.
Do not begin implementation if the gameplay shape is still ambiguous.
If the request is primarily about Douyin H5 Interactive platform shell, portrait H5 delivery shape, app-shell structure, or requests phrased as `抖音互动空间` / `抖音互动H5`, route through `gsp-douyin-h5` first.

Before coding, confirm or inherit:
- camera / presentation model
- movement grammar
- obstacle or enemy grammar
- fail and restart loop
- HUD priority

For archetypes like `runner`, `platformer`, `survivor`, or `breakout`, lock the subtype first.
Example: `runner` alone is not specific enough. Decide whether it is lane-based, side-view platform, or top-down dodge before implementation.
