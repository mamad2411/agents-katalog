# Global settings

Machine-global settings, stored at `~/.lattice/globalSettings.json` — distinct
from per-project `userSettings.ts`. "Global" = facts about the *machine*, not a
project: one backend, one terminal-server, one machine's RAM/CPU, one shared Pi
config (`~/.pi/agent/`).

`../globalSettings.ts` is the read/write facade; per-field validators live
next to the shapes they produce. The `GlobalSettings` type is declared in the
node-free `types.ts` here (re-exported by the facade) because the frontend
shares it through `../shared/wireTypes.ts` — add a field THERE, and keep every
type it references in a node-free module (`../mcp/types.ts`,
`../piModels/types.ts`, `../opengrep/types.ts`).

## What "global" covers

| Field | Meaning / runtime consumer | Validated in |
|-------|---------|--------------|
| `maxConcurrentAgents` | The spawn queue's **softCap** — requests above it are deferred in the queue, never dropped (`../spawnQueue.ts`). | `clampMaxConcurrentAgents` in `../globalSettings.ts` (bounds `[MIN_MAX_CONCURRENT_AGENTS=1, MAX_MAX_CONCURRENT_AGENTS=150]`; env-seeded default `LATTICE_MAX_CONCURRENT_AGENTS` else `DEFAULT_MAX_CONCURRENT_AGENTS=24`). The 150 upper bound stays well under the terminal-server hard cap (200) so the reserve band + manual terminals keep headroom. |
| `minFreeDiskGb` | Free-space reserve in GB on the worktree volume; absent → `DEFAULT_MIN_FREE_DISK_GB=10`. Consumed by `minFreeDiskBytes` / `reserveWorktreeDiskSpace` in `../worktree/diskSpace.ts`; zero still defers a checkout that cannot fit. See [worktree disk guidance](../worktree/CLAUDE.md#disk-space-lfs-gc) for in-flight reservations and the separate merge floor. | `sanitize` + `clampMinFreeDiskGb` in `../globalSettings.ts`: finite non-negative numbers, clamped at 10,000 with fractional values retained; `../routes/globalSettings.ts` rejects non-finite/negative input. |
| `autoMergeOnLowDisk` | Absent → enabled; `false` opts out. [diskPressureMerge.ts](../diskPressureMerge.ts) merges Ready-to-Merge tasks after a disk-deferred start or a low-disk monitor check; admission guards skip active workflow runs, merge runs, or post-merge hooks, and enforce the merge floor, ready-task availability, throttling and no-progress backoff. | Boolean checks in `../routes/globalSettings.ts` and `../globalSettings.ts`'s `sanitize`; only booleans accepted. |
| `resourceGovernor` | Absent → enabled; `false` opts out. `../spawnQueue/resourceGovernor.ts` holds new batch fan-out under CPU/RAM pressure beneath `maxConcurrentAgents`. [Spawn queue guidance](../spawnQueue/CLAUDE.md#contract--invariants) covers priority/interactive exemptions and the live-agent floor (`MIN_LIVE_AGENTS=2`, counting agents plus queue reservations, never raw PTYs). | Boolean checks in `../routes/globalSettings.ts` and `../globalSettings.ts`'s `sanitize`; only booleans accepted. |
| `mcpCustomServers` | User-added MCP server **definitions** (built-in catalog stays in code; secret values live in `~/.lattice/mcpSecrets.json`, never here). | `sanitizeCustomServers` in `../mcp/settingsValidation.ts`. |
| `mcpBuiltinOverrides` | Per-id partial edits of built-in catalog entries (e.g. edited args). | `sanitizeBuiltinOverrides` in `../mcp/settingsValidation.ts`. |
| `piModelMenu` | Curated `provider/model` patterns surfaced as "Pi — X" rows in the harness dropdowns; empty/absent → the default menu (see `piModels.ts`). | Inline string-array filter in `../globalSettings.ts`'s `sanitize`. |
| `piProviders` | Lattice-managed Pi providers (OpenAI-compatible endpoints, e.g. vLLM), reconciled INTO `~/.pi/agent/models.json` by `piModels.ts`. | `sanitizePiProviders` in `../piProviderValidation.ts` (which re-exports the `PiProvider`/`PiProviderModel` types declared in `../piModels/types.ts`). |
| `opengrep` | Opengrep rule-pack enables (`packs: { [packId]: boolean }`, absent = the pack's `defaultEnabled`). Machine-global because packs are installed once per machine under `~/.lattice/opengrep/rules/`. | `sanitizeOpengrepGlobalSettings` in `../opengrep/settings.ts` (unknown pack ids and non-boolean values dropped). |

## Read/write invariants

`sanitize()` validates supplied fields individually; omitted fields retain
their stored values, so partial PATCHes preserve unrelated settings.
`getGlobalSettings()` falls back to defaults for display; PATCH reads reject
unreadable/corrupt existing files, including non-object JSON (`[]`/`null`),
so partial edits cannot reset the remaining settings. Only a missing file
starts from defaults. Writes are serialized with `runExclusive` on the global
file's key and persisted atomically.

Use `updateGlobalSettingsWith(fn)` for derived writes (Pi auto-discovery,
MCP config import): it strictly reads and computes the patch inside the same
lock as `updateGlobalSettings`; `null` skips the write. Deriving a patch from
an earlier unlocked read can overwrite an intervening save.
`readGlobalSettingsStrict()` is the throwing read for destructive writes
elsewhere, such as Pi models.json reconciliation.

The facade re-exports MCP/Pi validators and the `GlobalSettings`,
`PiProvider`/`PiProviderModel` types, preserving the historical
`./globalSettings.js` import surface.

## Served by

`../routes/globalSettings.ts` — `GET`/`PATCH /api/global-settings`. A `PATCH`:

1. forwards each field through `updateGlobalSettings` (which sanitizes each);
2. immediately applies `setSpawnQueueSoftCap(updated.maxConcurrentAgents)`
   and `setSpawnQueueResourceGovernor(updated.resourceGovernor !== false)`
   to the live queue, without a restart;
3. when `piProviders` is supplied, awaits `reconcilePiModelsJson()`, then
   awaits `refreshEndpointDiscovery({ force: true,
   maxWaitMs: PI_MODELS_CONFIG.discoveryAwaitMs })`. Forced refresh avoids
   adopting a sweep started before the save; the budget bounds the caller's
   wait, while discovery work continues after it expires.

## Command reference

From `backend/`: `npm run build`, `npm test`, `npx tsc --noEmit`.
Validator coverage: `../__tests__/mcp.settingsValidation.test.ts` and
`../__tests__/piModels.test.ts` (both use the facade's re-exports).
