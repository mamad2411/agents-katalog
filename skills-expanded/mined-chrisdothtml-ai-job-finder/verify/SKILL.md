---
name: verify
description: How to run and drive this app to verify UI/server changes at runtime
---

# Verifying job-finder changes

## Launch

- Dev server: `yarn app:dev` (nodemon) or `yarn server:start`; serves at
  `http://localhost:8000` (PORT env, default 8000). Check first — it's often
  already running.
- In dev mode the UI is bundled from `src/ui` per request via esbuild
  middleware, so UI edits are picked up on page reload — no rebuild step.

## Drive

- The app blocks on onboarding unless localStorage has
  `ai-job-finder-storage` with `{"isOnboarded":true,...}`. To skip onboarding
  in a fresh Playwright profile:
  `localStorage.setItem('ai-job-finder-storage', JSON.stringify({ isOnboarded: true, settings: {} }))`
  then reload. Restore `{"isOnboarded":false,"partialSettings":{}}` when done.
- Jobs data comes from `/api/jobs`, companies from `/api/companies` — both already
  populated locally.
- Jobs-list view prefs persist under localStorage key `ai-job-finder-ui-prefs`.

## Gotchas

- Playwright MCP screenshots with relative paths land in the repo root, not
  `.playwright-mcp/` — use absolute scratchpad paths.
- Job cards animate in (`cardIn`, staggered by index); screenshot right after
  reload catches half-faded cards. Wait a beat before capturing.
- The server on :8000 is usually the user's own dev server — never kill or
  restart it. Close the Playwright browser when done.
