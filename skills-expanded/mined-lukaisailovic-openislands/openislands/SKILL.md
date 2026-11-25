---
name: openislands
description: Build and maintain OpenIslands data dashboards — typed manifests of visual islands bound to local files (CSV / JSON / Parquet / SQLite / markdown), edited safely over the OpenIslands MCP server in Code Mode (one `execute` tool you drive with JavaScript). Use whenever a project has apps/<id>/manifest.json or an .mcp.json naming the openislands MCP server, and you are adding or changing datasets, islands, pages, actions, queries, or connectors, fixing a validation or binding error, or authoring a SQL transform.
---

# Working with OpenIslands

Every OpenIslands project is a **workspace**. Apps live under `apps/<id>/`, each its own
**manifest** (`apps/<id>/manifest.json`) of reusable visual **islands** bound to **typed data
contracts** built from local files. A one-app project is just a workspace with one app. You edit
the manifest — never rendering code. The data stays in the app's files; `serve` queries them live.
The whole point is that the dashboard **fails loudly** when a binding and the data disagree, instead
of silently rendering a wrong number, so an agent can keep it healthy for months.

## Code Mode: one tool, driven with JavaScript

You make every change through the **OpenIslands MCP server** (`@openislands/mcp`, already wired in
`.mcp.json`). It runs in **Code Mode**: instead of a tool per operation, you call **one tool —
`execute`** — and pass it a small **async JavaScript program** that drives the `oi` API. Compose as
many steps as you like in a single call (loops, conditionals, chaining); `return` a value and/or
`console.log` what you want to see. The script runs in a sandbox — no `require` / `process` /
network, only `oi`. (`execute`'s own tool description carries the full `oi` TypeScript API — read it
once; the essentials are below.)

```js
const app = oi.app();                 // the sole app; oi.app("id") to pick one in a multi-app workspace
const ov = await app.getOverview();   // orient: manifest + live columns + actions/queries/connectors
console.log(ov.datasets);
return ov.title;
```

`execute` returns `{ ok, result, logs, checkpoints_created? }` (or `{ ok:false, error, logs }` if the
script throws). The server is a safety boundary: **read freely, write through one validated pipeline.**
Nothing is written until you apply a validated proposal, and every write is snapshotted for rollback.

Everything runs through `execute` — there are no separate per-operation tools. Reading `oi`'s methods
in the `execute` tool description is the fastest way to see the whole surface.

### The `oi` API (essentials)

`oi.listApps()`, `oi.createApp({id,title?})`, `oi.deleteApp({id})` are workspace-level. `oi.app(id?)`
returns the app-scoped API — **omit `id` when there's only one app**, else pass the `<id>` under
`apps/`. On the app:

- **Orient / read:** `getOverview({verbosity?})`, `getManifest()`, `getDataSchema(dataset)`,
  `runSql({sql?|dataset?,limit?,verbosity?})` (ad-hoc read-only SELECTs), `previewDataset(dataset)`
  (alias for `runSql({ dataset })` — the findable name for reading back a dataset), `validateSql(sql)`
  (dry-run a transform), `validateManifest(manifest?)`.
- **Island catalog:** `listIslands()`, `getIslandSchema(type)`.
- **Edit (read-many / write-one):** `patchManifest(patch)` (preferred — one section at a time) or
  `replaceManifest(manifest)` (full rewrite) → returns a `proposal_id` + a diff, writes **nothing** →
  `applyEdit(proposal_id)` writes it and returns a `checkpoint_id` → `rollback(checkpoint_id?)` undoes
  it. `listCheckpoints()` / `pruneCheckpoints(keep?)`.
- **Typed data:** `listActions()` / `runActions([{ action, rows? | match? | set? }], { atomic? })`
  (insert / replace / delete / update); `listQueries()` / `runQuery(name, params?, opts?)` (typed reads).
- **Connectors:** `listConnectors()` / `runSync(name)` (provider pulls).

Every method returns a JSON object carrying an `ok` flag — on `ok:false`, read `error` / `errors`
(each names the offending field) and fix it. The exception is `getManifest()`, which returns the raw
manifest object. Pass JSON **objects**, not JSON strings.

## The edit loop

Orient, ground the edit in the live contract, stage, apply — usually one script:

```js
const app = oi.app();
const ov = await app.getOverview();                 // 1. read
await app.getIslandSchema("metric.kpi");            // 2. ground (required fields, span range)
const page = ov.pages[0];
page.islands.push({ type: "metric.kpi", title: "Net worth", dataset: "net_worth_monthly",
                    value: "net_worth_eur", format: "eur", span: 4 });
const staged = await app.patchManifest({ pages: [page] });   // 3. stage (already validated vs the data)
if (!staged.ok) return staged.errors;               //    each error names the page/island/field
return await app.applyEdit(staged.proposal_id);     // 4. apply → checkpoint_id (rollback if wrong)
```

