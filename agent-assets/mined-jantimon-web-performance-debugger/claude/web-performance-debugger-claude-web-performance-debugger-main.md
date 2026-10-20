# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`wpd` (package `@jantimon/web-performance-debugger`, bins `wpd` / `web-performance-debugger`) is a
TypeScript CLI that drives Chrome or Firefox via Puppeteer to **attribute layout/paint/style/
invalidation work back to source lines**, plus **CPU sampling** (on by default) that attributes
self-time to source/package. One user-facing axis picks where it runs: `--target chrome|firefox|node`.
Trust tiers, keep them straight: **counts** (trace-derived, windowed to the renderer main thread) are
exact; **slice ms** on a `--breakdown` bar and **wall/INP** are wall-tier directional (trace
`base::TimeTicks` / Chrome-clamped `performance.now()`); **CPU self-time** comes from the profiler's
own microsecond clock (*not* `performance.now()`), so its ms are a real signal, trustworthy in
aggregate (sampling noise ~few %). So it is not a wall-clock benchmark runner, but it *is* the right
tool for comparing JS cost (e.g. SSR `renderToString` lanes).

**`selfMs` is not "pure JS" on the browser lanes.** It is JS *plus the synchronous engine work JS
triggered*: a forced layout lands as self-time on the line that forced it (measured: ~85% of the
forced-layout probe's "JS" self-time is reflow). Only `--target node` (no DOM) measures pure JS.
This is a feature — it prices "delete this line" — but do not describe it as pure JS.

Read `README.md` for the user-facing surface; this file is the internal map; **`docs/dev/` holds the
measured facts behind the non-obvious choices** ([index](docs/dev/README.md)) and is the first stop
before changing the capture modes, the Gecko converter, or any cross-engine claim.

## Commands

```bash
npm run build           # tsc -> dist/ (ESM, NodeNext)
npm test                # unit only (pretest builds first); pure functions, no browser
npm run test:e2e        # e2e: drives the real CLI against headless Chrome (record -> query)
npm run lint            # oxlint src test scripts examples   (lint:fix to autofix)
npm run format          # oxfmt --write (format:check to verify; config in .oxfmtrc.json, ~prettier)
npm run knip            # dead exports/files/deps (config knip.json); a fresh dead export fails it
node dist/cli.js <...>  # run the CLI (installed bins: web-performance-debugger, wpd)
npm run changeset       # add a changeset; CI Release workflow versions+publishes on merge to main
```

CI (`.github/workflows/ci.yml`, Node 24) gates every PR (lint → format:check → build → knip → unit →
serial measurement, plus a browser-free `pack-smoke` and a Chrome `e2e`); a `release` job publishes
only on a green push to main. Firefox e2e runs nightly, not per PR. Four test lanes, and their
semantics matter:

- **unit** (`test/unit/*.test.mjs`) exercises pure functions against compiled `dist/`, no browser.
- **measurement** (`test/measurement/`, `npm run test:measurement`) is the browser-free `--target node`
  lane that RECORDS a real CPU profile, so it **runs serially** (`--test-concurrency=1`): a parallel
  worker competing for the CPU can inflate a near-no-op recording past a gate floor
  (docs/dev/measurement-ecosystem.md: never measure concurrently on one host).
- **chrome e2e** (`test/cli.e2e.test.mjs`) spawns the built CLI against real headless Chrome.
- **firefox e2e** (`test/firefox.e2e.test.mjs`) drives the gecko lane.

Each e2e suite **self-skips when its browser is absent** so `npm test`/`ci` stay green without one;
`WPD_E2E_REQUIRED=1` (chrome) and `WPD_E2E_FIREFOX_REQUIRED=1` (nightly firefox) make a missing browser
a hard failure so the e2e jobs can't silently pass. Grep the test dirs for a feature's coverage.
The broader smoke tests below stay manual (always `npm run build` first — the CLI runs `dist/`):

```bash
node dist/cli.js record examples/forces-layout.mjs --bench --iterations 5  # in-page; forced-layout detection
node dist/cli.js query blame latest --forced                        # source-attributed thrashing
node dist/cli.js record examples/counter-steps.mjs --url examples/react-counter/dist/index.html  # driver (default)
node dist/cli.js query spans latest                                 # per-span overview (run + steps)
node dist/cli.js query span latest "add rows"                       # one span's full anatomy
# examples/react-counter is a Vite app: cd examples/react-counter && npm install && npm run build (needed once for --url)
```

## Architecture

Flow: **`record` produces a `Recording` (model/recording.ts) → `query`/`assert`/`diff` consume it.**
`src/cli.ts` (commander) is the only entry point and wires every command; `cli-validation.ts` holds
the one numeric-validation policy (parsers that throw `InvalidArgumentError` at the argument boundary
before any browser launches).

The model lives in `model/`, one file per domain (open the file for its types). `recording.ts` is the
`Recording`/`Span`/`Breakdown` core AND a BARREL that re-exports the domain files (`events.ts`,
`cpu.ts`, `frames.ts`, `attribution.ts`, `meta.ts`, `sourcemap-meta.ts`), so `../model/recording.js`
stays the one import path. Alongside: `driver-step.ts` (the driver→steps contract), `marks.ts` (the
`wpd:*` mark namespace), `time.ts` (clock/us↔ms helpers), `host-cpu.ts` (`meta.hostCpuIndex`, a
comparability fact, **never a normalizer**), `measured.ts` (the `Measured<T>` not-measured-vs-0 honesty
wrapper), `reconcile.ts` (slice-sum-vs-wall residual), `span-merge.ts` (`mergeSpanOccurrences`:
collapse a repeated `measure` label to its lower-median-by-wall occurrence, verbatim), `span.ts`/
`spans.ts` (stored `Span` projection + the `query spans` adapter), `capture-mode.ts` (predicates over
`meta.capture`), `artifact.ts` (the schema-version + shape gates **every reader passes through**),
`query.ts` (the `--format json|toon` view shapes, kept OFF the stored types so the JSON contract cannot
silently drift), `compat.ts` (`comparabilityMismatches`: the axes that make a `diff` gate meaningless,
so it **refuses** rather than fabricating a pass/fail), and `group.ts` (the pure **run-group** manifest
+ `formationVerdict`/`pickMember`/`countDisagreements`; the fs writer/runner is `record/group.ts`, the
consumer primitives `commands/group.ts`).

`record` orchestration lives in `src/record/`: `options.ts` (`RecordOptions`, the internal flags
shape), `capture.ts` (`captureFor` picks the ONE capture mode + `capabilitiesFor`/`blameSemanticFor`/
`countScopeNote`), `page-option.ts` (`PageResolution`: resolves `--url` to a URL to navigate or a local
file to serve), `runpass.ts` (runs that one capture), `artifacts.ts` (serialization), `spans-build.ts`
(assembles `Span[]`), `breakdown-spans.ts` (per-span bar assembly, FIFO measure pairing, then
`mergeSpanOccurrences`), and `notes.ts` (`meta.notes`).

### Two execution modes (this is the central design fork)

`record` has two fundamentally different ways to run the user's module, with **different `run`
contracts** — keep them straight:

- **Driver mode** (default): the module runs *in Node* and `run({ page, ctx, measureStep })`
  drives the page via Puppeteer. Implemented by `browser/driver.ts`. Steps are defined by
  `measureStep(label, action, { until })`; each becomes a `kind: "step"` span on the one recording.
  Per-step INP is captured via an injected Event Timing `PerformanceObserver`, and per-step Long
  Animation Frames via an injected `long-animation-frame` observer (`summarizeLoaf` -> `Span.loaf`,
  Chrome-only, ungated by any capture cap, so it attributes a step's slow frames to scripts even on
  the default capture mode). Both observers are in-page, not CDP. `browser/until.ts` `waitForStable` is an
  opt-in `until` for streamed/soft navigations the default settle ends before. A
  `page.goto` inside a `measureStep` is traced, so a navigation step measures a cold boot.
- **Bench mode** (`--bench`): the module is served over http and `import()`'d *inside the
  browser*; `run(ctx)` gets no `page` handle (there is nothing to drive from inside) but has live
  `document`/`window`, and `--url` still supplies the host page. Implemented by
  `browser/harness.ts` (a function serialized into `page.evaluate`) + `browser/server.ts` (a
  temp static server — ESM `import()` can't use `file://`, and the blank host page is served
  same-origin to avoid cross-origin import). It measures only `run()` (page load/boot is
  excluded). The CLI sets the internal `RecordOptions.driver` to `!bench`.

`--iterations`/`--warmup` repeat `run()` in **both** modes: the mode that measures real interactions
needs a statistical footing as much as bench does. Driver labels are unique **within an iteration**,
not within the run: the repetitions are a label's samples, so
`mergeSteps` groups by label and each step reports the median of its own. That is also why
`DriverStep` carries `markIndex` separately from `index` -- the trace needs a name that is unique
per pass, while `index` is the step's stable position within an iteration.

Modules/HTML must live under the cwd (the static server is rooted there). `--url` names the host page
(a live URL or a local HTML file, `page-option.ts`). A module + `--url`
runs the module against that host; a module + no `--url` runs it against a blank page. **No module +
`--url` is the zero-authoring on-ramp**: the built-in load flow navigates to the target inside one
`"load"` step and settles, so the recorded window is the page's own cold boot (`runpass.ts`,
`driver.ts`). No module and no `--url` errors.

