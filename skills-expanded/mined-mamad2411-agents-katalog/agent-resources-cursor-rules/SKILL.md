# Cursor Rules — Agent Resources

These rules explain how to work on `agent-resources` inside Cursor. Skim this file before making changes so you understand the stack, the workflows, and the expectations.

---

## Project Snapshot
- **Stack:** Node 18+ (CommonJS), Express 4, express-handlebars, Supabase (DB/Auth), HTMX 2, Bulma 1, Tom Select, Tippy.js, FullCalendar, Nodemon for dev.
- **Entry point:** `index.js` wires middleware, static assets, Handlebars helpers (`util/handlebars.js`), route modules in `routes/`, and injects `supabaseUrl`/`supabaseKey` into views.
- **Data access:** Each domain has a `models/*.js` file that talks to Supabase via the shared client in `models/_base.js`. `util/supabase.js` simply re-exports the combined model APIs for easier importing inside routes.
- **Views & UI:** Server-side Handlebars templates live in `views/`, with partials in `views/partials/`. Client-side enhancements sit in `public/js/app.js` (an IIFE that exposes `App.*` helpers used from templates). Custom styling overrides Bulma via `public/css/styles.css`.
- **Supabase schema:** See `schema.sql` for tables, functions (`dup_class`, `redeem_class_code`), and the row-level security (RLS) policies that every query must respect. Keep those policies in mind when troubleshooting permission errors.

---

## Local Environment & Secrets
- Copy `.env.dist` to `.env` and fill in:
  - `SUPABASE_URL`, `SUPABASE_KEY` (anon/publishable key for client + server).
  - `SUPABASE_DB_PASS` if you run direct SQL locally.
  - `OPENAI_API_KEY` for the character import pipeline (`util/character-import.js`).
  - `SYSTEM_MESSAGE_*` when you want to broadcast a banner (rendered through `views/partials/alert/system-banner.handlebars`).
- Never hard-code secrets. Server surfaces only the anon key to the browser via `res.locals` → `<script>App.init(...)</script>` inside `views/partials/head.handlebars`.

---

## Commands & Tooling
- Install deps: `npm install` (preferred) or `bun install` if you already use Bun.
- Dev server: `npm run dev` (nodemon on port 3000). Cursor already has `bun run dev` running in Terminal 1—re-use that session or stop before starting another watcher.
- Production build: `npm run start`.
- Seed base classes (requires service-level Supabase key and an admin profile record): `npm run seed:classes`.
- Tests: not implemented. You must rely on manual verification plus linting tools you add yourself.

---

## Architectural Notes
### Routing & Middleware
- `util/auth.js` exports `isAuthenticated`, `authOptional`, and `requireAdmin`.
  - `isAuthenticated` expects `Authorization: Bearer <access token>` and `Refresh-Token` headers (HTMX requests get them from `App.init`). If tokens are missing it issues redirects using HX headers when necessary.
  - `authOptional` sets `res.locals.authOptional = true` and still hydrates `res.locals.profile` when tokens are present. Use it on pages that should render for anonymous visitors but behave differently when logged in (e.g., `routes/home.js`, `routes/missions.js` show views in read-only mode).
  - `requireAdmin` assumes the profile has already been loaded and short-circuits with `401/403` JSON errors if not authorized.
- Routes typically:
  1. Expect upstream middleware to populate `res.locals.profile` (+ `user`).
  2. Call into a `models/*` helper via `util/supabase`.
  3. Render server-side Handlebars templates. HTMX endpoints set `layout: false` and rely on `HX-Location`, `HX-Redirect`, or `HX-Push-Url` headers for navigation.
- **Common patterns to follow:**
  - Convert checkbox form data to booleans before sending to Supabase (`routes/missions.js`, `routes/classes.js` examples).
  - When editing collections (relationships, e.g., mission characters), fetch current rows and diff to add/remove entries to avoid duplicate rows.
  - Always propagate Supabase errors back to the client with `return res.status(400).send(error.message)` so HTMX can show them.

### Models & Supabase usage
- A single Supabase client (`models/_base.js`) reads `SUPABASE_URL` + `SUPABASE_KEY` and is shared by every model.
- Each model exports Promise-returning helpers (e.g., `models/mission.js#getMissions`) that already wrap `supabase.from(...).select(...)`. Use them instead of embedding SQL inside routes—this keeps logic centralized and consistent with RLS rules.
- When calling RPC functions (e.g., `models/class.js#duplicateClass` uses `dup_class`, `redeemUnlockCode` uses `redeem_class_code_for_user`), handle thrown errors explicitly. RLS errors surface as standard Supabase errors.

### Frontend runtime (`public/js/app.js`)
- The IIFE exposes a global `App` object that templates use via `hx-on:click="App.signOut()"`, etc. Any new client helper needs to be added to that return object.
- Responsibilities:
  - Initialize Supabase JS client on `DOMContentLoaded`, subscribe to `auth.onAuthStateChange`, and keep tokens in `localStorage`.
  - Decorate HTMX requests with auth headers on `htmx:configRequest`.
  - React to HTMX lifecycle events (`htmx:afterSwap`, `htmx:afterSettle`) to re-run tooltip/Tom Select wiring and manage auth-optional state.
  - Render the FullCalendar widget for authenticated users (data fetched from `/lfg/events/all`).
  - Provide UX helpers (modal open/close, copy to clipboard, form loading overlays).
- Keep this file framework-free and consistent with its existing imperative style.