The stage step **dry-runs the result against the live data**. If `ok` is `false`, read `errors` (each
names the page, island, and field) and fix the edit. Do **not** work around a binding error — it is the
safety net. Prefer **`patchManifest`** over `replaceManifest`: it merges one section into the current
manifest, so you never re-send (or re-typo) the whole document.

You can do the whole loop in one script, or split it across several `execute` calls — a `proposal_id`
persists between calls, so you can stage in one and apply in the next.

## The manifest model

```jsonc
{
  "version": 1,
  "title": "My dashboard",
  "datasets": { "<name>": { "source": "data/x.csv" } },   // or { "sql": "models/x.sql" }
  "pages":    [ { "id": "overview", "islands": [ /* islands */ ] } ],
  "actions":  { "<name>": { "dataset": "<name>", "mode": "insert" } },   // optional, typed writes
  "queries":  { "<name>": { "dataset": "<name>", "select": [], "where": [] } },  // optional, typed reads
  "connectors": { "<name>": { "module": "connectors/x", "datasets": {} } }       // optional, external pulls
}
```

- **datasets** — a named map. Exactly one of `source` (a `.csv` / `.json` / `.parquet` / `.sqlite` /
  `.md` file) **or** `sql` (a path to a DuckDB transform). SQLite sources need a `table`. Source files
  live under `data/`, `models/`, or `docs/`.
- **pages → islands** — each island has a `type`, an optional `span` (1–12 grid columns), and type-specific
  fields. Data islands name a `dataset` and the columns they bind (e.g. `value`, `x`, `y`, `label`).
  A page uses either a flat `islands` array or tabbed `groups`, not both. A group is
  `{ id, title?, islands }` and renders as a tab (deep-linked via `?group=<id>`) — reach for groups
  to split a busy page instead of adding a second sidebar page.
- **actions** — declare a typed write (`insert` / `replace` / `delete` / `update`) into a writable
  dataset; run rows through `runActions`. The match predicate and new values for `delete`/`update`
  are passed at call time, not in the manifest.
- **queries** — declare a typed, parameterized read; run it through `runQuery`. No raw SQL in queries —
  heavy shaping lives in a `sql` transform the query reads from.

Don't put transforms inside island configs. **The manifest stays declarative; data shaping lives in the
SQL/data layer.**

## Discover the island catalog — don't guess

Island configs are the keystone schema and can change. Always ground an edit in the live contract:

- `oi.app().listIslands()` → every built-in type with its required fields, a one-line description, and
  its span range (`minSpan` / `recommendedSpan` / `maxSpan`).