`browser/launch.ts` launches Chrome **sandboxed by default**; a sandbox startup failure is re-thrown
as guidance naming the opt-in (`--disable-browser-sandbox`, for containers/restricted CI), never a
silent unsandboxed retry (`isSandboxLaunchError`/`sandboxLaunchError`). A transient cross-process boot
failure (`net::ERR_INVALID_HANDLE`, "detached Frame", common on a heavy `--url` boot) IS retried, on a
fresh browser, up to a bounded limit (`retryTransientNav`); `notes.ts` records that the numbers are
from the successful attempt.

### One capture per run: the capture modes (why numbers are trustworthy)

Every invocation is **exactly one capture pass** — one browser launch, one run of the flow, one
recording. `record/capture.ts` `captureFor(opts, browser)` picks the ONE `CaptureConfig` (categories,
cpu on/off, keepThreadIds, gecko) from the flags; there is no multi-pass plan and no pass windowing.
`meta.capture` is the scalar naming the capture mode. The chrome capture modes:

- **default** (no flag) — `categories: null` (no trace), CPU sampler on. The four-slice CPU bar, no
  rendering counts, cleanest wall (~1%).
- **`--breakdown`** — light trace (`breakdownTraceCategories()`: the shipped set MINUS `.stack`, MINUS
  `invalidationTracking`, plus gc, plus `v8.cpu_profiler`, `keepThreadIds` on). CPU samples come from
  the trace's `v8.cpu_profiler` ProfileChunk stream (`trace/profile-chunks.ts`), **not** the CDP
  sampler (no CDP profiler runs here), so they are continuous across a cross-document navigation: a
  navigating driver step keeps its CPU attribution. `trace/breakdown.ts` tiles the reconciling
  `js·style·layout·paint·gc·other·idle` bar per span, and layout/style/paint counts come out exact.
  The forced COUNT needs `.stack` (unavailable here), but forced-layout BLAME is available: the read
  that forced each flush is sampled from the stream's per-sample `data.lines` executing line
  (`trace/sampled-blame.ts`), the same flush-site semantic `--deep` reads exactly.
