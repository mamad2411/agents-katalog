# ccm-feedback

## Build & Test
- `bun install` — install dependencies
- `bun run build` — esbuild → `dist/w.js` (also copied to `public/w.js` by config)
- `bun run dev` — esbuild watch
- `bun run serve` — build + serve `public/` on `:5173`
- `bun run check` — `tsc --noEmit`
- `bun run lint` — biome check
- `bun run lint:fix` — biome auto-fix

There is currently no test suite. Verification = `bun run check` + `bun run lint` + manual browser smoke test on the demo page.

## Architecture
Single-package, single-script-tag widget. `src/` → `dist/w.js` via `esbuild.config.mjs`. The built file is hosted (Netlify) and consumed via `<script src="…/w.js" data-project="…">`.

- **Entry:** `src/index.ts` reads `data-*` attrs from its own `<script>` tag, then mounts.
- **Shadow DOM:** widget UI lives in an open Shadow DOM (so host pages and test harnesses can introspect it; CSS isolation comes from the shadow root, not the closed mode). Markers/overlay live outside the shadow root so they hit-test against page elements.
- **Stores:** common contract `AnnotationStore` in `src/store.ts` with two impls:
  - `Store` (localStorage) — default, no infra. Key: `ccm-feedback:<projectName>`.
  - `CloudStore` (`src/cloud-store.ts`) — Supabase PostgREST + Realtime. Activated when both `data-supabase-url` and `data-supabase-key` are set on the script tag (or passed to `init()`). Falls back to localStorage when either is empty. Auto-disabled on localhost / `*.local` so dev never writes to the production demo DB.
- **DOM anchoring** (`src/dom/`): four-strategy resolver — `@medv/finder` CSS selector, XPath, text snippet w/ prefix/suffix + neighbor text, structural fingerprint (tag chain). Position stored as % of anchor element bounding box.
- **Annotation kinds:** `target` (element anchor), `pin` (viewport coord), `area` (viewport rect). Schema in `src/types.ts`.
- **i18n:** English (default) + French in `src/i18n.ts`.

## Supabase (optional cloud mode)
- Single table `ccm_widget_annotations`. Schema in `supabase/migrations/0001_init.sql`. Subsequent migrations: `0002_status_pin_area.sql`, `0003_realtime.sql`.
- Widget speaks raw PostgREST + Realtime over `fetch` and native `WebSocket` — no `@supabase/supabase-js` dependency.
- Self-hosters: create a Supabase project, run all migrations in order, paste the project URL + anon key into the script tag's `data-supabase-url` / `data-supabase-key`. Service role key is **never** used by the widget.
- Local dev `.env` is for the maintainer's demo project only. `.env.example` documents the shape. The widget runtime never reads env vars.

## Code Style
- TypeScript strict mode with `exactOptionalPropertyTypes`
- Conventional Commits: `type(scope): description`
- Biome for formatting + linting

## Branch flow
- Work happens on `dev` or worktree branches off `dev`.
- PRs target `dev`. Never merge to `main` without explicit user instruction.

## Attribution
- ccm-feedback originated as a fork of [SitePing](https://github.com/NeosiaNexus/SitePing) by NeosiaNexus, MIT licensed.
- `LICENSE` preserves the original copyright. `NOTICE` documents the attribution.
- The codebase has diverged architecturally (monorepo → single-script-tag widget) and is maintained independently. The `upstream` git remote has been removed; no upstream sync path remains.
