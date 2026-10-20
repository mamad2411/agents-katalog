# Trekker — agent notes

A self-hosted TV and film tracker. Next.js 16 (App Router, React 19, Server
Actions), Tailwind v4, SQLite via Prisma 7 (better-sqlite3), TMDB for the
catalogue. The README is the tour for people deciding whether to run it;
`docs/build-log.md` is thorough and current — read it for what a feature is
*for* before changing how it works.

## Commands

- `npm run dev` — dev server (`prisma generate` runs first automatically)
- `npm run build` / `npm start` — production
- `npm test` — vitest, against throwaway SQLite databases in `tests/.tmp/`
- `npm run typecheck` / `npm run lint`

## Layout

- `src/app` — routes. Pages are server components; interactivity lives in
  `src/components`.
- `src/lib` — all server logic. Files ending `-actions.ts` are `"use server"`
  modules called from the client; the rest are server-only helpers.
- `src/generated/prisma` — generated, gitignored, never edited by hand.
- `prisma/` — schema and migrations. Schema comments carry design reasoning;
  keep them true.

## Conventions worth knowing

- British English throughout, code and copy alike: favourites, normalise,
  catalogue.
- Comments explain constraints and reasoning, not mechanics. Match that.
- All watched-state writes go through `recordPlay` in `src/lib/plays.ts` —
  `WatchedEpisode`/`WatchedMovie` are a uniqueness index over `Play`, and
  writing them anywhere else desynchronises the two.
- Theming: `data-theme` on `<html>`, not the OS media query — use the `dark:`
  and `light:` variants defined in `globals.css`, never Tailwind's built-in
  `dark:`. The ink ramp inverts between themes; on fixed-colour surfaces use
  literal `text-black`/`text-white`.
- Title pages are their own world below 40rem: the ink ramp is forced dark there
  whatever the theme, and `light:` deliberately does not match at all. Anything
  rendered on one needs the `ios-*` markers — panels are `card`, secondary text
  is `ios-dim` *beside* its `text-ink-300|400`, plain white text is `ios-bright`,
  popovers are `ios-menu`. Those markers emit no CSS above 40rem, so each one
  needs real utilities and a `light:` pair next to it; and because they are
  unlayered they beat utilities below it, so an accent-filled selected state must
  not carry `ios-surface` or it will be repainted. See the "Title pages" block at
  the foot of `globals.css`.
- Denormalised titles and posters on rows are deliberate: list rows must render
  without a TMDB call.
- External calls (TMDB, Plex, Overseerr) fail soft and are fanned out through
  `mapLimit` in `src/lib/concurrency.ts` — never an unbounded `Promise.all`.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
