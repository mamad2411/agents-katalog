---
name: darktide-ui
description: "Understand, design, and modify Warhammer 40,000: Darktide native Lua UI. Use for views, HUD elements, widgets and pass templates, scenegraph layout, native styling, input and navigation, scrolling collections, and UI resource lifecycles."
license: MIT
metadata:
  author: deluxghost
  version: "1.0.0"
  repository: https://github.com/deluxghost/darktide-skills
---

# Darktide UI

## The UI Model

Darktide's Lua UI composes drawing and interaction passes over the engine's `Gui` facilities. A widget is a collection of passes and their data, not a self-contained button, panel, or window class. A button's appearance and behavior come from its pass template and the code using it.

Four structures cooperate but have different responsibilities:

- **Ownership:** A view or HUD owns its lifecycle; view elements encapsulate child components, and widgets belong to their drawing owner.
- **Layout:** A scenegraph supplies named coordinate frames, sizes, and alignment. Its parent-child relationships do not route input or establish resource ownership.
- **Drawing:** The owner selects widgets and renderers; passes produce visuals, interaction state, and logic. Layers and masks determine composition.
- **Input:** Input services, the view stack, and component navigation decide which interface can act. Being visible or visually on top does not itself grant exclusive input.

### From Definitions To A Running UI

Definitions and pass templates are construction data. Their runtime relationships are:

```text
definitions.scenegraph_definition -> UIScenegraph -> owner._ui_scenegraph
pass template -> UIWidget.create_definition -> definitions.widget_definitions
              -> UIWidget.init -> live widgets in drawing lists and name maps
definitions.animations -> UISequenceAnimator -> live scenegraph/widget values
```

An owner receives data and input during `update`, advances its components and animations, and changes live widget `content` and `style`. During `draw`, `UIRenderer.begin_pass` provides the scenegraph, input, and render settings; `UIWidget.draw` resolves each widget's geometry and executes its passes in order, then `UIRenderer.end_pass` closes that rendering context. Visual passes submit engine GUI drawing commands; hotspot and logic passes perform interaction work within the same traversal. Updating Lua data does not itself draw anything, and changing a construction template does not retroactively change an existing widget.

Common controls are compositions, not extra primitive types: a label uses a `text` pass; a button combines a `hotspot` with text and decorative passes; a slider adds drag logic and track/thumb visuals. A grid arranges many widgets and supplies scrolling/navigation around them. These compositions explain why a control's visible bounds, clickable bounds, and layout footprint can differ.

## Reading An Interface

All game paths here are relative to `<source>`, the game resource root containing `scripts/main.lua`, not a mod's own `scripts` folder.

The following map selects the main UI code locations; it is not a complete file listing. Under `scripts/ui/`:

- `views/`: named screens and their registry in `views.lua`. A screen's class owns behavior; its definitions, settings, animations, and blueprints describe presentation and construction.
- `hud/`: player HUD element sets and implementations under `elements/`.
- `constant_elements/`: UI-manager-owned interfaces spanning individual views or player HUD instances, such as chat, subtitles, and notifications; their visibility still depends on UI state.
- `view_elements/`: parent-owned components such as grids, tabs, input legends, and item previews. Component definitions and settings stay beside the class.
- `pass_templates/`: reusable pass lists/factories for buttons, checkboxes, dropdowns, sliders, steppers, scrollbars, text input, keybinds, and item visuals.
- `view_content_blueprints/`: shared item and item-stat entry blueprints; view-specific blueprints also live with their views.
- `widget_logic/`: `ui_widget_grid.lua`, the layout/scroll/navigation controller used by collections.
- `utilities/`: specialized UI helpers. `default_pass_styles.lua` and `default_pass_values.lua` at the UI directory root supply widget-factory defaults.

Outside that directory, `scripts/managers/ui/` contains the runtime machinery: `ui_widget.lua`, `ui_passes.lua`, `ui_renderer.lua`, `ui_scenegraph.lua`, `ui_resolution.lua`, the view/HUD managers, fonts, and animation. `scripts/settings/ui/` contains shared workspace, sound, and other UI settings. `scripts/utilities/ui/` contains helpers for text, colors, popups, and related presentation data.

For a visible part, follow its pass to the selected content/style fields, then to the code updating those fields. For behavior, follow the input consumer and the owner calling it. A definition alone does not explain runtime appearance or interaction: templates, animations, layout controllers, and owner code can all write the live state.

## Composition Choices

- Use a managed **view** for a screen with its own opening, closing, and input relationship to other screens; a **HUD element** for gameplay-overlay content; a **view element** for a component with its own layout and behavior inside a parent. A small section or popup can remain a widget group when it shares its parent's lifecycle.
- Shared pass templates, `UIFontSettings`, `Color`, GUI materials, sounds, and input legends supply the native visual and interaction vocabulary, including focus, hover, disabled, pressed, and navigation feedback. A page header and a compact embedded panel use different spacing and visual weight within that vocabulary.
- Keep application data separate from its widget presentation. Widgets can be reconstructed, hidden, or culled; selection, edited values, and the choice of when to commit them belong to the interface's behavior, not merely to whether a pass was drawn.

Read the relevant reference when working on that part of the interface:

- [Layout and rendering](references/layout-and-rendering.md): available pass types and their inputs, scenegraph coordinates, widget geometry, native appearance, text, materials, layers, masks, and animation.
- [Input and collections](references/input-and-collections.md): frame timing, mouse and controller interaction, focus, editing, grid settings/blueprints/layout, sizing, rendering, and scrolling contracts.
- [Lifecycle and integration](references/lifecycle-and-integration.md): views, HUD and child elements, readiness, view-stack behavior, DMF registration, packages, and renderer ownership.

The references establish the working model and available building blocks. Source lookup then resolves a chosen template's exact factory arguments, callbacks, or version-specific behavior; it need not begin by rediscovering the whole UI system.
