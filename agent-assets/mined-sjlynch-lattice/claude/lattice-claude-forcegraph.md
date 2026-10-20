# forceGraph

3D file-tree DAG view (three.js / 3d-force-graph); `components/ForceGraphView.tsx`
is a re-export shim. Deeper: [hooks/CLAUDE.md](hooks/CLAUDE.md) (effects,
init/teardown), [labelPhysics/CLAUDE.md](labelPhysics/CLAUDE.md) (repulsion
**and** label texture/registry rules), `graphSettingsPanel/CLAUDE.md` (settings
→ scene effects). Not here: scan data (`src/hooks/CLAUDE.md`),
`extensionStyles.ts`, `taskColors.ts`.

## Two named subsystems (shared vocabulary)

- **Idle controller** (`idleController*.ts`) — render-on-demand gate, a
  ref-counted `pauseAnimation`/`resumeAnimation` wrapper. The RAF loop runs only
  while a **reason** is held (`engine`, `interact`, `refresh`, `labelPhysics`,
  `agents`, `halo`), never for a hidden tab or collapsed container. Settled =
  0 frames; only slow-only reasons (`agents`/`labelPhysics`/`halo`) → ~30fps.
- **Agent Presence Layer (APL)** (`agentOverlay*.ts` + `hooks/useAgentOverlay`)
  — per live agent (Claude/Codex/Pi; `task-activity` and `agent-activity`) a
  presence node, fading focus beams to touched files, a file label, and a
  satellite per subagent. Lives in `graph.scene()`, NOT `graphData`, so agents
  never reheat the sim. Activity that arrives before its agent's node (another
  socket) is buffered in `agentActivityBuffer.ts` and replayed — dropping it
  left a label-less dot. `showSubagentLabels` (default off) only toggles the
  subagent type prefix.

## Module map

- `ForceGraphView.tsx` — exported **retry shell** around the coordinator (props,
  selection/hover, shared refs, JSX), which calls `hooks/useGraphSceneRuntime` →
  `hooks/useGraphInteraction` → `useGraphViewChromeModel` (hooks/CLAUDE.md →
  "Coordinator phases"). `GraphViewChrome`/`GraphViewOverlays`/`Graph*` are
  render-only.
