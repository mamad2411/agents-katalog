---
name: damas-frontend
description: >-
  Conventions and patterns for building and editing the Damas-MSA web frontend
  (apps/web): TanStack Start (file routes, SSR), Tailwind v4, shadcn/ui, lucide,
  and Motion (framer-motion) animations. Covers the checkers Board, the move-trail
  ("estela") behavior, piece/board skins, the 3-theme system, the API client
  (handling version_conflict and the abandon dialog), Clerk auth gating, and
  accessibility (AA, reduced-motion). USE THIS SKILL for any visual or UI
  implementation work in Damas-MSA — building or editing routes, the board,
  animations and effects, the lobby/ranking/profile/shop screens, theme or skin
  rendering, or loading/empty/error states. Trigger even when the user just says
  "make the board nicer", "add an animation", "the trail/estela", "style the
  profile", "add the hint button", or names a component (Board, HintButton,
  ThemeSwitcher) — without mentioning the stack. Do NOT use for backend, rules,
  or AI work (use damas-backend), nor for standalone design deliverables like
  accessibility audits, UX copy, design critiques, or user research (use the
  design:* skills).
---

# Damas-MSA — Frontend conventions

The web app lives in `apps/web` (TanStack Start, Vite). The shared rules engine
`@damas/rules` is imported directly so the UI can highlight legal moves without a
round-trip. The authoritative spec is `docs/PRD.md` §13 (Diseño y UX) and §14.

Goal: a frontend that feels **alive and polished** (animations, the move trail,
skins) while staying **accessible** and **honest to the rules** — the UI only
ever offers legal moves, but the Backend remains the authority (never trust the
client for game state).

## Stack & where things go

| Concern | Choice | Notes |
|---|---|---|
| Framework | TanStack Start | File routes in `src/routes/`, `createFileRoute`, `__root.tsx` |
| Styling | Tailwind CSS **v4** | `@import "tailwindcss";` in `src/styles.css`; no `tailwind.config.js` needed |
| Components | shadcn/ui + lucide | Accessible primitives (Dialog, Tabs, Card, DropdownMenu) |
| Animation | **Motion** (`motion`/`framer-motion`) | Add when implementing F7; see "Animations" below |
| Data | `src/lib/api.ts` | Typed client; never `fetch` the API ad-hoc from components |
| Auth | `@clerk/clerk-react` | Gated via `Protected`; token bridged into the API client |

Env vars live in the **monorepo root** `.env`; `vite.config.ts` sets
`envDir: "../.."`. Client vars must be prefixed `VITE_` (this is Vite, NOT
Next.js — never `NEXT_PUBLIC_`).

## Routing (TanStack Start)

- One file per route under `src/routes/`; export `Route = createFileRoute(path)({ component })`.
- `routeTree.gen.ts` is **generated** by the dev/build — never edit it by hand.
- `__root.tsx` owns the `<html>` document, `<HeadContent/>`, `<Scripts/>`, the
  nav bar, and the `ClerkProvider` + token bridge. Wrap authed screens in
  `Protected` (shows the landing to signed-out users).

## The Board is the heart of the UX

`src/components/Board.tsx` renders the NxN grid (8 or 10 depending on variant).
Rules to preserve when editing it:

- **Legal moves come from `@damas/rules` `getLegalMoves(cells, "human")`** — memoize
  on `[cells, interactive]`. The board lights up only origins/destinations that
  are legal. Because `getLegalMoves` already returns *only* captures when a
  capture exists, mandatory-capture is enforced for free — don't special-case it.
- **Both interaction modes** (PRD §13.6): click-to-move (select origin → legal
  destinations highlight → click destination) AND drag-and-drop. Keep both working.
- **Multi-jump chains** share an origin/destination but differ by `path`. When the
  user picks a destination, send the full `path` to the backend so it can
  disambiguate (the move object from `getLegalMoves` already carries `path`).
