# graphSettingsPanel

Small UI-only modules for the floating graph settings panel. `config.ts` owns
labels/ranges/toggle metadata and `controls.tsx` owns reusable row components.
Keep persisted key names backwards-compatible via `tabStorage.ts` and the shared
`latticeLocalStorage` key builders.

## Graph settings flow

This doc also owns how a setting reaches the scene (code in `../graphSettings.ts`
and `../hooks/useGraphSettings*.ts`). Adding a setting: field + default in
`GraphSettings`/`DEFAULT_SETTINGS`, a row in `config.ts`, and an effect in the
matching split below — decide render-only vs physics first.

- Tabs (rows in `config.ts`, bespoke controls in `../GraphSettingsPanel.tsx`):
  Sizes, Physics (`dagLevelDistance`/`chargeStrength`/`linkDistance`/
  `velocityDecay`/`chargeTheta`/`repulsionMode`), Spread (`alphaDecay`/
  `warmupTicks`/`collideRadius`, `tidyLayoutOnLoad`/`tidySpread`), Rendering
  (`linkWidth`, `showLinks`, `batchedLinks`/`batchedNodes`, `pixelRatio`,
  `selectionGlowStrength`/`selectionGlowScale`).
- `useGraphSettings` keeps its `{ settings, setSettings, settingsRef }` shape
  over `usePerProjectGraphSettings` (persistence + ref mirror),
  `useGraphSettingsSprites`, `useGraphSettingsPhysics`,
  `useGraphSettingsLayoutShape`, `useGraphSettingsRendering` and
  `graphSettingsEffectUtils` (`hasMountedNodes`).

### Render-vs-physics splits (settings effects, all guarded)

Effects skip the initial mount and empty/unmounted graphs (`nodeThreeObject`
reads `settingsRef` live, so the data-sync build already uses current values —
a pre-population refresh/reheat is a byte-identical wake):

- **Sizes** → clear label registries + `graph.refresh()` (no sim restart),
  trailing-debounced (`SPRITE_REFRESH_DEBOUNCE_MS`): sliders fire per pointer
  move and each refresh rebuilds every sprite, so a drag pays one rebuild.
  Persistence is debounced too (`SETTINGS_PERSIST_DEBOUNCE_MS`), with the
  pending save flushed on unmount and before a save for another project.
- **Physics** (Physics tab fields) → poke `d3Force` + `d3ReheatSimulation`; the
  pokes run on *every* run incl. setup, so persisted non-defaults aren't left at
  d3 defaults.
  `repulsionMode` swaps `forceManyBody`↔`forceLocalRepulsion` only when the
  active force changes; the detached cached force is `initialize([])`d (drops
  node refs) and reattachment supplies current nodes/context.
- **Layout shape** (`useLayoutShapeSettings`) → push `d3AlphaDecay`/
  `warmupTicks` every run; install/remove the `forceCollideXZ` slot when
  `collideRadius` crosses 0; reheat on change to a populated graph. Not neutral
  by default: `alphaDecay` 0.014 (d3: 0.0228) and `warmupTicks` 15 shape every
  default layout; only `collideRadius` (0) is off. `applyCollisionRadius` drops
  the cached closure on removal (releasing its nodes/scratch); re-enable creates
  a fresh force.
- **`linkWidth` / `pixelRatio`** → render-only prop + `wakeForRefresh`, no
  reheat. `showLinks` off is render-only via `useGraphFilter`'s `linkVisibility`
  (links still drive layout). `batchedLinks`/`batchedNodes` are owned by their
  hooks (`useBatchedLinks`/`useInstancedNodes`), not effects.
- Selection glow: `useSelectionGlowSettings` — strength read live, scale
  rebuilds selected halos (see `../hooks/CLAUDE.md`).
