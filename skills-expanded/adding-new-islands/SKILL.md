---
name: adding-new-islands
description: >-
  How to add a new built-in island to the OpenIslands monorepo end to end — first the
  interface/API design discipline and the .describe() copy conventions (the island is authored
  by an agent reading the schema, so the interface IS the product), then the exact file-by-file
  wiring: the schema registration points, the compiler binding-check, the runtime renderer +
  registry, the CLI skeleton, tests, and which docs are generated vs hand-edited. Use when adding,
  designing, reviewing, or naming a new island/chart/visual-block type, or when answering "how do
  I add an island to OpenIslands". The canonical worked example is the `divergence.bars` island.
---

# Adding a new island

An island is a stable, code-backed visual block with a typed config. An **agent** authors the
manifest by reading the island's schema and picking + configuring instances — it never writes
rendering code. So the schema and its `.describe()` copy ARE the product surface. Design the
interface first; the wiring is mechanical once the shape is right.

Before starting, read `CONTRIBUTING.md` ("Adding an island") and skim `packages/schema/src/index.ts`
to match the conventions of the nearest existing island. **Always copy a sibling**, not these
snippets — the real code is the source of truth.

## Part 1 — Design the interface (do this before any code)

1. **Name by intent, not by primitive.** Convention is `<intent>.<form>` (`category.bar`,
   `waterfall.bars`, `correlation.scatter`). The intent word must tell the agent *when to pick this
   island* and disambiguate it from neighbors — not describe the shape. Sanity-check the word for
   baggage: `divergence.bars` was chosen over `deviation.bars` because "deviation" reads as
   *standard deviation / error bars* in a data context.

2. **Happy path = one line.** Required fields are only those without which nothing renders
   (`dataset` + the bindings). Everything else is optional with a sensible default. An agent should
   get a working island from `{ type, dataset, <bindings> }` and refine from there.

3. **Make contradictory configs unrepresentable, not validated.** If two knobs can conflict,
   collapse them into one. (For `divergence.bars` a separate `colors` knob was dropped because a
   two-element `buckets` array already expresses a custom two-tone — one path, no XOR to police.)

4. **Declarative only — no computation in config.** Data shaping lives in SQL, never in the island.
   (`divergence.bars` has no `baseline` field: diverge-from-target is a `value - target` subtraction
   the author writes in SQL.) If you're tempted to add an `operation`/`formula`/`compute` field,
   stop — that field belongs in the data layer.

5. **No "just in case" knobs.** Every optional field is more surface the agent must learn and more
   error cases. Ship the minimal set; add fields later, backward-compatibly, when a real use case
   appears.

6. **Bind only to fields that exist.** Every prop that names a dataset column is checked by the
   compiler (Part 2, step 2) so `validate` fails loudly and names the island. That check is the
   safety net — keep it honest, never route around it.

## Part 2 — Write the `.describe()` copy (the agent reads only this)

- **Type description:** name the intent, give 2–4 concrete use cases, and *explicitly disambiguate
  from the nearest neighbors*. The pattern that works: "…Pick this over `category.bar` when values
  are signed and direction is the message, and over `waterfall.bars` when each bar stands alone
  rather than accumulating." Without the "pick this over X when…" clause the agent guesses.
- **Field description:** state the type, the semantics, and *what omitting it does* — "omit for a
  default green-positive / red-negative two-tone", "rows with a null value are skipped". State the
  default in the copy; don't make the agent infer it.
- Write for an LLM that is choosing and configuring, not for a human reading API docs.

## Part 3 — The wiring (every place to change)

The **schema is the keystone**: define it once, and the CLI, runtime, and compiler follow through
discriminated unions and `Record<IslandType, …>` maps — which fail to compile if you miss a spot.
That compile error is your checklist; `pnpm typecheck` enforces it.

### 1. `packages/schema/src/index.ts` — define + SEVEN registrations
- Define the Zod object next to its closest sibling (a chart → near `WaterfallBars`/`CategoryBar`),
  with `...baseFields` and a `.describe()` per Part 2; `export type X = z.infer<typeof X>`.