- **`--deep`** — full trace (`.stack` + `invalidationTracking`), sampler OFF. The attribution report:
  forced-by read-sites, dirtied-by writes, the thrash detector, invalidation rollup, exact counts,
  long tasks. No CPU model, and slice DURATIONS are suppressed (see below).

Firefox is one gecko pass at every capture mode (`gecko`/`gecko-deep`); node is the in-process `node-cpu`
lane. The capture modes are mutually exclusive (`--breakdown --deep` is rejected: two questions, two
invocations), and the CLI rejects `--breakdown` on firefox/node. There is no sampler-free wall mode:
the sampler's ~4-7% cost is systematic and cancels in `diff`/`cpu-diff`, so absolute-wall benchmarking
is a signal wpd does not measure. `--precise-wall` is retired -- an early `program.error` names the
migration (the CLI stub sunsets by the stated policy, not this schema bump).

**Why the split, present-tense [measured] constraints** (docs/dev/cpu-profiling.md):

- **The CPU sampler must NEVER ride a `.stack` trace.** `disabled-by-default-devtools.timeline.stack`
  makes Blink walk the JS stack on every Layout, and the sampler bills that walk to the JS frame that
  forced the layout — the same frame the real forced-layout cost lands on, inflating self-time
  **+21%**. So the sampler rides only the light no-`.stack` trace (`--breakdown`) or no trace
  (default); `--deep`, which needs `.stack`, runs the sampler OFF.
- **The light `--breakdown` trace costs ~2-5% wall** over sampler-only and leaves sampled self-time
  clean (+0-1%), which is why one fused pass is honest.
- **`--deep` suppresses slice ms.** The `.stack` trace inflates real style recalc up to **+38%**, so a
  `--deep` recording reports `layoutMs`/`styleMs`/`paintMs` and any bar as `null` (`durations: false`
  in `capabilitiesFor`); it leads with identities + exact counts, and shows span wall (honest window
  width) only.

**Counts are trace-derived, main-thread windowed.** There are no CDP/`getMetrics` counters (`cdp.ts`
holds only the profiler calls). `metrics/summarize.ts` sums `Layout`/`UpdateLayoutTree`(-parse)/
`Paint` on the renderer main-thread pid/tid the breakdown bar tiles (`trace/main-thread.ts`), which
reproduces the top-process scope (an OOPIF's own-process count is a separate off-thread count,
never summed). A `--url` boot navigates the blank host page to the target on a NEW renderer process,
so `wpd:run:start` lands on the pre-navigation renderer; `main-thread.ts` **re-anchors** to the thread
that carried the post-navigation work (and `notes.ts` says the counts describe the loaded page, not
the blank host). `layoutMs`/`styleMs`/`paintMs` are now **wall-tier** trace `base::TimeTicks` ms (~1%
directional), valid only on the light trace. Because every invocation is one pass that runs every
iteration for the wall samples, a counting capture mode's counts **total across `--iterations`**
(`countScopeNote` says so); a driver step's counts window to iteration 0 (`labelWindows`), so per-step
counts stay one iteration's work. Bench `wallMs` is the **sum of the timed samples**, not a window.

**The artifact is one file (schema 5).** `Recording` = the collapsed `Span[]` (the run window, each
driver step, and every user `performance.measure`) + meta. **The `spans[]` is the SOLE count/timing
store**: the run-level counts, wall, INP, longest-task and per-iteration stats live on the run span
(`kind: "run"`), each driver step on its own step span -- there is no `summary` object. `assert`/`diff`/
the record report read the run span (`model/span.ts` `runSpan`) and `meta.jsSelfMs`; `summarize.ts` still
produces a build-time `RecordingSummary` struct to fill those spans, but it is never serialized. Siblings: the raw
`.cpuprofile` and the resolved `.cpu.json` `CpuModel`. The classified `events[]` DEEP EVENT LOG is
written INTO the recording only under `--deep` (chrome) and firefox — every other capture mode leaves it
empty, which keeps the default artifact digest-sized. `model/artifact.ts` REJECTS any artifact whose
`meta.schemaVersion !== SCHEMA_VERSION` with a re-record message rather than mis-parsing it. A
`measure` label emitted every `--iteration` recurs, and `mergeSpanOccurrences` reports the
lower-median-by-wall occurrence VERBATIM (`aggregation: "median"`, `samples`, `wallMin/MaxMs`), never
a per-slice average, so the bar stays a real reconciling sample.

### Trace pipeline (trace/)

