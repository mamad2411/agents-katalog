---
name: tldraw-sdk
description: Embed the tldraw infinite canvas SDK in React: setup, persistence, snapshots, the store, editor API, licensing, and versioning. Use when the user integrates or works with the tldraw editor.
---

# tldraw SDK

React SDK for infinite canvas apps (the engine behind tldraw.com). Current
line is v5 (v5.2 as of mid-2026). Important: tldraw does NOT follow semver.
Minor versions ship roughly monthly and may contain breaking changes, so pin
an exact version and read release notes (tldraw.dev/releases) before bumping.

## Setup

```bash
npm install tldraw            # exact-pin in package.json
npm create tldraw@latest      # alternative: scaffold from starter kits
```

```tsx
import { Tldraw } from "tldraw"
import "tldraw/tldraw.css"

export default function App() {
  return (
    <div style={{ position: "fixed", inset: 0 }}>
      <Tldraw />
    </div>
  )
}
```

The component must have a sized container (it fills its parent). Starter kits
cover common builds (multiplayer, shader, image pipeline, workflow, agent).

## Licensing

Free without a key in development, but production use requires a license key
from tldraw.dev (free hobby and trial tiers exist, commercial licenses for
business use). Pass it as `<Tldraw licenseKey={...} />`. Without a valid key
the SDK is only permitted, and will only work, in dev environments. With a
license you may hide the "Made with tldraw" attribution.

## Persistence and snapshots

```tsx
<Tldraw persistenceKey="my-app-doc" />
```

`persistenceKey` stores the document in IndexedDB and syncs across tabs of the
same browser. For your own backend, use snapshots:

```ts
import { getSnapshot, loadSnapshot } from "tldraw"
const { document, session } = getSnapshot(editor.store)
// persist document (canvas content); session is per-user (camera, selections)
loadSnapshot(editor.store, { document, session })
```

For live incremental persistence, `editor.store.listen(fn, { scope: "document", source: "user" })`
and debounce writes.

## Editor API

Get the editor imperatively via `onMount`, or `useEditor()` inside child
components (as `components` overrides or inside `<Tldraw>{children}</Tldraw>`):

```tsx
<Tldraw
  onMount={(editor) => {
    editor.createShape({ type: "geo", x: 100, y: 100, props: { w: 200, h: 100, geo: "rectangle" } })
    editor.zoomToFit()
  }}
/>
```

- Common calls: `createShapes`, `updateShapes`, `deleteShapes`,
  `getSelectedShapes`, `select`, `getShape(id)`, `getCurrentPageShapes`,
  `setCurrentTool("draw")`, camera control (`zoomToBounds`, `setCamera`),
  `toImage` / SVG export helpers.
- Group mutations with `editor.run(() => { ... })`; add
  `{ history: "ignore" }` to keep changes out of undo.
- The store is reactive (signals): subscribe in React with `useValue`, or
  `react()` from `tldraw` for imperative code.

## UI customization

- `components` prop swaps or removes UI parts and canvas layers
  (`{ Toolbar: null }` hides the toolbar; `InFrontOfTheCanvas` renders your
  own overlay React on the canvas).
- `overrides` prop edits actions, tools, and menus; `cameraOptions`
  constrains zoom/pan; deep-dark/light themes and custom theming supported
  in v5.
- Readonly: `editor.updateInstanceState({ isReadonly: true })`.

## Gotchas

- Two copies of tldraw's CSS or React in a monorepo produce a broken canvas:
  dedupe.
- Shape ids must be created with `createShapeId()`, not raw strings.
- Assets (images/video) need an asset store when you leave persistenceKey
  land; wire `assetUrls`/`assets` options or the sync asset handlers.
- SSR frameworks: render the canvas client-side only (dynamic import with
  ssr disabled in Next.js).
