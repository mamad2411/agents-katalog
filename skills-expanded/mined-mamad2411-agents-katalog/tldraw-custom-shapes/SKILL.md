---
name: tldraw-custom-shapes
description: Extend tldraw with custom shapes (ShapeUtil), custom tools (StateNode), bindings between shapes, and toolbar wiring. Use when the user builds their own shape types or tools on the tldraw canvas.
---

# tldraw custom shapes and tools

## ShapeUtil: define a shape

```tsx
import { HTMLContainer, Rectangle2d, ShapeUtil, T, TLBaseShape } from "tldraw"

type NoteShape = TLBaseShape<"my-note", { w: number; h: number; text: string }>

export class NoteShapeUtil extends ShapeUtil<NoteShape> {
  static override type = "my-note" as const
  static override props = {
    w: T.number,
    h: T.number,
    text: T.string,
  }

  getDefaultProps(): NoteShape["props"] {
    return { w: 200, h: 200, text: "" }
  }

  getGeometry(shape: NoteShape) {
    return new Rectangle2d({ width: shape.props.w, height: shape.props.h, isFilled: true })
  }

  component(shape: NoteShape) {
    return (
      <HTMLContainer style={{ background: "#ffe066", pointerEvents: "all" }}>
        {shape.props.text}
      </HTMLContainer>
    )
  }

  indicator(shape: NoteShape) {
    return <rect width={shape.props.w} height={shape.props.h} />
  }
}
```

Register: `<Tldraw shapeUtils={[NoteShapeUtil]} />`. Then
`editor.createShape({ type: "my-note", x, y })`.

Key points:

- `props` uses `T` validators from tldraw; validated on every change, and the
  schema drives persistence/sync compatibility. Only JSON-serializable props.
- `component` renders on canvas; wrap HTML in `HTMLContainer` (or SVG in
  `SVGContainer`). Set `pointerEvents: "all"` if the shape's content must
  receive events (default routing goes to canvas tools).
- `indicator` is the selection outline (SVG).
- Behavior flags: override `canEdit`, `canResize`, `isAspectRatioLocked`,
  `hideRotateHandle`, etc. Implement `onResize` (use `resizeBox` helper for
  box shapes) or resizing does nothing.
- Evolving props later requires migrations:
  `createShapePropsMigrationSequence` plus a `migrations` static, otherwise
  old persisted documents fail validation.

## Custom tools: StateNode

```tsx
import { StateNode } from "tldraw"

export class NoteTool extends StateNode {
  static override id = "my-note"
  override onEnter() { this.editor.setCursor({ type: "cross" }) }
  override onPointerDown() {
    const { currentPagePoint } = this.editor.inputs
    this.editor.createShape({ type: "my-note", x: currentPagePoint.x, y: currentPagePoint.y })
    this.editor.setCurrentTool("select")
  }
}
```

Register with `<Tldraw tools={[NoteTool]} ... />`. Tools are nodes in the
editor's state chart; complex tools nest children states (see the built-in
draw/select tools for patterns). Handle `onPointerMove`, `onPointerUp`,
`onKeyDown`, `onCancel` as needed.

## Toolbar and UI wiring

Adding a tool does not add a button. Provide UI overrides:

```tsx
const uiOverrides = {
  tools(editor, tools) {
    tools["my-note"] = {
      id: "my-note", icon: "color", label: "Note", kbd: "n",
      onSelect: () => editor.setCurrentTool("my-note"),
    }
    return tools
  },
}
```

Pass `overrides={uiOverrides}` and, to place the button, override
`components.Toolbar` rendering `DefaultToolbar` with an added
`TldrawUiMenuItem` (same pattern for keyboard shortcuts dialog).

## Bindings: relationships between shapes

Bindings are records connecting two shapes (how arrows attach). Custom
bindings subclass `BindingUtil`:

- `static type` and `props` validators like shapes.
- Lifecycle hooks run when related shapes change:
  `onAfterChangeToShape`, `onAfterChangeFromShape`, delete hooks
  (`onBeforeDeleteToShape`) to clean up or reposition.
- Create via `editor.createBinding({ type: "sticker", fromId, toId, props })`;
  query with `editor.getBindingsFromShape(shape, "sticker")`.
- Register with `<Tldraw bindingUtils={[StickerBindingUtil]} />`.

Use bindings for "pin A to B" mechanics (stickers, connectors, org charts)
instead of manually syncing positions in listeners.