`parse.ts` (raw trace JSON → `NormalizedEvent[]`, `findWindow`/`findSteps` locate
`wpd:run`/`:step:N` marker windows; `keepThreadIds` keeps `pid/tid` for the breakdown pass only) →
`classify.ts` (event name/category → `EventKind`:
layout/style/paint/composite/invalidation/scripting/gc/task/usertiming/other) → `stacks.ts`
(rewrites trace stack URLs back to local source paths; **async** because it resolves bundle
frames through sourcemaps via `sourcemap.ts`) → `analysis.ts` (`markForced`, `forcedLayouts`).
Alongside: `taxonomy.ts` (the `EventKind` → work-slice map
and paint classification), `main-thread.ts` (picks the renderer main-thread `pid/tid` the counts and
the bar share), `steps.ts` (per-step windowing/merge), `frames.ts` (the off-thread frame side track
parsed from the already-enabled `devtools.timeline.frame` category — display-only,
[rendering-counts.md](docs/dev/rendering-counts.md)), `scope.ts` (per-flush layout/style scope from
the event `args` — dirtyObjects/elementCount, a p50/max distribution per span, NEVER a sum), and
`breakdown.ts` (the `--breakdown` engine:
`(trace events, profile samples, window) → Breakdown`, disjoint main-thread self-time tiled
`js/style/layout/paint/gc/other`, `idle := window − Σ`).