- Register the type in all six of these (each is keyed by `IslandType`, so a miss is a TS error):
  `BUILTIN_ISLAND_SCHEMAS`, the `BuiltinIsland` union, the `DrilldownIsland` union *(only if it may
  be embedded in a row drilldown — charts yes; full-page/editor islands no)*, and the three span
  maps `ISLAND_MIN_SPAN` / `ISLAND_MAX_SPAN` / `ISLAND_DEFAULT_SPAN` (charts are typically 4 / 12 / 6).

### 2. `packages/compiler/src/index.ts` — `islandRequirements()`
Add a `case "<type>":` that `add(...)`s every prop naming a dataset column. Literal config (color
thresholds, labels) adds nothing. This is what makes `validate` check bindings and name the island.

### 3. `packages/runtime/src/islands/<Name>.tsx` + `registry.tsx`
- New renderer mirroring a sibling: a **pure** data-shaping function (exported, so tests assert it
  without ECharts/DOM), a `buildOptions()` for the Kumo `<Chart>`, and the component. Reuse the
  shared helpers (`format.js`, `chart.js`, `SeriesLegend`, `isDateCategories`) — don't reinvent.
- Register in `registry.tsx`'s `REGISTRY` via `lazyIsland(() => import("./<Name>.js"), "<Name>")`
  (renderers are lazy-loaded — every chart pulls in echarts; the registry keeps it code-split).
  If the island binds no dataset, also update `islandNeedsData()`.

### 4. `packages/cli/src/scaffold.ts` — `islandSkeleton()`
Add a starter config (`dataset`/bindings = `"TODO"`). `scaffold.test.ts` asserts every built-in type
has a skeleton that passes validation, so a miss fails tests.

### 5. Tests
- `packages/runtime/test/<name>.test.ts`: assert the pure data-shaping function (boundaries, default
  behavior, null/missing handling, empty input). Mirror `waterfallBars.test.ts`.
- `packages/schema/test/index.test.ts`: add a parse case (minimal config + one exercising options).

### 6. Docs — hand-edited vs generated (DO NOT mix these up)
- **Hand-edit:** `docs/data-app-model.md` catalog row; `apps/docs/content/docs/islands/overview.mdx`
  row; `apps/docs/content/docs/islands/charts.mdx` (a new `## <type>` section with a `<LiveIsland>`
  example — copy the `waterfall.bars` block).
- **Generated — never hand-edit:** `apps/docs/content/docs/reference/manifest.mdx` is built from the
  schema. Run `pnpm --filter @openislands/docs gen:reference` (or `pnpm gen:reference` in `apps/docs`)
  to regenerate it; the island's section + field table come straight from your `.describe()` copy.
- **Skill source:** add the island to the catalog in `skills/openislands/SKILL.md` (the single
  source), then `pnpm sync:skill` to propagate to `templates/*/.agents`, `.mcp.json`, `AGENTS.md`.
  Never hand-edit the synced copies.

## Part 4 — Gate
```
pnpm build && pnpm typecheck && pnpm test && pnpm lint && pnpm validate:templates
```
`typecheck` catches a missed registration; `test` catches a missing skeleton; `validate:templates`
re-syncs the skill and checks every template manifest's bindings against live data. (Ignore oxfmt
`format:check` — it flags pre-existing files and is not a gate.)

## Worked example — `divergence.bars`
The diverging bar chart added via this exact process. Read these files as the canonical template:
- `packages/schema/src/index.ts` — search `DivergenceBars` (schema + the 7 registrations)
- `packages/compiler/src/index.ts` — search `case "divergence.bars"`
- `packages/runtime/src/islands/DivergenceBars.tsx` — pure `bucketColor`/`buildDivergenceBars` + renderer
- `packages/runtime/test/divergenceBars.test.ts` — the pure-function test
- `packages/cli/src/scaffold.ts` — its `islandSkeleton` entry

Design calls it embodies, as precedent: dropped a `baseline` field (diverge-from-target = SQL),
dropped a `colors` knob (a 2-bucket array covers it), chose half-open `[gte, lt)` buckets (no
boundary ambiguity), skipped rows with a null value (0 deviation ≠ no data).
