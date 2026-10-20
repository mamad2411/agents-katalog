---
description: FastAPI Viz Studio server, WebSocket protocol, and web frontend
globs: server/**/*.py,web/**/*
alwaysApply: false
---

# Viz Studio (Server + Web)

## Stack

- **Backend**: `server/app.py` — FastAPI, static mount of `web/dist/`
- **Frontend**: `web/dist/index.html` + `app.js` — Three.js, no build step in CI

## SimSession

Holds `DoublePendulumCart`, controller (`EvolvedController` / `RandomController` / `ZeroController`), and physics overrides. Rebuild controller via `_rebuild_controller()` after genome or mode changes.

## API surface

| Endpoint | Purpose |
|----------|---------|
| `WebSocket /ws/sim` | Live stepping; sends `frame_dict` JSON per step |
| `GET /api/network` | Evolved network topology JSON |
| Static `/` | Viz Studio UI |

## Frame payload

`frame_dict` keys: `cart_x`, `p1`, `p2`, `theta1`, `theta2`, `action`, `tip_height`, `above_threshold`, `gravity`, `friction`, `done`, `step`.

Keep field names stable — `web/dist/app.js` and `assets/demo_trajectory.json` depend on them.

## Modes

| Mode | Source |
|------|--------|
| Live | WebSocket → `SimSession.step()` |
| Replay | `assets/demo_trajectory.json` |
| Network viz | `/api/network` or `assets/network.json` |
| Training tab | User-loaded `metrics.jsonl` |

## Development rules

- Route all live simulation through `SimSession` + `DoublePendulumCart` — do not duplicate physics in the frontend.
- Use `Evaluator` patterns for any server-side scoring, not ad-hoc loops.
- Frontend changes go in `web/dist/` unless user requests a separate src/build pipeline.
- `pendulum-neat serve --checkpoint PATH` preloads genome into session before uvicorn starts.
