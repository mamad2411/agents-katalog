# Editor UI patterns for Rasterra

Use this reference for application-shell and viewport work. It records patterns verified against Bevy 0.19 Feathers and the local Jackdaw editor; it is not a direction to copy Jackdaw's visual system.

## Theme boundary

Feathers composes each styled widget from three layers:

```text
headless behavior + semantic/accessibility state + themed visual scene
```

Follow the same order for a custom Rasterra control. Preserve the headless component and its events, then replace or patch layout and theme components. Feathers resolves semantic color tokens through `UiTheme`; use the token-bound background, border, and text components so a theme replacement updates existing UI.

Rasterra deliberately differs from Jackdaw here. Jackdaw has a large project palette of direct `Color` constants. Its interaction architecture is useful, but its token breadth and direct-color usage are not the model for Rasterra.

## Command controls

A painting command may have several callers:

```text
toolbar button ─┐
menu item ──────┼─> Rasterra action -> authoritative state/document
shortcut ───────┘
```

The control should identify the action, not reimplement it. A shared action layer can answer whether a command is available, execute it, and provide its active state. UI systems translate those answers into `InteractionDisabled`, selected variants, and accessible descriptions.

Do not introduce a general operator framework for the first POC. A typed enum or focused events are enough until parameterized commands, undo metadata, or modal tools demonstrate the need for more machinery.

## Canvas ownership and input arbitration

For a single canvas, still make ownership explicit:

1. Hit-test the cursor against `ComputedNode` and `UiGlobalTransform`.
2. On pointer-down, capture the canvas entity and start a stroke.
3. Route subsequent samples to the captured canvas even if the cursor leaves it.
4. Release capture when the stroke ends or is cancelled.
5. Refuse a new stroke while text editing, a modal operation, or a blocking overlay owns input.

This scales to multiple document views without rewriting the stroke pipeline. Jackdaw's active-viewport resource demonstrates the same principle, including pinning a target during a drag.

`InputFocus` can contain a window or other non-text entity. Suppress shortcuts only when the focused entity has the marker used by Rasterra's editable controls.

## Brush browser

The brush catalog is runtime data, so build its tiles from a `SceneList` rather than hardcoding one BSN entity per preset. Each tile should contain an owned brush ID, accessible label, optional preview handle, and selection observer. Keep image loading asynchronous and render a stable fallback when a preview is absent or fails to decode.

Start with a scrollable grouped grid or list. Docking, arbitrary splits, detachable panels, and a generalized workspace layout are not prerequisites for validating painting.

## Testing seams

- Test action dispatch and disabled/selected synchronization without rendering.
- Test canvas hit testing and capture transitions with explicit node bounds and pointer samples.
- Test that text focus and overlays prevent stroke starts.
- Test brush selection by stable brush ID, not by entity identity or display label.
- Reserve screenshot comparisons for layout or appearance regressions.
