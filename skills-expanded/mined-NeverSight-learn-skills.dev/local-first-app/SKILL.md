---
name: local-first-app
description: Local-first CRUD blueprint — Next.js + node:sqlite, single-user. Use this skill whenever the user wants to scaffold a tracker/dashboard app, add a persisted entity, or package as a desktop binary. Do NOT use for palette (color-system) or layout (frontend-design).
license: MIT
metadata:
  author: Antonin Januska
  version: "1.4.0"
  tags: [nextjs, react, typescript, sqlite, local-first, desktop, architecture, charts]
---

# Local-First App

## Overview

A blueprint for building a **local-first, single-user CRUD app for one specific function** — a game-backlog tracker, a workout log, a book/collection catalog, a habit tracker, a personal dashboard. One purpose, one user, one machine: it runs entirely in the browser, persists to a local SQLite file, and can ship as a single self-contained desktop binary. **No backend service, no auth, no network dependency for core function.** The "server" is just Next.js server components and server actions talking to a local file. This skill is the *architecture*; the specific function is yours. Computation is welcome *inside* a CRUD app (a habit tracker derives streaks; a collection tracks totals), but a pure computation-only tool with **no persisted entities** doesn't need this machinery — use just a pure core + a form, and skip `src/db`, migrations, loaders, and the screen shells.

**Core principle:** every **derived value** — CRUD-derived state (rollups, filters, status counts) *and* any computation — lives in a **pure, framework-free core** (`src/<domain>/`) that imports nothing from React, Next, or the DB. `lib/` never aggregates; it maps DB rows and *calls* the core. Client components import the core directly and run it in the browser. Persistence is a thin `server-only` SQLite layer. This separation makes the logic testable, reusable (a future CLI), and packageable.

*Scope: one-user, one-machine, local-data CRUD apps. Not for apps needing real multi-user auth, server-side secrets, a hosted API, or horizontal scale — that's a different architecture.*

## The stack (pin to these)

| Layer | Choice | Why |
|---|---|---|
| Framework | **Next.js (App Router)**, `output: "standalone"` | Server components for the data boundary; standalone build compiles to a binary. Start in React from day one. |
| UI | **React + TypeScript (strict)** | `noUncheckedIndexedAccess: true`, `moduleResolution: "Bundler"` |
| Component lib | **Mantine** (`@mantine/core`, `/hooks`, `/dates`, `/charts`, `/form`, `/modals`) | Mature, batteries-included: AppShell, tables, inputs, dark mode, charts, `useForm`+zodResolver, confirm modals. Don't roll your own or use an immature/personal component lib. |
| Persistence | **`node:sqlite`** (built-in `DatabaseSync`) | **No native addon** — `better-sqlite3` needs per-platform native rebuilds, which kills the single-binary goal. Same driver on Node 24 and Deno; needs **Node ≥ 22.5** (flagged on 22.x, unflagged on ≥ 23). Load-bearing; don't swap it. |
| Validation | **zod** at every server boundary | One schema per write path; parse before touching the DB |
| Data fetching | **none** — no TanStack Query / SWR / Redux | Reads are server components; derive/compute in the browser. No client cache layer to add. |
| Math/diagrams | **KaTeX** (formulas), **Mermaid** (lazy client render) | *Only if the app computes non-obvious numbers.* A pure CRUD tracker can skip these. |
| Test | **vitest** | Pure-core unit tests, test-first |

## Architecture — three hard layers

```
src/<domain>/   PURE logic core   — no I/O, no React, no next, no db. The product's brain.
src/db/         server-only store — node:sqlite, typed query API, versioned migrations
lib/            server/client glue — 'server-only' loaders + row mappers (call the core; no aggregation here), zod schemas, formatters, colors, config
app/            routes            — server pages load data → pass plain rows to 'use client' children
components/     UI                — 'use client'; import the pure core directly and compute in the browser
```

