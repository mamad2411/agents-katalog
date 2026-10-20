# Settings Tools tab

`../ToolsTab.tsx` composes these sections and exposes `ToolsTabHandle` to the
parent controller. Hooks and the handle run before its `!active` render gate;
switching tabs does not stop them. Shared Save/Cancel and persistence flow:
[settings/CLAUDE.md](../CLAUDE.md). Styles: `styles/settings/tools.css` under `frontend/src/`.

## Module map

- `useOpengrepToolsState.ts` owns status, drafts, loaded/touched flags, errors,
  load/poll effects, immediate actions and scan results.
- `toolsTabUtils.ts` owns draft conversion, list cleanup, budget normalization,
  display formatting, licence acknowledgement detection and polling constants.
- `OpengrepEngineSection.tsx` shows engine resolution, install progress and
  status/action errors; its install button delegates through `runAction`.
- `OpengrepPacksSection.tsx` renders enable drafts and install/update/remove
  actions; first installs with a Commons Clause licence require confirmation.
- `OpengrepScanFilterSection.tsx` renders per-project draft controls and load errors.
- `OpengrepScanNowSection.tsx` runs the active project's scan and shows its
  record/digest counts or last scan, plus a link to the markdown digest.

## Save boundaries

Engine install and pack install/update/remove act immediately via
`/api/opengrep/*`; Cancel does not undo them. `runAction` refreshes status after
success or failure. Run scan uses persisted settings, without saving drafts.

Pack checkboxes draft machine-global `globalSettings.opengrep.packs`.
`getOpengrepGlobalPatch()` returns the whole copied packs map inside `{ packs }`
only when **`packLoaded && packTouched`**, otherwise `undefined`.
`getOpengrepProjectPatch()` likewise requires **`projectLoaded && projectTouched`**
and returns the whole `userSettings.opengrep` object: `severityFloor`,
`ignoreRuleIds`, `ignoreFingerprints`, `extraRulePaths`, `excludeGlobs`,
`digestBudgetKb`. `ToolsTab` builds these patches; the hook does not persist them.
The parent `saveSettings.ts` consumes the project patch, then the global patch
through `saveGlobalSettings`, in the shared save flow linked above.

Both loaded flags become true only after successful settings reads. Project
reads use `fetchUserSettingsStrict`, which throws instead of treating failure
as empty settings. Failed loads show errors and leave the corresponding pack
checkboxes/scan-filter controls disabled. Saving empty defaults would erase saved
enables or ignore lists, including fingerprints appended through `opengrep_ignore`.
With no project, global settings/status still load and pack enables can save;
the project read is skipped, its patch stays undefined, filter/scan controls
stay disabled, and the controller calls only `saveGlobalSettings`.

## Async lifetime

Opening or changing folders while open reloads status/settings and resets loaded/touched
flags and project drafts/results. Settings-load callbacks use the effect's
`cancelled` flag, set on cleanup. Status success/error replies check both the
current folder and `openRef`; scan results/errors check only the current folder.
These are not generation guards across close/reopen or switching away and back.
`runAction` error updates and scan-finally's `setScanning(false)` are unguarded.
Status polling runs every `POLL_MS` (1500 ms) only while open and busy (engine
install, pack fetch, server scan or local `scanning`); tab visibility is irrelevant.
The interval is cleared on effect cleanup (close, idle, folder change, unmount).

Contracts: [toolsTabUtils.test.ts](../../../__tests__/toolsTabUtils.test.ts) covers pure helper behavior;
[backend/src/opengrep/](../../../../../backend/src/opengrep/CLAUDE.md) owns install, pack, scan and digest rules.
