# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- `npm run dev` — Vite dev server with HMR.
- `npm run build` — type-check (`tsc -b`) then production build. The build fails on any type error.
- `npm test` — run the full Vitest suite once (jsdom environment).
- `npm run lint` — oxlint (config in `.oxlintrc.json`; only `rules-of-hooks` and `only-export-components` are enforced).
- `npm run preview` — serve the built `dist/` locally; use this to exercise the installable, offline PWA build.

Run a single test file or pattern:

```bash
npx vitest run src/test/session.test.ts       # one file
npx vitest run -t "rolls over"                 # tests matching a name
npx vitest src/test/session.test.ts            # watch mode
```

CI (`.github/workflows/deploy-pages.yml`) runs lint → test → build, then deploys `dist/` to GitHub Pages on every push to `main`. Keep all three green.

## Architecture

A React 19 + TypeScript + Vite PWA. No router, no state library, no backend — three screens driven by `useState` in `App.tsx`, and all persistence is `localStorage`. The design deliberately keeps the timer logic pure and the content declarative.

**Data is the source of truth (`src/routines.ts`).** Routines are plain data (`Routine` → `Move[]`, typed in `src/types.ts`). The timer, progress bar, per-move preview, and "next up" text all derive from this array. Adding or changing a routine means editing only this file. One-sided stretches are authored once and expanded into separate left/right moves by `bothSides()` at definition time, so the rest of the app never special-cases sidedness beyond displaying a label.

**The session is a pure reducer (`src/session.ts`).** `sessionReducer(routine, state, action)` is framework-free and fully unit-tested. Key behaviors to preserve:
- `tick` consumes a number of *elapsed seconds* and rolls over across move boundaries (can finish several moves in one tick). "Skip" (`next`) reuses the same `goToNext` path, so skipping behaves identically to a move's timer running out.
- `previous` mirrors a music player: it first restarts the current move, and only steps back on a second press.
- State is never mutated; every action returns a new `SessionState`.

**The hook adds wall-clock timing (`src/hooks/useSession.ts`).** `useRoutineSession` wraps the reducer in `useReducer` and drives `tick` from `Date.now()` deltas rather than counting intervals, so a throttled or backgrounded tab catches up instead of drifting. If you change timing, keep it measured against the wall clock.

**Persistence and streaks (`src/storage.ts`).** `AppState` is saved to `localStorage` under `morning-stretches.v1`. All reads go through `parseAppState`, which defensively coerces unknown/corrupt data back to a valid shape — extend it whenever you add a field. Every storage call is wrapped in try/catch so private-browsing/quota failures never break the app. Dates are `YYYY-MM-DD` keys in the viewer's *local* timezone (`toDateKey`); `computeStreak` treats a streak as alive if the last completion was today or yesterday (gap ≤ 1 day).

**Screen flow (`src/App.tsx`).** `screen` moves through `home → session → complete`. A `sessionKey` counter is bumped and passed as the `SessionView` `key` to force a fresh remount (and thus a fresh countdown) on start/repeat. Completions are recorded in `completeSession`, and `appState` is persisted via an effect whenever it changes.

**Effects live at the edges.** `SessionView` fires the chime (`src/audio.ts`, Web Audio, must never throw) on move changes and completion, and requests a screen wake lock (`src/hooks/useWakeLock.ts`) while running. Both feature-detect and degrade silently when unsupported.

## Gotchas

- **Base path.** `vite.config.ts` sets `base: '/morning-stretches/'` for GitHub Pages. Asset URLs, the PWA manifest `start_url`/`scope`, and the service-worker `navigateFallback` all depend on it. Note `index.html` still uses root-absolute (`/favicon.svg`) paths that Vite rewrites at build time.
- **PWA/service worker.** `registerType: 'autoUpdate'` means a deployed update activates on next load; test SW behavior via `npm run build && npm run preview`, not the dev server.
- Prefer adding logic to `session.ts`/`storage.ts` (pure, testable) over components, and add a test in `src/test/` alongside existing ones.
