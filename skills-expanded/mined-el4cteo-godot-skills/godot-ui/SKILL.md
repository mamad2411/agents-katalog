---
name: godot-ui
description: Build Godot 4.7 user interfaces that work on PC, mobile and console - anchors and containers, responsive stretch settings, safe areas, Themes and type variations, gamepad/keyboard focus navigation, offset_transform animation (4.7), RichTextLabel, localization, accessibility (screen readers), drag and drop, HUD over 3D. Use for menus, HUDs, inventories, settings screens or any Control node work.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# UI (4.7)

Build UI as scenes (`ui/hud/hud.tscn`) made in the editor, or with `../godot-core/scripts/scene_edit.py`. Scripts only fill in data and react. Input actions and gamepads are in `godot-input`.

## Layout fundamentals
- **Containers do the layout.** Use `VBoxContainer`/`HBoxContainer`, `GridContainer`, `MarginContainer` (padding), `PanelContainer` (background), `CenterContainer`, `ScrollContainer`, `FlowContainer` (wrapping tags/items), `AspectRatioContainer`, `TabContainer`, `FoldableContainer` (4.5+) and `SplitContainer`. Children of containers ignore their own anchors and position.
- Size flags decide each child's share: `size_flags_horizontal = SIZE_EXPAND_FILL` (+ `size_flags_stretch_ratio`), `SIZE_SHRINK_CENTER`, and so on. `custom_minimum_size` sets a floor.
- The root of a UI scene is a `Control` with `set_anchors_and_offsets_preset(PRESET_FULL_RECT)`. HUD corners use anchor presets (`PRESET_TOP_LEFT` …) plus a MarginContainer.
- To animate or juice controls inside containers, use the **4.7 `offset_transform_*`** properties (`offset_transform_enabled`, `_position`, `_rotation`, `_scale`, `_pivot_ratio`, `_visual_only`). Containers don't overwrite them, unlike `position`/`scale`. `pivot_offset_ratio` (4.6+) sets a pivot as a fraction of size, so (0.5, 0.5) is the center.
- `mouse_filter`: `STOP` (default for most), `PASS`, or `IGNORE` for decorative overlays that would otherwise block clicks to the game. Use `mouse_behavior_recursive`/`focus_behavior_recursive` (4.5+) to disable a whole subtree.

## Multi-resolution and devices
- New 4.7 projects use stretch mode `canvas_items` + aspect `expand`. Design at 1920×1080 (or 1280×720) and anchor to edges so wider and taller screens just reveal more space. Pixel-art games use `viewport` + integer scaling (see `godot-2d`).
- Mobile safe area (notches): read `DisplayServer.get_display_safe_area()` and pad the root MarginContainer (see the reference).
- Text size: minimum ~24 px at 1080p for TV/console legibility, and touch targets of at least ~48 px at the base resolution.
- `Window.content_scale_factor` gives a user-facing "UI scale" option.

## Theme instead of per-node overrides
- Make one `Theme` resource (`ui/theme/main_theme.tres`) and set it on the root Control, or project-wide in `gui/theme/custom`. Define default fonts, sizes and StyleBoxes there.
- Variants: set `theme_type_variation = &"DangerButton"` on a node, and define `DangerButton` (base type `Button`) in the theme. This is better than scattered `add_theme_*_override` calls.
- Fonts: use `FontFile` with `FontVariation` for weight and spacing. For crisp text at any scale, enable MSDF on the font import (great for world-space labels).

## Focus and navigation (required for gamepad and console)
- Every interactive control needs `focus_mode = FOCUS_ALL`. Call `grab_focus()` on the first button when a menu opens. 4.6+ separates mouse and keyboard focus: `grab_focus(true)` focuses without showing the outline.
- Godot picks neighbors automatically, by geometry. Override them with `focus_neighbor_*`/`focus_next` in grids and odd layouts.
- Built-in actions `ui_accept`, `ui_cancel`, `ui_up/down/left/right`, `ui_focus_next` already map to arrows, Enter, Escape and gamepad. Add your own bindings to them, never replace them.
- Track focus with `get_viewport().gui_focus_changed`, for example for sounds or scrolling into view. Make sure no menu is ever left with nothing focused.

## Text
- `Label` (`autowrap_mode`, `text_overrun_behavior`, `LabelSettings` for outline and shadow, stacked effects in 4.5+), `RichTextLabel` (`bbcode_enabled`, `append_text`, `[url]` + `meta_clicked`, `[img height=1em]` in 4.7, custom effects).
- Localization: write keys or English source text, then `tr("KEY")` / `tr_n()`. Nodes auto-translate their text (`auto_translate_mode`). Add `.po` or `.csv` files in Project Settings → Localization, and switch with `TranslationServer.set_locale("de")`. C# `Tr()` strings are extracted to POT too (4.6+).

## Accessibility (4.5+, AccessKit)
Standard controls are announced automatically. Give icon-only buttons `accessibility_name`, use `accessibility_description` for extra context and `accessibility_live` for changing status text. Keep focus order logical, because screen readers follow it.

## HUD over 3D and world-space UI
- HUD: a `CanvasLayer` with your Control tree, so it ignores the camera.
- World-space health bars: either `Label3D`/`Sprite3D` (billboard), or a `SubViewport` holding Controls rendered to a `ViewportTexture` on a quad. Projecting a 3D point with `camera.unproject_position()` onto a 2D control is also cheap.

## Common mistakes
- Setting `position`/`size` on children of containers (it gets overwritten). Use size flags, minimum size or offset transforms instead.
- Full-screen invisible Controls with `mouse_filter = STOP` that block game input.
- Menus that can't be closed or navigated without a mouse.
- Hard-coded strings in code that never pass through `tr()`.

Responsive layout, menu focus, tweened buttons, inventory drag and drop, safe area (compiled by the tests): [references/patterns.md](references/patterns.md)
