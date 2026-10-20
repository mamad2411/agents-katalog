# backend/src/health

Tree-sitter-driven per-file metrics pipeline. Each file is parsed to an AST
(with universal regex helpers for languages lacking a grammar), run through
Halstead token counts and a Maintainability Index, and folded into a composite
0-100 health score plus a set of code "smells".

## Files

- `parser.ts` — shared runtime/grammar loads; `GRAMMARS` registers keys, WASM
  filenames, and extensions, deriving `grammarKeyForExt` and the loader map.
  Rejected initialization/load promises are evicted so later calls retry.
  One parser per grammar is pooled for the process/worker lifetime; callers
  of `getParser` must never call `.delete()` on the shared parser.
- `nodeKinds.ts` / `nodeKinds/` — per-language node-kind sets
  (function/branch/loop/etc.): `nodeKinds.ts` (`nodeKindsFor`) + `nodeKinds/base.ts`
  plus one file per language (`typescript.ts`, `python.ts`, `go.ts`,
  `csharp.ts`, `java.ts`, `ruby.ts`, `rust.ts`). Import from `./nodeKinds.js`.
- `decodeSource.ts` — `decodeSourceText(buf)`: BOM-aware byte → text decode
  (UTF-16LE/BE BOM → UTF-16, else UTF-8) run before analysis, so a UTF-16
  `.ps1`/`.cs` isn't analysed as NUL-interleaved garbage. Used by
  `watcher/fileAnalysis.ts` and `../scanner/readForAnalysis.ts`.
- `walker.ts` + `walker/` — shim plus the single AST pass producing a
  `FileAnalysis`; see `walker/CLAUDE.md`. `walker.ts` orchestrates the
  walk via a `context.ts` `WalkerContext` plus visitor helpers in
  `visitors.ts` (`handleComment`, `handleFunctionEntry`/`Exit`,
  `handleFileStructure`, `handleImportsAndStrings`, `handleAstSmells`,
  `handleExportTracking`, `updateComplexity`, `handleAwaitExpression`,
  `handleCallExpression`), which in turn delegate to the sub-passes
  `complexity.ts`, `depth.ts`, `functionRecord.ts`, `functionNames.ts`,
  `parameters.ts`, `docstrings.ts`, and `smells.ts`
- `halstead.ts` — operator/operand tokenization + Maintainability Index
- `universal.ts` + `universal/` — shim plus focused universal text helpers:
  `commentSyntax.ts` (per-language line/block comment markers),
  `lineCounts.ts` (line-kind counter), `strip.ts`
  (`stripStringsAndComments` lexer) + `stripRegex.ts` (its JS/TS
  regex-vs-division disambiguation), and `smells.ts` (regex/heuristic
  fallback-language smells)
- `analyze.ts` + `analyze/` — top-level `analyzeFile` entry point +
  `computeFromTree` orchestrator. `analyzeFile` owns every successfully returned
  parse tree and calls `tree.delete()` in `finally` after computation, even if
  `computeFromTree` throws. Published metrics/cache results must retain no
  AST/tree/node handles. For worker/watchdog boundaries see
  [watcher/CLAUDE.md](./watcher/CLAUDE.md) and
  [scanner/CLAUDE.md](../scanner/CLAUDE.md); backend WASM/worker memory concerns
  are distinct from browser-renderer OOM symptoms. Delegates to:
  - `analyze/language.ts` — `languageForExt` (extension → `HealthLanguage`)
  - `analyze/fallback.ts` — `analyzeFallback` + `DEFAULT_METRICS` (used for
    unsupported languages, oversize files, parser/parse failures)
  - `analyze/functionMetrics.ts` — `aggregateFunctionMetrics` (per-function
    rollups: complexity max/total, function length, param counts, docstring/
    boolean-param/mixed-sync-async tallies) and `computeCallGraph` (internal
    call density + god-function heuristic)
  - `analyze/smells.ts` — `assembleSmells` (table-folds AST smell tokens,
    magic strings, universal regex smells, and threshold-derived smells into the
    final `HealthSmell[]`)
