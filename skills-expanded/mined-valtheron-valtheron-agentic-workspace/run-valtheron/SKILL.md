---
name: run-valtheron
description: Build, run, and drive valtheron-agentic-workspace. Use when asked to start the app, run the dev servers, test the backend API, take a screenshot of the frontend, or interact with the running app.
---

Full-stack app (Express + React/Vite). Drive it via `.claude/skills/run-valtheron/smoke.sh` for automated smoke testing, or launch backend + frontend manually and interact with `curl`.

All paths below are relative to the repo root.

## Prerequisites

Node.js 20+ (pre-installed in this container).

No system packages needed beyond what's already available.

## Setup

```bash
npm run install:all
cp backend/.env.example backend/.env
```

Env vars (all optional for local dev — defaults work):

| Var | Default | Notes |
|-----|---------|-------|
| `PORT` | `3001` | Backend port |
| `JWT_SECRET` | dev default | Warns on startup; production refuses default |
| `ANTHROPIC_API_KEY` | — | Only for LLM task execution routes |
| `OPENAI_API_KEY` | — | Only for LLM task execution routes |
| `STRIPE_SECRET_KEY` | — | Only for donation checkout |

## Run (agent path)

Run the smoke script — it installs deps, starts both servers, runs 7 endpoint checks, and reports:

```bash
bash .claude/skills/run-valtheron/smoke.sh
```

Output ends with PIDs for both servers. They keep running after the smoke tests pass; `Ctrl-C` or `kill` to stop.

For manual API interaction after launch:

```bash
curl -s http://localhost:3001/api/health
curl -s http://localhost:3001/api/agents | head -c 200
curl -s http://localhost:3001/api/analytics/dashboard | head -c 300
curl -s http://localhost:3001/api/security/events | head -c 300
curl -s http://localhost:3001/api/security/kill-switch
curl -s http://localhost:5173/api/health   # via Vite proxy
```

Logs: `/tmp/valtheron-backend.log`, `/tmp/valtheron-frontend.log`.

## Run (human path)

```bash
npm run dev   # starts backend (port 3001) + frontend (port 5173) via concurrently
```

Opens nothing — visit `http://localhost:5173` in a browser. `Ctrl-C` stops both.

## Build

```bash
cd frontend && npm run build   # outputs to frontend/dist/
```

## Test

```bash
cd backend && npm test        # 447/448 pass (~45s) — 1 flaky stress-test timeout
cd frontend && npx vitest run  # 218/218 pass (~10s)
```

## Gotchas

- **Kill-switch API uses German field names** — the response has `"aktiv"` not `"active"`. The smoke script handles both.
- **Backend port conflict** — if port 3001 is in use, the server prints a clear error and exits. Check with `lsof -i :3001`.
- **No browser in container** — `chromium-cli` is not available; frontend testing is limited to `curl` against the Vite dev server and its proxy. For visual verification, build and inspect the HTML output.
- **Stress test flaky** — `backend/src/__tests__/performance.test.ts` "handles 100 concurrent requests" times out in ~50% of container runs. Safe to ignore.

## Troubleshooting

- **`EADDRINUSE` on port 3001**: Another backend instance is running. `pkill -f "tsx watch src/server.ts"` then retry.
- **`Cannot find module './app.js'`**: You're running `node dist/server.js` without building first. Use `npm run dev` (tsx) for dev, or `npm run build && npm start` for production.
