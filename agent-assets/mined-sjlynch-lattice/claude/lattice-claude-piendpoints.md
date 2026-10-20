# Settings Pi tab

`../PiTab.tsx` edits the machine-global Pi endpoints (`globalSettings.piProviders`)
and the curated "Pi — X" model menu (`piModelMenu`); this folder holds its
endpoint draft hooks. Shared Save/Cancel and persistence flow:
[settings/CLAUDE.md](../CLAUDE.md). How the backend reconciles providers into
`~/.pi/agent/models.json`, auto-discovers and curates the menu:
`backend/src/piModels/CLAUDE.md`.

## Module map

- `../PiTab.tsx` — orchestrator: loads providers (`probe.reset()` + `seed`),
  wires the `PiTabHandle` patch, renders `PiEndpointCard` per endpoint and
  `PiModelMenu`.
- `../PiEndpointCard.tsx` — one endpoint: id / baseUrl / key, Detect (or
  "Refresh now"), the Auto-discover checkbox, the model checklist with
  context-window ("262K ctx") and thinking-level (`xhigh · max`) badges, and the
  Advanced toggle → `../PiEndpointAdvanced.tsx` (provider `api` select over
  Pi's four values — blank means `openai-completions` — compat
  `thinkingFormat` / `supportsDeveloperRole` / `supportsReasoningEffort`, custom
  request headers).
- `../PiModelMenu.tsx` + `../usePiModelMenuDraft.ts` — curated-menu checklist and
  its draft / provider auto-include.
- `useEndpointState.ts` — endpoint list + `touched` + `patch` / `add` / `remove`
  through one shared `mutate`; row request identity (`getProvider` /
  `requestToken` / `isCurrentRequest`); `add` mints via `nextEndpointId` so a
  saved id is never re-minted.
- `useProbeDetection.ts` — per-endpoint `probing` / `detected` / `probeError` and
  the `POST /api/pi-endpoints/probe` flow; reports `{id, contextWindow?}` via
  `onDetected` (a reachable endpoint listing nothing is an error); `reset` /
  `seed` / `dropEndpoint`.
- `usePiEndpointEditors.ts` — compat / header / model / detect handlers, all via
  `mutate`. Manual Detect forwards a snapshot of the explicit custom headers via
  `probePiEndpoint` (`api/settings.ts`).
- `../piTabUtils/` — pure helpers: `headers.ts` (cleanup, ordered row edits),
  `providers.ts` (compat edits, save gating/sanitization `piProvidersPatch`,
  endpoint ids, `dropEndpointKey`), `models.ts` (probe application, model/menu
  derivation, `alwaysShownPatterns`, `AGGREGATOR_MODEL_COUNT`).
- `../usePiEndpoints.ts`, `../piTabUtils.ts` — compatibility barrels only.

## Invariants

- **Providers patch:** `piProvidersPatch` is `undefined` until the saved list
  LOADED *and* was touched — the backend deletes every managed provider missing
  from the list. A failed load shows an error and disables "Add endpoint".
- Saves keep explicit empty maps (headers / compat `{}`) so a user can clear
  advanced overrides; absent fields preserve hand-written config on adoption.
- **Key by `ep.id`, never array index:** `useProbeDetection`'s three maps,
  `PiTab`'s `advancedOpen` and the React `key` — removing a non-last endpoint
  must not hand a survivor another row's detected list / Advanced section /
  probe error. Removal drops that id's entries.
- Cards / advanced / menu get index-pre-bound callbacks, but every mutation
  flows through `useEndpointState`'s `mutate`.
- **Request identity:** editing `id` / `baseUrl` / `apiKey` / `headers` / `api` or
  removing the row invalidates an in-flight probe immediately (even A → B → A
  before the next render); metadata edits and index shifts keep identity.
  `applyDetectedModels` requires the current row request token — never just the
  same endpoint id or the click-time index.
- **Session fence:** `reset()` on every dialog open and on unmount bumps a
  generation; with the per-detect token and the row-current predicate it drops
  stale successes, errors, detected-model application and `finally`/busy
  cleanup. So a slow Detect from before Cancel can't land after reopen and
  clobber curated models on an unrelated Save, and an old request can't clear a
  newer one's busy state or populate a removed-and-reused id. Pinned by
  `__tests__/piProbeStaleSession.test.ts`.
- `seed(providers)` primes `detected` from the SAVED models on load: the
  checklist shows `detected ∪ selected`, so without it un-ticking an
  auto-discovered model in manual mode removed the only row that could restore it.
- **Auto-discover** (default on) hands the model list to the backend's
  `refreshEndpointDiscovery`; while on, the checklist is read-only, since a hand
  un-tick would be undone by the next refresh.
- The model menu renders `alwaysShownPatterns` as fixed because the backend
  surfaces them regardless of curation — a checkbox that silently does nothing
  is worse than none. Both stop at `AGGREGATOR_MODEL_COUNT` (5), which must equal
  the backend's `PI_MODELS_CONFIG.aggregatorModelCount`
  (`backend/src/piModels/config.ts`); past it the card says so and models are
  curated by hand.
- **Menu hydration** (`usePiModelMenuDraft`): checkboxes and `toggle` stay
  read-only until this session's saved-menu GET succeeds (rows retained across
  close/reopen included); `PiModelMenu` shows loading or the error with Retry;
  `getPatch` is `undefined` meanwhile so Save preserves the curated menu.
  Provider patterns auto-include only after hydration; a cancelled load or error
  can't settle a later session. Pinned by
  `__tests__/piModelMenuDraftLoading.test.ts`.
- A keyless endpoint is fine: the backend writes it with `apiKey: "local"` so Pi
  doesn't reject the whole `models.json`.

Tests: named after the module (`piTabUtils`, `piProviderClearing`, …) in
`frontend/src/__tests__/`.