- `crossFile.ts` + `crossFile/` — shim plus focused cross-file modules:
  `resolveImport.ts` (extension/index/alias/Python-relative resolution),
  `graph.ts` (thin orchestrator — edge construction, Tarjan SCCs,
  reachability, and dead-code classification, delegating to sibling
  `importGraph`/`cycles`/`reachability`/`deadCode` modules; see
  `crossFile/CLAUDE.md`), `roots.ts` (entry-point detection +
  `RESOLVABLE_IMPORT_EXTS`), and `apply.ts` (patch fanIn/fanOut/inCycle
  smells + the `deadCode` status back into `HealthMetrics`).
  The dead-code pass is reachability-from-roots, not raw `fanIn===0`, so dead
  islands/cycles and entry points classify correctly; it is deliberately kept
  out of `computeScore` (orphan status is a signal, not a penalty). Roots come
  from the scan (`scanner/scan.ts`) and the watcher (`crossFileAnalyzer.ts`);
  the `D` overlay consumes the result.
  - **Resolver accuracy (TS-first).** `resolveImport.ts` maps NodeNext
    `.js`/`.mjs`/`.cjs`/`.jsx` imports to TS twins and resolves `baseUrl` bare
    imports via `tsconfig.ts` (relative imports stay importer-relative).
    `walker/importEdges.ts` captures re-exports, string-literal
    `import()`/`require()`, all names in Python `import a, b as c`, and
    `pkg.name` candidates for `from pkg import name`. Python dotted imports
    resolve against importer ancestors. See
    [crossFile/CLAUDE.md](./crossFile/CLAUDE.md) for the resolver module map.
  - **Entry-point roots** (`roots.ts`): conventional filenames (`index`/`main`/
    `*.config.*`/tests/`.d.ts`), standalone process/CLI entries (`*-server`,
    `*.worker`, files under a `scripts/`|`tools/` dir — spawned by path, never
    imported), user `deadCodeEntryGlobs`, and package.json entry targets across
    all in-tree `package.json`s (`main`/`module`/`source`/`bin`/`exports` + file
    refs inside `scripts`).
  - **Dead-eligible languages** (`RESOLVABLE_IMPORT_EXTS` in `roots.ts`): only
    unreachable `.ts/.tsx/.js/.jsx/.py/.pyi` modules can be `dead`.
    Unreachable `.mjs`/`.cjs` remain `uncertain`: tooling/runtime assets loaded
    by path lack modeled import edges.
  - **Confidence guard** (`crossFile/deadCode.ts`, `classifyDeadCode`): applies
    only with ≥20 resolvable non-root files and `dead / resolvable > 0.7`.
    The population includes reachable and unreachable eligible files, excluding
    roots; `dead` counts files initially classified `dead`. On a trip, every
    `dead` becomes `uncertain`, `deadCodeStats.downgraded` is true, and
    `scanner/scan.ts` logs a warning. Fewer than 20 files or exactly 70% dead
    do not trip it.
  - **Cache coupling:** import extraction feeds the `(mtime,size)`-keyed health
    cache, which does NOT invalidate on analyzer-logic changes. Any change to
    edge capture / resolution MUST bump `CACHE_VERSION` in `cachePaths.ts` or
    existing projects keep serving stale `imports` (this was why the first cut
    showed most files dead).
- `crossFileAnalyzer.ts` — watcher-facing diff/broadcast wrapper around the
  cross-file pass. Coalesces a burst of file events into one trailing-edge
  pass (150 ms — each pass is a synchronous full-project O(V+E) walk on the
  main thread, so the window is what stops an agent writing files continuously
  from stalling HTTP/WS/pty relaying every few dozen ms). Memoizes the
  present-file `Set` alongside the root set (both invalidated by
  `invalidateRoots`, called on every add/remove/re-seed): reusing ONE Set
  identity across content-only passes is what lets the case-fold import index
  in `crossFile/resolveImport/caseFold.ts` (a WeakMap keyed by that Set) hit
  instead of being rebuilt per keystroke on Windows/macOS.
- `scoreMetadata.ts` — serializable source of truth for score component ids,
  ordering, weights, thresholds, and direction. The frontend health legend imports
  this file directly; do not duplicate score metadata in UI code.
