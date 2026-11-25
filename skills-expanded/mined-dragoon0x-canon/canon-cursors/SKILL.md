---
name: canon-cursors
description: Use when designing or auditing cursor behavior — matching cursor shape to affordance, custom cursors, drag cursors, resize cursors, and the hover+cursor pairing rule. Trigger when the user mentions cursor, pointer, mouse cursor, drag cursor, or resize handle.
---

# CANON · Cursors

The cursor tells users what will happen before they click. Wrong cursor = broken promise.

## Cursor-affordance pairing

| Affordance | Cursor | CSS |
|---|---|---|
| Clickable button/link | Pointer | `cursor: pointer` |
| Text content (selectable) | Text | `cursor: text` |
| Draggable element | Grab / grabbing | `cursor: grab` / `cursor: grabbing` |
| Resizable edge/corner | Resize | `cursor: ew-resize`, `ns-resize`, `nwse-resize` |
| Disabled element | Not-allowed | `cursor: not-allowed` |
| Loading (system-level) | Wait | `cursor: wait` |
| Loading (element-level) | Progress | `cursor: progress` |
| Default (non-interactive) | Default | `cursor: default` |
| Crosshair (precision) | Crosshair | `cursor: crosshair` |
| Help (tooltip-ish) | Help | `cursor: help` |
| Zoom in/out | Zoom-in / zoom-out | `cursor: zoom-in` |

## The hover+cursor rule

From `canon-interaction`: if the element changes on hover, the cursor must match the action. Hover effect without cursor change is ambiguous. Cursor change without hover effect is invisible.

## Custom cursors

Custom cursor images are acceptable for specialized tools (drawing apps, games). Rules:

- Provide a fallback: `cursor: url(custom.png), pointer`
- Keep the hotspot correct (the click point).
- Size: 32×32px maximum (OS recommendation).
- Don't use custom cursors for standard web interactions.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| `cursor: pointer` on non-interactive elements | False promise |
| No cursor change on interactive elements | Hidden affordance |
| `cursor: pointer` on text inputs | Confusing — text cursor expected |
| Custom cursor on every element | Disorienting |
| `cursor: not-allowed` on elements that are actually clickable | Lying to the user |
| Grab cursor on non-draggable element | Broken promise |

## Audit checklist

- [ ] Every interactive element uses `cursor: pointer`
- [ ] Draggable elements use `cursor: grab` (and `grabbing` on drag)
- [ ] Disabled elements use `cursor: not-allowed`
- [ ] Resizable edges use the correct resize cursor
- [ ] No `cursor: pointer` on non-interactive content
- [ ] Custom cursors have a standard fallback
- [ ] Text-selectable areas use default or text cursor

## Sources

- MDN · cursor CSS property
- WCAG 2.2 · 1.4.1 Use of Color (cursor is a signal)
- Apple HIG · Pointer (cursor guidance)