**Data flow:**
- **Reads:** server component (`export const dynamic = "force-dynamic"`) calls a `'server-only'` loader → maps DB rows to a plain client-row type → passes to a `'use client'` child. Mantine compound components (`Table.*`, `Accordion.*`) are client references — never render them from a server component.
- **Writes:** `'use server'` action → zod parse → rule guard (load → check → throw) → typed DB call → `revalidatePath()`.
- **Derive/compute:** roll-ups, filters, summaries, and math all live in the pure core (`a derived value? → the core, always`), called from client components and `lib/` loaders. `lib/` maps rows and *calls* the core; it holds no aggregation logic of its own.

Two row shapes, not one: a lightweight **list row** (scalars + cheap counts) and a **detail aggregate** (row + children + a core summary, a superset). A `toX(row, derived)` mapper builds each — the two loaders return different shapes by design. A third shape exists for bolt-on computation (a calculator/report mixed into an otherwise-CRUD app) — see references/ARCHITECTURE.md.

→ Full data-layer, migrations, and shared-state detail: **[references/ARCHITECTURE.md](./references/ARCHITECTURE.md)**

## CRUD as screens — never modals

Every list/view/create/edit is an **addressable route**, not modal state. One screen per operation, identical layout across every entity:

```
app/<entity>/
  page.tsx             list      → loadEntities()         → <EntityList>   (per-entity)
  new/page.tsx         create    → <FormScreen>           → createEntity action
  [id]/page.tsx        detail    → loadEntityDetail(id)   → <EntityDetail> (per-entity)
  [id]/edit/page.tsx   edit      → <FormScreen mode=edit> → updateEntity action
  not-found.tsx        requireX → notFound()  (bad [id] → 404, not 500)
  error.tsx            catches throws   ·   loading.tsx (optional)
```

- **The URL is the state:** deep-linkable, refresh-safe, back/forward works, nothing to lose mid-flow. Don't reach for App Router's intercepting-route modal pattern for data entry — for one user on one machine, plain screens are simpler and the clarity is the point. **When the entity set needs periodic re-checking rather than one-off CRUD** (staleness checks, due-for-follow-up items), a plain list is the wrong shape — see the review-deck pattern below. **The one modal exception is a destructive-delete confirm** (Mantine `openConfirmModal`, which needs `<ModalsProvider>` in the root stack) — it shows the cascade blast radius (`also deletes 4 tasks`) from the detail loader's counts, then runs the `deleteEntity` action inside `startTransition` → `revalidatePath` → `redirect` to the list. Don't build a delete *screen*; don't delete without the count.
- **Edit is the new screen, prefilled.** One `<EntityForm>` (a `mode` prop) is the single source of truth for the fields; new mounts it empty, edit mounts it with the loaded row. It validates against **one zod schema** (`lib/schemas/<entity>.ts`, `z.coerce.*` on non-strings) — `zodResolver` on the client for inline errors, the *same* schema `safeParse`d in the `'use server'` action as the authority. Submit via Mantine `useForm.onSubmit` calling the action (with the **typed values object, not FormData**) inside `startTransition`; the action returns `fieldErrors` on failure → `form.setErrors`, else writes → `redirect('/<entity>/[id]')` (post/redirect/get) and `revalidatePath`s list + detail.
- **Shared form shell; per-entity list/detail.** The high-value reuse is the **form/editor shell** (`<FormScreen>` / an `EditorShell`) that every entity's new+edit screens share — same chrome, only the inner fields differ. List and detail screens are usually **per-entity components** (a `CardList`, a `CardDetail`); promote them to shared `<ListScreen>`/`<DetailScreen>` shells only if the duplication actually bites. Don't force a three-shell triad up front.
- **Review-deck triage — a fourth screen shape for periodic re-checking.** When an existing entity set needs recurring re-verification rather than one-off CRUD (items due for follow-up, records gone stale), don't bolt it onto the list screen as row actions. Model it as a deck: a pure core selector (`itemsDueForReview(items, now): Item[]`) picks the working set, and a dedicated screen shows one item at a time — top card + 1-2 actions, a progress bar, and explicit empty/done states — advanced by swipe or keyboard. One decision at a time beats a table the user has to scan and triage manually.

