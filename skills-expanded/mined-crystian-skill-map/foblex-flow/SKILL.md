---
name: foblex-flow
description: Authoritative guide for working with Foblex Flow (@foblex/flow) in the skill-map UI. Use whenever editing Angular code in ui/ that touches graph rendering — templates with f-flow / f-canvas / f-connection / fNode / fConnector / fDraggable / fZoom / fMarker directives; TypeScript importing from @foblex/flow (FFlowModule, FCanvasComponent, provideFFlow, withA11y, EFConnectionConnectableSide, EFMarkerType, FConnectionMarkerArrow, etc.); CSS targeting .f-* classes or .sm-gnode; angular.json style configuration for the Foblex theme; or any task involving node layout, connector rendering, pan/zoom behavior, edge styling, drag handles, keyboard navigation, or performance of the graph view. Covers the nine non-negotiable rules learned the hard way, the antipattern checklist, and points at the full API reference for every directive and component.
---

# Foblex Flow — working rules for skill-map

Foblex Flow (`@foblex/flow`) is the graph library that powers `ui/src/app/views/graph-view/`. Upstream documentation is sparse, so this skill is the authoritative operational guide. Before writing or reviewing any graph-related code, read the non-negotiables below.

**Installed version: 19.1.6** (migrated from 18.6.1). The migration adopted v19's unified `[fConnector]` model, the renamed `f-connection` endpoint inputs (`fSourceId` / `fTargetId`), the opt-in keyboard a11y layer (`provideFFlow(withA11y(...))`), and the Foblex-owned selection contract. Legacy names still work but are deprecated; new code uses the v19 names.

**Reference material** (load on demand):

