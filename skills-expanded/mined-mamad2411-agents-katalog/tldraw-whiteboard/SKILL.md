---
name: tldraw-whiteboard
description: Use when David wants to create visual whiteboard graphics for YouTube videos using the tldraw SDK, OR inspect/extract content from an existing .tldr board file. Triggers on tldraw, whiteboard, visual diagram, canvas graphic, video visual, board design, "what's in this board", "read this column from the tldr".
---

# tldraw Whiteboard

Two modes:
1. **Authoring** — build new board graphics in `sandbox/tldraw/` (App.tsx programmatic shapes).
2. **Inspecting** — read content from an existing `.tldr` file (parse JSON, extract richText, isolate a column).

For inspection workflow see `references/extract-from-tldr.md`.

---

## Authoring Mode

Build visual whiteboard graphics for David's YouTube videos using the tldraw SDK. The app lives at `sandbox/tldraw/` and runs locally via `npm run dev` on port 5173.

### Setup

The tldraw app is already scaffolded at `sandbox/tldraw/`. If it doesn't exist:

```bash
npm create vite@latest tldraw -- --template react-ts
cd tldraw
npm install
npm install tldraw
```

All visuals are built programmatically in `src/App.tsx` using the tldraw Editor API.

### How It Works

Everything happens in the `onMount` callback. You create shapes programmatically using `editor.createShape()`. Each "page" or section is offset horizontally (e.g. section 1 at x=0, section 2 at x=1500, section 3 at x=3200). David pans between them during recording.

```tsx
import { Editor, Tldraw, createShapeId, toRichText } from 'tldraw'
import 'tldraw/tldraw.css'

export default function App() {
  const handleMount = (editor: Editor) => {
    editor.user.updateUserPreferences({ colorScheme: 'light' })
    // Create shapes here...
    setTimeout(() => {
      editor.zoomToFit({ animation: { duration: 500 } })
    }, 100)
  }

  return (
    <div style={{ position: 'fixed', inset: 0, background: '#ffffff' }}>
      <Tldraw onMount={handleMount} />
    </div>
  )
}
```

### Shape Types & API

#### Text
```tsx
editor.createShape({
  id: createShapeId('mytext'),
  type: 'text',
  x: 100, y: 100,
  props: {
    richText: toRichText('HEADLINE TEXT'),
    size: 'xl',  // 's' | 'm' | 'l' | 'xl'
    color: 'black',
  },
})
```

#### Geo
```tsx
editor.createShape({
  id: createShapeId('mybox'),
  type: 'geo',
  x: 100, y: 200,
  props: {
    w: 340, h: 140,
    geo: 'rectangle',
    color: 'violet',
    fill: 'solid',
    richText: toRichText('Box content here'),
    size: 'm',
    font: 'sans',
  },
})
```

#### Arrows (point-based only — bindings don't work via createShape)
```tsx
editor.createShape({
  id: createShapeId('myarrow'),
  type: 'arrow',
  x: 300, y: 400,
  props: {
    color: 'black',
    start: { x: 0, y: 0 },
    end: { x: 100, y: 150 },
  },
})
```

**CRITICAL: Do NOT use binding-based arrows (boundShapeId). They throw validation errors.**

### Colors
`'black'` `'white'` `'grey'` `'light-violet'` `'violet'` `'blue'` `'light-blue'` `'green'` `'light-green'` `'yellow'` `'orange'` `'light-red'` `'red'`

### Geo Shapes
`'rectangle'` `'ellipse'` `'diamond'` `'star'` `'hexagon'` `'cloud'` `'triangle'` `'arrow-right'` `'arrow-left'` `'arrow-up'` `'arrow-down'`

### David's Design Preferences

- **Headlines:** `size: 'xl'`, uppercase, `color: 'black'` (or `'white'` on dark bg)
- **Subtitles:** `size: 'm'`, sentence case, `color: 'grey'`
- **Section labels:** `size: 's'`, uppercase, colored to match their section
- **Bullet text inside shapes:** 5-10 words max per box.
- **No newline characters** — they render as literal `\n`. Use separate shapes.
- **Generous spacing** — min 80px gap between rows, 40px between columns. Row gap between tiers: 140-180px.
- **Multiple sections:** Offset each section horizontally by 1500-1700px.
- **Always `editor.zoomToFit()` at the end** with a small delay.
- Different colors for different concepts. Mix shapes. Color-code: red=warning, green=positive, violet=vision, orange=question, blue=tools.
- Match arrow colors to target shape's color.
- Default to white bg (`colorScheme: 'light'`, `#ffffff`), but **always ask David** — he may want dark mode (`colorScheme: 'dark'`, `#1e1e2e`, titles white).
- Animations sparingly via `setTimeout`. When in doubt, show everything at once.
- Keep toolbar visible during recording.

### Loading an existing `.tldr` into the live app

Use `parseTldrawJsonFile` + `getSnapshot` + `loadSnapshot` from the SDK. Put the `.tldr` in `sandbox/tldraw/public/` and `fetch()` it on mount. **Back up `App.tsx` first** — the load-on-mount pattern replaces the current store.

### Running

```bash
cd sandbox/tldraw
npm run dev
```

Opens at `http://localhost:5173/`. After code changes, hit **Reset data** in the error screen or browser, then refresh.

### Process

1. David provides section content (bullets from video outline).
2. Decide structure pattern (concept map, bullet list, flow, timeline).
3. New file per video: `src/videos/<video-name>.tsx`. Import from `App.tsx`.
4. David reviews in browser, gives feedback. Iterate.

### Authoring Rules

- **Max 10 words per shape.**
- **Never use newline characters.**
- **Each section gets its own horizontal space.**
- **Always use point-based arrows.**
- **Variety over uniformity.**

---

## Inspection Mode

When David asks "what's in this board / column / section" → load the `.tldr` and parse. See `references/extract-from-tldr.md` for the full workflow, code snippets, and column-isolation algorithm.

Quick rules:
- `.tldr` is JSON. Records at `data['records']`, filter `typeName == 'shape'`.
- Text lives in `props.richText` (ProseMirror tree), NOT `props.text`. Walk the tree.
- Sort by `(y, x)` for reading order.
- David's boards are columns of vertically-stacked sections. To isolate a column: find its header → find next header in the same x-band → that's your y bound.
- Gaps in y usually mean a tall video/image shape, not missing content.