## Relationships — FKs, assembled in loaders, cross-linked

Entities reference each other with real foreign keys; joins are assembled in `lib/` loaders, never followed by the pure core.

- **Schema:** turn FKs on (`PRAGMA foreign_keys = ON` — node:sqlite defaults them OFF), declare delete intent (`ON DELETE CASCADE` for ownership, `RESTRICT`/`SET NULL` otherwise — `SET NULL` needs a nullable column). Let the DB constraint reject orphans; surface the violation, never swallow it.
- **Store:** per-relation queries (`listTasksByProject(id)`) + a *batched* count (`countTasksByProject()` — one `GROUP BY`, no N+1).
- **Loaders, two per parent:** `loadProjects()` → list rows + cheap counts; `loadProjectDetail(id)` → a `{ project, tasks }` aggregate.
- **Pure core stays relationship-agnostic** — hand it the assembled aggregate (`summarizeProject(project, tasks)`); it never reads the DB to follow a relation.
- **Cross-link both ways:** parent detail renders a reusable `<RelatedList>` (child rows link to `/<child>/[id]`; a `+ New` link prefills the FK via `/<child>/new?projectId=<id>`); child detail links back to its parent. Relationship navigation is just links between detail routes.

→ Full route topology: **[references/ARCHITECTURE.md](./references/ARCHITECTURE.md)** · worked 1:N + N:N relationship patterns: **[references/RELATIONSHIPS.md](./references/RELATIONSHIPS.md)**

## Conventions (carry these verbatim)

- **All derivation in the core:** rollups, summaries, and math live in `src/<domain>/`; `lib/` only maps rows and calls the core. "A derived value? → the core, always." DB-context business rules run as a **guard step in the server action** (load → check → throw); extract them to pure predicates (`rules.ts`) only when they grow or need tests.
- **Exact quantities** *(when a value must be precise)*: store as **integer base units** (grams, seconds, scaled fixed-point) at the DB/zod boundary; the pure core works in **major units as floats**. Convert at the boundary, nowhere else. Never store an exact quantity as a float. Floats are fine for display and simple arithmetic, but iterative summation drifts — sum in base units when an exact total matters.
- **Imports:** extensionless relative imports (`./summary`). Bundler resolves TS directly.
- **No silent fallbacks:** the pure core *throws* on invalid input; the UI guards inputs before calling it. A fallback that masks a missing row is a bug.
- **Types:** explicit interfaces for every input/result. `noUncheckedIndexedAccess` is on — handle `undefined` from index access.
- **Empty state is the default state:** a fresh local-first DB has zero rows on day one — there's no seed data. Every list screen needs a real empty state (a short message + the primary "add" CTA) designed *before* the first entity exists, not a bare table header.

## UI & data-viz quality signals

These are the corrections that recur most — treat them as defaults:

- **Charts:** never plot different-unit quantities on one axis (a total over years next to a monthly figure misleads). Show the actual value at each bar end; give every chart a bar/line toggle and multiple scale-grouped views; don't force a $0 line baseline (auto-fit the y-domain); make hover/tooltips work.
- **Tables:** one grouped table with parent-owned filter pills that drive columns AND chart series together — not many split tables. Always include the diff/delta column for paired figures.
- **Color:** centralize all chart color in one module; color by **semantic role**, not hue; provide light + dark variants; ride meaning on **blue-vs-orange (warm/cool), never red-vs-green**, and add a `+/−` glyph so color is never the only signal.
- **Legibility (recurring failure):** set the floor at the theme/globals level — body ≥16px, weight ≥400, contrast ≥4.5:1, line-height ≥1.5. Cards/tables need a surface background distinct from the canvas; flat same-color containers read as illegible.
- **Explainability** *(when the app computes non-obvious numbers)*: show each formula once (KaTeX) with values plugged in + a JavaScript-form toggle; collapsible "underlying math" under dashboard stats; an in-app `/docs` area with Mermaid diagrams. A pure CRUD tracker skips formulas but still ships the `/docs` concept area.