### Views, Partials, and Styling
- Layout injection happens in `views/layouts/main.handlebars`. It includes `{{> head}}`, `{{> nav}}`, renders system banners/alerts, and hosts `{{{body}}}`.
- Use partials for reusable UI: nav, alert banners, LFG fragments, auth forms, etc. Many of them are designed for HTMX swaps (set `layout: false` when rendering from routes).
- CSS guidelines:
  - `public/css/styles.css` handles HTMX state transitions, custom modals, Tom Select overrides, form loading overlays, and video container ratios.
  - Stick to Bulma utility classes where possible; extend inside `styles.css` when necessary. Keep new selectors scoped to avoid collisions with Bulma.

### Domain-specific expectations
- **Characters** (`routes/characters.js`):
  - Data gating: ability/gear descriptions must be blanked unless the viewer has unlocked the relevant classes (or explicitly hosts an LFG context). Preserve the logic around `getUnlockedClasses` and `hostingViaLfg`.
  - Class pickers dynamically filter to unlocked classes. Reuse `filterClassDataForUser`.
  - Character import uses OpenAI (`util/character-import.js`) + `zod-gpt` to parse freeform text. Ensure prompts stay deterministic and results pass the schema before persisting.
- **Classes** (`routes/classes.js`):
  - Admin vs player capabilities differ (players auto-set `is_player_created`, statuses limited to alpha/beta, etc.). Respect those guardrails if you touch class creation/update.
  - Unlock codes rely on Supabase RPCs; always surface errors clearly.
  - Release classes that are not unlocked render a teaser view—keep that logic in sync with any future changes.
- **Missions & LFG**:
  - Mission creation attaches characters via the join table and responds with `HX-Location` so HTMX can navigate.
  - Public mission search (`models/mission.js#searchPublicMissions` / `getRandomPublicMissions`) strips nested Supabase join structures into plain arrays. Follow the same transformation if you add new selectors.
  - LFG routes supply calendar events plus segmented tabs (My Posts, Joined, Public). Many endpoints return partials for HTMX `hx-target`s.

---

## Working Style in Cursor
1. **Plan before editing.** Skim relevant route + model + view files. When a change spans multiple areas (e.g., UI + route + model), consider writing a todo list with `TodoWrite` to stay organized.
2. **Mind running processes.** Check `.cursor/projects/.../terminals/` to see if a dev server is already live before starting another. Reuse the existing watcher, or stop it explicitly.
3. **Prefer targeted edits.** Use `Read`, `Grep`, and `ApplyPatch` for single-file changes. Avoid bulk search/replace via shell; rely on Cursor tools for safety.
4. **Respect existing patterns.** Follow the same logging, error handling, and HTMX response headers the current routes use.
5. **Keep code comments minimal but meaningful.** Only annotate non-obvious logic (e.g., why we remove descriptions without unlocks). Inline docs already exist for most helpers—extend them sparingly.
6. **No destructive git commands.** Never `git reset --hard` or similar. If you need to inspect repo state, stick to `git status`, `git diff`, etc.

---

## Feature Workflow Checklist
1. **Understand the data.** Read the relevant section in `schema.sql`, plus the corresponding `models/*.js` file, before changing queries.
2. **Update the model or utility first** if new data is needed. Keep Supabase interactions centralized.
3. **Modify routes/controllers.** Use the exported helpers, ensure middleware matches the access pattern (`isAuthenticated` vs `authOptional`), and return HTMX-friendly responses.
4. **Adjust Handlebars views/partials.** Keep markup Bulma-friendly. For HTMX fragments, remember `layout: false`.
5. **Touch front-end JS only when necessary.** Add new methods to the `App` return object and expose them via `hx-on` attributes or event listeners.
6. **Style in `public/css/styles.css`.** Co-locate new selectors near related features and keep them responsive.
7. **Manual verification.** With `npm run dev` running:
   - Exercise the affected route/page in the browser.
   - Confirm HX navigation works (headers, modals, etc.).
   - For Supabase writes, inspect the response payloads / console logs for errors.
   - If you changed mission/LFG/class flows, test both authenticated and anonymous states.
8. **Linting/tests.** No automated test suite exists. Run `npm run lint` only if you add one; otherwise rely on ESLint-in-editor or `node --check` equivalents.

---

## Data & Seeding
- The repo does not auto-run migrations. Apply DDL statements manually through Supabase (or `schema.sql`) when needed. Document any schema drift in PR descriptions.
- `util/seed-classes.js` seeds canonical classes by:
  1. Loading an admin profile (role = admin).
  2. Mapping constant lists from `util/enclave-consts.js`.
  3. Calling `ClassModel.createClass` per entry.
  Use it only against non-production projects unless authorized.

---

## Key Reference Files
- `README.md` — Install/run instructions and dependency list.
- `index.js` — Express bootstrap, middleware, router wiring.
- `routes/*.js` — Server endpoints (auth, profile, characters, missions, classes, LFG).
- `models/*.js` — Supabase data access helpers. Keep business logic close to data shape here.
- `views/` — Handlebars layouts, pages, and partials. HTMX partials live under `views/partials/`.
- `public/js/app.js` — Client orchestrator: auth tokens, HTMX hooks, calendars, modals.
- `public/css/styles.css` — Bulma overrides, HTMX state transitions, modals, Tom Select styling.
- `util/` — Shared helpers: auth middleware, Handlebars helpers, Supabase aggregator, Enclave constants, system message builder, AI-assisted character importer.

Keep this document up to date as the architecture evolves. When you introduce new infrastructure (e.g., tests, linters, build steps), add concise guidance here so future Cursor sessions inherit the right context.
