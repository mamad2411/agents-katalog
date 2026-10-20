# backend/src/piModels

Pi model config for the harness dropdowns. `../piModels.ts` is a re-export
barrel (`discovery`, `reconcile`, `probe`, `autoDiscover`); consumers keep
importing from `'../piModels.js'`. The load-bearing split is **read vs. write
of Pi config**.

## Read-only discovery map

- `discovery.ts` — stable public facade for the read-only side. Exposes
  `getPiModels(curated?)`, `resolvePiModel(projectPath)`, the historical
  `parsePiListModels` / `reconcileModelsCache` exports, `resetPiModelsCache`,
  types, and the `normalizePiModel` re-export. **Never writes Pi config.**
- `parser.ts` — parses the fixed-width `pi --list-models` table
  (`parsePiListModels`) and owns `reconcileModelsCache`, including the
  transient-failure rule: `null` means timeout/spawn error, so keep the last
  good cache (or return uncached `[]` cold); `''` is a successful empty listing
  and is cached.
- `listModels.ts` — executes `pi --list-models` with timeout, parses combined
  stdout+stderr because Pi prints the table to **stderr**, memoizes successful
  parsed results for `PI_MODELS_CONFIG.modelsCacheTtlMs`, and provides
  `resetPiModelsCache()` for management-side invalidation.