- `oi.app().getIslandSchema(type)` → the full JSON Schema for one type, plus its `layout`
  (`{ minSpan, recommendedSpan, maxSpan }`) and `notes`. **Check this before setting `span`** — see
  [Layout & sizing](#layout--sizing).

Tabbed `groups` are **page** structure, not an island, so they **won't** appear in `listIslands()`
— their shape (`{ id, title?, islands }`) is in the manifest anatomy above.

Built-ins span metrics (`metric.kpi`, `metric.scorecard`), charts (`timeseries.line`, `category.bar`,
`category.combo`, `category.pie`, `waterfall.bars`, `divergence.bars`, `breakdown.treemap`, `correlation.scatter`,
`distribution.heatmap`, `compare.radar`, `map.choropleth`, `funnel.steps`), gauges (`gauge.goal`,
`gauge.rings`, `gauge.meter`), tables/feeds (`table.grid`, `timeline.feed`, `rank.list`,
`status.grid`, `activity.calendar`), content (`note.card`, `source.doc`, `content.editor`), input
(`search.box`, `form.entry`), and boards (`board.kanban`). Prefer a built-in; an unknown type renders a
placeholder until a custom renderer exists under `components/custom/`.

## Layout & sizing

Every island has a **min / recommended / max** span on the 12-column grid. Check
`oi.app().getIslandSchema(type)` (its `layout` + `notes`) before you set `span`:

- **Keep compact islands narrow.** KPIs, funnels, gauges, pies, and radars cap well below full
  width (e.g. `metric.kpi` and `funnel.steps` max out at 6, recommended 4) — past their natural
  size they only stretch into dead space. A `span` over the max is a **named validation error**.
- **Let data-dense islands go wide.** Tables, time-series, bar/combo/waterfall charts, heatmaps,
  treemaps, calendars, feeds, status grids, and maps run the full 12.
- **Omit `span` to get the recommended width** — the island renders at its natural size.
- **Don't ship a lone KPI.** Group 2+ KPIs in a row, or use `metric.scorecard` for a tidy strip.

`validate` and the edit methods surface **advisory layout warnings** (a `warnings` array on
`patchManifest` / `replaceManifest` / `validateManifest`) for these smells — a standalone KPI, a
compact island stretched past its recommended span. They never block the apply; treat them as a
nudge toward a tidier layout.

## Recipes

Each recipe is the body of a `execute` script (assume `const app = oi.app();` at the top).

**Add a chart to a page.** Read the current page, append the island, send just that page:

```js
const ov = await app.getOverview();
const page = ov.pages.find((p) => p.id === "overview");
page.islands.push({ type: "rank.list", title: "Top assets", dataset: "allocation",
                    label: "class", value: "value_eur", span: 6 });
const s = await app.patchManifest({ pages: [page] });
return s.ok ? await app.applyEdit(s.proposal_id) : s.errors;
```

A page in `pages` is **upserted by `id`** (same id replaces, new id appends). `remove_pages: ["id"]`
deletes one.

**Add a dataset from a file.** Put the file under `data/` (use your file tools), then bind it and check
its inferred columns in one script:

```js
const s = await app.patchManifest({ datasets: { crypto: { source: "data/crypto.csv", description: "holdings" } } });
if (!s.ok) return s.errors;
await app.applyEdit(s.proposal_id);
return await app.getDataSchema("crypto");           // confirm columns before binding islands to it
```

**Add a derived dataset (SQL transform).** Transforms shape data with DuckDB SQL. Author the SQL first
and dry-run it, *then* wire it in:

1. Write the file under `models/` with your file tools, e.g. `models/transforms/allocation.sql`:
   ```sql
   SELECT class, SUM(value_eur) AS value_eur FROM holdings GROUP BY class
   ```
2. Dry-run it inside a script:
   `return await app.validateSql("SELECT class, SUM(value_eur) AS value_eur FROM holdings GROUP BY class")`.
   You get back the result columns, or the **exact** DuckDB error (e.g. `Catalog Error: Table "holding" does
   not exist`). Fix it until it's valid. A transform can read any other dataset by its name.
3. Wire it: `app.patchManifest({ datasets: { allocation: { sql: "models/transforms/allocation.sql" } } })`.

**Add a typed write (action).** Targets a writable file dataset (CSV / SQLite), not a `sql` transform:

```js
await app.patchManifest({ actions: { log_txn: { dataset: "transactions", mode: "insert",
  description: "Record a transaction",
  fields: { amount: { type: "number", min: 0 }, kind: { type: "string", enum: ["in","out"] } } } } });
// ...applyEdit, then append rows:
return await app.runActions([{ action: "log_txn", rows: [{ amount: 50, kind: "in" }] }]);
```

Every row is validated all-or-nothing and the file is snapshotted for rollback. Flat-file
datasets (CSV) store no null — pass `""` for an empty value, or omit the field to use its `default`.

**Correct a value or delete a row.** Actions support `insert`, `replace`, `delete`, and `update`.
The match predicate and new values are passed at call time. An empty `match` is rejected:

```js
// correct a value, then delete a row — declare actions with mode "update" / "delete"
await app.runActions([{ action: "fix_meal", match: { id: "m-42" }, set: { protein_g: 30 } }]);
return await app.runActions([{ action: "delete_meal", match: { id: "m-42" } }]);
```

**Add a typed read (query).** Declarative, parameterized, no raw SQL:

```js
await app.patchManifest({ queries: { by_class: { dataset: "allocation",
  select: ["class", "value_eur"], params: { class: { type: "string" } },
  where: [{ field: "class", op: "eq", param: "class" }] } } });
// ...applyEdit, then run it:
return await app.runQuery("by_class", { class: "BTC" });
```

**Remove something.** In a record section, set the entry to `null`:
`app.patchManifest({ queries: { by_class: null }, actions: { log_txn: null } })`. For pages, use `remove_pages`.

**Connectors.** `app.listConnectors()` shows each connector's status. **Keyless** connectors
(`auth: none`) need no human action — call `runSync(name)` directly. For OAuth2/bearer connectors,
authorization is human-only (the Connect button in the running dashboard) — surface that to the user
if `connected` is false; don't try to sync. When connected, `app.runSync(name)` pulls into its
datasets (checkpointed).

## Rules that keep the app healthy

- **Validate is the contract.** A binding error names the page, island, and field — fix the manifest or
  the data, never silence it.
- **Bind only to columns that exist.** Use `getDataSchema` / `validateSql` to confirm columns before
  binding.
- **Sources stay under `data/` / `models/` / `docs/`.** Secrets (`.env*`) and `.openislands/` are
  off-limits.
- **Prefer `patchManifest`; pass objects.** Re-sending a full manifest is the easiest way to introduce a
  typo.
- **Files are the source of truth.** There is no static export — `serve` reads the files live and pushes
  updates over SSE as they change.

## Running it

```bash
npx openislands serve        # boots the live dashboard at 127.0.0.1:4321
npx openislands validate     # compiles + checks every binding against the data (names what's wrong)
```

`serve` refuses to boot an invalid manifest, so `validate` (or a failed `patchManifest`) tells you exactly
what to fix.