- **Pieces are owner-coded** in `cells` (1/3 human, 2/4 AI); `player_color` only
  decides *paint* and who opens. Map owner→color for rendering; never store color
  in cells (see PRD §14.1).
- **Accessibility:** every square has an `aria-label`; the grid is keyboard
  navigable (arrows + Enter); maintain a square aspect ratio that scales to the
  viewport; on mobile the status panel moves below the board.

## Move trail ("estela") — PRD §14.14

This is a signature effect. Get it exactly right:

- The trail shows **only the last move**, derived from `history[history.length-1]`
  (origin + `path`, which includes every hop of a capture chain).
- When a new move lands, the previous trail is **fully replaced** — at any instant
  there is exactly **one** trail on screen: the last mover's.
- **Color by side:** human trail and AI trail use distinct colors so you can tell
  at a glance who just moved.
- It must be **idempotent on resume**: derive it from persisted `history`, don't
  replay the game. Reading an active game (GET /game/active) and showing the trail
  for the last AI move is the normal path (see `routes/game.tsx`).

## Animations (Motion) — add in F7, design now

Principles, so effects feel intentional rather than flashy:

- **Slide, don't teleport:** a moved piece animates along its `path`; captured
  pieces fade out; promotion gets a small crown pop.
- **Derive from state, stay idempotent:** animations read from `history`/state so a
  refresh or cross-device resume never double-plays. Animate the *delta*, then
  settle to the persisted board.
- **Respect `prefers-reduced-motion`:** when set, skip motion — jump to the final
  position and show a static trail. Wire this once in a hook (e.g.
  `useReducedMotion` from Motion) and branch on it.
- **Animated skins** (`cosmetics.animated`) keep a subtle idle effect (shimmer/
  particles); they must also honor reduced-motion.
- Keep durations short (~150–250ms for moves) so fast play never feels sluggish.

## Themes vs skins — keep them separate (PRD §13.3, §5.9)

- **Theme** = global UI palette. 3 options (`neon`/`minimal`/`classic`) via a
  `data-theme` attribute on `<html>` and CSS variables. Persisted in `users.theme`
  (synced cross-device), with `localStorage` fallback before login.
- **Skins** = equippable cosmetics, independent of theme: piece skins (yours AND
  the AI's, separate slots), board skins, profile frame, shield/badge. Assets are
  SVG/Lottie served from the frontend, resolved by `cosmetics.asset_key`.
- A skin may bring its own palette or adapt to the theme. Never conflate the two
  systems in code: a `ThemeSwitcher` changes tokens; equipping a skin changes an
  asset reference in `users.equipped`.

## API client — always go through `src/lib/api.ts`

- All calls use the typed helpers (`getActiveGame`, `createGame`, `playMove`,
  `surrender`, `getRanking`, …). Add new endpoints there, not inline in components.
- Auth: a token getter is registered by the Clerk `TokenBridge` in `__root.tsx`;
  requests send `Authorization: Bearer <JWT>`. Without Clerk configured the client
  falls back to the `x-dev-user` header (dev mode) — keep that fallback intact.
- Errors throw `ApiRequestError(status, code)`. Handle the meaningful codes in the
  UI, especially:
  - `active_game_exists` → show the abandon **confirmation dialog** (PRD §14.4),
    then retry with `confirmAbandon: true`.
  - `version_conflict` → another device moved (optimistic lock, §14.10); refetch
    the game and re-sync before letting the user retry.

## Loading / empty / error states (PRD §13.8)

Every data screen needs all three: skeletons while loading, a friendly empty
state ("aún no tienes partidas"), and an error with a *Reintentar* button.
Don't ship a screen that only handles the happy path.

## Reference

- Components inventory: PRD §13.9. Screens & routes: PRD §13.4.
- Existing code to match: `apps/web/src/components/Board.tsx`,
  `apps/web/src/routes/game.tsx`, `apps/web/src/lib/api.ts`,
  `apps/web/src/routes/__root.tsx`.
- Run locally: `bun run dev:web` (port 3002). Build: `bun --cwd apps/web run build`.