- `files.ts` — read-only readers for `~/.pi/agent/models.json` (custom
  provider friendly names / default-menu provider set) and `settings.json`
  (Pi's current `defaultProvider/defaultModel`).
- `menu.ts` — curates the "Pi — X" `menu`: curated `globalSettings.piModelMenu`
  wins when non-empty; otherwise default to every model from a
  models.json-declared provider plus Pi's current default. Entries remain valid
  if reported by `pi --list-models` **or** declared in `models.json`, so a
  fragile CLI probe doesn't hide explicitly configured models. Auto-discovered
  providers with at most `PI_MODELS_CONFIG.aggregatorModelCount` (5) models bypass
  curation; larger lists respect it. Only labels that actually collide get a
  `(provider-id)` suffix.
- `types.ts` — shared `PiModelInfo`, `PiMenuEntry`, `PiModelsResult`,
  `ModelsJson`, cache shapes, and `PiProvider` / `PiProviderModel`
  (re-exported by `../piProviderValidation.ts`). Node-free: the frontend
  shares them through `../shared/wireTypes.ts`.

## Write-side management

- `reconcile.ts` — `reconcilePiModelsJson()` upserts
  `globalSettings.piProviders` into `~/.pi/agent/models.json` (atomic
  temp→rename), preserving every hand-written provider and precisely deleting
  removed-managed ones via the `~/.lattice/piManagedProviders.json` sidecar.
  Absent `headers` / `compat` preserve prior hand-written values on adoption;
  explicit `{}` clears those overrides from models.json. The empty maps remain
  in global settings so later sweeps cannot restore the cleared overrides.
  Every managed provider always gets an `apiKey` (defaults `"local"`) — one
  keyless provider makes Pi reject the *whole* file. Reconcile invalidates
  discovery's cache, skips the write entirely when the file already matches, and
  is **serialized** (`runExclusive`) using the shared `atomicWriteFile` — it now
  runs on every discovery sweep, so two calls can overlap, and Pi re-reads
  models.json every time `/model` opens (a plain rename over a file another
  process holds throws EPERM on Windows). It reads `globalSettings` STRICTLY:
  an unreadable/corrupt `globalSettings.json` aborts the reconcile rather than
  reading as "no providers" and deleting every managed one.
- `probe.ts` — `probeEndpointModels()` GETs `<baseUrl>/models` (OpenAI-compatible)
  behind the "Detect models" button, returning `{id, contextWindow?}` per model.
  The context window comes from whichever key the server uses
  (`max_model_len` on vLLM/NInfer/SGLang, `context_length` on
  llama.cpp/LM Studio, …) and is carried onto the saved provider model, so
  models.json gets the endpoint's real window instead of Pi's conservative default.
  This module also implements `probeThinkingLevels()`: POST one deliberately
  invalid `reasoning_effort` to `/chat/completions` and parse the rejection's
  accepted levels. Both probes receive the provider's explicitly configured
  literal `headers`; names/values are validated before requests. Custom headers
  override defaults case-insensitively, with the last configured spelling winning.
  Header values and `apiKey` never resolve environment variables or execute
  command syntax: `$VAR` / `${VAR}` stays literal, and a `!command` apiKey supplies
  no token. Endpoints requiring resolved secrets may reject probes; endpoints
  allowing unauthenticated access can succeed. Thinking probes return tokens,
  `[]` (2xx: no validation, recorded so the model isn't re-asked), or `null` for
  NO answer (network error / timeout, non-400/422 status such as 5xx/401, or an
  unparseable rejection). On `null`, keep thinking data untouched and retry next
  sweep, never mark the model "ordinary". Pinned by `__tests__/piProbeHeaders.test.ts`.
- `autoDiscover.ts` — `refreshEndpointDiscovery()` keeps each `autoDiscover`
  endpoint's model list matching what it actually serves: probe → merge into
  `globalSettings.piProviders` → reconcile. Discovery sees only currently served
  `/models` entries; it cannot enumerate unloaded weights or load another model.
  Called at boot, after a settings save, and from `GET /api/pi-models` (every
  harness dropdown open). A failed or empty probe KEEPS the stored models —
  blanking them is what leaves Pi with no model to run — and reconcile runs on
  every sweep, so a models.json that drifted out of sync is repaired even when
  the probe changed nothing. All model-list and thinking probes use the captured
  provider request configuration and finish before the provider list is
  **re-read inside the global-settings write lock** (`updateGlobalSettingsWith`).
  Inside that lock, results apply only to a provider with the same id, still
  enabled for auto-discovery, and a matching `baseUrl` / `apiKey` / `headers` fingerprint.
  Key or header edits during either probe retain the newer provider's models
  and thinking data, including saves queued ahead of the sweep's write.
  Capability detection runs once per newly-seen model; `[]` records "asked,
  nothing extended". Lists above `PI_MODELS_CONFIG.thinkingProbeModelLimit` (25)
  skip capability probing, independently of the menu's cutoff (5): a provider
  with 6–25 models can require curation and still receive thinking probes.
  Pinned by `__tests__/autoDiscover.test.ts`.
- `thinkingLevels.ts` — parsing, sanitization and thinking-level-map helpers;
  HTTP execution belongs to `probe.ts`. Pi gives a model `xhigh` / `max` ONLY if
  it declares a `thinkingLevelMap`; with the map absent Pi **silently clamps**
  them to `high` (verified: asking for `max` sends `reasoning_effort: "high"`, no
  error). Levels are detected, never hardcoded. `parseAcceptedEffortTokens`
  needs ≥2 recognizable tokens before trusting a message, so prose can't produce
  a map that hides levels which actually work. `sanitizeThinkingLevels` keeps an
  empty array so the "asked" marker survives the settings round-trip.
  `extendsBeyondStandard` checks for `xhigh` / `max`; `buildThinkingLevelMap`
  maps Pi's levels to accepted
  server tokens (including `off` aliases), or `null` for unsupported levels.
- `sweepScheduler.ts` — the scheduling policy behind it, isolated so it is
  testable without a server: join an in-flight sweep (even inside the TTL, or
  the caller reads state that sweep is about to replace), throttle by TTL only
  when idle, `force` never adopts a sweep that started before the change that
  forced it (and two concurrent forcers still run ONE sweep at a time), and
  `maxWaitMs` bounds the WAIT without bounding the work (an HTTP
  handler must not sit behind a probe timing out against a dead host).
  Pinned by `__tests__/sweepScheduler.test.ts`.
- `config.ts` — tunables (`PI_MODELS_CONFIG`: list/probe timeouts, cache TTL)
  + `piAgentDir()` (`~/.pi/agent`), shared by both sides.

Model **SELECTION** is per-spawn via the `--model` flag
(`agentCommandBuilder.ts` defines `buildPiModelFlag`; `worktree/commands.ts`
retains its compatibility re-export); `settings.json` defaults are never touched.

## Served by / tested by

`routes/settings/piModels.ts` (`GET /api/pi-models`) +
`routes/settings/piEndpoints.ts` (`POST /api/pi-endpoints/probe`).
`__tests__/piModels.test.ts` pins `parsePiListModels`, `reconcileModelsCache`,
`sanitizePiProviders` (via the `'../globalSettings.js'` / `'../piModels.js'`
surfaces), `parseProbedModels` (the `/models` context-window spellings), and
`buildMenu`'s collision handling.

Commands from `backend/`: `npm run build`, `npm test`, `npx tsc --noEmit`.