→ Full color/theme system, data-viz rules, explainability, and legibility detail: **[references/UI.md](./references/UI.md)**
→ Packaging to a desktop binary (`deno compile` / `deno desktop`): **[references/PACKAGING.md](./references/PACKAGING.md)**

## Examples

✅ **Derived state in the pure core — a tracker with no math**
```ts
// src/backlog/summary.ts — pure: rollups/counts, throws on bad input. No arithmetic, same pattern.
export function summarize(games: Game[]): BacklogSummary {
  const byStatus = { backlog: 0, playing: 0, beaten: 0 };
  for (const game of games) byStatus[game.status]++;
  return { total: games.length, byStatus, pctBeaten: games.length ? byStatus.beaten / games.length : 0 };
}
```

The identical core pattern carries real computation when the domain has it:

✅ **Calculation in the pure core, called from the client**
```ts
// src/measure/bmi.ts — no React, no db, throws on bad input
export function bmi(weightKg: number, heightM: number): number {
  if (weightKg <= 0 || heightM <= 0) throw new Error("invalid measurements");
  return weightKg / (heightM * heightM);
}
```
```tsx
// components/BmiPanel.tsx — 'use client', imports the core directly
const value = bmi(weightKg, heightM);
```

❌ **Your own cheap math hidden behind an API route**
```ts
// app/api/calculate/route.ts — pointless network hop; the math has no secrets and is cheap
export async function POST(req) { /* ...the bmi math inline... */ }
```

✅ **API route for an *external* fetch (the legit use)**
```ts
// app/api/product-image/route.ts — proxy/scrape/quote a third party, SSRF/size/type-guarded
export async function GET(req) { /* validate host → fetch upstream → return */ }
```
Mutations → server actions; reads → server components; **API route handlers are for external/integration endpoints** (image proxy, scraping, third-party quotes), not for wrapping your own domain logic.

✅ **Schema as a TS string export (binary-safe)**
```ts
// src/db/schema.ts
export const BASE_SCHEMA = `CREATE TABLE IF NOT EXISTS items (...);`;
```

❌ **Schema read from disk at runtime (ENOENTs next to a shipped binary)**
```ts
const schema = readFileSync(join(process.cwd(), "src/db/schema.sql"), "utf8"); // breaks in the packaged app
```

✅ **Exact quantities: base units at the boundary, major units in the core**
```ts
createItem({ weightGrams: Math.round(kilograms * 1000) });   // store
const kilograms = row.weight_grams / 1000;                   // read, then hand to the core
```

❌ **Exact quantity stored as a float**
```ts
createItem({ weight: 1.37 });   // float drift; store exact quantities as scaled integers
```

✅ **Relationship assembled in the loader, core stays pure**
```ts
// lib/projects.ts — loader composes the aggregate; one batched count, no N+1
export async function loadProjectDetail(id: number): Promise<ProjectDetail> {
  const db = getDb();
  const project = requireProject(db, id);
  const tasks = listTasksByProject(db, id);     // single scoped query
  return { project, tasks, summary: summarizeProject(project, tasks) }; // pure core gets the assembled shape
}
```

❌ **Core follows the relation into the DB (and N+1s)**
```ts
// src/project/summary.ts — pure core must not import the db or query per-row
function summarize(project: Project) {
  const tasks = getDb().prepare("SELECT * FROM tasks WHERE project_id = ?").all(project.id); // wrong layer + N+1
}
```

## Gotchas