- [`references/api-reference.md`](references/api-reference.md) — every directive, component, input, output, event, method, CSS class, theme token, and enum.
- [`references/examples/`](references/examples/) — verbatim copies of every official example from [`libs/f-examples/`](https://github.com/Foblex/f-flow/tree/main/libs/f-examples) in the Foblex repo, organized by category (nodes, connectors, connections, extensions, plugins, advanced, reference-apps). Start at [`references/examples/README.md`](references/examples/README.md) for the index and the six canonical patterns that repeat across all examples. **When in doubt, the examples win** — they are the Foblex team's own reference shape.

## Mental model

- Foblex Flow does NOT own graph state. Your app owns nodes, groups, connections, ids, validation, and persistence.
- Angular templates render the current state; user actions emit events; your app mutates state; Angular rerenders.
- Connections are **connector-to-connector**, NOT node-to-node. Each `<f-connection>` names a source connector (`fSourceId`) and a target connector (`fTargetId`); both must match a registered `fConnectorId`. (Pre-v19 these inputs were `fOutputId` / `fInputId`, still accepted but deprecated.)
- Do NOT assume React-Flow-style APIs (`[nodes]`, `[edges]`, `setNodes()`, `addEdge()`). Those do not exist.

## The nine non-negotiables

Skipping any of these produces silent failures: missing visuals, degraded performance, or wrong positioning. All nine were learned the hard way — do not relitigate them, apply them.

### 1. One id per connector, one registry (unified `[fConnector]` model)

v19 replaces the legacy `fNodeInput` / `fNodeOutput` / `fNodeOutlet` directives with a single `[fConnector]` directive whose role is set by `fConnectorType` (`'source' | 'target' | 'source-target' | 'outlet'`, default `'source-target'`). All connector ids now live in **one registry**: there are no separate input/output namespaces anymore, so a `fConnectorId` must be unique across the flow, and one id can serve as both endpoint roles via `source-target`.

skill-map's canonical shape (the same-element pattern, directives on the `[fNode]` host):

```html
<div fNode fDragHandle
     fConnector fConnectorType="source-target"
     [fNodeId]="node.id"
     [fNodePosition]="node.position"
     [fConnectorId]="node.id">
  <sm-node-card … />
</div>
```

Connector ids are **plain node ids**. The old `node.id + '-in'` / `node.id + '-out'` suffix convention is gone: with one connector per node and a unified registry there is nothing to disambiguate, and `<f-connection>` binds `[fSourceId]="edge.from"` / `[fTargetId]="edge.to"` directly. Session anchors (spawn overlay) use the same directive with a narrower role: `fConnector fConnectorType="source" [fConnectorId]="session.id"`.

Two defaults changed with the unified directive, worth knowing when porting legacy code:

- `fConnectorMultiple` defaults to **true** (a legacy `fNodeOutput` was single-connection unless `fOutputMultiple` was set).
- `fCanBeConnectedTo` replaces the legacy `fCanBeConnectedInputs` for connection allow-lists.

**Legacy note**: the old directives still work (deprecated since v19, one release of grace, do not write them in new code). Under them, ids lived in per-direction registries, so `fInputId` and `fOutputId` on the same node had to be different strings (hence the `-in` / `-out` suffixes you will still see in the official v18-era examples). Reusing `node.id` for both silently dropped every edge. If edges do not show and the console is clean, check that every `fSourceId` / `fTargetId` on your connections matches a registered `fConnectorId` (see troubleshooting #1).

### 2. Wire the theme — either the global `default.scss` OR per-view SCSS mixins

Connections and markers render as invisible SVG without the theme. Two supported paths:

**Path A — global import via `angular.json` (what skill-map uses today):**

Wire `../node_modules/@foblex/flow/styles/default.scss` as the first entry in the `styles` array. Two gotchas:

- **Workspace hoisting**: this repo uses npm workspaces. `@foblex/flow` hoists to the repo-root `node_modules/`, not `ui/node_modules/`. The `../` is required — a literal `node_modules/@foblex/flow/...` resolves relative to `ui/` and fails.
- **Package `exports` blocks subpaths**: `@foblex/flow`'s `package.json` declares `exports` that only expose `.` and `./package.json`. A package-resolution specifier (`@foblex/flow/styles/default.scss`) is rejected by modern resolvers. The raw filesystem path via `../node_modules/...` bypasses exports and works.

`angular.json` changes do NOT hot-reload — dev server restart required.

**Path B — per-view SCSS mixins (what every official `libs/f-examples/*` does):**

```scss
@use '@foblex/flow/styles' as flow-theme;

::ng-deep { @include flow-theme.theme-tokens(); }          // CSS vars (--ff-*)

::ng-deep f-flow {
  @include flow-theme.flow($scoped: false);                // base styles
  @include flow-theme.connection($scoped: false);          // connections
  @include flow-theme.connection-markers($scoped: false);  // markers
  // …only the features this view uses
}

@include flow-theme.node($selectorless: false);
```

Available mixins: `theme-tokens`, `flow`, `node`, `group`, `connector`, `connection`, `connection-markers`, `drag-handle`, `resize-handle`, `rotate-handle`, `minimap`, `selection-area`, `background`, `grid-system`. Use this path when you need a feature only in one view (smaller CSS, no angular.json surgery), or when debugging theme drift — it makes it obvious which mixins the view depends on. Examples: `references/examples/` → any `example.scss`.

**Dark mode**: the shipped theme already paints a full dark palette under `.dark` and `[data-theme='dark']` (see `@foblex/flow/styles/tokens/_semantic.scss` — every `--ff-color-*` is redeclared in that block). Whatever class your app uses to flag dark mode (PrimeNG/Aura uses `.app-dark` here, registered via `darkModeSelector` in `app.config.ts`), make sure `.dark` is **also** toggled on `documentElement` so Foblex picks up its own dark tokens. The `ThemeService` in this repo flips both classes from a single signal.

Antipattern — do NOT redeclare `--ff-color-*` inside your own `.app-dark { ... }` block to "force" the graph into dark. That duplicates the package's palette, drifts the day Foblex updates a token, and is exactly the "papering over a missed setup step" pattern AGENTS.md prohibits. The fix is one line in the theme service, not a parallel token table.

### 3. Never animate or override properties Foblex controls via inline styles

Foblex applies `transform: translate(x, y)` inline on every `[fNode]` element (from `fNodePosition`) and on `.f-canvas` (from zoom/pan). App-level CSS that touches those transforms fights the library. Do NOT write:

- `transition: transform ...` on a node class — every position update gets smoothed for the transition duration; connection paths recalculate mid-interpolation → visible lag on zoom/pan/drag.
- `:hover { transform: translateY(-1px) }` on a `[fNode]` — overwrites Foblex's position translate; hovered nodes snap to the viewport origin.
- Any `transform` or `transition: transform` on `.f-canvas` — zoom stutter.
- `will-change: transform` on `[fNode]` — redundant and can burn GPU memory.

For hover/focus affordances use `background`, `border`, `border-color`, `border-radius`, `box-shadow`, `color`, `padding`. Those are safe to animate. If you feel the urge to animate a position yourself, you are duplicating Foblex's job — use `centerGroupOrNode(id, animated)`, `setScale(scale, pivot, animated)` etc. instead.

### 4. Use Foblex's own connection markers — never hand-roll `<svg><defs><marker>`

Foblex ships `<f-connection-marker-arrow>` and `<f-connection-marker-circle>` that project inside `<f-connection>`. They follow the theme (`--ff-marker-color` defaults to `--ff-connection-color`) and automatically participate in selection and snap states.

```html
<f-connection [fSourceId]="..." [fTargetId]="..." class="my-edge-kind">
  <f-connection-marker-arrow type="end" />
</f-connection>
```

For custom shapes (diamonds, triangles, anything beyond an arrow) use the `fMarker` directive on an inline `<svg>` with your own `<path>`. See `references/api-reference.md` §Connection Markers.

If you catch yourself writing `<svg class="defs"><marker id="...">...</marker></svg>` and `marker-end: url(#id)` in CSS, stop — you are reinventing the library.

### 5. Per-kind connection styling goes through theme tokens, not `::ng-deep`

The default theme reads `--ff-connection-color`, `--ff-connection-width`, `--ff-marker-color` (see `@foblex/flow/styles/tokens/_ff-aliases.scss`). Override the tokens on a class attached to `<f-connection>`:

```css
.f-conn--mentions {
  --ff-connection-color: var(--sm-edge-mentions);
  --ff-connection-width: 2.5px;
  --ff-marker-color: var(--sm-edge-mentions);
}
```

CSS custom properties inherit through Angular's emulated encapsulation, so **no `::ng-deep` is needed** for this.

When a property has no theme token (e.g. `stroke-dasharray`) or you need to hide something the library renders, fall back to `::ng-deep` **scoped to a wrapper element you own, in the view's component CSS**. View-specific Foblex overrides belong in the view's stylesheet, not global `src/styles.css`. Canonical pattern:

```css
/* graph-view.css */
.graph__canvas-wrap ::ng-deep .f-conn--related .f-connection-path {
  stroke-dasharray: 4 3;
}
```

`.graph__canvas-wrap` bounds the reach; `::ng-deep` pierces into Foblex's rendered SVG. `::ng-deep` is deprecated in Angular but still the officially documented escape hatch — and Foblex's own examples use it. Use it narrowly, one rule at a time, under a wrapper class you own.

### 6. Foblex separates interaction from rendering — disabling behavior does NOT hide the visual

Example: `<f-connection [fReassignDisabled]="true">` prevents drag-to-reassign but the theme still paints the endpoint drag-handle circles (blue rings by default, from `--ff-color-accent`). Read-only views must both disable the interaction via input AND suppress the visual. For suppression:

- **Prefer token overrides** when the theme exposes one. Drag-handle ring → `--ff-connection-drag-handle-stroke`:
  ```css
  .graph__canvas-wrap {
    --ff-connection-drag-handle-stroke: transparent;
  }
  ```
  Custom properties inherit through Foblex's SVG, so the `<circle>` stays in the DOM (preserves the library's layout and hit-testing) but renders invisible. Zero `::ng-deep`.
- **Connector sockets** (the 16×16 circles painted on every connector element (`[fConnector]`, or the legacy `fNodeInput` / `fNodeOutput`) by `_socket-frame` — blue when connected, neutral when idle, see `_connector.scss`) follow the same pattern. To suppress them entirely (e.g. for an "arrow only" read-only graph) override the four colour tokens at the wrapper level:
  ```css
  .graph__canvas-wrap {
    --ff-connector-background-color: transparent;
    --ff-connector-border-color: transparent;
    --ff-connector-connected-color: transparent;
    --ff-connector-node-ring-color: transparent;
  }
  ```
  The connector elements (`[fConnector]`, or legacy `<div fNodeInput>` / `<div fNodeOutput>`) MUST stay in the DOM (they are the geometric anchors the connection layer reads to compute arrow endpoints — see rule 8 for the complementary positioning requirement). Painting them invisible keeps the geometry while removing the visual noise.
- When no token exists, override `fill` / `stroke` directly via `::ng-deep` scoped to a wrapper you own. **Prefer `fill: transparent` / `stroke: transparent` over `display: none`** — the library often depends on the element existing for internal calculations.

### 7. `::ng-deep` is Foblex's documented escape hatch, not a hack

Foblex's own reference examples (e.g. `apps/example-apps/uml-diagram` in Foblex/f-flow) style connections, markers, drag handles and minimaps with `::ng-deep <component-host-tag> { ... }`. It is deprecated in Angular but still functional and is the documented path when a theme token does not exist. Rules of use in this repo:

1. Prefer token overrides (rule 5) whenever the property has one.
2. When `::ng-deep` is the only option, scope it under the view's component host or a wrapper class you own.
3. Keep each rule narrow — single concern, minimal properties.
4. The rule lives in the view's component CSS, NOT in `src/styles.css`. Globals are for rules that are genuinely app-wide.

### 8. Connector sub-elements need explicit positioning — directives don't add orientation classes

Connector directives apply fixed host classes (`[fConnector]`: `f-component`, `f-connector`, plus role classes `f-connector-source` / `f-connector-target` / `f-connector-source-target` / `f-connector-outlet`; legacy directives: `f-node-input`, `f-node-output`) plus state classes (`f-connector-multiple`, `f-connector-disabled`, `f-connector-connectable`, legacy `f-node-input-connected`, etc. — see `fesm2022/foblex-flow.mjs` host bindings). What they do **NOT** do is translate `fConnectorConnectableSide` (legacy `fInputConnectableSide` / `fOutputConnectableSide`) into orientation classes like `.top` / `.bottom` / `.left` / `.right`. Those orientation classes exist in `_socket-frame` (`@foblex/flow/styles/domains/_connector.scss`) as `&.top { top: calc(var(--ff-connector-size) / -2); ... }` etc., but the SCSS only fires when **you put the class on the element manually**.

The default theme applies `position: absolute` plus a 16×16 size to every connector socket via `_socket-frame`. Without an explicit `top` / `right` / `bottom` / `left` from your CSS, `position: absolute` defaults to the upper-left corner of the nearest positioned ancestor — i.e. **the connector renders at the card's top-left corner, and the connection's arrow follows it there.** Symptom: arrows appear "off to one side" of the card or partially behind it; nodes look fine until you eyeball where edges actually terminate.

This bites only when connectors are **sub-elements** of the node card. Two layout shapes:

**Sub-element pattern** (two connector elements inside the card; ids stay distinct because the unified registry rejects duplicates):

```html
<div fNode [fNodeId]="node.id" class="sm-gnode">
  <div fConnector
       fConnectorType="target"
       [fConnectorId]="node.id + '-in'"
       [fConnectorConnectableSide]="'top'"
       class="sm-gnode__connector sm-gnode__connector--in"></div>
  <span>{{ node.label }}</span>
  <div fConnector
       fConnectorType="source"
       [fConnectorId]="node.id + '-out'"
       [fConnectorConnectableSide]="'bottom'"
       class="sm-gnode__connector sm-gnode__connector--out"></div>
</div>
```

```css
.sm-gnode { position: relative; /* …content… */ }
.sm-gnode__connector { position: absolute; pointer-events: none; }
.sm-gnode__connector--in {
  top: calc(var(--ff-connector-size) / -2);
  left: 50%;
  transform: translateX(-50%);
}
.sm-gnode__connector--out {
  bottom: calc(var(--ff-connector-size) / -2);
  left: 50%;
  transform: translateX(-50%);
}
```

The `calc(var(--ff-connector-size) / -2)` matches the math `_socket-frame` uses internally for `&.top` / `&.bottom`, so the socket centers exactly on the card's edge regardless of theme overrides to `--ff-connector-size`.

**Same-element pattern (skill-map today, and every official example — bracket, call-center, uml-diagram):**

```html
<div class="sm-gnode-host"
     fNode [fNodeId]="node.id"
     fConnector fConnectorType="source-target" [fConnectorId]="node.id">
  …
</div>
```

When the directive sits on the card itself, the card IS the connector — connection geometry anchors to the card's edges naturally and no extra positioning is needed. This is skill-map's current shape (rule 1); the v18-era official examples do the same thing with the legacy pair (`fNodeInput [fInputId]="m.id"` plus `fNodeOutput [fOutputId]="m.id"` on one element, which the unified `source-target` type folds into a single directive). The sub-element trap above only matters when you split connectors out into child elements.

If you're tempted to delete CSS rules positioning connector sub-elements (`[fConnector]`, legacy `[fNodeInput]` / `[fNodeOutput]`) because "Foblex's `_socket-frame` covers it" — stop. The socket is positioned `absolute` but with no offsets; you own the offsets.

### 9. Foblex's drag directives consume `pointerup` — use `mouseup` for drag-end detection

`fDragHandle` and `fDraggable` capture the pointer for the drag lifecycle (likely via `setPointerCapture` + propagation handling). A `pointerup` listener registered on `document` — even with `{ capture: true, once: true }` and a `queueMicrotask` defer — does NOT reliably fire when a node drag ends. The event is consumed or rerouted internally before reaching the handler.

Symptom: you wire a `pointerdown` → `pointerup` pair on `document` to detect "drag ended" (e.g. to flush a buffer or persist final positions to localStorage), it works in isolation but never fires after a `[fNode]` drag. State silently never updates.

**Fix**: listen on `mouseup` instead. The browser fires both pointer and mouse events for the same physical interaction; Foblex intercepts pointer events but not mouse events. The middle-mouse pan in `graph-view.ts` (`onCanvasMouseDown` → `document.addEventListener('mouseup', …)`) has used this approach since day one — that was the hint.

```ts
onNodePointerDown(event: PointerEvent): void {
  this.pointerDownAt = { x: event.clientX, y: event.clientY };
  document.addEventListener('mouseup', this.onNodeMouseUp, { once: true });
}

private dragInProgress = false;
private dragBuffer: TNodePositions | null = null;

private readonly onNodeMouseUp = (): void => {
  // Defer one microtask so any final fNodePositionChange Foblex emits
  // synchronously around the up event lands in the buffer first.
  queueMicrotask(() => {
    if (!this.dragInProgress) { this.dragBuffer = null; return; }
    this.dragInProgress = false;
    if (this.dragBuffer) this.nodePositions.set(this.dragBuffer);
    this.dragBuffer = null;
    writeStoredNodePositions(this.nodePositions());
  });
};

onNodePositionChange(id: string, position: IPoint): void {
  // Buffer in a non-signal field. Writing the signal here would
  // invalidate the `graph` computed and force a full @for diff over
  // nodes/edges 60–120×/sec for nothing — Foblex already updates the
  // dragged node's DOM transform internally during drag.
  if (!this.dragBuffer) this.dragBuffer = { ...this.nodePositions() };
  this.dragBuffer[id] = { x: position.x, y: position.y };
  this.dragInProgress = true;
}
```

Two reinforcing perf wins land in this pattern, both hidden by a 120 fps rAF reading:

1. **Single signal write at drag-end** — not 60–120/sec during drag. Eliminates the `graph` computed invalidation cascade through the @for over nodes and edges.
2. **Single localStorage I/O at drag-end** — sync `setItem` calls during drag pile up as 1–5 ms stalls each (more on slow disks). The avg fps stays high but every frame during drag has a stall, producing perceivable jank.

If you reach for `pointerup` thinking it is the "modern pointer event API", read this rule first.

## Antipattern checklist

If you catch yourself typing any of these, stop and re-read the rule in parentheses:

- `<svg ...><marker id="..."` — use `<f-connection-marker-arrow>` (rule 4)
- `marker-end: url(#...)` in CSS — use `<f-connection-marker-arrow>` (rule 4)
- `::ng-deep .f-connection-path { stroke: ...; stroke-width: ... }` — override `--ff-connection-color` / `--ff-connection-width` on the `<f-connection>` class (rule 5)
- `::ng-deep .f-canvas` with any rule — almost certainly wrong; the canvas transform is library-controlled (rule 3)
- `transition: transform ...` or `transform: ...` on `[fNode]` / `.f-canvas` (rule 3)
- `display: none` on a library-rendered element — use `fill: transparent` / `stroke: transparent` instead (rule 6)
- View-specific Foblex CSS in `src/styles.css` — move to the view's component CSS (rules 5 and 7)
- Custom class names prefixed with `f-` — that prefix is reserved by Foblex. Our nodes use `sm-gnode` for this reason. Pick a project prefix (`sm-`) for your own classes
- Restoring a viewport with `canvas.setPosition(...)` + `canvas.setScale(...)` — use the `[position]` / `[scale]` input bindings on `<f-canvas>` instead (see "Persisted viewport" pattern)
- Binding `[position]` / `[scale]` to a **constant** (field-init literal, `readonly` value that never reassigns) — Foblex re-evaluates the inputs on every CD pass and reconciles against its internal viewport, so any user pan / zoom gets undone the next time the host re-renders. Bind to a signal that `(fCanvasChange)` writes (see "Persisted viewport" pattern)
- Redeclaring `--ff-color-*` inside your own `.app-dark { ... }` block — the package already ships dark defaults under `.dark` / `[data-theme='dark']`; toggle that class on the document root from your theme service instead (rule 2, "Dark mode")
- Deleting your own `position: absolute; top/bottom: ...` rules from connector sub-elements because "Foblex's `_socket-frame` already handles it" — it sets `position: absolute` and a 16×16 size, but no offsets; you own the offsets when connectors are sub-elements (rule 8)
- Expecting `fConnectorConnectableSide` (or the legacy `fInputConnectableSide` / `fOutputConnectableSide`) to add `.top` / `.bottom` / `.left` / `.right` classes automatically — they don't; the directive only stores the side as metadata, the orientation classes are SCSS sub-classes you place yourself (rule 8)
- Writing `fNodeInput` / `fNodeOutput` / `fNodeOutlet` (or `fInputId` / `fOutputId` on `<f-connection>`) in new code: deprecated legacy since v19; use `[fConnector]` + `fConnectorId` and `fSourceId` / `fTargetId` (rule 1)
- Binding sides on both the connector AND the connection: `fConnectorConnectableSide` on `[fConnector]` and `fSourceSide` / `fTargetSide` on `<f-connection>` compete for the same decision; pick ONE level. skill-map binds at the connection level only (`[fSourceSide]="outputSide()"` / `[fTargetSide]="inputSide()"`), connector-level sides stay unset
- Writing `selectedNodeId.set(...)` directly from a click handler, deep link, or effect: every programmatic selection write routes through `applySelection(id)` so Foblex's internal selection, the `.f-selected` paint, and the keyboard layer's active item stay in sync (see "Selection single-owner contract")
- Wrapping the `<div fNode>` inner DOM in a shared `<ng-template>` and projecting it with `<ng-container *ngTemplateOutlet>` for DRY-ness — Foblex's content queries on `[fNode]` don't reach into embedded views, so connectors disappear and every node renders at `(0,0)` in a redraw loop. Duplicate the markup in each branch instead (see "Performance levers from the stress-test example")
- Adding `<f-background>` and seeing the grid only at the edges (centre is solid colour) — `<f-canvas>` paints `--ff-canvas-background-color` opaque on top of the background layer. Override it to `transparent` at your wrapper (see "Background grid" canonical pattern)
- Painting an `:hover` / `:focus` outline using `border-color` change on `[fNode]` cards while a sibling-class state (`.sm-gnode--selected` / `.sm-gnode--highlighted`) sets the same property — the cascade fights between user gestures and selection state. Keep gesture state on a different property (`box-shadow`) so the two layers compose instead of conflict
- `document.addEventListener('pointerup', …)` to detect the end of a `[fNode]` drag — `fDragHandle` consumes pointerup; the listener never fires. Use `mouseup` instead (rule 9)
- Mirroring every `(fSelectionChange)` into app state unconditionally: `SelectByPointer` selects on **pointerdown**, so grabbing a node to move it reports a selection at drag start and pops the inspector open mid-drag. Reject the event while `f-dragging` is on the flow host, and re-assert the app selection at the `mouseup` flush (see "Drag is not a click")
- Guarding only the app's `(click)` handler with a drag-distance check and assuming drags can no longer select, the library's own `fSelectionChange` never passes through that handler
- Writing to a signal that feeds the `graph` computed (typically `nodePositions`) on every `(fNodePositionChange)` — invalidates the @for over nodes/edges 60–120×/sec. Buffer the position in a non-signal field and flush once at `mouseup` (rule 9)
- Calling `localStorage.setItem` (or any sync I/O) from inside `(fNodePositionChange)` — sync writes during drag stall the main thread per frame and produce visible jank even when rAF reads 120 fps. Defer to the `mouseup` flush (rule 9)

## Canonical patterns

### Read-only graph (no editing, no reassign, no selection)

```html
<f-flow fDraggable>
  <f-canvas fZoom [fZoomStep]="0.06" [fZoomDblClickStep]="0.35">
    <f-connection
      [fSourceId]="edge.from"
      [fTargetId]="edge.to"
      [fSourceSide]="outputSide()"
      [fTargetSide]="inputSide()"
      fType="segment"
      fBehavior="fixed"
      [fReassignDisabled]="true"
      [fSelectionDisabled]="true"
      [class]="'f-conn--' + edge.kind"
    >
      <f-connection-marker-arrow type="end" />
    </f-connection>
    <!-- nodes carry: fConnector fConnectorType="source-target" [fConnectorId]="node.id" -->
  </f-canvas>
</f-flow>
```

Endpoint ids are plain node ids matched against `fConnectorId` (rule 1). Sides are bound at the **connection level only** (`fSourceSide` / `fTargetSide`, type `EFConnectionConnectableSide`, driven here by the layout-direction signals); connector-level `fConnectorConnectableSide` stays unset so the two levels never fight.

```css
.graph__canvas-wrap {
  /* Token overrides: hide reassign rings, let library keep the DOM intact */
  --ff-connection-drag-handle-stroke: transparent;
}
.f-conn--mentions {
  --ff-connection-color: var(--sm-edge-mentions);
  --ff-connection-width: 2.5px;
  --ff-marker-color: var(--sm-edge-mentions);
}
/* stroke-dasharray has no token — scoped ::ng-deep, component CSS only */
.graph__canvas-wrap ::ng-deep .f-conn--related .f-connection-path {
  stroke-dasharray: 4 3;
}
```

### Persisted viewport (localStorage / restore across reloads)

Restoring pan position and zoom is the ONE place where the intuitive imperative API (`setPosition` + `setScale`) produces silent, visually broken output. Symptoms: arrows missing on first paint, nodes rendered at an offset, and both only reconciling after the first user pan/zoom. Reason: the calls update the transform model out of phase with the connection measurement pass, so the SVG connection layer renders against stale geometry.

**Use the `[position]` and `[scale]` input bindings on `<f-canvas>` instead.** This is the pattern the official `libs/f-examples/advanced/undo-redo` uses — Foblex applies the transform once, atomically, on the first render.

**Critical**: bind to **signals**, NOT to field-initialized literals. Foblex re-evaluates `[position]` / `[scale]` on every change-detection pass; if the bound value drifts from the canvas's internal viewport (e.g. user pans → internal viewport moves; the bound literal stays at its boot value), Foblex re-applies the bound value to "reconcile" and snaps the canvas back to the boot position. Symptom: every re-render of the host (a WebSocket-driven `nodes` refresh, a filter toggle, anything that invalidates a parent computed) snaps the viewport back to wherever it was when the component mounted. Storing the viewport in signals that `(fCanvasChange)` writes keeps the binding always in sync with the canvas's own state, so reconciliation is a no-op.

A reproducible test for the bug: start the app, pan the canvas a bit, then trigger any state change that re-runs change detection on the host (e.g. WS push, filter toggle). If the canvas snaps back, the bindings are constants instead of signals — F5 "fixes" it because the field initializer re-runs and picks up the panned position from localStorage, which masks the underlying defect.

```ts
private readonly savedViewport = readStoredViewport(); // localStorage parse

// Signals — NOT field-init constants. (fCanvasChange) writes them on
// every pan / zoom so the binding stays in sync with the canvas's
// internal viewport, neutralising Foblex's reconcile-on-CD behaviour.
protected readonly viewportPosition = signal<IPoint>(
  this.savedViewport
    ? { x: this.savedViewport.x, y: this.savedViewport.y }
    : { x: 0, y: 0 },
);
protected readonly viewportScale = signal<number>(this.savedViewport?.scale ?? 1);

private hasCompletedInitialLayout = false;

constructor() {
  effect(() => {
    const data = this.graph();
    if (data.nodes.length === 0) return;
    queueMicrotask(() => {
      if (this.hasCompletedInitialLayout) {
        this.canvas()?.fitToScreen({ x: 40, y: 40 }, false); // filter-driven refit
        return;
      }
      this.hasCompletedInitialLayout = true;
      // If a viewport was restored, the [position] / [scale] bindings already
      // placed the canvas. Only auto-fit on a clean slate.
      if (!this.savedViewport) this.canvas()?.fitToScreen({ x: 40, y: 40 }, false);
    });
  });
}

onCanvasChange(event: FCanvasChangeEvent): void {
  // Mirror the canvas's internal viewport into our bound signals so a
  // future change-detection pass doesn't reconcile and snap back.
  this.viewportPosition.set({ x: event.position.x, y: event.position.y });
  this.viewportScale.set(event.scale);
  if (!this.hasCompletedInitialLayout) return;
  localStorage.setItem(KEY, JSON.stringify({
    x: event.position.x, y: event.position.y, scale: event.scale,
  }));
}
```

```html
<f-canvas
  fZoom
  [position]="viewportPosition()"
  [scale]="viewportScale()"
  [debounceTime]="150"
  (fCanvasChange)="onCanvasChange($event)"
>
```

Notes:

- Initialise the signals **in a field initializer** (not after `ngOnInit`) — the binding is evaluated on first template pass.
- `(fCanvasChange)` MUST write back into the signals. That is what keeps the bound value in sync with the canvas. Skipping the write is the bug.
- The `hasCompletedInitialLayout` guard is essential. Without it, the first auto-fired `fCanvasChange` (triggered by the initial binding) overwrites storage with `{0,0,1}` before the user has touched anything.
- Never mix two sources of truth for the SAME axis on one mount: position has only one public path anyway (the `[position]` binding, see below); for scale, pick the `[scale]` binding OR `setScale()`, not both.
- **Foblex 18.6 removed the public `setPosition`** (it is now an internal `_setPosition`), so there is NO imperative pan setter left: EVERY position change goes through the `[position]` signal binding, the restore path AND post-mount interactions like a middle-mouse pan. Drive the pan by writing the same `viewportPosition` signal `[position]` is bound to, Foblex applies the transform and redraws on the input change (no manual `redraw()`), which is exactly what `middle-mouse-pan.ts` does. `setScale()` stays public for post-mount zoom (wheel / pinch / buttons), and `getPosition()` / `getScale()` still read the live viewport.

### Selection single-owner contract + node/edge highlighting (click or arrows → light up neighbours)

The highlight/dim mechanics were lifted from `apps/example-apps/tournament-bracket` in Foblex/f-flow, but the ownership stance changed with v19: **Foblex owns selection now**. (The old skill-map shape where the app owned selection exclusively and Foblex never saw it is gone; with the keyboard layer installed, Foblex's internal selection drives the `.f-selected` paint and the keyboard focus, so a divergent app-only signal would desync them.)

**The bridge** (see `graph-view.ts`, `applySelection` / `onFlowSelectionChange` for the authoritative wording): every PROGRAMMATIC selection write (click handler, isolate, deep links, escape/background deselect, the filter guard) goes through one helper that sets the app signal AND pushes into Foblex; user gestures (click, arrow keys, Shift+area rectangle, Ctrl/Cmd+A) flow the other way, Foblex mutates its own selection and reports through `(fSelectionChange)`. Writes are idempotent, so the two paths converging on the same id is harmless.

```ts
private applySelection(id: string | null): void {
  this.selectedNodeId.set(id);
  this.flow()?.select(id === null ? [] : [id], [], false);
}

// Foblex → app bridge. Exactly one selected node drives the inspector /
// highlight state; empty and multi-node selections (Shift+area
// rectangle, Ctrl/Cmd+A) both map to "no inspected node".
protected onFlowSelectionChange(event: FSelectionChangeEvent): void {
  if (isFlowDragging(this.flow()?.hostElement)) return;   // see "Drag is not a click" below
  const ids = event.fNodeIds;
  this.selectedNodeId.set(ids.length === 1 ? (ids[0] ?? null) : null);
}
```

Wire `(fSelectionChange)="onFlowSelectionChange($event)"` on `<f-flow fDraggable>`. The third argument of `FFlowComponent.select(nodes, connections, isSelectedChanged)` is `false` so the programmatic write does not re-emit `fSelectionChange` (that would loop the bridge). The event payload is `FSelectionChangeEvent` with `fNodeIds` / `fGroupIds` / `fConnectionIds` (in v19 these are aliases of the canonical `nodeIds` / `groupIds` / `connectionIds` fields).

**Derived state** (an adjacency map computed from the graph):

```ts
readonly selectedNodeId = signal<string | null>(null);

private readonly adjacency = computed<Map<string, Set<string>>>(() => {
  const map = new Map<string, Set<string>>();
  for (const edge of this.graph().edges) {
    if (!map.has(edge.from)) map.set(edge.from, new Set());
    if (!map.has(edge.to)) map.set(edge.to, new Set());
    map.get(edge.from)!.add(edge.to);
    map.get(edge.to)!.add(edge.from);
  }
  return map;
});
```

**Pure helpers** (no side effects, drive the template classes):

```ts
isSelected(id: string)    { return this.selectedNodeId() === id; }
isHighlighted(id: string) { /* neighbour of selected */ }
isDimmed(id: string)      { /* selected exists, this is neither selected nor neighbour */ }
isEdgeHighlighted(e)      { /* one endpoint matches selected */ }
isEdgeDimmed(e)           { /* selected exists, neither endpoint matches */ }
```

**Template**: project edges and nodes through `ngProjectAs="[fConnections]"` / `ngProjectAs="[fNodes]"`, bind `isSelected` / `isHighlighted` / `isDimmed` to `sm-gnode--*` classes on each `<div fNode>` (plus `(click)="selectNode(...)"` / `(dblclick)="openNode(...)"`) and `isEdgeHighlighted` / `isEdgeDimmed` to `f-conn--*` classes on each `<f-connection>`. Style: `--selected` / `--highlighted` via `border-color` + `box-shadow`; `--dimmed` via host `opacity` (cascades to the SVG path, no `::ng-deep`); `.f-conn--highlighted { --ff-connection-width: 3px }` declared after the per-kind selectors so source order wins.

Notes:

- **Edge dim via host opacity**, not stroke alpha. The `<f-connection>` host has emulated encapsulation but `opacity` cascades to the SVG path it renders. No `::ng-deep`. Same trick the bracket SCSS uses.
- **Deselect** by listening for `(click)` on a wrapper around the canvas and ignoring clicks whose `event.target.closest('.sm-gnode')` (or any other interactive overlay) is non-null. Foblex's `<f-flow>` does not expose a "background-only click" event. The deselect itself is `applySelection(null)`, never a bare signal write. Two guards are mandatory on this handler: (a) a drag-distance check against the wrapper's own `mousedown` anchor, because the browser synthesizes a `click` at the END of any background drag (down and up both land on the canvas), so releasing a Shift+marquee would otherwise wipe the selection it just built; (b) skip when `shiftKey`/`ctrlKey`/`metaKey` is held, those are selection-BUILDING gestures (additive marquee, `SelectByPointer` toggle) that Foblex answers by keeping its selection, and clearing on its behalf fights the library.
- **Single click selects, double click navigates** to the inspector. Same gesture as Finder / file managers; descoverable. Maintain a small drag-distance guard in the click handler so a node-drag doesn't fire `selectNode`.
- **Selection guard via effect**: when filters change and the selected node is no longer visible, clear the selection (`effect(() => { if (!this.graph().nodes.some(n => n.id === id)) this.applySelection(null); })`). Avoids dangling highlight state on both sides of the bridge.

**Drag is not a click: the bridge must reject drag-induced selections.**

`SelectByPointer` runs in Foblex's `_pointerDownClaimants`, so **grabbing a node to MOVE it already selects it**, on pointerdown, before anyone knows a drag is coming. The selection is then reported the instant the drag threshold is crossed (`EmitStartDragSequenceEvent` → `EmitSelectionChangeEventRequest`). A bridge that mirrors every `fSelectionChange` therefore pops the inspector open **mid-drag**, on a gesture that never meant "inspect this". A drag-distance guard on the `(click)` handler does NOT save you: the guard only covers the app's own handler, the library's event bypasses it entirely.

The only order-safe discriminator is the **`f-dragging` host class** (`F_CSS_CLASS.DRAG_AND_DROP.DRAGGING`, the same class Foblex's `:host(.f-dragging)` styles read). `EmitStartDragSequenceEvent` stamps it one statement BEFORE emitting the selection change, so it is already on the `<f-flow>` host when the handler runs. Everything else is too late: `(fDragStarted)` is emitted AFTER the selection event, and the position stream (`fNodePositionChange`) only starts on the following `onPointerMove`.

```ts
export function isFlowDragging(host: HTMLElement | null | undefined): boolean {
  return host?.classList.contains(F_CSS_CLASS.DRAG_AND_DROP.DRAGGING) === true;
}
```

Suppressing the mirror is only half the fix: Foblex's internal selection now holds the dragged node (painted `.f-selected`) while the app still inspects another one. **Re-assert the app's selection when the drag settles**, `applySelection(this.selectedNodeId())`, from the rule 9 `mouseup` flush. That moment is safe to mutate library state from: Foblex finalizes its drag on `pointerup`, which the browser fires *before* `mouseup`, so the whole finalize + `reset()` pipeline has already run. Do NOT hang the re-assert on `(fDragEnded)` instead: it fires for every drag kind, and a Shift+area marquee applies its selection in `SelectionAreaFinalize` *before* that event, so a blanket re-assert would wipe the marquee.

The re-assert itself must also be **multi-selection aware**: when the settled drag moved a multi-node selection (marquee or Ctrl/Cmd+click set; grabbing an already-selected node keeps the whole set and drags the group), Foblex's selection IS the user's intent, and pushing the app's single id over it would drop the group at release. Skip the re-assert when `flow.getSelection().fNodeIds.length > 1`; the single-node divergence it exists to fix cannot occur in that case. Related gesture handlers need the same courtesy: the app's own node `(click)` select must not run when a multi-select modifier (Shift/Ctrl/Cmd) is held, or it collapses the set the library just built on pointerdown. Note the multi-select toggle modifier is Ctrl (Cmd on macOS) by default (`fMultiSelectTrigger`); binding Shift+click to it is futile while `<f-selection-area>` keeps its default Shift trigger, because `SelectionAreaPreparation` claims the pointer first and `SelectByPointer._isSelectionPhase` hard-rejects selection updates on Shift while the area holds the claim.

A plain click is untouched by all of this: the class is never stamped, the single emit arrives on pointerup via `finalizeDragSequence`, and the inspector opens as it always did.

### Keyboard a11y layer (v19, opt-in via `provideFFlow(withA11y(...))`)

v19 splits accessibility in two layers:

- **Semantic layer, ALWAYS on**: roles, `aria-roledescription`, accessible names for nodes/connections, and a live region for announcements. It ships in every v19 flow with zero setup; there is no way (and no reason) to opt out.
- **Keyboard layer, strictly opt-in**: arrow-key spatial node navigation, grab-and-move, keyboard connect, delete, select-all, and zoom keys. It only activates when the component registers `provideFFlow(withA11y(config))` in its `providers`. Opt-in because every pre-a11y app ships its own key handling and a default-on layer would double-drive selection and deletion.

skill-map's exact provider snippet (from `graph-view.ts`):

```ts
providers: [
  provideFLayout(DagreLayoutEngine, { mode: EFLayoutMode.MANUAL }),
  // Opt-in keyboard layer (Foblex v19): arrows move the selection
  // spatially, Space+arrows moves the selected node. The graph is
  // read-only, so the connection-creation and delete actions are
  // unbound. Selection ownership: Foblex is the single owner, see
  // `applySelection` / `onFlowSelectionChange`.
  provideFFlow(
    withA11y({
      keys: {
        connect: [],
        deleteSelected: [],
      },
    }),
  ),
],
```

`IFA11yConfig` fields:

| Field | Default | Meaning |
|---|---|---|
| `keyboard` | `true` (once `withA11y` is installed) | Master switch for the whole keyboard layer |
| `moveStep` | `10` | Canvas units per arrow key while a node is grabbed |
| `coarseMoveStep` | `50` | Same, for Shift+arrow |
| `messages` | English catalog | `Partial<IFA11yMessages>` overrides for every spoken/attached string |
| `keys` | see below | `IFA11yKeys` per-action key binding overrides |

`IFA11yKeys` defaults: `grab: [' ']` (Space), `connect: ['c']`, `deleteSelected: ['Delete', 'Backspace']`, `selectAll: ['a']` (with Ctrl/Cmd), `zoomIn: ['+', '=']`, `zoomOut: ['-', '_']`, `zoomReset: ['0']`. An **empty array unbinds the action** (that is how skill-map disables connect and delete on its read-only graph). Arrows, Enter, and Escape are structural and stay fixed.

Notes for this repo:

- **Grab stays enabled**: Space grabs the selected node, arrows move it, Space/Enter drops, Escape cancels. The movement flows through the SAME `fNodePositionChange` output as mouse drag, so the rule 9 buffer-and-flush persistence path covers keyboard moves with zero extra code.
- The keyboard layer moves Foblex's own selection, which is why the selection single-owner contract (previous pattern) is a prerequisite: without the `applySelection` bridge, arrow-key selection and the app's `selectedNodeId` drift apart.
- `provideFFlow(...features)` is the v19 flow-level feature composer; `withControlScheme(...)` also exists for alternative pointer/wheel gesture schemes (not used in skill-map, mention only).

Drop `<f-background>` + a pattern component as a sibling of `<f-canvas>` inside `<f-flow>`:

```html
<f-flow fDraggable [fCache]="…">
  <f-background>
    <f-rect-pattern />   <!-- or <f-circle-pattern /> for dots -->
  </f-background>
  <f-canvas …> … </f-canvas>
</f-flow>
```

`FFlowModule` re-exports `FBackgroundComponent` and the pattern components — no extra imports. Line colour comes from `--ff-background-line-color` / `--ff-background-dot-color` which already track `.dark`. `<f-rect-pattern>` accepts `vSize` / `hSize` / `vColor` / `hColor` if you want to tune density or override colours per view.

**Gotcha — wired but invisible in the centre**. `_flow-canvas.scss` paints both `<f-flow>` AND `<f-canvas>` with solid backgrounds (`--ff-flow-background-color` and `--ff-canvas-background-color` resp.). Since `<f-canvas>` renders **above** `<f-background>` in the DOM order Foblex builds, its solid fill covers the grid wherever the canvas extends — i.e. exactly the centre region around your nodes, which is where the grid most matters. Override the canvas background to transparent at your wrapper:

```css
.graph__canvas-wrap {
  --ff-canvas-background-color: transparent;
}
```

`<f-flow>` keeps its colour as the "paper" layer behind the grid; node cards keep their own opaque fills. The grid is now visible across the whole pannable surface. To retint it for an alternate theme, override `--ff-flow-background-color` (the surface) and `--ff-background-line-color` (the strokes) at your wrap, both cascade into the SVG without `::ng-deep`; `<f-rect-pattern>` also accepts `[vColor]` / `[hColor]` inputs for data-driven colours.

### Smooth wheel zoom

The wheel zoom has no easing option; the library has no "animated" wheel. Smoothness comes from step size. `fZoomStep` defaults to `0.1` which feels abrupt. For graph views with up to ~100 nodes, `0.04–0.08` gives a continuous feel.

- Default: `0.1`
- Abrupt: >`0.1`
- Balanced: `0.06`
- Very fine: `0.03` (can feel slow on tall viewports)

Double-click zoom (`fZoomDblClickStep`) uses a larger step by default (`0.5`). `0.25–0.35` is usually right when the wheel is already fine.

## Useful patterns from the official examples

These are not non-negotiables — they are canonical shapes that repeat across `libs/f-examples/*`. Full catalog and code in [`references/examples/README.md`](references/examples/README.md).

- **Post-render viewport setup**: wire `(fLoaded)` or `(fFullRendered)` on `<f-flow>` and call `FCanvasComponent.resetScaleAndCenter(animated)` once the graph is measured. Use `(fFullRendered)` when the next step needs real connector geometry.
- **Per-connector side overrides**: `fConnectorConnectableSide` on the connector element (legacy `fOutputConnectableSide` / `fInputConnectableSide`) pins the edge to `top | right | bottom | left | auto` per connector, independent of the connection-level `fSourceSide` / `fTargetSide`. skill-map does NOT use connector-level sides; it binds sides at the connection level only (see the "Read-only graph" pattern and the antipattern about double-binding sides).
- **Markers catalog**: use `<f-connection-marker-arrow>` / `<f-connection-marker-circle>` for the defaults, and `svg[fMarker]` for custom geometry. The `EFMarkerType` enum covers `START`, `END`, `SELECTED_START`, `SELECTED_END`, `START_ALL_STATES`, `END_ALL_STATES` — use `*_ALL_STATES` unless selection needs a different glyph.
- **Signals + OnPush + standalone** is the default authoring shape in every example. Stick with it.
- **Performance levers from the stress-test example** (`libs/f-examples/nodes/stress-test`): three independent toggles to scale to thousands of nodes.
  1. **`[fCache]="true"` on `<f-flow>`**: enables Foblex's internal geometry cache. Connector positions and connection geometry are reused across redraws (pan / zoom / drag). Safe ON by default — the library invalidates the cache on relevant input changes.
  2. **`ngProjectAs="[fNodes]"` / `ngProjectAs="[fConnections]"`** on a `<ng-container>` wrapper around the iteration. Foblex defines content-projection slots for nodes and connections; using them clarifies the structure and is a **prerequisite for `*fVirtualFor`** (virtualization needs to know which slot it is feeding).
  3. **`*fVirtualFor`** (`FVirtualFor`, standalone directive — import explicitly, NOT bundled in `FFlowModule`). Virtualises node rendering: only nodes whose bounding box intersects the viewport plus a buffer end up in the DOM. Pays off around 300+ visible nodes; below that the bookkeeping cost outweighs the saved render cost. The stress-test ships it behind a checkbox for a reason — make it opt-in via a config flag in this repo too. Companion shape:
     ```html
     <ng-container ngProjectAs="[fNodes]" *fVirtualFor="let node of nodes()">
       <div fNode [fNodeId]="node.id" [fNodePosition]="node.position">…</div>
     </ng-container>
     ```
     `*fVirtualFor` does NOT support a `track` clause — it has its own `fVirtualForTrackBy` input if you need it.

  **Trap**: do NOT extract the `<div fNode>` body into a shared `<ng-template>` + `*ngTemplateOutlet` for DRY across the virtualization on/off branches, Foblex's content queries don't reach embedded views so connectors vanish and every node piles at `(0,0)` in a redraw loop (full symptoms in the antipattern checklist + troubleshooting #10). Duplicate the markup inline in each branch.
  Skill-map wires these three behind `ui/src/app/views/graph-view/graph-view.config.ts` (`GRAPH_PERF_FLAGS`). The perf HUD bottom-left in the canvas (FPS, frame time, heap, cache age) is the feedback loop for deciding when to flip them.

## Full API reference

Every directive, component, input, output, method, event, CSS class, token, and enum lives in [`references/api-reference.md`](references/api-reference.md). Load that file when you need:

- Exact input/output signatures of a directive or component
- The full list of CSS classes (`.f-canvas`, `.f-connection-*`, `.f-gnode-*`, markers, drag handles)
- The theme token catalog (`--ff-*` variables and what consumes them)
- Event payload shapes (`FCanvasChangeEvent`, node/connection events)
- Enums: `EFConnectionConnectableSide` (connection-level sides, what skill-map uses), `EFConnectableSide` (connector-level sides), `EFConnectionType`, `EFConnectionBehavior`, `EFMarkerType`, `EFZoomDirection`
- The v19 additions: the `[fConnector]` directive inputs, the renamed `f-connection` endpoint inputs, `provideFFlow` / `withA11y` / `IFA11yConfig` / `IFA11yKeys`, `FSelectionChangeEvent`
- SCSS mixin map for manual theme composition

## Official examples

Verbatim copies of every official `libs/f-examples/*` split by category under [`references/examples/`](references/examples/). Load the matching category file when touching that feature:

- [`examples/nodes.md`](references/examples/nodes.md) — node composition, drag handles, selection, resize, rotate, grouping, stress tests.
- [`examples/connectors.md`](references/examples/connectors.md) — legacy `fNodeInput` / `fNodeOutput` (v19: `[fConnector]`), connectable side, rules, outlets, limiting connections.
- [`examples/connections.md`](references/examples/connections.md) — `f-connection` types / behaviours / markers / content / waypoints and the drag-to-connect / reassign / snap lifecycle.
- [`examples/extensions.md`](references/examples/extensions.md) — background, grid, zoom, auto-pan, minimap, magnetic guides, palette, selection area.
- [`examples/plugins.md`](references/examples/plugins.md) — Dagre and ELK layout plugins + the shared `utils/` helpers.
- [`examples/advanced.md`](references/examples/advanced.md) — copy/paste, undo/redo, drag lifecycle, custom event triggers.
- [`examples/reference-apps.md`](references/examples/reference-apps.md) — pointers to the full-app demos (UML Diagram, Schema Designer, Tournament Bracket, Call Center, AI Low-Code Platform).

**Rule**: if our code disagrees with the corresponding example, the example wins. The Foblex team ships these to demonstrate the canonical shape.

## When something does not work and the console is clean

In order of likelihood:

1. **Edges missing** → rule 1: a connection's `fSourceId` / `fTargetId` does not match any registered `fConnectorId` (one unified registry in v19; typos and stale suffix conventions like `-in` / `-out` are the usual culprits). On legacy-directive code, the equivalent failure is `fInputId` / `fOutputId` colliding on the same node.
2. **Connections invisible, everything else fine** → rule 2 (theme not imported, or wrong path for monorepo).
3. **Zoom/pan lags, connectors "chase" nodes** → rule 3 (we animate a transform the library controls).
4. **Hovered node jumps to origin** → rule 3 (`:hover { transform: ... }` on a `[fNode]`).
5. **Blue circles at connection endpoints** → rule 6 (drag-handle ring; reassign disabled does not hide it; override `--ff-connection-drag-handle-stroke`).
6. **Arrow marker has wrong shape or wrong color** → rule 4 (check if we are rolling our own SVG markers) + rule 5 (check `--ff-marker-color` override).
7. **Restored viewport renders with arrow/node offset until first pan** → "Persisted viewport" canonical pattern (switch `setPosition`/`setScale` imperative calls to `[position]` / `[scale]` input bindings on `<f-canvas>`).
8. **Graph stays light when the rest of the app goes dark** → rule 2 "Dark mode": Foblex listens for `.dark` / `[data-theme='dark']`, not your PrimeNG/Aura selector. Toggle both classes from the theme service from a single signal.
9. **Connection arrows terminate at the wrong place — off to one side, behind the card, or far from where the connector should sit** → rule 8: connector sub-elements are `position: absolute` (set by `_socket-frame`) but get no top/right/bottom/left from the library. Without your own `top: calc(var(--ff-connector-size) / -2); left: 50%; transform: translateX(-50%)`, they collapse to `0,0` of the card and arrows follow them.
10. **All nodes pile up at canvas origin (0,0), canvas is mostly blank with only shadows, and the tab keeps redrawing** → the inner DOM of `[fNode]` was extracted to an `<ng-template>` and reused via `<ng-container *ngTemplateOutlet>`. Angular content queries don't cross into embedded views, so Foblex sees no connectors (`[fConnector]`, legacy `fNodeInput` / `fNodeOutput`), geometry never resolves, redraw runs forever. Duplicate the markup inline in each branch instead.
11. **Background grid renders only at the edges of the canvas wrap; centre region around the nodes is solid colour** → `<f-canvas>` is opaque (`--ff-canvas-background-color`) and covers `<f-background>` underneath. Override the canvas background to `transparent` at the wrapper (see "Background grid" canonical pattern).
12. **Filtering changes the layout — unmoved nodes jump and the viewport re-fits** → dagre is being run over the filtered subset on every change. Run dagre once over the FULL collection (cached `computed`) and only project to `visibleIds` at render time. Do not call `fitToScreen` from a filter-change effect; restrict it to the first render only and let the user use the explicit "Fit" toolbar button afterwards.
13. **Drag a node, release, refresh — the node is back at its previous position; pointerup-based persistence "just doesn't fire"** → `fDragHandle` consumes `pointerup` (rule 9). Switch the document listener to `mouseup`. Same fix applies to any one-off post-drag side effect (analytics, undo snapshot, etc.).
14. **Drag feels choppy even though the perf HUD reads 120 fps** → state is being written on every `(fNodePositionChange)`. Two compounding causes: (a) signal write invalidates the `graph` computed → @for diff over all nodes/edges 60–120×/sec; (b) sync `localStorage.setItem` per move adds 1–5 ms stalls per frame. Buffer the position in a non-signal field, flush at `mouseup` (rule 9).
15. **Pan / zoom snaps back to the boot position on every WS update / filter change / any host re-render — but a full F5 "fixes" it** → `[position]` / `[scale]` are bound to constants (field-init literals). Foblex re-evaluates the inputs on every CD pass and reconciles against its internal viewport, undoing the user's pan. F5 masks it because the field initializer re-runs and reads the panned position from localStorage. Bind to signals that `(fCanvasChange)` writes (see "Persisted viewport" canonical pattern).
16. **Dragging a node opens the inspector / changes the app's selection, even though the click handler has a drag-distance guard** → `SelectByPointer` selects the grabbed node on pointerdown and Foblex reports it via `fSelectionChange` the moment the drag threshold is crossed, bypassing the app's `(click)` handler entirely. Reject the event while the `<f-flow>` host carries `f-dragging`, then re-assert the app selection at the `mouseup` drag-end flush (see "Drag is not a click" under the selection contract).
17. **Anything else** → open the matching file under [`references/examples/`](references/examples/) and diff our shape against the canonical one. If our code does not match, align it before inventing a workaround.
