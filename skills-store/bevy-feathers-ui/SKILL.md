---
name: bevy-feathers-ui
description: Build Rasterra editor UI with Bevy 0.19 Feathers today while preserving a path to project-specific styling on `bevy_ui_widgets` headless components. Use for controls, panels, themes, accessibility, interaction events, widget state, or custom Rasterra widget design.
---

# Build Rasterra UI from Feathers to Headless Widgets

Read `CONTRIBUTING.md`, then use `bevy-bsn-ui` for scene syntax.

## Use Feathers first

1. Enable Bevy's `bevy_feathers` feature.
2. Add `FeathersPlugins` and insert a `UiTheme`, initially `UiTheme(create_dark_theme())`.
3. Instantiate widgets through BSN `SceneComponent`s such as `@FeathersButton`; do not use deprecated `*_bundle` constructors.
4. Supply props such as `@caption`, `@variant`, and `@corners`, then patch ordinary components such as `Node` at the call site.
5. Add `AccessibleLabel`, focus/navigation components, disabled or checked state, and `on(...)` observers explicitly where required.
6. Follow the versioned Feathers gallery for the exact widget API.

## Use Feathers tokens as the palette

Feathers' `tokens` module is Rasterra's default semantic color vocabulary. Reuse tokens such as `WINDOW_BG`, `TEXT_MAIN`, `TEXT_DIM`, pane and group colors, list-row states, button states, focus, input, scrollbar, and menu colors before defining anything project-owned.

Apply colors through `ThemeBackgroundColor`, `ThemeBorderColor`, `ThemeTextColor`, or `InheritableThemeTextColor`. Do not resolve `UiTheme::color` into a raw color during scene construction: retaining the token component lets a changed `UiTheme` propagate to existing entities.

Only add a project token when the role is absent from Feathers, for example a canvas checkerboard or an out-of-gamut warning. Namespace it as `rasterra.*`, insert its value into the active `UiTheme`, and still consume it through a theme component. Do not create aliases such as `rasterra.panel.bg` for an existing Feathers token.

In 0.19, `ThemeProps` contains colors only. A small, restrained set of project layout metrics is appropriate for spacing, thumbnail size, or canvas geometry; do not call those color theme tokens or grow a second full design system.

## Separate behavior from presentation

Use events from `bevy_ui_widgets` as the stable seam:

- Handle `Activate` for buttons and menu actions.
- Handle `ValueChange<T>` for editable values; inspect `is_final` when continuous edits should commit only at interaction end.
- Store checkbox state in `Checked`, slider state in `SliderValue`, and disabled state in `InteractionDisabled` as the headless API expects.
- Prefer external state synchronization for document and tool state. Use helpers such as `checkbox_self_update`, `radio_self_update`, or `slider_self_update` only for genuinely local widget state.

Do not make domain systems query Feathers marker types. Translate widget events into Rasterra actions or resources so presentation can change independently.

Use a small Rasterra action seam for commands that may be invoked from a button, menu, shortcut, or tablet control. Derive `InteractionDisabled` from action availability and derive active/selected visuals from authoritative tool state. This is one of the useful editor patterns in Jackdaw and does not require adopting its broad token catalog.

## Follow Feathers' implementation pattern

Feathers itself is a useful reference for custom Rasterra controls. Its `SceneComponent` implementations compose an unstyled headless component such as `Button` or `Checkbox` with layout, focus/navigation, cursor, theme-token, font, and child entities. Follow that layering: keep the headless behavior component intact and replace the surrounding visual scene deliberately. Compose related variants by patching an existing scene, as `FeathersToolButton` patches `FeathersButton`, instead of copying the whole widget.

## Customize incrementally

Choose the least costly level that meets the design:

1. Patch Feathers layout and visuals in BSN.
2. Compose Feathers primitives into a project-owned scene function.
3. Create a Rasterra `SceneComponent` that uses headless widget behavior and project styling.
4. Replace a Feathers control only when its visual or interaction constraints require it.

## Rasterra icon and font assets

- Use the project SVG image loader for icons inside Feathers/BSN UI. Load an
  `.svg` as `Handle<Image>` and compose it with `ImageNode`; scene-mesh SVG
  renderers run before the UI pass and cannot participate in UI layout,
  clipping, or picking.
- Keep icon-only controls accessible with `AccessibleLabel`. Use text when a
  compact symbol would be ambiguous.
- Pair icons with text for persistent, high-level navigation when space allows;
  familiarity can justify icon-only variants later, but should not be assumed
  for a new interaction model.
- Prefer the vendored Lucide vocabulary and add only glyphs the application
  uses. Record the pinned upstream commit and retain its license text under
  `assets/`.
- Rasterra applies the vendored Geist face to `ThemedText` at the app boundary.
  In Bevy 0.19, set `TextFont.font` with a `Handle<Font>`/`FontSource` and use
  `FontSize::Px` or `FontSize::Rem`, not a bare float.

When building a custom headless widget, include semantics, keyboard/focus behavior, accessibility, interaction state, and event/state synchronization before visual polish. The headless components intentionally provide behavior without styling.

## Editor input boundaries

- Route canvas input only when the cursor is inside the computed canvas or viewport node.
- Capture the target viewport/canvas when a stroke begins so leaving its bounds does not retarget the active stroke.
- Suppress canvas shortcuts and painting while a relevant text input, modal interaction, or overlay owns input.
- Do not interpret any non-`None` `InputFocus` as text entry; test whether the focused entity is actually an editable control.
- Keep these gates in one input-routing layer rather than duplicating them in every tool.

Read [editor-patterns.md](references/editor-patterns.md) when building the application shell, canvas routing, command controls, or a brush browser.

Read [ui-project-structure.md](references/ui-project-structure.md) before
splitting `src/app.rs`, adding a panel or major editor workflow, creating a
shared widget module, or proposing a UI crate.

## Caveats

- Feathers is suitable for broad tooling use in 0.19 but remains incomplete and subject to breaking changes.
- `bevy_ui_widgets` is also experimental and uses external state management by default.
- Bevy UI 0.19 supports blurred [`BoxShadow`] rendering, but it has no
  backdrop-filter/background-blur component. Rasterra uses a project-owned,
  region-masked camera post-process adapted from Bevy PR #24609. It runs after
  tonemapping and before the UI pass, so blur-visible content must be scene
  content rather than another UI node. Keep the canvas texture on a 2D sprite
  and retain a transparent UI node for layout, hit testing, and overlays.
- Do not copy Bevy `main` examples without comparing them with the 0.19 tag; BSN syntax evolved during development.
- Prefer Rasterra-owned wrappers at repeated design-system boundaries, not wrappers around every Feathers widget.
- Feathers' 0.19 theme lookup covers color, not spacing, typography, or arbitrary style values.

## Primary references

- [Bevy 0.19 Feathers announcement](https://bevy.org/news/bevy-0-19/#more-feathers-widgets)
- [Bevy 0.19 Feathers gallery](https://bevy.org/examples/ui-user-interface/feathers-gallery/)
- [Bevy 0.19 Feathers counter](https://bevy.org/examples/ui-user-interface/feathers-counter/)
- [Bevy 0.19 headless widget API](https://docs.rs/bevy/0.19.0/bevy/ui_widgets/)
- [Bevy standard headless widget example](https://bevy.org/examples/ui-user-interface/standard-widgets/)