**The `--deep` attribution pipeline** reads the full-trace event log two ways. `thrash.ts`
(`analyzeThrash`) is the chrome dual annotation: per top-level task in `ts` order, it pairs each
forced flush (a `layout`/`style` event with a resolved read-site `.stack`) with the WRITE(s) that
dirtied it since the last flush (the `invalidationTracking` records), matching invalidation kind to
flush kind ([measured] 42 of 43 forced flushes on the probe). It yields both the per-read `dirtiedBy`
map (surfaced under `query blame --forced` and `query span`) and the `ThrashReport` interleave
(write→read→write→read, the run-span thrash count). `firefox-dirtied.ts` (`firefoxDirtiedBy`) is the
firefox `--deep` counterpart: Gecko cause stacks carry the write natively but only the FIRST
invalidation since the last flush, so it emits a `first-invalidation` `DirtiedByWriteRollup` (no
forced-by, no thrash — blame-semantics.md's never-fake-parity rule), reachable via `query blame
--dirtied`.

**Forced-reflow detection** is the key feature and depends on a non-obvious config: layout/style
events only carry a JS stack when JS forced them synchronously, and capturing that stack requires
the `disabled-by-default-devtools.timeline.stack` category in `trace/categories.ts`. `markForced`
flags layout/style events that have a resolved user stack (`e.at`).

Two things this rule is **not**, both documented in
[docs/dev/blame-semantics.md](docs/dev/blame-semantics.md):

- **Not DevTools' rule.** DevTools ignores the stack entirely and requires nesting inside a JS
  invocation event *plus* a >=30ms per-task aggregate. Ours flags cheap forced layouts DevTools
  stays silent on — defensible for a CI gate, but do not describe it as "what DevTools does".
- **Firefox reaches the same read site by a different route.** Chrome's `.stack` names the geometry
  **read** at the flush. Firefox has no such stack, so `query blame --forced` samples it: a
  DOM-accessor label frame over a Layout-category flush, attributed to the nearest JS ancestor's
  executing line + the property name. Same read-site semantic, comparable at line granularity, but a
  sampled estimate (cheap reads can be missed, the line can lag one statement). Gecko's marker
  **cause** stack names the **write** instead, so it is kept off `blame` (reachable via `query get`
  under `args.data.invalidationStack`), never the `--forced` answer.

### Output & consumption

- `metrics/summarize.ts` builds the internal (never-serialized) `RecordingSummary` struct from trace
  events alone (counts main-thread windowed, durations wall-tier on the light trace, `Measured` null
  where the capture mode observed nothing); `spans-build.ts` reads it into the run/step spans.
- `commands/query.ts` = 6 verbs: `spans`, `span`, `events`, `blame`, `get`, and the `--dirtied` mode
  of `blame` (plus `cpu`/`frame` in `commands/cpu.ts`); `commands/query-view.ts` renders each verb's
  view shape into the human report. `query spans` (via `model/spans.ts`) is the
  compact **overview**: a read-only OUTPUT ADAPTER that folds whatever bar a recording already holds
  (seven-slice `SpanBreakdown` or four/six-slice `CpuBreakdown`) onto one `UnifiedSlices` shape — no
  new stored type — surfacing each span's `aggregation` (`first`/`sum`/`median`) and, for a merged
  measure, its `samples`/wall spread. **`query span <label>`** is the drill-in: one span's full
  anatomy (bar, wall/aggregation/spread, Measured counts, INP/interaction, the forced read-sites +
  dirtied-by writes + thrash rollup an event-log capture mode carries, and per-span hot functions on the
  CPU-sampler scripting axis — the run span from the sibling CpuModel, a `--breakdown` chrome
  step/measure or firefox measure span from stored top-K `SpanHot` refs joined to the model by id
  (`profile/span-hot.ts`; MEASURE-pooled, share-denominated, floor-suppressed, never the bar's `js`
  slice — docs/dev/cpu-attribution.md)). `<label>` is a bare label or a `kind:label` qualifier — span identity is
  kind+label, so a bare label matching more than one kind is a collision the caller resolves.
  **Agents/users should read `query spans` then drill with `query span`/`query get <id>`, not the
  multi-MB recording.** `assert.ts` gates the exact count thresholds (recording *or* per-step via the
  step spans in `model/step-view.ts`) AND per-slice budgets (`--max-slice <name>=<ms>`, parsed by
  `model/spans.ts` `parseSliceBudgets`, gating a target span's reconciling-bar slice ms; a slice the
  capture mode did not measure is a loud `n/a` FAIL, never a silent pass). `diff.ts` compares two recordings:
  the gated exact-count deltas plus advisory per-span slice-ms deltas (`diffSpanSlices`), matched by
  `kind:label`, with comparability warnings when a metric is measured on one side only.
- `commands/resolve.ts`: the `latest` keyword resolves via a **cwd-keyed** pointer file under the XDG
  state dir (`$XDG_STATE_HOME/wpd/pointers/<hash>.json`, else `~/.local/state/wpd/pointers/`) that
  `record` writes — so no `recordings/` dir is dropped into a consumer's cwd. **Never resolve
  recordings by mtime**. `resolveConsumption` is the group-aware entry: `latest` resolves to the group manifest
  when the pointer carries `group` (a group-forming record set it; a later non-group record cleared
  it), an explicit `.group.json` path is a group, and every other explicit path is a recording (so a
  member path always resolves to the recording). Group-aware verbs (`query spans`/`span`, `assert`,
  `diff`, `cpu`/`frame`/`blame`) branch on it, routing to a member via `pickMember` or stitching
  across members; a plain recording keeps its exact single-file path.
- `output/format.ts`: every output supports JSON or TOON (`--format toon`); recordings are
  read back auto-detecting the format. `output/ascii.ts`: terminal tables/sparklines (ANSI-aware:
  widths are measured by *visible* length via `output/color.ts`'s `visibleLength`, so colored cells
  stay aligned). `output/color.ts`: TTY-aware ANSI helpers; **disabled by default** (the library
  stays plain when called directly, so unit tests and programmatic/agent use get no escape codes).
  Only `cli.ts` opts in, via a `preAction` hook resolving the global `--color auto|always|never`
  (auto = `isTTY && !NO_COLOR`). Structured `--format` output never calls the helpers, so it
  is plain regardless. Color lives only in the human report/table builders (`commands/cpu.ts`,
  `commands/record.ts`): heat-colored `self %`, cyan packages, dimmed paths/source/secondary counts,
  bold headline numbers.

### Framework addons (optional, isolated)

Framework support (React today) is an **optional addon, never core**. All addon code lives under
`src/addons/react/` + `src/addons/react-dev/` behind ONE narrow interface, `model/addon.ts` `Addon`
(`{ name, pageInit?, enrich? }`), wired in `src/addons/registry.ts` `activeAddons(mode)`. The core
(`record`/`query`/`driver`) calls addons only through that interface + `addonPageInits`/`runEnrich`; it
imports no addon internals. `--framework off|auto` (default auto; `RecordOptions.framework`): `off`
resolves to no addons, so no addon code runs and no addon facts enter the recording (the `Span.addons`
slot stays absent); `meta.framework` records the resolved mode as a core fact either way.
An addon READS what the capture recorded and attaches facts to `Span.addons` (`{ react?: ReactFacts;
"react-dev"?: ReactDevFacts }`, fact types exported BY the addon modules, referenced from core only
through the slot); it never changes what is captured. `pageInit` installs a browser-lane in-page probe
before app code (the React `__REACT_DEVTOOLS_GLOBAL_HOOK__` detection hook + a per-step commit channel,
`runpass.ts` installs it via `evaluateOnNewDocument`; the driver reads the per-step channel). `enrich`
runs post-capture (record.ts `enrichAddons`, node.ts) over the built spans + CpuModel + event log.
`query span` renders a labeled `React (addon)` block; `SpanAnatomy.addons` mirrors it in JSON. The
measured facts behind the shapes are in [react-attribution.md](docs/dev/react-attribution.md); read it
before touching the hook, the anchor allowlist, or the TimeStamp classifier.

### CPU profiling (always on wherever a chrome capture samples; no opt-out)

For JS cost, the V8 sampling profiler runs bracketed around the timed window, its source set by the
capture mode (per the capture-mode list above): CDP `Profiler.start/stop` (`metrics/cdp.ts`, the only
calls left there) on the default mode, the trace's `v8.cpu_profiler` ProfileChunk stream
(`trace/profile-chunks.ts`, same `RawCpuProfile` shape, merging the per-process streams a navigation
splits) on `--breakdown`. It rides the ONE capture mode, never a pass of its own, and is **OFF on
`--deep`, where the sampler cannot ride a `.stack` trace (+21%)**. `profile/cpuprofile.ts` resolves the
raw `.cpuprofile` into a self-contained `CpuModel`
(per-function self/total + a thresholded call graph) **at record time** (the served-server URL is
ephemeral), reusing `makeSourceResolver` + `SourceMapResolver`. Self-time rolls up by **package**
(`packageRollup`, pnpm-safe) or **file** (`fileRollup`); `query cpu --by package|file|function` picks
the lens. Two files land: the raw `.cpuprofile` (DevTools/Speedscope) and `<base>.cpu.json` (the model
the verbs read). Verbs: `query cpu` (overview), `query frame <id>` (callers/callees), `cpu-diff`
(self-time deltas, noise-filtered). The narrative is [cpu-profiling.md](docs/dev/cpu-profiling.md); for
per-span CPU attribution (which spans carry samples, the hot list, sourcemap trust)
[cpu-attribution.md](docs/dev/cpu-attribution.md).

Non-obvious constraints:

- **CDP callFrame line/column are 0-based** (converted to 1-based in `resolveCallFrame`, unlike the
  1-based trace stack frames); puppeteer harness frames drop via `isToolFrameUrl`.
- **`SourceMapResolver` reads remote maps** (for `--url` sites) via the script's `sourceMappingURL`
  **or its `SourceMap`/`X-SourceMap` response header** (production builds often strip the comment, keep
  the header); once a map resolves, minification is irrelevant.
- **ONE resolver per run**, constructed in `record()` and threaded through `runPass`/`attachStacks`/
  `buildCpuModel`: it shares the fetch cache AND the **diagnostics**. Every `loadMap` records an
  outcome (`no-sourcemap-url`/`script-fetch-failed`/`map-fetch-failed`/`map-parse-failed`); a swallowed
  failure reads as "the feature does not exist" (minified names, one bundle-shaped bucket). So
  `record()` mutates `meta.sourcemaps` + pushes a note (WARNING only when 0 of N resolved) **after
  `buildCpuModel` but before any artifact is serialized** -- that ordering is load-bearing, since
  `meta` is shared by reference with every artifact.
- **An unmapped remote frame buckets by origin** (`(cdn.example.com)`), never `"app"`: blaming
  unmapped third-party code on the user's bundle is the mis-attribution `classifyPseudoUrl` guards
  against.
- Resolved local source paths are stored **relative to root** (`relativizeSource`, with a `/private`
  symlink fallback in `resolveOriginalSource`): portable recordings, stable `cpu-diff` joins across
  machines. `node:` builtins, remote urls, and paths outside root stay absolute, as do artifact
  back-pointers (so any cwd reopens them); the terminal report prints paths through `displayPath` so an
  absolute home path never leaks into a pasted report. On-disk numbers round to 4 decimals in
  `serialize`; the raw `.cpuprofile` stays exact. Display names prefer the sourcemap's `pos.name` over
  the minified V8 name (`CpuFunction.minified`), which also joins `cpu-diff` across builds.

**Node runtime (`--target node`)**: a CPU-only lane skipping Chrome. `runtime/node.ts` (`recordNode`)
imports the module *in this process* and profiles `run()` with node's built-in `inspector` Session
(`Profiler.start/stop`, same `RawCpuProfile` shape as CDP), bracketed around the timed loop. It reuses
`buildCpuModel` via `{ runtime: "node" }`, which swaps in `makeNodeSourceResolver` (rewrites `file://`
frames to local paths; `node:` builtins fall to the `(node)` bucket); the tool's own loop frames drop
via `isToolFrameUrl` (`/runtime/node.`). CPU-only means no rendering counts: `recordAndReport`
dispatches to `recordNode` + `printNodeReport` (CPU headline + per-iteration timing, no DOM tables).
The CLI errors on browser-only flags; the node lane is `workload.lane: "node"` (which `recordingRuntime`
derives `"node"` from), and `meta.capture` is `"node-cpu"`.