- **Foreign keys default OFF in node:sqlite** — they're a *per-connection* PRAGMA, not a schema property. Run `PRAGMA foreign_keys = ON` in `openDatabase()` before any query, or `ON DELETE CASCADE` and orphan-rejection silently do nothing.
- **A manual cascade delete alongside `ON DELETE CASCADE` isn't dead code** — even with the pragma on, an explicit child-delete inside the same transaction is a defensible belt-and-suspenders: it protects against a future code path that opens a second raw connection without setting `foreign_keys = ON`. Rely on the FK cascade as the primary mechanism, but don't flag the redundant explicit delete as a smell to remove.
- **Open the DB hardened, once** — in `openDatabase()` set `journal_mode = WAL`, `busy_timeout = 5000`, `synchronous = NORMAL`, `foreign_keys = ON`, and cache the connection on `globalThis` (`globalThis.__db ??= …`). Without WAL + busy_timeout a read racing a write throws `SQLITE_BUSY`; without the globalThis guard Next's dev HMR reopens the file → "database is locked". See references/ARCHITECTURE.md.
- **`node:sqlite` breaks vitest/Vite** — it's a runtime builtin but NOT in `module.builtinModules`, so Vite mangles the specifier. Redirect `node:sqlite` to a tiny `createRequire` shim via a `pre` resolve plugin in `vitest.config.ts` (test-only; prod imports it directly). Also alias `@/*` → repo root there.
- **Schema must be an inlined TS string**, not a `.sql` file — `readFileSync(process.cwd()/...)` ENOENTs next to a packaged binary.
- **No `db.transaction()` in node:sqlite** — write a `runInTransaction(db, fn)` wrapper (`BEGIN IMMEDIATE`/`COMMIT`/`ROLLBACK`); better-sqlite3's helper doesn't exist here.
- **Migrations:** track `PRAGMA user_version`, run on boot. Run each `up()` + its `user_version` bump in *one* transaction (no half-applied state); a fresh DB runs `BASE_SCHEMA` then jumps `user_version` to the max (skipping migrations); keep each migration idempotent (`CREATE IF NOT EXISTS`, guarded `ALTER ... ADD COLUMN`).
- **`params`/`searchParams` are async in Next 15** — `await` them in page components (`const { projectId } = await searchParams`); sync access type-errors and breaks the FK-prefill pattern.
- **`requireX` should call `notFound()`** (`next/navigation`), not throw a plain `Error` — otherwise a bad `[id]` serves a 500 instead of a 404.
- **Compound Mantine components are client-only** — rendering `Table.*` / `Accordion.*` from a server component throws. Fetch on the server, pass plain rows to a `'use client'` child.
- **Wizard/tab state resets mid-flow** unless you hoist shared derived state into a context provider *above* the steps — selections and computed results must survive Next/Back.
- **Derived aggregates silently undercount** — a roll-up (e.g. "total used") must account for *every* contributing source, not just one type. Build a fixture that would catch it, and expose the number via the collapsible math so it's auditable.
- **Forgetting `force-dynamic`** on a data route serves a stale snapshot — local-first reads should be dynamic.

## Troubleshooting

- **Packaged binary is ~750MB** — you compiled the repo root; compile the **standalone `server.js`** instead so only the slim node_modules embeds (~115MB). See references/PACKAGING.md.
- **Hydration mismatch on theme/colors** — the color hook must follow Mantine's *computed* color scheme and resolve after mount, not read OS `prefers-color-scheme` at SSR time.
- **`deno desktop` reuses a stale `.next`** — always `next build` first; compile needs `-A` (else Next throws `NotCapable` on `process.env`).
- **Chart looks alarming/wrong** — you're probably comparing different units on one axis or forcing a $0 baseline; see references/UI.md.

## Integration

- **color-system** — supplies the role-mapped palettes + contrast verification for the chart/theme module here.
- **typography** — sets the readability floor (size/weight/contrast/line-height) referenced above.
- **ideal-react-component** — the component structure for the `'use client'` UI layer.
- **frontend-design** — builds the actual layout/visual design; this skill decides architecture + data flow.
- **track-roadmap / track-session** — drive the feature-by-feature build: plan features, discuss via questions, then implement and verify.