- `scoreModel.ts` — backend-only adapter that adds metric extractor functions to
  `scoreMetadata.ts` components for scoring
- `score.ts` + `constants.ts` — final score calculation over the score model; shared thresholds
- `scoreMath.ts` — the shared `clamp01`/`norm` primitives both `score.ts` and
  `scoreModel.ts` use; single source so the two scorers can't silently diverge
- `watcher.ts` + `watcher/` — shared per-project health watcher: the facade
  owns singleton creation, public API, and shutdown flush; the folder owns
  event analysis and guarded scan publication. See [watcher/CLAUDE.md](./watcher/CLAUDE.md)
  for the module map, event flow, and concurrency/worker contracts.
- `analysisWorker.ts` — the eval-worker primitives shared by
  `watcher/isolatedAnalyze.ts` and `../scanner/healthWorkerRunner.ts`
  (`DEFAULT_ANALYSIS_STALL_MS`, `spawnEvalWorker`, `terminateQuietly`,
  `createStallTimer`, `unref` chosen per call site); protocol and respawn policy
  stay in each caller.
- `cache.ts` + `cachePaths.ts` + `cacheFile.ts` — persistent per-file health
  cache at `<project>/.lattice/health-cache.json`, keyed by absolute path with
  `(mtime,size)` staleness. `cache.ts` is the `HealthCache` class: in-memory
  state + its load/get/set/delete/prune/save/flush transitions, debounced
  coalesced writes, save-chain serialization, dirty-bit rearm-on-failure.
  `set()` dirties only a new or changed entry (stat fields, then a deep
  compare of metrics/imports), so an unchanged rescan's flush writes nothing.
  `cachePaths.ts` owns the location + `CACHE_VERSION` (bump it on any import-
  extraction/resolver change — see the crossFile cache-coupling note above —
  and on any change to cached metric output, e.g. v5: Rust lifetimes in the
  universal strip pass).
  `cacheFile.ts` owns the crash-safe I/O: raw read plus the same-dir temp
  write → atomic rename (transient-Windows-rename retry + temp cleanup).
  `tsconfig.ts` — tsconfig alias resolution
- `walkTree.ts` — `walkSourceTree`, the one bounded, skip-dir-aware directory
  walker shared by tsconfig discovery + `crossFile/packageRoots.ts`
- `configReloader.ts` — `ConfigReloader`: loads the project ignore matcher
  (root `.gitignore` + the common gitdir's `info/exclude`, matching the
  scanner's `loadGitignore`) + tsconfig aliases and refreshes them when the
  ROOT `.gitignore`/`tsconfig*` changes (full rescan). `info/exclude` is read
  at load time only — it lives under `.git`, which the watcher ignores. A
  NESTED `tsconfig*` edit reloads only the merged alias map
  (`reloadAliasesForNestedTsconfig`) and re-runs cross-file, with no rescan
  broadcast; a nested `.gitignore` is ignored
- `index.ts` / `utils.ts` — public re-export barrel; `smellsToArray` helper
- `types.ts` — `HealthMetrics` / `HealthSmellId` definitions

Adding a smell: update `types.ts` (id + label), emit it from `walker/` or
`universal/smells.ts`, and add a `scoreModel.ts` component if it gates the
score.

Adding a language (AST metrics):

1. Extend `GrammarKey` and add a `GRAMMARS` entry in `parser.ts` with the
   available WASM filename and extension aliases. Both extension lookups are
   derived from that table.
2. Provide a `NodeKinds` factory in `nodeKinds/`, then import and dispatch it
   in `nodeKinds.ts` (`buildNodeKinds`, used by `nodeKindsFor`).
3. Align `languageForExt` in `analyze/language.ts` and `HealthLanguage` in
   `types.ts` so emitted language metadata matches the registered extensions.

AST metrics do not automatically enable cross-file import/reachability
analysis; import extraction (`walker/`), resolution, root detection, and
dead-code eligibility (`crossFile/`) need separate support (see above).
Changes to cached analysis output require a `CACHE_VERSION` bump in
`cachePaths.ts`; see the cache-coupling note above.

Commands from `backend/`: `npm run build` (build), `npm test` (tests),
`npx tsc --noEmit` (type-check).