**Firefox backend (`--target firefox`)**: a second browser lane over WebDriver BiDi (no CDP).
`browser/backend.ts` `capsFor()` is a plain caps object (`cdpCounts/trace/throttle/cpuProfile/
geckoProfiler`) so `runPass` stays one function with capability guards, not a class tree.
`browser/launch.ts` returns `client: CDPSession | null` (null on firefox); every CDP call site is
gated by a cap or a null check, never `client!`, and `runDriver` takes a nullable client. Firefox has
**no** CDP trace, invalidationTracking, or throttling; the CLI errors on `--breakdown`/`--cpu-throttle`
and `meta.notes` says so loudly (never fake zeros). **INP is NOT in that list** -- it is an in-page
Event Timing observer in `driver.ts`, ungated by caps, and it works. `meta.browser` is `"firefox"`
(absent = chrome, so old recordings stay valid).

The lane is ONE gecko pass at every capture mode (`mode: "gecko"`, or `"gecko-deep"` when `--deep` adds
the dirtied-by write report — same capture, a reporting tier over it). The CLI refuses to turn the
profiler off here: the gecko pass is this lane's *only* source of CPU samples, layout/style markers,
the reconciling bar, AND read-site blame, so without it every rendering count reads 0. The browser
closes to flush a shutdown dump, which `waitForGeckoDump` polls to stable; the dump stays a **path** on
`PassResult` (never a retained string) and is `copyFile`d to the artifact, since a 16M-entry ring
buffer serializes to 16MB+ even for a trivial probe. `sampleIntervalUs` is read back from the dump's
`meta.interval` (what the sampler actually ran at), never hardcoded.