- `rendererStatus.ts` / `GraphRendererNotice.tsx` — classify init errors and
  `webglcontextlost`; `webglcontextrestored` clears the notice and wakes.
  Neither proves OOM or a GC defect; user advice:
  [browser memory troubleshooting](../../../README.md#browser-memory-troubleshooting).
- `HealthTooltip` (+ `HealthTooltipSections`, `healthTooltipMetrics`,
  `healthScoreContributions`, `tooltipPosition`, `cursorTracker`),
  `SecurityTooltip` — write their own `transform`; pointer moves never re-render.
- `Security{FindingsPanel,FindingList,FindingDetail,ReviewControls}.tsx` +
  `securityFindings.ts` — findings panel (virtualized, fixed
  `SECURITY_ROW_HEIGHT`; honors the Settings severity floor) + review launcher.
  Recommendations stay in the harness conversation (no report/Apply UI); nothing
  auto-fixes, suppresses, scans or launches tasks (review rules:
  `backend/src/opengrep/CLAUDE.md` → "Triage and review").
- `TimelineScrubber.tsx` + `timeline{Range,Diff,Reset}`,
  `useTimelineScrubberDrag`, `CommitTooltip` — git timeline scrubber.
- `nodeObjectFactory.ts` (`nodeThreeObject`) applies `spriteDecision.ts` (pure,
  THREE-free; recolor precedence security > health > loc > dead > base; metric
  views suppress change ring + label).
- `sprites`/`spriteShapes`/`spriteTextures`/`spritePicking`; `canvasTexture.ts`
  (every hand-painted texture); `spriteMaterialCache.ts`
  (`createSpriteMaterialCache` + teardown's `disposeSharedGraphResources`).
- `{loc,health,deadCode,security,labels}Overlay` + `metricOverlayFactory` —
  overlay configs/registries; dead-code and security are pure recolors
  (security's path lookup normalizes Windows casing/separators).
- Labels: `measuredLabelTexture`, `labelTexture`, `labelSpriteResources`,
  `floatingLabelSprite`, `labelSync` (in-place Alt delta), `labelRepulsion{,
  Frames}` → labelPhysics/CLAUDE.md.
- Sibling-child toggles (per changed id, no `graph.refresh()`): `haloResources`
  + `halo` + `selectionHaloSync`; `worktreeRing{,Sync}` (`W`);
  `changeRing{,Sync,Materials,Textures}` (timeline rings + ghosts);
  `mountedNodes.ts` (helpers for every delta walker).
- APL: `claudeNodeSprite.ts`, `agentOverlay.ts` façade over
  `agentOverlay{Context,…,Placement}.ts`, `agentLabelRects.ts` (pure packing;
  labels slide only along their node's side).
- `idleController{,Reasons,Loop,Engine,Interact}.ts`; `sceneFrameDriver.ts`
  (`onFrame`) + `nodeMotionDriver.ts`; `motionSyncGate.ts` (batched upload gate).
- `instancedLinks`/`instancedNodes` (+ `*Resources`, `instancedBatching`,
  `matrixBuffer`) — default-on batching into one `LineSegments` / per-style
  `InstancedMesh`es.
- `graphSettings.ts`; `localRepulsionForce.ts` (`repulsionMode==='local'`);
  `layoutShapeForces.ts` (`forceCollideXZ`); `linkedCellGrid.ts` (shared X/Z
  grid; closure-free cursor yields each pair once, j > i, in fixed order;
  callers own rounding + pair math); `radialTidyLayout.ts`; `sceneSetup.ts`;
  `cameraState.ts`; `depthMap`; `menu`; `renderOrders`; `graphMemGauges.ts`;
  `searchMatcher.ts` (keep aligned with backend `search.ts`).

## Load-bearing invariants (do not violate)

**Render loop**
- Hold an idle reason *while* animating, release on settle — never "while
  enabled". APL holds `agents` only while `tick()` reports motion; holding it
  while any agent existed pinned 60fps.
- One-shot mutations must wake the paused loop: `kick()` for motion,
  `wakeForRefresh()` for set changes (agent removal, halo, ring, labels, canvas
  resize — `renderer.setSize` clears without rendering).
- Pauses go through `queueMicrotask` (the library re-arms RAF at frame end and
  `onEngineStop` fires inside it, overwriting a sync pause); resumes stay sync,
  idempotent, re-entrancy-guarded.
- Custom forces scale impulses by `alpha` and skip Y (DAG-pinned `fy`) so the
  sim still settles to 0 frames.
- Frame/motion drivers rebuild cached listener arrays only on membership
  change; unsubscribe replaces it at once, even the last (a paused graph may
  never dispatch again); in-flight dispatch keeps its snapshot; motion and drag
  lists are separate, drag first; library callbacks stay callable when empty.
- Node motion needs `onEngineTick` + `onNodeDrag` + `onNodeDragEnd`; dragging a
  settled graph doesn't tick, so `onNodeDrag` (not `isEngineHot()`) signals it.
- APL releases never wait for `tick` (paused while agents keep working):
  `applyActivity` disposes expired beams first, the hook's 30 s timer calls
  `reapSatellites` then wakes, `AgentPathIndex.clear()` runs when the last agent
  leaves and on destroy. APL label layout snaps without an idle reason.

**Scene & data**
- Filter only via `nodeVisibility`/`linkVisibility` (`hooks/useGraphFilter`),
  never structural add/remove (keeps the sim stable). The digest
  (`refresh()`/`graphData()`) *removes* filtered nodes from the scene, so a
  between-digest flip (`changeRingSync` ghosts) must update the node, its link's
  `__lineObj` AND `getInstancedLinks(graph).rebuild()` or a line dangles; hide
  via `setGhostRootShown` (disables layers — Raycaster ignores `.visible`); a
  ghost with no `__threeObj` falls back to `clearLabelsAndRefresh`.
- Every full `graphData()` swap (incl. the ghost merge, which keeps
  `structuralData`) bumps `dataGeneration`; batched rebuilds depend on it.
- Structure-only consumers key off `useStructuralScan(data)`, not `data`, and
  never read metric fields from it.
- Ghosts come from `GitHistoryResult.deletedPaths` — never infer deletion from
  scan absence (`SOURCE_EXTS` filters) or latest `git log` status (date order
  crosses branches); they link to the nearest existing ancestor dir.
- H/Z/D views hide ghosts + metrics-ignored files (render-only, separate from
  scanner exclusions/hidden exts); absent `metricsIgnoredExts` = defaults
  (`api/types/settings.ts`), explicit `[]` opts back in. Security hides ghosts
  but keeps metrics-ignored config files.
- Hover is gated off mid-drag (`pointerDraggingRef`), else every rotate frame
  `flushSync`s a tooltip.
- With `batchedNodes` on, the per-node base sprite stays mounted at `.visible =
  false` (raycasts ignore it) as pick target and child anchor. Recolor overlays
  and ghosts use per-node sprites.
- `worktreeRingsRef` lets `buildNodeObject` re-attach rings on rebuild;
  `clearWorktreeRings` walks the current scene, never a remembered id set.
- All canvas textures go through `canvasTexture.finishCanvasTexture`
  (`SRGBColorSpace`) so colors match the Legend.

**GPU & memory**
- Retry remounts the coordinator and hooks (re-running init alone leaves hooks
  on the old graph); `App.tsx` keys the view by `activeFolder`. Teardown order:
  hooks/CLAUDE.md.
- Module-level caches survive remounts, bounded by key: `sprites.materialFor`
  (style), `claudeNodeSprite` + `worktreeRing` (color; id-hash fallback can mean
  one per task), `changeRingMaterials`, `haloResources`, connector line
  materials. Removing a node/ring/agent never drops an entry; only
  `disposeSharedGraphResources` at teardown does (an undisposed cache pinned the
  dead renderer).
- Halo singletons (the library's `_deallocate` frees their GPU side per
  `refresh()`; three re-uploads): only teardown's `disposeHaloResources` disposes;
  removing a halo just detaches its Group; pulse/reset use `peek*Material`.
- Labels: balance every texture build with a release, never `.clear()` a
  registry (use `clearAllLabelRegistries`), never evict/zero/dispose an in-use
  entry, keep `MAX_NAME_LABELS` + cache caps — detail labelPhysics/CLAUDE.md →
  "Label resources".
- `instancedLinkResources` growth calls `geometry.dispose()` while the old
  attribute is installed. `setEnabled(false)` restores `linkThreeObject(null)`,
  detaches motion, frees resources + captured links, keeps the controller stamp
  (`dispose()` drops it only if still owned); disabled hooks allocate nothing.
  Pre-hydration string endpoints re-capture in `onFrame`.
- Each node style mesh owns its `instanceMatrix` + material (freed on growth,
  removal, disable); borrowed sprite textures are never freed here; the shared
  quad survives disable, freed only on dispose.
- Register a mem gauge beside new long-lived GPU resources (`graphMemGauges.ts`).

## Camera

`up = (0,1,0)`; polar clamped to `[0, 0.75π]`; OrbitControls (not Trackball);
`dagMode = 'td'` (`sceneSetup.configureCameraControls`). Position + orbit target
persist per project (`hooks/useCameraPersistence`).

## Tests

Named after the module — grep `<module>` in `frontend/src/__tests__/`. Less
obvious: `ghostLinkSync` (changeRingSync), `agentOverlayPausedLoop`. See
[__tests__/CLAUDE.md](../../__tests__/CLAUDE.md).