`profile/gecko.ts` converts the raw dump (v34) to a `RawCpuProfile` (fed to `buildCpuModel` unchanged)
plus `NormalizedEvent[]`: Reflow/Styles markers (kind layout/style, `forced` from a JS cause, driving
flush COUNTS — but NOT `forcedLayoutMs`, which is not-measured on every lane: the markers under-report
the forced subset **~7x** vs Chrome, `capabilitiesFor`'s `forcedDurations` is false, and the honest
total-layout duration is the reconciling bar's `layout` slice) and
**sampled read-site blame events** (`sampled:true`, the read line + property, driving `blame --forced`;
`summarize` skips them so they never double-count a flush; a sampled estimate that can lag one
statement). Launched `MOZ_PROFILER_STARTUP_FEATURES=js,cpu`: the `cpu` feature populates the per-sample
`threadCPUDelta`, whose ~0 values are the honest `idle` signal `computeGeckoCpuBreakdown`
(`profile/gecko-breakdown.ts`) tiles into a `js·style·layout·browser·gc·idle` bar. Firefox
`performance.measure` spans become per-span `Span`s carrying a `breakdown`, collapsed across
`--iterations` by the same `mergeSpanOccurrences`. Under `--deep`, `firefox-dirtied.ts` reads the
marker cause stacks into the first-invalidation dirtied-by report. `parseGecko` **throws** on a missing
`JavaScript` category or an empty thread list: both would yield an empty-but-valid model reporting ~0
scripting time, the fake zero this lane refuses. `isToolFrameUrl` also drops `/__wpd_blank__` (BiDi
attributes bench harness frames to the served host page). Fixture:
`test/fixtures/gecko-shutdown.trimmed.json`. Read [firefox-cpu.md](docs/dev/firefox-cpu.md) and
[gecko-profile-format.md](docs/dev/gecko-profile-format.md) before touching any of it.

## Conventions / gotchas

- ESM throughout: relative imports **must** use `.js` extensions in `.ts` source (NodeNext).
- Naming is standardized on **layout** (not "reflow") everywhere except the idiom *forced
  reflow*; **paint** (not "repaint"). Don't reintroduce the old names.
- The `EventKind` union (`model/events.ts`, re-exported by the `model/recording.ts` barrel so
  `../model/recording.js` still resolves it; mapped by `classify.ts`), the `wpd:*` mark namespace
  (`model/marks.ts`), and the trace category list (`trace/categories.ts`) are the coupling points
  across files; change each in its one home.
- **No single-letter identifiers, except the integer counters `i`/`j`/`n`.** Locals, params,
  `for...of`/`catch` bindings, destructured aliases, and sort-comparator params otherwise get
  descriptive names (`event` not `e`, `group` not `g`, `frame` not `f`, `(left, right)` not
  `(a, b)`). This holds even inside browser-serialized functions (harness/driver/settle), where
  names don't affect serialization. Exported names, type names, and object property keys are exempt.
  Enforced by the `local/id-length` oxlint rule (`lint/id-length.ts`, `min: 2`, `exceptions:
  ["i","j","n"]`, `properties: "never"`).
- **When more than one clock is in scope, a timestamp identifier names its clock** (`traceTs`,
  `pageNowMs`, `profileTs`), so a `* 1000` / `/ 1000` is never read for its direction. The unit
  conversions live in one place (`model/time.ts`: `usToMs`/`msToUs`/`cdpSecondsToMs`); use them
  rather than a bare factor.
- **No em-dashes or AI-prose in comments.** Use ASCII punctuation (`:`, `;`, `()`, `.`) and keep
  comments terse and technical; drop chatty tells (`à la`, `Best-guess`, `Nudge the engine`).
  The standalone `"—"` used as a missing-value placeholder in table *output* is allowed; to name
  that glyph in a comment, wrap it in backticks or double quotes (the rule skips quoted literals).
  Enforced by the `no-comment-slop` oxlint plugin (the released `eslint-plugin-no-comment-slop`
  package, wired through `jsPlugins`): no trailing period, no em-dash, no banner/separator comments,
  no foreign syntax (`///`, `#region`, XML doc tags), no inflated jargon, JSDoc (not `//`) for the
  comment documenting an export or a type/class member, and a one-line doc on every member once a
  type is mostly documented (three docs or 40% coverage). `no-trailing-comment` runs on `src`/`scripts` only (compact
  inline annotations stay in `test`/`examples`). `max-comment-lines` runs at a repo-tuned budget
  (10 lines, not the plugin default of 3) so the multi-line `[measured]` comments this repo keeps
  stay legal; a comment past 10 lines gets split into blank-line-separated sections.
- **No hedging endcaps.** Do not append an unrequested caveat, counterargument, or moralizing endcap
  to a sharp claim in a comment or doc merely to demonstrate balance. If a boundary condition changes
  the truth of the claim, put it in the mechanism or scope the claim correctly. If it does not, cut
  it. Accuracy belongs in the argument; model self-protection does not.
- **No archeology.** Comments and docs describe the code as it is now, never how it used to be.
  Cut past-tense narration ("used to", "was null before", "until 0.5.0", "the bug this fixes",
  "measured before this was fixed"), version/PR numbers used as rationale, and incident logs.
  **Keep every `[measured]` number and the prohibition it justifies** -- those are why the code is
  the way it is -- but phrase them as present-tense constraints: "Never run the CPU sampler on a
  `.stack` trace: it inflates self-time +21%", not "it had its own pass until 0.5.0".
  The test: would someone implementing this from scratch today still write the sentence? If it only
  makes sense as "here is what we changed", it belongs in the changeset and the PR description,
  which is where history lives. This applies to `docs/dev/` too: state the finding, not its
  discovery story.
- **Retirement stubs sunset by policy, not by mood.** A removed flag/verb keeps a hidden stub that
  fires a named migration error. The stub lives until TWO further breaking releases have shipped AND
  3 months have passed since its introduction (the commit adding its `program.error`), whichever is
  later; then it becomes a plain unknown-option error. Stated once here so no stub's lifetime gets
  re-argued.
- Per the user's global rule: use `trash`, never `rm -rf`.
- **`npm run knip` gates dead exports/files/deps** (`knip.json`). It reads `src` from `cli.ts` +
  `index.ts`; `index.ts` is the public surface (knip credits it as an entry). `ignoreExportsUsedInFile`
  keeps it to genuinely-dead symbols, not over-exports. Unit tests import compiled `dist/`, which knip
  cannot map back to `src`, so a pure function exported ONLY for a unit test reads as dead: mark such
  an export `@testOnly` (the `tags: ["-testOnly"]` filter clears it, and the tag says why it exists).
  A truly dead export still fails knip.
- **Commit messages carry no tooling attribution.** Do NOT append a `Co-Authored-By:` trailer, a
  `🤖 Generated with Claude Code` line, a `claude.ai/code/...` session link, or any similar
  advertisement to commit messages or PR bodies. Write the message as the change itself, nothing
  more.
- **Changesets are release notes, not design docs.** A changeset becomes a `CHANGELOG.md` entry read
  by someone deciding whether to upgrade: say what changed, what breaks, and what to do about it.
  Budget **~5 lines, ~15 for a breaking change**. The reasoning (why the bug existed, what was
  measured, what was ruled out) belongs in the PR description and the code comments, both of which
  outlive the changeset. Lead with **Breaking:** where it applies, and order a release's changesets
  breaking-first.
- **Stacked PRs for dependent slices, not as a default.** When one task splits into dependent,
  separately-reviewable slices -- a refactor a feature then builds on, a probe-backed fix plus the
  feature that consumes it -- stack the PRs instead of one giant PR or a manual restack after the base
  lands. A mini task stays one PR; unrelated changes stay independent PRs. Stack with the `gh stack`
  extension (`gh extension install github/gh-stack`, needs gh 2.90+ and git 2.20+): `gh stack init -b
  main`, `gh stack add <branch>` per slice, `gh stack submit` to open and link the chain -- each PR
  targets the branch of the PR below it (github.com and the mobile app drive the same stacks). Review
  is per layer: open any PR to see only its own diff. **Merge from the tip, squash method:** landing
  the top PR lands every layer below it in one operation, and squash gives each PR its own clean commit
  linked to that PR (bottom-up), so a 4-PR stack becomes 4 commits. The coordinator/maintainer merges
  the tip once every PR in the stack is green and reviewed. Every existing rule still holds: descriptive
  branch names, no attribution trailers, and one changeset PER PR that changes user-visible behaviour
  (same as today).
- **Cross-engine / profiling work**: `docs/dev/` ([index](docs/dev/README.md)) holds the measured
  facts the code depends on but cannot state itself. Read the relevant one BEFORE touching that
  code: `gecko-profile-format.md` (raw v34 schemas, marker phases, cause-stack encoding, line/col
  base) for the Gecko converter; `engine-mapping.md` (Gecko<->Blink names, what is actually
  comparable) before any cross-engine claim; `blame-semantics.md` (read-site vs write-site blame,
  the dirtied-by reports, the thrash detector) before touching `markForced`/`thrash.ts` or any blame
  claim; `cpu-profiling.md` (the capture modes, sampler contamination, what `selfMs` includes) before
  changing the capture modes or the interval; `cpu-attribution.md` (which spans carry CPU samples, per-span
  hot functions, sourcemap trust) before changing span-level CPU output; `firefox-cpu.md` (the
  Gecko profiler config and its honest idle) before touching the `MOZ_PROFILER_*` setup;
  `rendering-counts.md` (what each count counts, which ones reproduce, why there is no composite
  count) before adding a name to `classify.ts` or gating a count; `frame-floor.md` (the one-frame
  floor on `wall`/`INP`, and why the headless mode sets its height) before changing the headless
  option or adding a headless flag; `trace-buffer.md` (what raises the trace-buffer ceiling, what
  drops events, the incremental event-level parser, and the `--deep` event-log serialization ceiling)
  before changing `trace/tracing.ts`, `trace/scan.ts`, or the buffer size; `driver-timing.md` (what a
  step's `wallMs` times, the settle floor, the INP input/processing/presentation split) before
  touching `browser/driver.ts` or presenting a step's wall as a cost; `navigation-and-lcp.md` (whether
  LCP fires headless, the boot-entry race, the static/hard/soft step classification) before wiring an
  LCP number into a span; and `facts.md` (the ledger of load-bearing measured numbers + the files that
  must agree, checked by a unit test) before changing any pinned number. The scope/market files
  (`core-features.md`, `orchestrator-boundary.md`, `measurement-ecosystem.md`) inform user-facing copy,
  feature scope, and field comparisons rather than engine code.
- **Claims about engine behaviour need a probe, not a mechanism.** A plausible mechanism is not
  evidence, however obviously true it reads: sourcemaps, INP, Gecko cause stacks and sampler
  isolation all behave in ways a mechanism alone predicts wrongly. Run `examples/forces-layout.mjs`
  in both engines and look at the output before writing the sentence (`docs/dev/README.md` has the
  rule and its corollaries).

## Regenerating the README demo (`examples/demo-gif/`)

The README hero is a [VHS](https://github.com/charmbracelet/vhs) recording of the `--target node` CPU
lane over `examples/ssr-demo`. The tape, the render/publish steps, and the tape gotchas live in
`examples/demo-gif/` (`demo.tape` + `README.md` + a directory `CLAUDE.md`); the rendered `demo.gif` is
git-ignored and hosted via a GitHub user-attachments URL, so the npm tarball stays lean. **Read
`examples/demo-gif/CLAUDE.md` before you touch the tape.**
